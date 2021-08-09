#!/usr/bin/env python
# coding: utf-8

# ### Bits and pieces for Shop Env Monitor
# 
# Source: thingspeak

import json
import thingspeak as thingspeak
import pandas as pd
import numpy as np
import datetime
import urllib.request
import altair as alt
### own colormap
import palettable

alt.data_transformers.disable_max_rows()
today = datetime.datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z')
yesterday = (datetime.datetime.utcnow()-datetime.timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')

sbell = thingspeak.TSAccount('https://api.thingspeak.com/','869L0PHK8GKAIIYQ')

### cellar
sbellc = thingspeak.TSChannel(acc_host_addr='https://api.thingspeak.com/',api_key='QS3DYISJPLE5EQCW'
,ch_id=1037066)
dt11 = sbellc.get_a_channel_field_feed(['field1','field2'],parameters={'days':14})
dt11_df = pd.DataFrame(dt11['feeds'])
dt11_df = dt11_df.set_index(pd.DatetimeIndex(dt11_df['created_at']))
dt11_df['field1'] = dt11_df['field1'].astype('float64')
dt11_df['field2'] = dt11_df['field2'].astype('float64')
dt11_df.rename(columns = {'field1':'temperature','field2':'humidity'},inplace = True)


### shop
sbellc = thingspeak.TSChannel(acc_host_addr='https://api.thingspeak.com/',api_key='QS3DYISJPLE5EQCW'
,ch_id=843357)
bmp = sbellc.get_a_channel_field_feed(['field3','field4'],parameters={'days':6})
bmp_df = pd.DataFrame(bmp['feeds'])
bmp_df = bmp_df.set_index(pd.DatetimeIndex(bmp_df['created_at']))
bmp_df['field3'] = bmp_df['field3'].astype('float64')
bmp_df['field4'] = bmp_df['field4'].astype('float64')
bmp_df.rename(columns = {'field3':'temperature','field4':'pressure'},inplace = True)


### Tysons Room
sbellc = thingspeak.TSChannel(acc_host_addr='https://api.thingspeak.com/',api_key='QS3DYISJPLE5EQCW'
,ch_id=1027974)
tmp36 = sbellc.get_a_channel_field_feed('field1',parameters={'days':14})
tmp36_df = pd.DataFrame(tmp36['feeds'])
tmp36_df = tmp36_df.set_index(pd.DatetimeIndex(tmp36_df['created_at']))
tmp36_df['field1'] = tmp36_df['field1'].astype('float64')
tmp36_df.rename(columns = {'field1':'temperature'},inplace = True)
                   

### DuckBarn
sbellc = thingspeak.TSChannel(acc_host_addr='https://api.thingspeak.com/',api_key='QS3DYISJPLE5EQCW'
,ch_id=1047747)
test = sbellc.get_a_channel_field_feed(['field1','field2','field3'],parameters={'days':14})
test_df = pd.DataFrame(test['feeds'])
test_df = test_df.set_index(pd.DatetimeIndex(test_df['created_at']))
test_df['field1'] = test_df['field1'].astype('float64')
test_df['field2'] = test_df['field2'].astype('float64')
test_df['field3'] = test_df['field3'].astype('float64')
test_df.rename(columns = {'field1':'temperature','field2':'temperature_2','field3':'humidity'},inplace = True)

#need to merge datasets and rename columns - or squash with column variable name as attribute
# do it with subsampled data to 
data_list = {'Cellar':dt11_df,
             'DuckBarn':test_df,
             'TysonRoom':tmp36_df,
             'Shop':bmp_df}

dfsub = pd.concat([test_df.rename(columns={'temperature': 'DuckBarnTemp_Internal', 'temperature_2': 'DuckBarnTemp_External'}),
                   tmp36_df.rename(columns={'temperature': 'TysonsRoomTemp'}),
                   bmp_df.rename(columns={'temperature': 'ShopTemp'}),                   
                   dt11_df.rename(columns={'temperature': 'CellarTemp'}),                   
                  ]).resample('15T').mean()

dfsub = dfsub[str((datetime.datetime.utcnow()-datetime.timedelta(days=numdays)).date()):str(datetime.datetime.utcnow().date())]

### plots
selector = alt.selection_single(
    fields=['key'], 
    empty='all',
    bind='legend'
)

area1 = alt.Chart(dfsub.reset_index()).transform_fold(
    ['DuckBarnTemp_Internal','DuckBarnTemp_External','TysonsRoomTemp','duckTd','ShopTemp','CellarTemp']
).mark_line(clip=True
).encode(
    alt.X('created_at:T'),
    alt.Y('value:Q'),
    alt.Color('key:N'),
    opacity=alt.condition(selector, alt.value(1), alt.value(0))
).add_selection(
    selector
).properties(
    width=750,
    height=150
).interactive()

area1.save('FarmEnv_7day_Temp_Timeseries.json')

#

f1 = alt.Chart(dfsub.reset_index()).mark_rect().encode(
    alt.X('hoursminutes(created_at):O', title='hour of day - inside duck barn'),
    alt.Y('monthdate(created_at):O', title='date'),
    alt.Color('DuckBarnTemp_Internal:Q', title='temperature (C)', scale=alt.Scale(range=palettable.cmocean.sequential.Thermal_20.hex_colors)),
    tooltip=['hoursminutes(created_at):O','monthdate(created_at):O','DuckBarnTemp_Internal:Q']
).properties(
    width=720
)

f2 = f1.encode(
    alt.X('hoursminutes(created_at):O', title='hour of day - outside duck barn'),
    alt.Color('DuckBarnTemp_External:Q', title='temperature (C)', scale=alt.Scale(range=palettable.cmocean.sequential.Thermal_20.hex_colors)),
    tooltip=['hoursminutes(created_at):O','monthdate(created_at):O','DuckBarnTemp_External:Q']
)


f3 = f1.encode(
    alt.X('hoursminutes(created_at):O', title='hour of day - Cellar'),
    alt.Color('CellarTemp:Q', title='temperature (C)', scale=alt.Scale(range=palettable.cmocean.sequential.Thermal_20.hex_colors)),
    tooltip=['hoursminutes(created_at):O','monthdate(created_at):O','CellarTemp:Q']
)

f4 = f1.encode(
    alt.X('hoursminutes(created_at):O', title='hour of day - Shop'),
    alt.Color('ShopTemp:Q', title='temperature (C)', scale=alt.Scale(range=palettable.cmocean.sequential.Thermal_20.hex_colors)),
    tooltip=['hoursminutes(created_at):O','monthdate(created_at):O','ShopTemp:Q']
)

f5 = f1.encode(
    alt.X('hoursminutes(created_at):O', title='hour of day - Shop'),
    alt.Color('TysonsRoomTemp:Q', title='temperature (C)', scale=alt.Scale(range=palettable.cmocean.sequential.Thermal_20.hex_colors)),
    tooltip=['hoursminutes(created_at):O','monthdate(created_at):O','TysonsRoomTemp:Q']
)

(f1 & f2 & f3 & f4 & f5).save('FarmEnv_7day_Temp_HeatMap.json')