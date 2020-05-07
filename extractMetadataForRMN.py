import pickle
import numpy as np

# from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

stopset = set(stopwords.words('english'))
# tokenizer = RegexpTokenizer(r'\w+')
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')

embeddings_dict = {}
with open("data/glove/glove.6B.300d.txt", 'r') as f:
    for line in f:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], "float32")
        embeddings_dict[word] = vector
    
We = []
wmap = {}
with open('data/cdmn_mds/movie_lines.txt', encoding='ISO-8859-1') as f:
    ldb  = list(map(lambda x: x.split(' +++$+++ ')[-1], f.read().split('\n')))
    # tkns = word_tokenize(" ".join(ldb).lower())
    tkns = tokenizer.tokenize(" ".join(ldb).lower())
    tkns = [w for w in tkns if w not in stopset and w in embeddings_dict]
    for t in tkns:
        if t not in wmap:
            widx = len(wmap)
            wmap[t] = widx
            We.append(embeddings_dict[t])
# with open('rmn/data/_metadata.pkl', 'rb') as f:
#     wmap, _, _ = pickle.load(f)
    
with open('data/cdmn_mds/movie_characters_metadata.txt', encoding='ISO-8859-1') as f:
    cdb  = list(map(lambda x: x.split(' +++$+++ '), f.read().split('\n')))
    cmap = dict((i, cdb[i][0]) for i in range(len(cdb)))
    
with open('data/cdmn_mds/movie_titles_metadata.txt', encoding='ISO-8859-1') as f:
    bmap = list(map(lambda x: x.split(' +++$+++ ')[0], f.read().split('\n')))
    
with open('rmndata/metadata.pkl', 'wb') as f:
    pickle.dump((wmap, cmap, bmap), f, protocol=2)

with open('rmndata/glove.We', 'wb') as f:
    pickle.dump(np.array(We), f, protocol=2)
