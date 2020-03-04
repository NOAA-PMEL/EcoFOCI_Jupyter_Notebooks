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
request_url = '/tabledap/OfficeRedboard_WxStation.jsonlKVP?time%2Ctemperature%2CRH_Percent%2CSLP%2CAltitude%2CUVA%2CUVB%2CUVindex&time%3E=2020-02-26T00%3A00%3A00Z&orderByMax(%22time%22)'

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
d.dataset_id='OfficeRedboard_WxStation'

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
    if (jsonout['temperature'] < (df.mean()['temperature']-df.std()['temperature']) ):
            jsonout.update({"tempAlert": "alert alert-info"})
            print("h")
    elif (jsonout['temperature'] > (df.mean()['temperature']+df.std()['temperature']) ):
            jsonout.update({"tempAlert": "alert alert-danger"})
            print("h")

    #moisture
    if (jsonout['RH_Percent'] < (df.mean()['RH_Percent']-df.std()['RH_Percent']) ):
            jsonout.update({"moistAlert": "alert alert-info"})
    elif (jsonout['RH_Percent'] > (df.mean()['RH_Percent']+df.std()['RH_Percent']) ):
            jsonout.update({"moistAlert": "alert alert-danger"})            
    #pressure
    if (jsonout['SLP'] < (df.mean()['SLP']-df.std()['SLP']) ):
            jsonout.update({"pressAlert": "alert alert-info"})
    elif (jsonout['SLP'] > (df.mean()['SLP']+df.std()['SLP']) ):
            jsonout.update({"pressAlert": "alert alert-danger"}) 
    #UVA
    if (jsonout['UVA'] < (df.mean()['UVA']-df.std()['UVA']) ):
            jsonout.update({"UVAAlert": "alert alert-info"})
    elif (jsonout['UVA'] > (df.mean()['UVA']+df.std()['UVA']) ):
            jsonout.update({"UVAAlert": "alert alert-danger"})             
    #UVB
    if (jsonout['UVB'] < (df.mean()['UVB']-df.std()['UVB']) ):
            jsonout.update({"UVBAlert": "alert alert-info"})
    elif (jsonout['UVB'] > (df.mean()['UVB']+df.std()['UVB']) ):
            jsonout.update({"UVBAlert": "alert alert-danger"})             
    #UVindex
    if (jsonout['UVindex'] < (df.mean()['UVindex']-df.std()['UVindex']) ):
            jsonout.update({"UVindexAlert": "alert alert-info"})
    elif (jsonout['UVindex'] > (df.mean()['UVindex']+df.std()['UVindex']) ):
            jsonout.update({"UVindexAlert": "alert alert-danger"})             

except:
    jsonout.update({"messages":"no data in 3hr window to calculate trends",
                   "tempAlert": "alert alert-warning",
                   "pressAlert": "alert alert-warning",
                   "moistAlert": "alert alert-warning",
                   "UVAAlert": "alert alert-warning",
                   "UVBAlert": "alert alert-warning",
                   "UVindexAlert": "alert alert-warning"})


# In[186]:


with open('OfficeEnvMonitor.json', 'w') as my_data_file:
    my_data_file.write(json.dumps(jsonout,indent=0))


# In[ ]:




