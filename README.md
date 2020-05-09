# FilmCharacterRelationships
  This repository 

## Script functions 

extractCharacterVerbs.py: Extracts the verbs used by each character in the dataset 
via dependancy parsing and coreference resolution using SpaCy. 

extractMetadataForRMN.py: Extracted the metadata, span, movie and character embeddings, for the Relationship Modeling Network
proposed in the paper "Feuding Families and Former Friends"" written by Mohit Iyyer et al. 

fixCharacterGenders.py: Some of the characters in the cornell dataset,data/cdmn_mds, don't have genders so for some of 
these characters the script obtains the genders. 

getConversationsSpanUnigrams: Creates a bag of words embedding for each span in a movie.   

util.py: Utility functions uses in another scripts. 

positive-negative.py: An attempt to predict whether a relationship is positive or negative. Uses a logistic regression model 
input as power and agency of a pair of characters. 





