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

def pa_df_from_verbs(verb_dict, verbose=False):
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

def ug_df_from_convs(cdb, lmap, wmap, s_min=5, verbose=False):
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

def get_pa_maps(pa_file='vmaps/pa_from_vmaps.csv'):
    with open(pa_file) as f:
        f.readline()
        pal = list(map(lambda x: x.split(','), f.read().split('\n')))
        pmap = dict((x[0], float(x[-1])) for x in pal[0:-1])
        amap = dict((x[0], float(x[-2])) for x in pal[0:-1])
    return pmap, amap

def sl_df_from_traj(trajectories, pmap, amap):
    #returns the average trajectories with the respective relationships
    df = pd.read_csv(trajectories)
    del df['Span ID']

    df = df.groupby(['Book', 'Char 1', 'Char 2']).mean().reset_index()

    desc_probs  = df.values[:, 3:]
    _, num_desc = desc_probs.shape
    norm_probs  = desc_probs/np.sum(desc_probs, axis=1)[:, None]

    df.loc[:, ['Topic {}'.format(x) for x in range(num_desc)]] = norm_probs

    df['p1'] = df['Char 1'].map(pmap)
    df['p2'] = df['Char 2'].map(pmap)
    df['a1'] = df['Char 1'].map(amap)
    df['a2'] = df['Char 2'].map(amap)

    return df, num_desc

def get_char_gender(path="data/cornell movie-dialogs corpus/movie_characters_metadata.txt"):
    metadata_f = open(path, "r", encoding="utf8",errors='ignore')
    char_gender_dict = {}
    for character_metadata in metadata_f:
        fields = character_metadata.split(" +++$+++ ")
        char_id = fields[0]
        char_gender = fields[4].lower()
        char_gender_dict[char_id] = char_gender
    return char_gender_dict

def get_r_w_f_m(num_desc,full_df):
    char_gender_map = get_char_gender()
    full_df['g1'] = full_df['Char 1'].map(lambda x: char_gender_map[x])
    full_df['g2'] = full_df['Char 2'].map(lambda x: char_gender_map[x])

    f_m_df = full_df[((full_df['g1'] == 'm') & (full_df['g2'] == 'f')) | ((full_df['g1'] == 'f') & (full_df['g2'] == 'm'))].copy()
    return f_m_df



