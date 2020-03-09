#!/usr/bin/env python
# coding: utf-8

# ### Plots for Office Env Monitor
# Last 180 days only
# 


from erddapy import ERDDAP
import pandas as pd
import datetime

stations = ['channel_843357_thingspeak','OfficeRedboard_WxStation','LabEnvMonitor']
station_accuracy = {stations[0]: {'Temp':2,'Baro':1,'RH':5},stations[1]: {'Temp':0.5,'Baro':1,'RH':3},stations[2]: {'Temp':0.5,'Baro':1,'RH':3}}

#---------------------------------------------------------------------------------------------------------------#
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import YearLocator, WeekdayLocator, MonthLocator, DayLocator, HourLocator, DateFormatter
import matplotlib.ticker as ticker

import cmocean
### specify primary bulk figure parameters
fontsize = 10
labelsize = 10
#plotstyle = 'seaborn'
max_xticks = 10
plt.style.use('seaborn-ticks')
mpl.rcParams['svg.fonttype'] = 'none'
mpl.rcParams['ps.fonttype'] = 42 #truetype/type2 fonts instead of type3
mpl.rcParams['pdf.fonttype'] = 42 #truetype/type2 fonts instead of type3
mpl.rcParams['axes.grid'] = False
mpl.rcParams['axes.edgecolor'] = 'black'
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['axes.labelcolor'] = 'black'
mpl.rcParams['grid.linestyle'] = '--'
mpl.rcParams['grid.linestyle'] = '--'
mpl.rcParams['xtick.major.size'] = 4
mpl.rcParams['xtick.minor.size'] = 2
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['xtick.minor.width'] = 0.5
mpl.rcParams['ytick.major.size'] = 4
mpl.rcParams['ytick.minor.size'] = 2
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['ytick.minor.width'] = 0.5
mpl.rcParams['ytick.direction'] = 'out'
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.color'] = 'black'
mpl.rcParams['xtick.color'] = 'black'
#---------------------------------------------------------------------------------------------------------------#

server_url = 'http://downdraft.pmel.noaa.gov:8080/erddap'

d = ERDDAP(server=server_url,
    protocol='tabledap',
    response='csv'
)
d.dataset_id=stations[1]

d.constraints={'time>=': datetime.datetime.now()-datetime.timedelta(days=180)}

df = d.to_pandas(

        index_col='time (UTC)',
        parse_dates=True,
        skiprows=(1,)  # units information can be dropped.
        )

df.sort_index(inplace=True)
df.columns = [x[1].split()[0] for x in enumerate(df.columns)]


# Horizon Plots
dayperiod = [30,60,90,180]

for numdays in dayperiod:

    df=df.resample('T').mean()
    dfsub = df[str((datetime.datetime.utcnow()-datetime.timedelta(days=numdays)).date()):str(datetime.datetime.utcnow().date())]
    anom = dfsub['temperature']-dfsub['temperature'].mean()

    fig, (ax1,ax2,ax3) = plt.subplots(3,1,sharex='col',figsize=(24,6))
    ax1.set_title(f'Anom Horizon charts throughout the day for past {numdays} days',loc='left')

    ax1.fill_between(dfsub.index.values,anom,where=anom>0,facecolor='#fcae91')
    ax1.fill_between(dfsub.index.values,anom-1,where=anom>1,facecolor='#fb6a4a')
    ax1.fill_between(dfsub.index.values,anom-2,where=anom>2,facecolor='#cb181d')
    ax1.fill_between(dfsub.index.values,anom,where=anom<0,facecolor='#bdd7e7')
    ax1.fill_between(dfsub.index.values,anom+1,where=anom<-1,facecolor='#6baed6')
    ax1.fill_between(dfsub.index.values,anom+2,where=anom<-2,facecolor='#2171b5')
    ax1.set_ylim([-1,1])

    anom = dfsub['RH_Percent']-dfsub['RH_Percent'].mean()
    ax2.fill_between(dfsub.index.values,anom,where=anom>0,facecolor='#bae4b3')
    ax2.fill_between(dfsub.index.values,anom-5,where=anom>5,facecolor='#74c476')
    ax2.fill_between(dfsub.index.values,anom-10,where=anom>10,facecolor='#238b45')
    ax2.fill_between(dfsub.index.values,anom,where=anom<0,facecolor='#fed98e')
    ax2.fill_between(dfsub.index.values,anom+5,where=anom<-5,facecolor='#fe9929')
    ax2.fill_between(dfsub.index.values,anom+10,where=anom<-10,facecolor='#cc4c02')
    ax2.set_ylim([-5,5])

    anom = (dfsub['SLP']-dfsub['SLP'].mean())/100
    ax3.fill_between(dfsub.index.values,anom,where=anom>0,facecolor='#f7f7f7')
    ax3.fill_between(dfsub.index.values,anom-10,where=anom>10,facecolor='#cccccc')
    ax3.fill_between(dfsub.index.values,anom-20,where=anom>20,facecolor='#969696')
    ax3.fill_between(dfsub.index.values,anom,where=anom<0,facecolor='#f7f7f7')
    ax3.fill_between(dfsub.index.values,anom+10,where=anom<-10,facecolor='#cccccc')
    ax3.fill_between(dfsub.index.values,anom+20,where=anom<-20,facecolor='#969696')
    ax3.set_ylim([-10,10])

    xfmt = mdates.DateFormatter('%d-%b')
    ax1.xaxis.set_major_formatter(xfmt)
    ax2.xaxis.set_major_formatter(xfmt)
    ax3.xaxis.set_major_formatter(xfmt)
    ax1.xaxis.set_major_locator(DayLocator(bymonthday=[1,15]))
    if numdays <=90:
        ax1.xaxis.set_minor_locator(DayLocator(range(0,32,1)))
    ax1.xaxis.set_minor_formatter(DateFormatter('%d'))
    ax1.xaxis.set_major_formatter(DateFormatter('%d\n%b %y'))
    ax1.xaxis.set_tick_params(which='major', pad=3)
    ax1.xaxis.set_tick_params(which='minor', pad=5)    

    fig.savefig(f'office_horizonplot_{numdays}.png',dpi=300)


for numdays in dayperiod:

    dfsub = df[str((datetime.datetime.utcnow()-datetime.timedelta(days=numdays)).date()):str(datetime.datetime.utcnow().date())]
    
    fig, (ax3, ax2, ax1) = plt.subplots(3,1,sharex='col',figsize=(24,6))
    ax1.plot(dfsub.index.values,dfsub['RH_Percent'],'g')
    ax1.fill_between(dfsub.index.values,dfsub['RH_Percent']-station_accuracy[stations[1]]['RH'],
                     dfsub['RH_Percent']+station_accuracy[stations[1]]['RH'],
                     color='grey',alpha=.25)
    ax1.set_ylabel('RH (%)')
    ax2.plot(dfsub.index.values,dfsub['temperature'],'r')
    ax2.fill_between(dfsub.index.values,dfsub['temperature']-station_accuracy[stations[1]]['Temp'],
                     dfsub['temperature']+station_accuracy[stations[1]]['Temp'],
                     color='grey',alpha=.25)
    ax2.set_ylabel('Temperature (degC)')
    ax3.plot(dfsub.index.values,dfsub['SLP'],'k')
    ax3.fill_between(dfsub.index.values,dfsub['SLP']-station_accuracy[stations[1]]['Baro'],
                     dfsub['SLP']+station_accuracy[stations[1]]['Baro'],
                     color='grey',alpha=.25)
    ax3.set_ylabel('SLP (Pa)')


    xfmt = mdates.DateFormatter('%d-%b')
    ax1.xaxis.set_major_formatter(xfmt)
    ax2.xaxis.set_major_formatter(xfmt)
    ax3.xaxis.set_major_formatter(xfmt)
    ax1.xaxis.set_major_locator(DayLocator(bymonthday=[1,15]))
    if numdays <=90:
        ax1.xaxis.set_minor_locator(DayLocator(range(0,32,1)))
    ax1.xaxis.set_minor_formatter(DateFormatter('%d'))
    ax1.xaxis.set_major_formatter(DateFormatter('%d\n%b %y'))
    ax1.xaxis.set_tick_params(which='major', pad=3)
    ax1.xaxis.set_tick_params(which='minor', pad=5)  

    fig.savefig(f'office_timeseries_{numdays}.png',dpi=300)
    