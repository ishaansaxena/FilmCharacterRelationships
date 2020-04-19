import spacy
import textacy
import neuralcoref
import json

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
        movie_charNameToid_dict[character_name + ' ' + movie_id] = char_id
        # print(movie_conversations_dict)
        # print(movie_lines_dict)
    return movie_conversations_dict, movie_lines_dict, movie_charidToName_dict,movie_charNameToid_dict


if __name__ == "__main__":
    nlp = spacy.load('en')
    read_cornell_data()
    movie_conversations_dict, movie_lines_dict, movie_charidToName_dict,movie_charNameToid_dict = read_cornell_data()
    neuralcoref.add_to_pipe(nlp)
    data_json = {}

    # all_conversations = ""
    for movie_id in movie_conversations_dict:
        character_1, character_2, list_lines = movie_conversations_dict[movie_id]
        print("start conversation: ")
        conversation = ""
        for line_id in list_lines:
            replaceiyou_line = movie_lines_dict[line_id][3]
            char_speaking_id = movie_lines_dict[line_id][0]
            char_speaking_name = movie_lines_dict[line_id][2]
            opposing_character = character_1
            if (opposing_character == char_speaking_id):
                opposing_character = character_2

            opposing_character_name = movie_charidToName_dict[opposing_character]
            if "I" in replaceiyou_line:
                replaceiyou_line =  replaceiyou_line.replace("I", char_speaking_name)
            if "you" in replaceiyou_line:
                replaceiyou_line = replaceiyou_line.replace("you", opposing_character_name)
            if "You" in replaceiyou_line:
                replaceiyou_line = replaceiyou_line.replace("You", opposing_character_name)

            conversation += replaceiyou_line

        #print(conversation)
        #print("end conversation")

        doc1 = nlp(conversation)
        #print("coref_clustesr:")
        #print(doc1._.coref_clusters)

        coref_resolved_conversation = doc1._.coref_resolved
        #print("resolved conversation:")
        #print(coref_resolved_conversation)

        text = nlp(coref_resolved_conversation)
        #print("subject_verb_triplets:")
        text_ext = textacy.extract.subject_verb_object_triples(text)
        subject_verb_obj_list = list(text_ext)

        print(subject_verb_obj_list)

        for subject_verb_obj in subject_verb_obj_list:
            subject = str(subject_verb_obj[0])
            verb = str(subject_verb_obj[1])
            if (subject + ' ' + movie_id) in movie_charNameToid_dict:
                print("in here")
                data_json_key = movie_charNameToid_dict[subject + ' ' + movie_id]
                if data_json_key in data_json:
                    data_json[data_json_key].append(verb)
                else:
                   data_json[data_json_key] = []
                   data_json[data_json_key].append(verb)

    with open('character_verb.json', 'w') as outfile:
        json.dump(data_json, outfile)