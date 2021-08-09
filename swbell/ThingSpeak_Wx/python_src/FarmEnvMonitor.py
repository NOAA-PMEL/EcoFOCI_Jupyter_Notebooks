#!/usr/bin/env python
# coding: utf-8

# ### Bits and pieces for Shop Env Monitor
# 
# Source: thingspeak

# In[183]:


import json
import thingspeak as thingspeak
import pandas as pd
import numpy as np
import datetime
import urllib.request

today = datetime.datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z')
yesterday = (datetime.datetime.utcnow()-datetime.timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')

sbell = thingspeak.TSAccount('https://api.thingspeak.com/','869L0PHK8GKAIIYQ')
jsonout = json.loads("{}")

jsonout.update({'datetime':datetime.datetime.utcnow().timestamp()})
jsonout.update({ "messages": "Time is when last downloaded, not time of last measurement."})
jsonout.update({ "days": datetime.datetime.utcnow().day})

### cellar
sbellc = thingspeak.TSChannel(acc_host_addr='https://api.thingspeak.com/',api_key='QS3DYISJPLE5EQCW'
,ch_id=1037066)
dt11 = sbellc.get_a_channel_field_feed(['field1','field2'],parameters={'minutes':2})
dt11_df = pd.DataFrame(dt11['feeds'])
dt11_df = dt11_df.set_index(pd.DatetimeIndex(dt11_df['created_at']))
dt11_df['field1'] = dt11_df['field1'].astype('float64')
dt11_df['field2'] = dt11_df['field2'].astype('float64')
dt11_df.rename(columns = {'field1':'temperature','field2':'humidity'},inplace = True)

if dt11_df['temperature'].mean() <= 10:
    jsonout.update({"Temp_Cellar_Alert": "alert alert-info"})
elif (dt11_df['temperature'].mean() > 10) and (dt11_df['temperature'].mean() < 20):
    jsonout.update({"Temp_Cellar_Alert": "alert alert-warning"})
elif (dt11_df['temperature'].mean() >= 20):
    jsonout.update({"Temp_Cellar_Alert": "alert alert-danger"})
else:
    jsonout.update({"Temp_Cellar_Alert": ""})

jsonout.update({"Temp_Cellar": dt11_df['temperature'].mean()})               
###

### shop
sbellc = thingspeak.TSChannel(acc_host_addr='https://api.thingspeak.com/',api_key='QS3DYISJPLE5EQCW'
,ch_id=843357)
bmp = sbellc.get_a_channel_field_feed(['field3','field4'],parameters={'minutes':15})
bmp_df = pd.DataFrame(bmp['feeds'])
bmp_df = bmp_df.set_index(pd.DatetimeIndex(bmp_df['created_at']))
bmp_df['field3'] = bmp_df['field3'].astype('float64')
bmp_df['field4'] = bmp_df['field4'].astype('float64')
bmp_df.rename(columns = {'field3':'temperature','field4':'pressure'},inplace = True)

if bmp_df['temperature'].mean() <= 10:
    jsonout.update({"Temp_Shop_Alert": "alert alert-info"})
elif (bmp_df['temperature'].mean() > 10) and (dt11_df['temperature'].mean() < 20):
    jsonout.update({"Temp_Shop_Alert": "alert alert-warning"})
elif bmp_df['temperature'].mean() >= 20:
    jsonout.update({"Temp_Shop_Alert": "alert alert-danger"})
else:
    jsonout.update({"Temp_Shop_Alert": ""})

jsonout.update({"Temp_Shop": bmp_df['temperature'].mean()})                   

                   
###

### Tysons Room
sbellc = thingspeak.TSChannel(acc_host_addr='https://api.thingspeak.com/',api_key='QS3DYISJPLE5EQCW'
,ch_id=1027974)
tmp36 = sbellc.get_a_channel_field_feed('field1',parameters={'minutes':2})
tmp36_df = pd.DataFrame(tmp36['feeds'])
tmp36_df = tmp36_df.set_index(pd.DatetimeIndex(tmp36_df['created_at']))
tmp36_df['field1'] = tmp36_df['field1'].astype('float64')
tmp36_df.rename(columns = {'field1':'temperature'},inplace = True)
                   

if tmp36_df['temperature'].mean() <= 10:
    jsonout.update({"Temp_Tyson_Alert": "alert alert-info"})
elif (tmp36_df['temperature'].mean() > 10) and (tmp36_df['temperature'].mean() < 20):
    jsonout.update({"Temp_Tyson_Alert": "alert alert-warning"})
elif tmp36_df['temperature'].mean() >= 20:
    jsonout.update({"Temp_Tyson_Alert": "alert alert-danger"})
else:
    jsonout.update({"Temp_Shop_Alert": ""})

jsonout.update({"Temp_Tyson": tmp36_df['temperature'].mean()})                   
 
    
### DuckBarn
sbellc = thingspeak.TSChannel(acc_host_addr='https://api.thingspeak.com/',api_key='QS3DYISJPLE5EQCW'
,ch_id=1047747)
test = sbellc.get_a_channel_field_feed(['field1','field2','field3'],parameters={'minutes':1})
test_df = pd.DataFrame(test['feeds'])
test_df = test_df.set_index(pd.DatetimeIndex(test_df['created_at']))
test_df['field1'] = test_df['field1'].astype('float64')
test_df['field2'] = test_df['field2'].astype('float64')
test_df['field3'] = test_df['field3'].astype('float64')
test_df.rename(columns = {'field1':'temperature','field2':'temperature_2','field3':'humidity'},inplace = True)

if test_df['temperature'].mean() <= 10:
    jsonout.update({"Temp_DuckBarn_interior_Alert": "alert alert-info"})
elif (test_df['temperature'].mean() > 10) and (test_df['temperature'].mean() < 20):
    jsonout.update({"Temp_DuckBarn_interior_Alert": "alert alert-warning"})
elif test_df['temperature'].mean() >= 20:
    jsonout.update({"Temp_DuckBarn_interior_Alert": "alert alert-danger"})
else:
    jsonout.update({"Temp_DuckBarn_interior_Alert": ""})

jsonout.update({"Temp_DuckBarn_interior": test_df['temperature'].mean()})                   

if test_df['temperature_2'].mean() <= 10:
    jsonout.update({"Temp_DuckBarn_exterior_Alert": "alert alert-info"})
elif (test_df['temperature_2'].mean() > 10) and (test_df['temperature_2'].mean() < 20):
    jsonout.update({"Temp_DuckBarn_exterior_Alert": "alert alert-warning"})
elif test_df['temperature_2'].mean() >= 20:
    jsonout.update({"Temp_DuckBarn_exterior_Alert": "alert alert-danger"})
else:
    jsonout.update({"Temp_DuckBarn_exterior_Alert": ""})

jsonout.update({"Temp_DuckBarn_exterior": test_df['temperature_2'].mean()}) 
                      
                   
with open('MoonFlowerMonitor.json', 'w') as my_data_file:
    my_data_file.write(json.dumps(jsonout,indent=0))


