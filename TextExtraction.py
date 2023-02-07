#!/usr/bin/env python
# coding: utf-8

# In[9]:


import os
import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


# In[10]:


url_file_path= 'Input.xlsx'


# In[11]:


url_data= pd.read_excel(url_file_path)


# In[12]:


urls= url_data.iloc[:,1]


# In[13]:


print(urls)


# In[14]:


def writeText(ind,url):
    path= 'C://chromedriver.exe'
    browser= webdriver.Chrome(executable_path=path)
    browser.get(url)
    title= browser.title
    title= title[:-23]
    para= browser.find_elements(By.CLASS_NAME,'td-post-content')
    try:
        doc= para[0].text
        sen= list(doc.split('\n'))
        with open('extractedfolder/‪{}.txt'.format(title),'w',encoding='utf-8') as file:
            file.write(title)
            for i in range(len(sen)-1):
                file.write('\n')
                file.write(sen[i])
    except:
        pass
    
    return title
    


# In[15]:


indurls= []
headers= []
for i,url in enumerate(urls):
    title= writeText(i,url)
    lis=[url,title]
    indurls.append(lis)
    headers.append(title)


# In[8]:


import openpyxl


# In[16]:


df= pd.DataFrame(indurls,index=headers)


# In[17]:


df.head()


# In[19]:


df.to_excel('table.xlsx',encoding='utf-8')


# In[ ]:




