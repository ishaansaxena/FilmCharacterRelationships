import spacy
import textacy


def read_cornell_data():
    f = open("data/cornell movie-dialogs corpus/movie_conversations.txt","r", encoding="utf8", errors='ignore')
    movie_conversations = f.readlines()
    movie_conversations_dict = {}
    movie_lines = open("data/cornell movie-dialogs corpus/movie_lines.txt","r",encoding="utf8", errors='ignore')
    movie_lines_dict = {}
    for conversation in movie_conversations:
        fields = conversation.split(" +++$+++ ")
        character_1 = fields[0]
        character_2 = fields[1]
        movie = fields[2]

        list_lines = fields[3]
        list_lines = list_lines[2:len(list_lines)-3]
        list_lines = list_lines.split("\', \'")
        movie_conversations_dict[movie] = (character_1,character_2,list_lines)

    for line in movie_lines:

        fields = line.split(" +++$+++ ")
        line_id = fields[0]
        char_speaking = fields[1]
        movie = fields[2]
        actual_char_name = fields[3]
        actual_line = fields[4]

        movie_lines_dict[line_id] = (char_speaking,movie,actual_char_name,actual_line)

        #print(movie_conversations_dict)
        #print(movie_lines_dict)
    return movie_conversations_dict,movie_lines_dict
if __name__ == "__main__":
     nlp = spacy.load("en_core_web_sm")
     read_cornell_data()
     movie_conversations_dict, movie_lines_dict = read_cornell_data()
     for movie_id in movie_conversations_dict:
         character_1, character_2, list_lines = movie_conversations_dict[movie_id]
         print("start conversation: ")
         conversation = ""
         for line_id in list_lines:
             conversation+=movie_lines_dict[line_id][3]

         print(conversation)
         print("end conversation")
         text = nlp(conversation)
         text_ext = textacy.extract.subject_verb_object_triples(text)
         print(list(text_ext))
