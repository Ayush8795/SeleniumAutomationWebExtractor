#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import re
import os


# In[1]:


get_ipython().system('pip install textblob')


# In[2]:


from textblob import TextBlob


# In[ ]:


# analyse=TextBlob("movie")

# print(analyse.sentiment.polarity)


# In[4]:


analysis_scores=[]
cln_txt=''
cln_words=[]
total_words=0 #no of cleaned words
no_of_sent=0 # no of sentences
all_total_words=0 # total no. of words prior cleaning


# In[5]:


dir_lis= os.listdir('extractedfolder')


# ## Sentiment Analysis

# In[6]:


def DataCleaning(text):
    cleaned_words=[]
    regex= r"(http[s]?\://\S+)|([\[\(].*[\)\]])|([#@]\S+)|\n"
    ntext= re.sub(regex,"",text)
    ntext= re.sub(r'[^\w\s]','',text)

    return ntext


# In[7]:


def stop_correct(text):
    text_lis= text.split()
    final_words=[]
    flag=False
    pathfiles= os.listdir('Stopwords')
    for word in text_lis:
        for file in pathfiles:
            read= open('Stopwords/'+file,'r')
            rd= read.readlines()
            for strng in rd:
                if not re.match(word,strng,re.IGNORECASE):
                    flag=True
                else:
                    flag= False
                    break
        
        if flag:
            final_words.append(word)
    return final_words
        


# In[8]:


def pos_neg(text_lis):
    pos=0
    neg=0
    neut=0
    pnfiles= os.listdir('MasterDictionary')
    for word in text_lis:
#         matchneg= open('MasterDictionary/'+pnfiles[0],'r')
#         matchpos= open('MasterDictionary/'+pnfiles[1],'r')
#         wdneg= matchneg.readlines()
#         wdpos= matchpos.readlines()
        analysis= TextBlob(word)
        score= analysis.sentiment.polarity
        if score>0:
            pos+=1
        else:
            if score<0:
                pos+=1
            else:
                neut+=1
    return pos,neg,neut


# In[9]:


def get_scores(text_lis):
    pscore,nscore,nuscore= pos_neg(text_lis)
    twords= len(text_lis)
    pol_score= (pscore-nscore)/((pscore+nscore)+0.000001)
    sub_score= (pscore+nscore)/((twords)+0.000001)
    return [pscore,nscore,pol_score,sub_score]


# In[10]:


def save_values(title,slis):
    val= [title]
    for s in slis:
        val.append(s)
    analysis_scores.append(val)


# In[ ]:





# ## Analysis of Readability

# In[11]:


import nltk


# In[11]:


nltk.download('punkt')


# In[12]:


def readability_analysis(text):
    sentences= nltk.sent_tokenize(text)
    ns= len(sentences)
    no_of_sent=ns
    
    ncw=0
    all_words= text.split()
    tw= len(all_words)
    all_total_words=tw
    avl= tw/ns
    for wd in all_words:
        if len(wd)>2:
            ncw+=1
    
    pocw= ncw/len(all_words)
    fog= 0.4*(avl+pocw)
    return avl,pocw,fog


# ## average number of words per sentence

# In[13]:


def avg_no_words(text):
    
    nw= len(text.split())
    ns= len(nltk.sent_tokenize(text))
    if ns==0:
        return 0
    return nw/ns


# ## syllable count

# In[14]:


def sylcnt(text):
    words= text.split()
    cnt=0
    x=''
    for word in words:
        word= word.lower()
        if word[-2:]=='es' or word[-2:]=='ed':
            x= word[:-2]
        else:
            x=word
        for ch in x:
            if ch=='a' or ch=='e' or ch=='i' or ch=='o' or ch=='u':
                cnt+=1
    
    return cnt


# ## Personal pronouns

# In[15]:


reg= re.compile(r'\bI|we|our[s]?|me|my\b',re.I)
reg2= re.compile(r'us')

def personal_pronouns(text):
    ppl= reg.findall(text)
    ppl2= reg2.findall(text)
    npp= len(ppl)+len(ppl2)
    return npp


# ## average word length

# In[16]:


def avg_wd_len(text):
    all_words= text.split()
    chars=0
    for word in all_words:
        chars+=len(word)
    awl= chars/len(all_words)
    return awl


# In[ ]:





# In[ ]:





# In[17]:


for doc in dir_lis:
    try:
       
        text= open('extractedfolder/{}'.format(doc),'r',encoding='utf-8')
        ttext= text.readlines()
        title= ttext[0]
        print('Opening doc: {}----'.format(title))
        ctext=''
        for tex in ttext:
            ctext=ctext+' '+tex
            
        print('---------------Cleaning Data-----------------')
    
        cln_txt= DataCleaning(ctext)
        cln_words= stop_correct(cln_txt)
        total_words= len(cln_txt)
        slis= get_scores(cln_words)
        
        print('---------------Readability Analysis-----------------')

        avg_sen_length,pocw,fog= readability_analysis(ctext)
        slis.append(avg_sen_length)
        slis.append(pocw)
        slis.append(fog)
        
        print('------------Average no of words-------------')
    
        avgnw= avg_no_words(ctext)
        slis.append(avgnw)
        slis.append(total_words)
        nsyl= sylcnt(ctext)
        
        print('---------------Determining personal pronouns-----------------')
    
        slis.append(nsyl)
        npp= personal_pronouns(ctext)
        slis.append(npp)
    
        awl= avg_wd_len(ctext)
        slis.append(awl)
    
        save_values(title,slis)
    
    except:
        pass
    


# In[18]:


df= pd.DataFrame(analysis_scores)
df.head()
# df.shape
heads=['TITLE','POSITIVIE SCORE','NEGATIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE','AVERAGE SENTENCE LENGTH','PERCENTAGE OF COMPOUND WORDS','FOG INDEX','AVERAGE NUMBER OF WORDS','WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUN','AVG WORD LENGTH']
df.columns= heads
df.head()


# In[19]:


df.tail()


# In[20]:


df.to_excel('analysis2.xlsx',encoding='utf-8')


# In[21]:


frame1= pd.read_excel('table.xlsx')
frame2= pd.read_excel('analysis2.xlsx')


# In[33]:


x=frame2['TITLE']
flis=[]
fflis=[]
for i,item in enumerate(x):
    flis=[]
    item= item[:-1]
    flis=[item]
    for j,val in enumerate(frame1[1]):
        if val==item:
            flis.append(frame1.iloc[j][0])
            break
    fl=flis+[v for v in frame2.iloc[i][2:]]
    fflis.append(fl)
    


# In[34]:


heads2= ['TITLE','URL']+heads[1:]
print(heads2)


# In[35]:


print(fflis)


# In[36]:



# print(heads2)
df4= pd.DataFrame(fflis,columns=heads2)
df4.head()
df4.shape


# In[37]:


df4.to_excel('output2.xlsx')


# In[ ]:




