# FilmCharacterRelationship
  This repository contains the scripts and data for our project. 
  
##Data folders descriptions

cmdn_mds: contains the cornell dataset. For more information about the dataset please take a look at 

cdmn_mds/README.txt 

cmu_ng: The list that maps characters to their genders

corenlpsw: List of stopwords downloaded from core nlp 

imsdb_ssd: Scripts of movies,from the imsdb database,separated into dialogues and scenes

ms_cfap: character->power and character->agency map . 

## Script functions 

extractCharacterVerbs.py: Extracts the verbs used by each character in the dataset 
via dependancy parsing and coreference resolution using SpaCy. Download 'GoogleNews-vectors-negative300.bin' to run this script. 

extractMetadataForRMN.py: Extracted the metadata, span, movie and character embeddings, for the Relationship Modeling Network
proposed in the paper "Feuding Families and Former Friends"" written by Mohit Iyyer et al. 

fixCharacterGenders.py: Some of the characters in the cornell dataset,data/cdmn_mds, don't have genders so 
the script uses CMU name-gender corpus to obtain the genders for as many characters as possible. 

getConversationsSpanUnigrams: Creates a bag of words embedding for each span in a movie.   

util.py: Utility functions uses in another scripts. 

positive-negative.py: An attempt to predict whether a relationship is positive or negative. Uses a logistic regression model 
input as power and agency of a pair of characters. 





