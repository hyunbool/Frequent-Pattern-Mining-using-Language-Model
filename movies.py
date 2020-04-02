#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split

import sys
import os
sys.path.append('..')
try:
    import urllib.request
except ImportError:
    raise ImportError('Use Python3!')
import pickle
import numpy as np


# In[2]:


"""
movies = pd.read_csv('ml-25m/movies.csv')
ratings = pd.read_csv('ml-25m/ratings.csv')
    
ratings_train, ratings_test = train_test_split(ratings)
ratings_train.to_pickle("ratings_train.pkl")
ratings_test.to_pickle("ratings_test.pkl")

with open('ratings_train.pkl', 'rb') as f:
    ratings_train = pickle.load(f)
with open('ratings_test.pkl', 'rb') as f:
    ratings_test = pickle.load(f)
    
ratings_train['liked'] = np.where(ratings_train['rating']>=4, 1, 0)
ratings_train['movieId'] = ratings_train['movieId'].astype('str')
gp_user_like_train = ratings_train.groupby(['liked', 'userId'])

ratings_test['liked'] = np.where(ratings_test['rating']>=4, 1, 0)
ratings_test['movieId'] = ratings_test['movieId'].astype('str')
gp_user_like_test = ratings_test.groupby(['liked', 'userId'])

# 유저 n이 좋아한 영화 => positive example
# 유저 n이 싫어하는 영화 별로 그룹, 좋아하는 영화 별로 그룹핑
splitted_movies_train = [gp_user_like_train.get_group(gp)['movieId'].tolist() for gp in gp_user_like_train.groups]
splitted_movies_test = [gp_user_like_test.get_group(gp)['movieId'].tolist() for gp in gp_user_like_test.groups]

for i in range(len(splitted_movies_train)):
    splitted_movies_train[i].append('\n')
for i in range(len(splitted_movies_test)):
    splitted_movies_test[i].append('\n')
    
movies_train =[]
for i in range(len(splitted_movies_train)):
    movies_train.append(' '.join(splitted_movies_train[i]))
movies_test =[]
for i in range(len(splitted_movies_test)):
    movies_test.append(' '.join(splitted_movies_test[i]))
    
with open('splitted_movies_train.txt', 'w', encoding='utf-8') as file:
    file.writelines(movies_train)
with open('splitted_movies_test.txt', 'w', encoding='utf-8') as file:
    file.writelines(movies_test)
    
"""


# In[5]:


key_file = {
    'train':'splitted_movies_train.txt',
    'test':'splitted_movies_test.txt'
}
save_file = {
    'train':'splitted_movies_train.npy',
    'test':'splitted_movies_test.npy'
}
vocab_file = 'movies.pkl'

def load_vocab():
    vocab_path = vocab_file

    if os.path.exists(vocab_path):
        with open(vocab_path, 'rb') as f:
            word_to_id, id_to_word = pickle.load(f)
        return word_to_id, id_to_word

    word_to_id = {}
    id_to_word = {}
    data_type = 'train'
    file_name = key_file[data_type]
    file_path = file_name

    words = open(file_path).read().replace('\n', '<eos> ').strip().split()

    for i, word in enumerate(words):
        if word not in word_to_id:
            tmp_id = len(word_to_id)
            word_to_id[word] = tmp_id
            id_to_word[tmp_id] = word

    with open(vocab_path, 'wb') as f:
        pickle.dump((word_to_id, id_to_word), f)

    return word_to_id, id_to_word

def load_data(data_type='train'):
    '''
        :param data_type: 데이터 유형: 'train' or 'test' or 'valid (val)'
        :return:
    '''
    save_path = save_file[data_type]

    word_to_id, id_to_word = load_vocab()
        
    if os.path.exists(save_path):
        corpus = np.load(save_path)
        return corpus, word_to_id, id_to_word

    file_name = key_file[data_type]
    file_path = file_name

    words = open(file_path, 'r').read().replace('\n', '<eos> ').strip().split()

    print(word_to_id)
            
    corpus = np.array([word_to_id[w] for w in words])

    np.save(save_path, corpus)
    return corpus, word_to_id, id_to_word


if __name__ == '__main__':
    for data_type in ('train', 'test'):
        load_data(data_type)


# In[ ]:




