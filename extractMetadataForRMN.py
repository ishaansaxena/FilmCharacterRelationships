import pickle

wmap = {}
with open('data/cdmn_mds/movie_characters_metadata.txt', encoding='ISO-8859-1') as f:
    cdb  = list(map(lambda x: x.split(' +++$+++ '), f.read().split('\n')))
    cmap = dict((i, cdb[i][0]) for i in range(len(cdb)))
with open('data/cdmn_mds/movie_titles_metadata.txt', encoding='ISO-8859-1') as f:
    bmap = list(map(lambda x: x.split(' +++$+++ ')[0], f.read().split('\n')))

with open('rmndata/metadata.pkl', 'wb') as f:
    pickle.dump((wmap, cmap, bmap), f)
