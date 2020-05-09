import sys
sys.path.append("/Users/nikitarajaneesh/PycharmProjects/FilmCharacterRelationships")
from util import get_pa_maps
from util import sl_df_from_traj
from util import get_r_w_f_m
from util import get_char_gender

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

def get_f_m_df():
    p_map, a_map = get_pa_maps()
    trajectories = 'rmn/models/trajectories.log'
    train_df, num_desc = sl_df_from_traj(trajectories, p_map, a_map)
    f_m_df = get_r_w_f_m(num_desc,train_df)

    return f_m_df,num_desc

def get_pos_neg_val(avg_traj):
    topic_15 = avg_traj[15]
    topic_12 = avg_traj[12]
    topic_18 = avg_traj[18]
    topic_19 = avg_traj[19]

    pos_amount = topic_15 + topic_12
    neg_amount = topic_18+topic_19

    if(pos_amount > neg_amount):
        return 1
    else:
        return 0

def get_most_likely_descriptor(avg_traj):
    most_likely_descriptor = avg_traj.index(max(avg_traj))
    return most_likely_descriptor

def rels_pos_neg(get_f_m_df,num_desc):
    char_gender_dict = get_char_gender()
    p_a_pos_neg_d = []

    for row in get_f_m_df.itertuples():
        char_id_1 = row[2]
        char_id_2 = row[3]
        char_1_gender = char_gender_dict[char_id_1]
        char_2_gender = char_gender_dict[char_id_2]

        avg_traj = row[4:4+num_desc]
        pos_neg_val = get_pos_neg_val(avg_traj)

        p_1 = row[4+num_desc]
        p_2 = row[4+num_desc+1]
        a_1 = row[4+num_desc+2]
        a_2 = row[4+num_desc+3]

        char_p_a_pos = []

        if(char_1_gender == 'f'):
            p_f = p_1
            a_f = a_1
            p_m = p_2
            a_m = a_2
        else:
            p_f = p_2
            a_f = a_2
            p_m = p_1
            a_m = a_2

        char_p_a_pos.append(p_f)
        char_p_a_pos.append(a_f)
        char_p_a_pos.append(p_m)
        char_p_a_pos.append(a_m)
        char_p_a_pos.append(get_most_likely_descriptor(avg_traj))
        char_p_a_pos.append(pos_neg_val)
        p_a_pos_neg_d.append(char_p_a_pos)

    return np.array(p_a_pos_neg_d)

def get_one_hot_encoding(label_data,num_desc):
    label_data = label_data.astype(int)
    label_data = np.array(label_data)
    one_hot = np.zeros((label_data.size,label_data.max()+1))
    one_hot[np.arange(label_data.size),label_data] = 1

    return one_hot


if __name__ == '__main__':
    get_f_m_df,num_desc = get_f_m_df()
    p_a_pos_neg_d = rels_pos_neg(get_f_m_df,num_desc)

    p_a_pos_neg_d = pd.DataFrame(p_a_pos_neg_d)
    p_a_pos_neg_d = p_a_pos_neg_d.rename(columns={0: 'power_f',1:'agency_f',2:'power_m',3:'agency_m',4:'most_likely_d',5:'pos-neg'})
    p_a_data = p_a_pos_neg_d[['power_f','agency_f','power_m','agency_m']].to_numpy()
    pos_neg = p_a_pos_neg_d[['pos-neg']].to_numpy()[:,0]

    model = LogisticRegression(solver='sag',random_state=0)
    train_X = p_a_data[0:1000,:]
    train_Y = pos_neg[0:1000]
    model.fit(train_X,train_Y)
    train_accuracy = model.score(train_X,train_Y)
    test_X = p_a_data[1000:1285,:]
    test_Y = pos_neg[1000:1285]
    test_accuracy = model.score(test_X,test_Y)


    print('train accuracy:')
    print(train_accuracy)
    print('test accuracy')
    print(test_accuracy)

    most_likely_d = p_a_pos_neg_d[['most_likely_d']].to_numpy()
    most_likely_d = get_one_hot_encoding(most_likely_d[:,0],num_desc)

    pos_data = []
    neg_data = []

    for index in range(1000,p_a_data.shape[0]): #going through only test and checking
        if(pos_neg[index] == 1):
            pos_data.append(p_a_data[index].tolist())
        else:
            neg_data.append(p_a_data[index].tolist())
    pos_data = np.array(pos_data)
    neg_data = np.array(neg_data)
    print(pos_data.shape)
    print(neg_data.shape)