#!/usr/bin/env python
# coding: utf-8

# # n-gram 언어모델
# 단어 문장 대신 아이템 넣어서 평가

# In[156]:


#코드 참조:
#데이터 사이언스 스쿨: 확률론적 언어 모형(https://datascienceschool.net/view-notebook/a0c848e1e2d343d685e6077c35c4203b/)
from nltk import bigrams, word_tokenize
from nltk.util import ngrams
import nltk
nltk.download("book", quiet=True)
from nltk.book import *

import pandas as pd
import numpy as np
from nltk import ConditionalFreqDist


# In[42]:


movies = pd.read_csv('ml-25m/movies.csv')
ratings = pd.read_csv('ml-25m/ratings.csv')


# In[43]:


ratings['liked'] = np.where(ratings['rating']>=4, 1, 0)
ratings['movieId'] = ratings['movieId'].astype('str')
gp_user_like = ratings.groupby(['liked', 'userId'])


# In[44]:


# 유저 n이 좋아한 영화 => positive example
# 유저 n이 싫어하는 영화 별로 그룹, 좋아하는 영화 별로 그룹핑
splitted_movies = [gp_user_like.get_group(gp)['movieId'].tolist() for gp in gp_user_like.groups]


# In[159]:


for movie_list in splitted_movies:
    random.shuffle(movie_list)


# In[158]:


splitted_movies


# ## 아이템셋 토큰화
# - window 사이즈 2인 n-gram 모형
# - SS: 문장의 처음
# - SE: 문장의 끝

# In[160]:


sentences = []
for tokens in splitted_movies:
    bigram = ngrams(tokens, 2, pad_left=True, pad_right=True, left_pad_symbol="SS", right_pad_symbol="SE")
    sentences += [t for t in bigram]


# In[54]:


print(sentences[:150])


# In[132]:


movieId_to_name = pd.Series(movies.title.values, index = movies.movieId.values).to_dict()
name_to_movieId = pd.Series(movies.movieId.values, index = movies.title).to_dict()


# In[161]:


cfd = ConditionalFreqDist(sentences)


# In[162]:


from nltk.probability import ConditionalProbDist, MLEProbDist
cpd = ConditionalProbDist(cfd, MLEProbDist)


# In[73]:


cpd[100]


# In[60]:


def sentence_score(s):
    p = 0.0
    for i in range(len(s) - 1):
        c = s[i]
        w = s[i + 1]
        p += np.log(cpd[c].prob(w) + np.finfo(float).eps)
    return np.exp(p)


# In[149]:


def generate_sentence(seed=None, start_word="SS"):
    if seed is not None:
        import random
        random.seed(seed)
        
    c = start_word
    sentence = []
    sentence.append(c)
    
    while True:
        if c not in cpd:
            break
        w = cpd[c].generate()
        if w == "SE":
            break
        else:
            w2 = w
        sentence.append(w2)
        c = w
    
    moviename = []
    for i in sentence:
        mname = movieId_to_name[int(i)]
        moviename.append(mname)
    
    return sentence, moviename


# In[177]:


sentence, movie = generate_sentence(start_word="3")


# In[178]:


print(sentence)
print(movie)


# ## 개선해야할 점
# - 조건부 확률... 순서는 상관이 없기 때문에 이 점 개선

# In[201]:


def find_usr_with_id(mid):
    usr = []
    for i in splitted_movies:
        if mid in i:
            usr.append(i)
    
    # 해당 mid를 본 유저와 생성한 sentence를 비교
    compare = [] # 생성한 sentence와 비교해 일치율 구하기
    for u in usr:
        c = list(set(u).intersection(sentence))
        prob = (len(c) / len(sentence)) * 100
        compare.append(prob)
    
    return usr, compare


# In[202]:


usr, compare = find_usr_with_id("3")


# In[198]:


compare.index(max(compare))


# In[200]:


compare[2837:2850]


# In[204]:





# In[ ]:




