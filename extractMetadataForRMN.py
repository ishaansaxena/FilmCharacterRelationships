import pickle

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stopset = set(stopwords.words('english'))

wmap = {'': 0}
with open('data/cdmn_mds/movie_lines.txt', encoding='ISO-8859-1') as f:
    ldb  = list(map(lambda x: x.split(' +++$+++ ')[-1], f.read().split('\n')))
    tkns = word_tokenize(" ".join(ldb))
    tkns = [w for w in tkns if w not in stopset]
    for t in tkns:
        if t not in wmap:
            widx = len(wmap)
            wmap[t] = widx
    
with open('data/cdmn_mds/movie_characters_metadata.txt', encoding='ISO-8859-1') as f:
    cdb  = list(map(lambda x: x.split(' +++$+++ '), f.read().split('\n')))
    cmap = dict((i, cdb[i][0]) for i in range(len(cdb)))
    
with open('data/cdmn_mds/movie_titles_metadata.txt', encoding='ISO-8859-1') as f:
    bmap = list(map(lambda x: x.split(' +++$+++ ')[0], f.read().split('\n')))
    
with open('rmndata/metadata.pkl', 'wb') as f:
    pickle.dump((wmap, cmap, bmap), f, protocol=2)
