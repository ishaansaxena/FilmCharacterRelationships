import pandas as pd
import numpy as np

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import json

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
agency_to_int = {'agency_pos': 1, 'agency_neg': -1}
power_to_int  = {'power_agent': 1, 'power_theme': -1}

def agency_map(x):
    da = 0
    if x in agency_to_int:
        da = agency_to_int[x]
    return da

def power_map(x):
    da = 0
    if x in power_to_int:
        da = power_to_int[x]
    return da

def lemmatize(x):
    return WordNetLemmatizer().lemmatize(x, 'v')

def pa_dataframe_from_verbs(verb_dict, verbose=False):
    verb_set = pd.read_csv('data/ms_cfap/agency_power.csv')

    verb_set['verb_base']  = verb_set['verb'].apply(lemmatize)
    verb_set['agency_int'] = verb_set['agency'].apply(agency_map)
    verb_set['power_int']  = verb_set['power'].apply(power_map)

    with open(verb_dict) as f:
        d = json.load(f)

    pa_map = {}
    for char_id, verbs in d.items():
        pa_map[char_id] = [0, 0, 0]
        for verb_raw in verbs:
    #         verb = lemmatize(verb_raw.split(' ')[-1])
            verb = lemmatize(verb_raw)
            try:
                da = verb_set.loc[verb_set['verb_base'] == verb]['agency_int'].tolist()[0]
                dp = verb_set.loc[verb_set['verb_base'] == verb]['power_int'].tolist()[0]
                pa_map[char_id][0] += da
                pa_map[char_id][1] += dp
                pa_map[char_id][2] += 1
            except:
    #             print(verb_raw)
                continue
        if verbose:
            print(char_id, pa_map[char_id])
    
    with open('data/cdmn_mds/movie_characters_metadata.txt', encoding='ISO-8859-1') as f:
        cdb  = list(map(lambda x: x.split(' +++$+++ '), f.read().split('\n')))
        cl   = [cdb[i][0] for i in range(len(cdb))]
    
    for char_id in cl:
        if char_id not in pa_map:
            pa_map[char_id] = [0, 0, 0]

    df = pd.DataFrame.from_dict(pa_map, orient='index')
    df.columns = ['agency', 'power', 'verb_count']
    df['av'] = df['agency']/df['verb_count']
    df['pv'] = df['power']/df['verb_count']
    return df

def unigram_dataset_from_conversations(cdb, lmap, wmap, s_min=5, verbose=False):
    cmap = {'Book':[], 'Char 1':[], 'Char 2':[], 'Span ID':[], 'Words': []}
    span = {}

    # Reset span_id and lists
    span_id  = -1
    prev_key = None
    ml, ul, vl, sl, wl = [], [], [], [], []

    # For each conv
    for conv in cdb:
        # Get conv info
        u, v, m, l = conv
        
        # Get lines and words from lines
        l = list(map(lambda y: y[1:-1], l[1:-1].split(', ')))
        w = tokenizer.tokenize(' '.join([lmap[i].lower() for i in l]))
        w = ' '.join([x for x in w if x in wmap])

        # Skip empty conversations
        if w == '':
            continue

        # Update check
        key = '{},{},{}'.format(m, u, v)
        if prev_key != None and key != prev_key:
            span_count = span_id + 1
            if span_count >= s_min:
                if verbose:
                    print("{} spans added to dataset".format(prev_key))
                cmap['Book'].extend(ml)
                cmap['Char 1'].extend(ul)
                cmap['Char 2'].extend(vl)
                cmap['Span ID'].extend(sl)
                cmap['Words'].extend(wl)
                span[prev_key] = span_count
            
            # Reset lists and counter
            span_id = -1
            ml, ul, vl, sl, wl = [], [], [], [], []

        # Update span counter aand lists
        span_id += 1 
        ml.append(m)
        ul.append(u)
        vl.append(v)
        wl.append(w)
        sl.append(span_id)
        prev_key = key

    return pd.DataFrame.from_dict(cmap), span