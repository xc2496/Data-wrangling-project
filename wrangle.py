#!/usr/bin/env python
# coding: utf-8

# # Gathering Data

# Import packages and assess datasets.

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


#read "twitter-archive-enhanced.csv" dataset.
dfTwitter = pd.read_csv('twitter-archive-enhanced.csv')
dfTwitter


# In[3]:


#download file from internet and read "image-predictions.tsv".
file_path = r'https://raw.githubusercontent.com/udacity/new-dand-advanced-china/master/%E6%95%B0%E6%8D%AE%E6%B8%85%E6%B4%97/WeRateDogs%E9%A1%B9%E7%9B%AE/image-predictions.tsv'
response = r.get(file_path)
with open(file_path.split('/')[-1],mode='wb') as file:
    file.write(response.content)
dfImage_Pred = pd.read_csv('image-predictions.tsv',sep='\t')
dfImage_Pred


# In[4]:


#Download from Twitter.

#consumer_key = 'YOUR CONSUMER KEY'
#consumer_secret = 'YOUR CONSUMER SECRET'
#access_token = 'YOUR ACCESS TOKEN'
#access_secret = 'YOUR ACCESS SECRET'

#auth = tp.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_secret)

#api = tp.API(auth)

#Print other users' contents from timeline
#public_tweets = api.user_timeline('WeRateDogs')
 
#for tweet in public_tweets:
#    print(tweet.text)


# In[ ]:





# Becasue of the contrain in the region, I am not able to use Twitter, so I read the json file directly.

# In[5]:


import zipfile
with open('tweet-json.zip','rb') as f:
    z_tweets = zipfile.ZipFile(f)
    z_tweets.extractall()

# check for the extracted file
z_tweets.namelist()


# In[6]:


# read the file in DataFrame
with open('tweet-json copy', 'r') as f:
    dfTweet_json = pd.read_json(f, lines= True, encoding = 'utf-8')

# check the data
dfTweet_json
# select the columns of interest : 'id', 'favorite_count','retweet_count'
dfTweet_json = dfTweet_json.loc[:,['id','favorite_count','retweet_count']]

#rename column id as tweet_id
dfTweet_json = dfTweet_json.rename(columns = {"id": "tweet_id"}) 
dfTweet_json.head()


# # Assessing Data

# ## Detect quality issues and tidiness issues in "dfTwitter" dataset.

# In[7]:


dfTwitter.info()


# In[8]:


#check rating_denominator
dfTwitter['rating_denominator'].value_counts()


# ### 1. The values in "rating_denominator" are not all integral tens digit, which also inclues some other integers, such as 11, 2, 16, 15, and 7.

# In[9]:


#check names
dfTwitter['name'].value_counts().head(20)


# ### 2. In dogs' names, there are some words with a, an, and the (articles), which is not a good way to identify the dogs' names. 

# In[10]:


(dfTwitter.iloc[:,-4:]=='None').astype(int).sum(axis=1).value_counts()


# ### 3. There is a mistake in dog's rates and some dogs have more thhan two rates.

# In[11]:


#check missing in names
(dfTwitter.loc[:,'name']=='None').astype(int).sum()


# ### 4. There are lots of missing in dogs' names. The data only have 745 input dog's names. 

# In[12]:


#check duplicatation
dfTwitter['tweet_id'].duplicated().sum()


# In[13]:


#Check for tweets with no image
dfTwitter['expanded_urls'].isnull().value_counts()


# ### 5. There are many tweets do not have images. 

# ## Detect quality issues and tidiness issues in "dfImage_Pred" dataset.

# 

# In[14]:


dfImage_Pred.info()


# In[15]:


#check duplications
dfImage_Pred['jpg_url'].duplicated().sum()


# In[ ]:





# ## Detect quality issues and tidiness issues in "dfTweet_json" dataset.

# In[16]:


dfTweet_json.info()


# 

# ## Document quality issues and tidiness issues in these three datasets.
# ### Quality Issues:
# #### dfTweeter:
# ##### 1. The datasets include infomation about retweet and forward.
# ##### 2. There are missing records in "expanded_urls" variable 
# ##### 3. The values in "rating_denominator" are not all integral tens digit, which also inclues some other integers, such as 11, 2, 16, 15, and 7.
# ##### 4. In dogs' names, there are some words with a, an, and the (articles), which is not a good way to identify the dogs' names.
# ##### 5. There are lots of missing in dogs' names. The data only have 745 inputs about dog's names.
# ##### 6. There are many tweets do not have images.
# ##### 7. In the column " source", there are record with the formats in HTML.
# #### dfImage_Pred:
# ##### 1. There are duplicated record in the dataset.
# ##### 2. In p1, p2, and p3, there is a mixed usage of upper case and lower case. The seperation of each word was not consistent.
# 
# ### Tidiness Issues:
# #### In dfTwitter，the "rate" of dogs used four variables to measure, they are: doggo,floofer,pupper, and puppo.
# #### The observations of these three dataframes are the same group of people, so we need to combine them into one dataframe. 

# In[ ]:





# # Cleaning Data

# In[17]:


# make copies of the datasets.
dfTwitter_C = dfTwitter.copy()
dfImage_Pred_C= dfImage_Pred.copy()
dfTweet_json_C = dfTweet_json.copy()


# ## dfTweeter:
# ### 1. The datasets include infomation about retweet and forward.
# #### - Delete retweet and forward records.

# In[18]:


dfTwitter_C = dfTwitter_C[dfTwitter_C['retweeted_status_id'].isnull()]
dfTwitter_C = dfTwitter_C[dfTwitter_C['in_reply_to_user_id'].isnull()]


# In[19]:


#test
dfTwitter_C.info()
#delete extra useless columns
dfTwitter_C.drop(['in_reply_to_status_id','in_reply_to_user_id','retweeted_status_id','retweeted_status_user_id','retweeted_status_timestamp'],axis=1,inplace=True)
dfTwitter_C.info()


# ### 2. There are missing records in "expanded_urls" variable
# #### -Delete missing records in "expanded_urls" variable

# In[20]:


dfTwitter_C = dfTwitter_C[dfTwitter_C['expanded_urls'].notnull()]


# In[21]:


#test
dfTwitter_C.info()


# ### 3. The values in "rating_denominator" are integral tens digit, which also includes some other integers, such as 11, 2, 16, 15, and 7.
# #### - For the data have two rating record, keep the first rate as the principle. If the cleaned data is still not in integral tens digit, change that number into the closest integral tens digit.
# 

# In[22]:


dfTwitter_C['rating_numerator'],dfTwitter_C['rating_denominator'] = dfTwitter_C['text'].str.extract(r'([0-9]+\.?[0-9]*\/[0-9]+0)',expand=True)[0].str.split("/",1).str


#Change one of the record manually
index = dfTwitter_C[dfTwitter_C['rating_numerator'].isnull()].index[0]
dfTwitter_C.loc[index,'rating_numerator']=24
dfTwitter_C.loc[index,'rating_denominator']=7

#change data type as float
dfTwitter_C['rating_numerator'] = dfTwitter_C['rating_numerator'].astype(float)
dfTwitter_C['rating_denominator'] = dfTwitter_C['rating_denominator'].astype(float)


# In[23]:


#test
dfTwitter_C['rating_denominator'].value_counts()


# In[24]:


dfTwitter_C['rating_numerator'].value_counts()


# ### 4. In dogs' names, there are some words with a, an, and the (articles), which is not a good way to identify the dogs' names.
# #### - Retrive back to the original post and gussing it is recorded after "This is...". Get the dogs' names from the original records.

# In[25]:


dfTwitter_C['name'] = dfTwitter_C['text'].str.extract(r'\S*[This is|Here is|Here\'s|named|Meet|Say hello to|Here we have]\s([A-Z][a-z]+).+',expand=True)


# In[26]:


#test
dfTwitter_C['name'].value_counts()


# ### 5. There are lots of missing in dogs' names. The data only have 745 input dog's names
# #### - I am not able to add any more information here, since the users didn't provide any inputs here.

# ### 6. There are many tweets do not have images.
# #### -There is no status data available from the Twitter API and not all tweets have an image. I did not confirm that all tweets with an image stored the image.

# ### 7. In the column " source", there are record with the formats in HTML.
# #### - Get the url

# In[27]:


dfTwitter_C['source'] = dfTwitter_C['source'].str.extract(r'>(.+)<',expand=True)


# In[28]:


#test
dfTwitter_C.head()


# ## dfImage_Pred:
# ### 1. There are duplicated record in the dataset.
# #### - Remove the duplicated records

# In[29]:


dfImage_Pred_C.drop_duplicates(subset='jpg_url',inplace=True)


# In[30]:


#test
dfImage_Pred_C['jpg_url'].duplicated().sum()
#Cool! The duplication is 0 now!


# ### 2. In p1, p2, and p3, there is a mixed usage of upper case and lower case. The seperation of each word was not consistent.
# #### - Change all the letters in lower case and change all the seprations as underscore.

# In[31]:


dfImage_Pred_C[['p1','p2','p3']] = dfImage_Pred_C[['p1','p2','p3']].applymap(str.lower)
dfImage_Pred_C[['p1','p2','p3']] = dfImage_Pred_C[['p1','p2','p3']].replace(' ','_').replace('-','_')


# In[32]:


#test
dfImage_Pred_C.head(5)


# ##  In dfTwitter，the "rate" of dogs used four variables to measure, they are: doggo,floofer,pupper, and puppo.
# ### - Combine the columns (doggo,floofer,pupper,puppo) and create a new column called "growth". Delete doggo,floofer,pupper, and puppo. 

# In[33]:


#Combine
dfTwitter_C['growth'] = dfTwitter_C['doggo']+dfTwitter_C['floofer']+dfTwitter_C['pupper']+dfTwitter_C['puppo']
dfTwitter_C['growth'] = dfTwitter_C['growth'].str.replace('None','')
dfTwitter_C = dfTwitter_C.replace(({'growth':{'':np.nan}}))

#Create new column and delete the old four columns.
dfTwitter_C.drop(['doggo','floofer','pupper','puppo'],axis=1,inplace=True)
dfTwitter_C[dfTwitter_C['growth'].notnull()]


# In[34]:


dfTwitter_C['growth'].value_counts()


# ## The observations of these three dataframes are the same group of people, so we need to combine them into one dataframe.
# ### Use merge to combine three dataframes.
# 

# In[35]:


dfCombine = pd.merge(dfTwitter_C,dfImage_Pred_C,how='inner',on='tweet_id').merge(dfTweet_json_C,how='left',on='tweet_id')


# In[36]:


#test
dfCombine.info()


# In[37]:


#test
dfCombine.head()


# The data looks good to evaluate now.  
# 

# In[38]:


#save the cleaned dataframe.
dfCombine.to_csv('twitter_archive_master.csv', index=False)


# In[ ]:




