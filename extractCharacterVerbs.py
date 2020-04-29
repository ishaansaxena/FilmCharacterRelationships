import spacy
import textacy
import neuralcoref
import json
from pycontractions import Contractions
import os

def read_cornell_data():
    f = open("data/cornell movie-dialogs corpus/movie_conversations.txt", "r", encoding="utf8", errors='ignore')
    movie_conversations = f.readlines()
    movie_conversations_dict = {}
    movie_lines = open("data/cornell movie-dialogs corpus/movie_lines.txt", "r", encoding="utf8", errors='ignore')
    movie_lines_dict = {}
    movie_characters = open("data/cornell movie-dialogs corpus/movie_characters_metadata.txt", "r", encoding="utf8",
                            errors='ignore')
    movie_charidToName_dict = {}
    movie_charNameToid_dict = {}
    for conversation in movie_conversations:
        fields = conversation.split(" +++$+++ ")
        character_1 = fields[0]
        character_2 = fields[1]
        movie = fields[2]

        list_lines = fields[3]
        list_lines = list_lines[2:len(list_lines) - 3]
        list_lines = list_lines.split("\', \'")
        movie_conversations_dict[movie] = (character_1, character_2, list_lines)

    for line in movie_lines:
        fields = line.split(" +++$+++ ")
        line_id = fields[0]
        char_speaking = fields[1]
        movie = fields[2]
        actual_char_name = fields[3]
        actual_line = fields[4]

        movie_lines_dict[line_id] = (char_speaking, movie, actual_char_name, actual_line)

    for character_metadata in movie_characters:
        fields = character_metadata.split(" +++$+++ ")
        char_id = fields[0]
        character_name = fields[1]
        movie_id = fields[2]
        movie_charidToName_dict[char_id] = character_name
        movie_charNameToid_dict[character_name.lower() + ' ' + movie_id] = char_id
        # print(movie_conversations_dict)
        # print(movie_lines_dict)
    return movie_conversations_dict, movie_lines_dict, movie_charidToName_dict,movie_charNameToid_dict


def get_stage_direction():
    imsdb_directory = 'data/imsdb_scenes_dialogs_nov_2015/scenes'
    movie_stage_direction_dict = {}
    movies_title_metadata = open("data/cornell movie-dialogs corpus/movie_titles_metadata.txt", "r", encoding="utf8",
                            errors='ignore')
    movie_title_name_to_id = {}

    for movie_metadata in movies_title_metadata:
        fields = movie_metadata.split(" +++$+++ ")
        movie_id = fields[0]
        movie_name = fields[1].replace(' ','')
        movie_title_name_to_id[movie_name] = movie_id

    for genre_directory in os.listdir(imsdb_directory):
        #print(genre_directory)
        for movie_file_name in os.listdir(imsdb_directory+ '/' + genre_directory):
            #print(movie_file_name)
            movie_name = movie_file_name.replace('_scene.txt','')
            if(movie_name in movie_title_name_to_id):
                movie_id = movie_title_name_to_id[movie_name]
                open_movie_state_direction = open(imsdb_directory+ '/' + genre_directory + '/' + movie_file_name,'r')
                movie_stage_direction_dict[movie_id] = open_movie_state_direction.read()

    return movie_stage_direction_dict

def get_subject_verb_obj_list(sentences):
    nlp = spacy.load('en')
    neuralcoref.add_to_pipe(nlp)

    doc1 = nlp(sentences)
    coref_resolved_conversation = doc1._.coref_resolved

    text = nlp(coref_resolved_conversation)

    #print(coref_resolved_conversation)
    text_ext = textacy.extract.subject_verb_object_triples(text)
    subject_verb_obj_list = list(text_ext)

    return subject_verb_obj_list

def dialoges_char_verbs(cont,data_json,movie_conversations_dict,movie_lines_dict,movie_charidToName_dict,movie_charNameToid_dict):
    # all_conversations = ""
    for movie_id in movie_conversations_dict:
        character_1, character_2, list_lines = movie_conversations_dict[movie_id]
        print("start conversation: ")
        conversation = ""
        for line_id in list_lines:
            cont_list = []
            original_line = movie_lines_dict[line_id][3]
            cont_list.append(original_line)
           # print(original_line)
            remove_shortform = list(cont.expand_texts(cont_list,precise=True))[0]
           # print(remove_shortform)
            replaceiyou_line = remove_shortform
            char_speaking_id = movie_lines_dict[line_id][0]
            char_speaking_name = movie_lines_dict[line_id][2]
            opposing_character = character_1
            if (opposing_character == char_speaking_id):
                opposing_character = character_2

            opposing_character_name = movie_charidToName_dict[opposing_character]
            if "I" in replaceiyou_line:
                replaceiyou_line = replaceiyou_line.replace("I", char_speaking_name)
            if "you" in replaceiyou_line:
                replaceiyou_line = replaceiyou_line.replace("you", opposing_character_name)
            if "You" in replaceiyou_line:
                replaceiyou_line = replaceiyou_line.replace("You", opposing_character_name)

            conversation += replaceiyou_line

        subject_verb_obj_list = get_subject_verb_obj_list(conversation)

        for subject_verb_obj in subject_verb_obj_list:
            subject = str(subject_verb_obj[0])
            verb = str(subject_verb_obj[1])
            if (subject.lower() + ' ' + movie_id) in movie_charNameToid_dict:
                data_json_key = movie_charNameToid_dict[subject.lower() + ' ' + movie_id]
                if data_json_key in data_json:
                    data_json[data_json_key].append(verb)
                else:
                    data_json[data_json_key] = []
                    data_json[data_json_key].append(verb)

def stage_direction_char_verbs(cont,data_json,movie_stage_direction_dict,movie_charNameToid_dict):
    for movie_id in movie_stage_direction_dict:
        print(movie_id)
        movie_stage_direction = movie_stage_direction_dict[movie_id]
        cont_list = movie_stage_direction.split('.')
        #  print(movie_stage_direction)
      #  cont_list.append(movie_stage_direction)
        print('expand texts')
        remove_short_form_list = list(cont.expand_texts(cont_list,precise=True))
        print('removed shortform')
        corrected_movie_stage_direction = ''
        for sentence in remove_short_form_list:
            corrected_movie_stage_direction+=sentence

        subject_verb_obj_list = get_subject_verb_obj_list(corrected_movie_stage_direction)

        for subject_verb_obj in subject_verb_obj_list:
            subject = str(subject_verb_obj[0])
            verb = str(subject_verb_obj[1])
            if (subject.lower() + ' ' + movie_id) in movie_charNameToid_dict:
                data_json_key = movie_charNameToid_dict[subject.lower() + ' ' + movie_id]
                if data_json_key in data_json:
                    data_json[data_json_key].append(verb)
                else:
                    data_json[data_json_key] = []
                    data_json[data_json_key].append(verb)

if __name__ == "__main__":
    cont = Contractions('GoogleNews-vectors-negative300.bin')  # change words like I'd -> I would
    print("before loading models")
    cont.load_models()
    print('done loading motherfucker')
    movie_conversations_dict, movie_lines_dict, movie_charidToName_dict, movie_charNameToid_dict = read_cornell_data()
    print('read cornell data')
    movie_stage_direction = get_stage_direction()
    data_json = {}
    print('got stage direction')
    dialoges_char_verbs(cont,data_json,movie_conversations_dict, movie_lines_dict, movie_charidToName_dict, movie_charNameToid_dict)
    stage_direction_char_verbs(cont,data_json,movie_stage_direction,movie_charNameToid_dict)

    with open('character_verb.json', 'w') as outfile:
       json.dump(data_json, outfile)