#!/usr/bin/env python
# coding: utf-8

# ### Bits and pieces for Lab Env Monitor
# 
# *output in jsonp - last measurement*

# In[183]:


import json
from erddapy import ERDDAP
import pandas as pd
import numpy as np
import datetime
import urllib.request

today = datetime.datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z')
yesterday = (datetime.datetime.utcnow()-datetime.timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')

server_url = 'http://downdraft.pmel.noaa.gov:8080/erddap'
request_url = '/tabledap/LabEnvMonitor.jsonlKVP?time%2CTemp_AQ%2CRH_AQ%2CBP_AQ%2CTempB%2CRHB%2CBPB%2CCo2_Conc%2CVOC&time%3E=2020-02-24T00%3A00%3A00Z&orderByMax(%22time%22)'

jsonout = json.loads(urllib.request.urlopen(server_url+request_url).read())


# In[184]:


jsonout.update({'datetime':datetime.datetime.strptime(jsonout['time'],
                                                     '%Y-%m-%dT%H:%M:%SZ').timestamp()})
jsonout.update({ "messages": "What sort of message would be helpful."})
jsonout.update({ "days": datetime.datetime.utcnow().day})


# In[185]:


d = ERDDAP(server=server_url,
    protocol='tabledap',
    response='csv'
)
d.dataset_id='LabEnvMonitor'

d.constraints={'time>=': datetime.datetime.now()-datetime.timedelta(hours=3)}
jsonout.update({"messages":"trends calculated using last 3hrs, red is greater than 1 std change, blue is greater than -1std change"})

try:
    df = d.to_pandas(

            index_col='time (UTC)',
            parse_dates=True,
            skiprows=(1,)  # units information can be dropped.
            )

    df.sort_index(inplace=True)
    df.columns = [x[1].split()[0] for x in enumerate(df.columns)]
    df_mean=df.mean()

    #temperature
    if (jsonout['Temp_AQ'] < (df.mean()['Temp_AQ']-df.std()['Temp_AQ']) ):
            jsonout.update({"tempAlert": "alert alert-info"})
    elif (jsonout['Temp_AQ'] > (df.mean()['Temp_AQ']+df.std()['Temp_AQ']) ):
            jsonout.update({"tempAlert": "alert alert-danger"})

    #moisture
    if (jsonout['RH_AQ'] < (df.mean()['RH_AQ']-df.std()['RH_AQ']) ):
            jsonout.update({"moistAlert": "alert alert-info"})
    elif (jsonout['RH_AQ'] > (df.mean()['RH_AQ']+df.std()['RH_AQ']) ):
            jsonout.update({"moistAlert": "alert alert-danger"})            
    #pressure
    if (jsonout['BP_AQ'] < (df.mean()['BP_AQ']-df.std()['BP_AQ']) ):
            jsonout.update({"pressAlert": "alert alert-info"})
    elif (jsonout['BP_AQ'] > (df.mean()['BP_AQ']+df.std()['BP_AQ']) ):
            jsonout.update({"pressAlert": "alert alert-danger"}) 
    #CO2
    if (jsonout['Co2_Conc'] < (df.mean()['Co2_Conc']-df.std()['Co2_Conc']) ):
            jsonout.update({"eCO2Alert": "alert alert-info"})
    elif (jsonout['Co2_Conc'] > (df.mean()['Co2_Conc']+df.std()['Co2_Conc']) ):
            jsonout.update({"eCO2Alert": "alert alert-danger"})             

    #VOC
    if (jsonout['VOC'] < (df.mean()['VOC']-df.std()['Co2_Conc']) ):
            jsonout.update({"VOCAlert": "alert alert-info"})
    elif (jsonout['VOC'] > (df.mean()['Co2_Conc']+df.std()['Co2_Conc']) ):
            jsonout.update({"VOCAlert": "alert alert-danger"})                      
except:
    jsonout.update({"messages":"no data in 3hr window to calculate trends",
                   "tempAlert": "alert alert-warning",
                   "pressAlert": "alert alert-warning",
                   "moistAlert": "alert alert-warning",
                   "eCO2Alert": "alert alert-warning",
                   "VOCAlert": "alert alert-warning"})


# In[186]:


with open('LabEnvMonitor.json', 'w') as my_data_file:
    my_data_file.write(json.dumps(jsonout,indent=0))


# In[ ]:




