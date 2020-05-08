import pickle
from util import ug_df_from_convs

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

    print('Processing conversations')
    df, span = ug_df_from_convs(cdb, lmap, wmap)
    print('Saving unigram dataframe')
    print('{} spans added for {} conversation diads'.format(len(df), len(span)))
    df.to_csv('rmndata/relationships.csv', index=False)
