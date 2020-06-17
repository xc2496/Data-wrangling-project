#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests as r
import os
import tweepy as tp
import json
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


#read data
df = pd.read_csv('twitter_archive_master.csv')


# In[3]:


df


# # Data Analysis and Visualization 
# 

# ## Research Questions:
# ### 1. What names of dogs are most popular?
# 

# In[4]:


name_list = df['name'].value_counts().head(10)
name_list


# In[5]:


#Visualization
name_list.plot(kind='bar', title = 'Names for Dogs (Frequency)');


# According to the number of frequencies of top 10 dog names, we can see that Oliver and Charlie are the most popular names. 
# 
# For a better visualization of all the dogs names, I would like to build a word cloud to show the popularity of names. 
# The larger the word is, the more dogs are called by that particular name.

# In[6]:


names_list = df.name.value_counts().index.tolist()
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
text = names_list
wordcloud = WordCloud(
    width = 2000,
    height = 2000,
    background_color = 'white',
    stopwords = STOPWORDS).generate(str(text))
fig = plt.figure(
    figsize = (30, 30),
    facecolor = 'c',
    edgecolor = 'c')
plt.imshow(wordcloud)
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()


# ### 2. What is the distribution of the dogs' stages?

# In[7]:


stages = df['growth'].value_counts()


# In[8]:


stages.plot(kind='bar',figsize=(8,5),color='#00a3af');


# Most of the dogs are at the pupper stage.

# ### 3. Do rating numerator and denominator have correlations to favoriate counts and retweet counts?
# 

# In[9]:


Rate = df[['rating_numerator','rating_denominator','retweet_count','favorite_count']].dropna()
Rate['Rate']=df['rating_numerator'] / df['rating_denominator']
Rate = Rate[Rate['Rate']<1.5]
sns.lmplot(x='Rate', y='favorite_count',data=Rate,size=8)


# In[10]:


sns.lmplot(x='Rate', y='retweet_count',data=Rate,size=8);


# In[11]:



sns.pairplot(Rate)


# According to the plots, the rate is positive correlated to the retweet count and favorite count.
