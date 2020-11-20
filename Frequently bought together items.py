#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# In[2]:


FILE_PATH = '/kaggle/input/groceries-dataset/Groceries_dataset.csv'
groceries = pd.read_csv(FILE_PATH)
#groceries = pd.read_csv(r'C:\Users\negar\Desktop\Datasets for Python Programming\Groceries_dataset.csv')


# In[3]:


groceries['Date'] = pd.to_datetime(groceries['Date'], format='%d-%m-%Y')
groceries = groceries.sort_values('Date')
groceries.index = list(range(0,len(groceries)))


# In[4]:


print('The number of customers is',groceries['Member_number'].nunique())
print('The number of goods is',groceries['itemDescription'].nunique())


# In[5]:


goods = set(list(groceries['itemDescription']))
# We survey on goods that have been bought at least 50 times and see the frequency of it
good_freq = {}
for good in goods:
    if list(groceries['itemDescription']).count(good) >= 50 : 
        good_freq[good] = list(groceries['itemDescription']).count(good)


# In[6]:


sorted_good_freq = sorted(list(good_freq.items()) , key = lambda x: x[1] , reverse = True )


# In[7]:


# Now we want to extract each receipt seperately. First we extract each customers all time receipts
customer_based = groceries.groupby(['Member_number','Date'])


# In[8]:


receipts = []

for unkn in customer_based.groups:
    sub = []
    for num in customer_based.groups[unkn]:    
        sub.append(groceries.iloc[num]['itemDescription'])
    receipts.append(sub)

receipts = sorted(receipts,key=len)


# In[9]:


two_items = list(filter(lambda x: len(x)==2,receipts))
two_items = sorted(two_items , key= lambda x : (x[0],x[1]) )
# two_items is a list containing all the receipts with only two items


# In[10]:


more_than_two_items = list(filter(lambda x: len(x)!=2,receipts))
more_than_two_items = sorted(more_than_two_items , key= lambda x : (x[0],x[1]) )
# more_than_two_items is a list containing all the receipts with more than two items


# In[11]:


for idx in range(len(two_items)):
    for num in range(idx,len(two_items)):
        if set(two_items[num]) == set(two_items[idx]):
            two_items[num] = two_items[idx]
# This is for unifying the same receipts with differect item positions


# In[12]:


freq_tgthr = {}
for receipt in two_items:
    c = 0
    for goods in receipts:
        if receipt[0] != receipt[1]:
            if receipt[0] in goods:
                if receipt[1] in goods:
                    c += 1
    #print(receipt[0],receipt[1])
                    freq_tgthr[str(receipt[0].capitalize()+'  and  '+str(receipt[1].capitalize()))]= c

#freq_tgthr = sorted(freq_tgthr, key = value , reverse = True )
{k: v for k, v in sorted(freq_tgthr.items(), key = lambda item: item[1] , reverse=True)}

# The final results is a dictionary that shows us which items have been bought together more frequently!!!


# In[ ]:




