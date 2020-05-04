import pandas as pd

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

import json

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

    df = pd.DataFrame.from_dict(pa_map, orient='index')
    df.columns = ['agency', 'power', 'verb_count']
    df['av'] = df['agency']/df['verb_count']
    df['pv'] = df['power']/df['verb_count']
    return df
    
if __name__ == "__main__":
    df = pa_dataframe_from_verbs('vmaps/cv.json', verbose=True)
    df.to_csv('vmaps/pa_from_vmaps.csv')
