import pickle

import pandas as pd
import numpy as np

# from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

stopset = set(stopwords.words('english'))
# tokenizer = RegexpTokenizer(r'\w+')
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')

with open('rmndata/metadata.pkl', 'rb') as f:
    wmap, _, _ = pickle.load(f)

with open('data/cdmn_mds/movie_lines.txt', encoding='ISO-8859-1') as f:
    ldb  = list(map(lambda x: x.split(' +++$+++ '), f.read().split('\n')))
    lmap = dict((x[0], x[-1]) for x in ldb)

with open('data/cdmn_mds/movie_conversations.txt', encoding='ISO-8859-1') as f:
    cdb  = list(map(lambda x: x.split(' +++$+++ '), f.read().split('\n')))
    cmap = {'Book':[], 'Char 1':[], 'Char 2':[], 'Span ID':[], 'Words': []}
    span = {}
    
    # For each conv
    for conv in cdb:
        u, v, m, l = conv
        
        # Get lines and words from lines
        l = list(map(lambda y: y[1:-1], l[1:-1].split(', ')))
        # w = word_tokenize(' '.join([lmap[i].lower() for i in l]))
        w = tokenizer.tokenize(' '.join([lmap[i].lower() for i in l]))
        w = ' '.join([x for x in w if not x in stopset and x in wmap])

        if w == '':
            continue
        
        # Span check
        k = '{},{},{}'.format(m, u, v)
        if k not in span:
            span[k] = -1
        span[k] += 1
        
        # Update info
        cmap['Book'].append(m)
        cmap['Char 1'].append(u)
        cmap['Char 2'].append(v)
        cmap['Span ID'].append(span[k])
        cmap['Words'].append(w)

df = pd.DataFrame.from_dict(cmap)
df.to_csv('rmndata/relationships.csv', index=False)
