import pickle
import numpy as np

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

if __name__ == "__main__":
    
    print('Creating set of restricted words')
    restricted_set = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')

    with open('data/cmu_ng/female.txt') as f:
        names = set(map(lambda x: x.lower(), f.read().split('\n')))
        restricted_set = restricted_set.union(names)
        
    with open('data/cmu_ng/male.txt') as f:
        names = set(map(lambda x: x.lower(), f.read().split('\n')))
        restricted_set = restricted_set.union(names)
        
    with open('data/corenlpsw/stopwords.txt') as f:
        toks = set(f.read().split('\n'))
        restricted_set = restricted_set.union(toks)

    print('Importing GloVe Embeddings')
    embeddings_dict = {}
    with open("data/glove/glove.42B.300d.txt", 'r') as f:
        for line in f:
            try:
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], "float32")
            except:
                print(word)
                continue
            embeddings_dict[word] = vector
   
    def w_condition(w):
        c = (w not in restricted_set) 
        c = c and (w in embeddings_dict)
        c = c and (len(w) > 2)
        return c

    print('Get word maps')
    We = []
    wmap = {}
    wcnt = {}
    wthresh = 2
    with open('data/cdmn_mds/movie_lines.txt', encoding='ISO-8859-1') as f:
        ldb  = list(map(lambda x: x.split(' +++$+++ ')[-1], f.read().split('\n')))
        # tkns = word_tokenize(" ".join(ldb).lower())
        tkns = tokenizer.tokenize(" ".join(ldb).lower())
        tkns = [w for w in tkns if w_condition(w)]
        for t in tkns:
            if t not in wcnt:
                wcnt[t] = 0
            else:
                wcnt[t] += 1

    wcntl = sorted(wcnt.keys(), key=wcnt.get, reverse=True)
    for i in range(len((wcntl))):
        tok = wcntl[i]
        if wcnt[tok] > wthresh:
            We.append(embeddings_dict[tok])
            wmap[tok] = len(wmap)

    We = np.array(We)
    print(' - {} words'.format(len(wmap)))
    
    print('Get character maps')
    with open('data/cdmn_mds/movie_characters_metadata.txt', encoding='ISO-8859-1') as f:
        cdb  = list(map(lambda x: x.split(' +++$+++ '), f.read().split('\n')))
        cmap = dict((i, cdb[i][0]) for i in range(len(cdb)))
    print(' - {} characters'.format(len(cmap)))
        
    print('Get movie maps')
    with open('data/cdmn_mds/movie_titles_metadata.txt', encoding='ISO-8859-1') as f:
        bmap = list(map(lambda x: x.split(' +++$+++ ')[0], f.read().split('\n')))
    print(' - {} movies'.format(len(bmap)))
        
    print('Writing metadata maps')
    with open('rmndata/metadata.pkl', 'wb') as f:
        pickle.dump((wmap, cmap, bmap), f, protocol=2)

    print('Writing GloVe embeddings')
    with open('rmndata/glove.We', 'wb') as f:
        pickle.dump(We, f, protocol=2)
