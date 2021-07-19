#!/usr/bin/env python
# coding: utf-8

# # Scraping Bangladesh's Drug Pricing Database

# In[1]:


# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[2]:


#search_url = "https://www.dgda.gov.bd/administrator/components/com_jcode/source/serverProcessing.php" - results in get request failure
site_url = "https://www.dgda.gov.bd/index.php/registered-products/allopathic"
response = requests.get(site_url)

doc = BeautifulSoup(response.text, 'html.parser')


# In[3]:


doc


# In[4]:


#target table (.dataTables_scroll -> .dataTables_scrollBody -> #gridData -> tbody) not accessible
doc.select('#gridData')


# In[5]:


# import POST request via cURL to python conversion @ curl.trillworks
import requests

cookies = {
    '64b89d05a4a7cf540e8cd068c2904eaf': 'fa7192c534ca78f84b6490b3023e3b62',
    'bd4dac94c5b33f61525233fb263569b2': 'a15cb41968cb6b5c235e9826ade10634',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.dgda.gov.bd',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.dgda.gov.bd/index.php/registered-products/allopathic',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

data = {
  'sEcho': '2',
  'iColumns': '9',
  'sColumns': '',
  'iDisplayStart': '0',
  'iDisplayLength': '100000', #tried changing this to 100000 to get all results, but the server doesn't like it
  'mDataProp_0': '0',
  'mDataProp_1': '1',
  'mDataProp_2': '2',
  'mDataProp_3': '3',
  'mDataProp_4': '4',
  'mDataProp_5': '5',
  'mDataProp_6': '6',
  'mDataProp_7': '7',
  'mDataProp_8': '8',
  'sSearch': '',
  'bRegex': 'false',
  'sSearch_0': '',
  'bRegex_0': 'false',
  'bSearchable_0': 'true',
  'sSearch_1': '',
  'bRegex_1': 'false',
  'bSearchable_1': 'true',
  'sSearch_2': '',
  'bRegex_2': 'false',
  'bSearchable_2': 'true',
  'sSearch_3': '',
  'bRegex_3': 'false',
  'bSearchable_3': 'true',
  'sSearch_4': '',
  'bRegex_4': 'false',
  'bSearchable_4': 'true',
  'sSearch_5': '',
  'bRegex_5': 'false',
  'bSearchable_5': 'true',
  'sSearch_6': '',
  'bRegex_6': 'false',
  'bSearchable_6': 'true',
  'sSearch_7': '',
  'bRegex_7': 'false',
  'bSearchable_7': 'true',
  'sSearch_8': '',
  'bRegex_8': 'false',
  'bSearchable_8': 'true',
  'iSortCol_0': '1',
  'sSortDir_0': 'asc',
  'iSortingCols': '1',
  'bSortable_0': 'false',
  'bSortable_1': 'true',
  'bSortable_2': 'true',
  'bSortable_3': 'true',
  'bSortable_4': 'true',
  'bSortable_5': 'true',
  'bSortable_6': 'false',
  'bSortable_7': 'true',
  'bSortable_8': 'false',
  'action': 'getDrugCompanyDatabaseData',
  'FilterAll': '4',
  'FilterItem': ''
}

response = requests.post('https://www.dgda.gov.bd/administrator/components/com_jcode/source/serverProcessing.php', headers=headers, cookies=cookies, data=data)


# In[6]:


#read json file
from io import StringIO

table = pd.read_json(StringIO(response.text))


# In[7]:


#confirm table import
table


# In[8]:


#drop unnecessary columns
table = table.drop(columns = ['sEcho', 'iTotalRecords', 'iTotalDisplayRecords'])


# In[9]:


#view new dataframe
table


# In[10]:


#convert dataframe back into series for element extraction
series = pd.Series(table.aaData)


# In[11]:


#every element will be extracted to a corresponding list via for loop

#initialize list
row_id = []
manufacturer = []
brand = []
generic_name = []
strength = []
form = []
retail_price = []
use = []
dar = []

#extract elements into corresponding lists
for element in series:
    row_id.append(element[0])
    manufacturer.append(element[1])
    brand.append(element[2])
    generic_name.append(element[3])
    strength.append(element[4])
    form.append(element[5])
    retail_price.append(element[6])
    use.append(element[7])
    dar.append(element[8])

#convert lists into dataframe    
df = pd.DataFrame(list(zip(row_id, manufacturer, brand, generic_name, strength, form, retail_price,
use, dar)), columns = ['row_id', 'manufacturer', 'brand', 'generic_name', 'strength', 'form', 'retail_price',
'use', 'dar'])


# In[12]:


#drop unnecessary index column and all records irrelevant for human use
df = df.drop(columns = 'row_id')


# In[13]:


#print dataframe to confirm
df.head(3)


# In[14]:


#add date of scrape to dataframe
from datetime import datetime

df['scrape_date'] = datetime.today().date()


# In[15]:


#print dataframe to confirm
df.head(3)


# In[16]:


# replace blank values with NaN to match csv output from base DGDA dataframe
df = df.replace(r'^\s*$', np.nan, regex=True)

# check to confirm
df[df['dar'] == '304--077']


# In[17]:


#check for duplicates
df[df.duplicated()]


# In[18]:


#read base csv
url = 'https://raw.githubusercontent.com/swatiyengar/dgda_scraper/main/bgd_scraped.csv'
dgda = pd.read_csv(url, error_bad_lines=False)
dgda.info()


# In[19]:


# drop index
dgda.drop(columns = 'Unnamed: 0')


# In[20]:


# check for duplicates
dgda[dgda['dar'] == '304--077']
dgda[dgda.duplicated()]


# In[21]:


#append scraped file to base file
dgda = dgda.append(df, ignore_index = True).drop(columns = 'Unnamed: 0')


# In[22]:


dgda


# In[23]:


#drop duplicates in scraped file based column names
dgda = dgda.drop_duplicates(subset = ['manufacturer','brand', 'generic_name','strength', 'form', 'retail_price', 'use', 'dar'], keep = 'first')


# In[24]:


#print dataframe
dgda


# In[25]:


# print to csv
dgda.to_csv('bgd_scraped.csv')

