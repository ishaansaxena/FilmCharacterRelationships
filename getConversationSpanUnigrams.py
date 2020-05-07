import pickle
import pandas as pd
import numpy as np

from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
span_min  = 5

def unigram_dataset_from_conversations(ldb, cdb, wmap, s_min=5, verbose=False):
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

if __name__ == "__main__":
    print('Loading word map')
    with open('rmndata/metadata.pkl', 'rb') as f:
        wmap, _, _ = pickle.load(f)

    print('Loading conversations')
    with open('data/cdmn_mds/movie_lines.txt', encoding='ISO-8859-1') as f:
        ldb  = list(map(lambda x: x.split(' +++$+++ '), f.read().split('\n')))
        lmap = dict((x[0], x[-1]) for x in ldb)

    with open('data/cdmn_mds/movie_conversations.txt', encoding='ISO-8859-1') as f:
        cdb  = list(map(lambda x: x.split(' +++$+++ '), f.read().split('\n')))

    df, span = unigram_dataset_from_conversations(ldb, cdb, wmap, verbose=True)
    print('Saving unigram dataframe')
    print('{} spans added for {} conversation diads'.format(len(df), len(span)))
    df.to_csv('rmndata/relationships.csv', index=False)
