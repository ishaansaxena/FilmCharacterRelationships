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
        movie_id = fields[2]

        list_lines = fields[3]
        list_lines = list_lines[2:len(list_lines) - 3]
        list_lines = list_lines.split("\', \'")
        if(movie_id not in movie_conversations_dict):
            movie_conversations_dict[movie_id] = []

        movie_conversations_dict[movie_id].append((character_1, character_2, list_lines))

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


def get_stage_imsbd():
    already_extracted = ['m49', 'm242', 'm52', 'm453', 'm516', 'm88', 'm548', 'm576', 'm171', 'm607', 'm285', 'm585',
                         'm0', 'm609',
                         'm444', 'm312', 'm435',
                         'm288', 'm63', 'm229', 'm425', 'm115', 'm408', 'm293', 'm116', 'm187', 'm130', 'm55', 'm499',
                         'm454', 'm109',
                         'm199', 'm56', 'm498', 'm249', 'm511', 'm308', 'm78', 'm446', 'm307', 'm90', 'm31', 'm28',
                         'm243', 'm278',
                         'm380',
                         'm467', 'm491', 'm149', 'm479', 'm462', 'm451', 'm102', 'm468', 'm15', 'm365', 'm67',
                         'm472', 'm528', 'm34', 'm409', 'm222', 'm540', 'm584', 'm57', 'm283', 'm181', 'm184', 'm71',
                         'm107', 'm328', 'm97', 'm315', 'm440', 'm176', 'm179', 'm411', 'm521', 'm221', 'm58', 'm272',
                         'm447', 'm236',
                         'm86', 'm200', 'm597', 'm478',
                         'm530', 'm14', 'm421', 'm126', 'm125', 'm579', 'm137', 'm245', 'm29', 'm505', 'm291',
                         'm407', 'm25', 'm423', 'm167’', 'm104', 'm306', 'm506', 'm123', 'm234', 'm257', 'm219', 'm517',
                         'm64', 'm414',
                         'm436',
                         'm298', 'm415', 'm601', 'm6', 'm36', 'm400', 'm296', 'm507', 'm287', 'm331', 'm598', 'm469',
                         'm72',
                         'm347', 'm267', 'm266', 'm240', 'm117', 'm178', 'm93', 'm51', 'm27', 'm496', 'm121', 'm61',
                         'm418', 'm173',
                         'm60',
                         'm363', 'm394', 'm145', 'm202', 'm329', 'm383', 'm159', 'm608', 'm162', 'm141', 'm256', 'm24',
                         'm65', 'm324', 'm533', 'm105', 'm30', 'm119',
                         'm152', 'm595', 'm534', 'm326', 'm497', 'm230', 'm330', 'm432', 'm38', 'm143', 'm309', 'm532',
                         'm335', 'm373', 'm59', 'm336', 'm477', 'm11', 'm570', 'm228', 'm577', 'm108', 'm98', 'm340',
                         'm43',
                         'm403', 'm99', 'm613', 'm300',
                         'm546', 'm271', 'm470', 'm280', 'm92', 'm381', 'm349', 'm482', 'm431', 'm515', 'm319', 'm201',
                         'm441', 'm158',
                         'm424', 'm87', 'm350', 'm33',
                         'm348', 'm572', 'm389', 'm437', 'm333', 'm248', 'm250', 'm502', 'm474', 'm129', 'm377', 'm188',
                         'm367', 'm170',
                         'm494', 'm2', 'm76', 'm247', 'm89',
                         'm40', 'm220', 'm133', 'm323', 'm169', 'm262', 'm390', 'm527', 'm110',
                         'm205', 'm21', 'm155', 'm358', 'm398', 'm439', 'm589', 'm581', 'm590', 'm281', 'm146', 'm276',
                         'm26', 'm599',
                         'm289',
                         'm46', 'm45', 'm606', 'm471', 'm168',
                         'm62', 'm318', 'm438', 'm128', 'm353', 'm10', 'm32', 'm16', 'm284', 'm218', 'm487',
                         'm428', 'm364', 'm166', 'm417', 'm165', 'm268', 'm520', 'm238', 'm258', 'm518', 'm578', 'm413',
                         'm582', 'm513',
                         'm370']

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
   # print(sentences)
   # print('coref resolved')
   # print(coref_resolved_conversation)
    text = nlp(coref_resolved_conversation)
    text_ext = textacy.extract.subject_verb_object_triples(text)
    subject_verb_obj_list = list(text_ext)

    return subject_verb_obj_list

def dialoges_char_verbs(cont,data_json,movie_conversations_dict,movie_lines_dict,movie_charidToName_dict,movie_charNameToid_dict):
    # all_conversations = ""
    for movie_id in movie_conversations_dict:
        list_conversations_movie = movie_conversations_dict[movie_id]
        print(movie_id)
        for character_1, character_2, list_lines in list_conversations_movie:
            conversation = ""
            for line_id in list_lines:
                cont_list = []
                original_line = movie_lines_dict[line_id][3]
                cont_list.append(original_line)
               # print(original_line)
                remove_shortform = list(cont.expand_texts(cont_list,precise=True))[0]
                #print(remove_shortform)
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
               # print(subject_verb_obj)
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
        remove_short_form_list = list(cont.expand_texts(cont_list,precise=True))
        corrected_movie_stage_direction = ''
        for sentence in remove_short_form_list:
            if(corrected_movie_stage_direction == ''):
                corrected_movie_stage_direction = sentence
            else:
                corrected_movie_stage_direction = corrected_movie_stage_direction + '.' + sentence

        print(corrected_movie_stage_direction)
        subject_verb_obj_list = get_subject_verb_obj_list(corrected_movie_stage_direction)
        print(subject_verb_obj_list)
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
    movie_conversations_dict, movie_lines_dict, movie_charidToName_dict, movie_charNameToid_dict = read_cornell_data()
    print('read cornell data')
    movie_conversation_count = 0
    movie_stage_direction = get_stage_imsbd()
    print('got stage direction data')
    data_json = {}
    cont = Contractions('GoogleNews-vectors-negative300.bin')  # change words like I'd -> I would
    print("before loading contractions models")
    cont.load_models()
    print('done loading  contrations models')
    dialoges_char_verbs(cont,data_json,movie_conversations_dict, movie_lines_dict, movie_charidToName_dict, movie_charNameToid_dict)
    print('extracted verbs from dialogues written to cvd.json')
    with open('cvd.json', 'w') as outfile:
     json.dump(data_json, outfile)

    stage_direction_char_verbs(cont,data_json,movie_stage_direction,movie_charNameToid_dict)
    print('extracted verbs from stage direction written to cvsd.json')
    with open('cvsd.json', 'w') as outfile:
        json.dump(data_json, outfile)
