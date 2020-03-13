#!/usr/bin/env python
# coding: utf-8

# In[37]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import gensim
import random
from gensim.models import Word2Vec


# In[15]:


movies = pd.read_csv('ml-25m/movies.csv')
ratings = pd.read_csv('ml-25m/ratings.csv')


# In[16]:


movieId_to_name = pd.Series(movies.title.values, index = movies.movieId.values).to_dict()
name_to_movieId = pd.Series(movies.movieId.values, index = movies.title).to_dict()


# In[17]:


# Randomly display 5 records in the dataframe
for df in list((movies, ratings)):
    rand_idx = np.random.choice(len(df), 5, replace=False)
    display(df.iloc[rand_idx,:])
    print("Displaying 5 of the total "+str(len(df))+" data points")


# In[18]:


ratings_train, ratings_test = train_test_split(ratings)


# In[27]:


ratings_train['liked'] = np.where(ratings_train['rating']>=4, 1, 0)
ratings_train['movieId'] = ratings_train['movieId'].astype('str')
gp_user_like = ratings_train.groupby(['liked', 'userId'])


# In[ ]:


# 유저 n이 좋아한 영화 => positive example
# 유저 n이 싫어하는 영화 별로 그룹, 좋아하는 영화 별로 그룹핑
splitted_movies = [gp_user_like.get_group(gp)['movieId'].tolist() for gp in gp_user_like.groups]


# In[51]:


for movie_list in splitted_movies:
    random.shuffle(movie_list)


# In[52]:


print("전처리 완료")


# In[53]:


model = Word2Vec(sentences = splitted_movies,
                 iter = 20, # epoch
                 size = 100, # music dataset 파라미터 사용
                 sg = 1, # skip-gram: 1
                 hs = 0, # Set to 0, as we are applying negative sampling.
                 negative = 5, # negative sampling
                 window = 9999999)
model.save('item2vec_embeddings')


# In[ ]:




