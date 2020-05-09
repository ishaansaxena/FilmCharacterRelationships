#!/usr/bin/bash

python3 extractMetadataforRMN.py
python3 getConversationSpanUnigrams.py 
gzip rmndata/relationships.csv

cp rmndata/relationships.csv.gz rmndata/metadata.pkl rmndata/glove.We rmn/data/
cp rmndata/relationships.csv.gz rmndata/metadata.pkl rmndata/glove.We rmn_w_pa/data/
