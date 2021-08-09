#!/usr/bin/env python
# coding: utf-8

# ### Bits and pieces for Shop Env Monitor
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
request_url = '/tabledap/channel_843357_thingspeak.jsonlKVP?time%2Centry_id%2Ctemperature%2CRH_Percent%2CBarotemperature%2CSLP&time%3E=2019-12-19&orderByMax(%22time%22)'
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
d.dataset_id='channel_843357_thingspeak'

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
    if (jsonout['Barotemperature'] < (df.mean()['Barotemperature']-df.std()['Barotemperature']) ):
            jsonout.update({"tempAlert": "alert alert-info"})
    elif (jsonout['Barotemperature'] > (df.mean()['Barotemperature']+df.std()['Barotemperature']) ):
            jsonout.update({"tempAlert": "alert alert-danger"})
          
    #pressure
    if (jsonout['SLP'] < (df.mean()['SLP']-df.std()['SLP']) ):
            jsonout.update({"pressAlert": "alert alert-info"})
    elif (jsonout['SLP'] > (df.mean()['SLP']+df.std()['SLP']) ):
            jsonout.update({"pressAlert": "alert alert-danger"}) 
                     
except:
    jsonout.update({"messages":"no data in 3hr window to calculate trends",
                   "tempAlert": "alert alert-warning",
                   "pressAlert": "alert alert-warning",
                   "moistAlert": "alert alert-warning"})



with open('ShopEnvMonitor.json', 'w') as my_data_file:
    my_data_file.write(json.dumps(jsonout,indent=0))





