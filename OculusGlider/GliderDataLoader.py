import warnings
warnings.filterwarnings("ignore")

from erddapy import ERDDAP
import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import cmocean

from requests.exceptions import HTTPError


class erddap_glider(object):
    
    def __init__(self, glider_id='sg401', server_url = 'http://downdraft.pmel.noaa.gov:8080/erddap'):
        self.glider_id = glider_id
        self.server_url = server_url
    
    def list_data(self, verbose=False):
        e = ERDDAP(server=self.server_url)
        self.df = pd.read_csv(e.get_search_url(response='csv', search_for=self.glider_id))
        if verbose:
            print(self.df['Dataset ID'])

    def constrain_data(self,start_date='2019-01-01T00:00:00Z',variables=None):
        self.constraints = {
            'time>=': start_date,
            'time<=': str(datetime.datetime.today()),
        }

        self.variables = variables


    def load_data(self,year='2019'):
        self.dfs = {}
        for index,row in self.df.iterrows():
            if (self.glider_id in row['Dataset ID']) and (year in row['Dataset ID']):
                print(row['Dataset ID'])

                try:
                    e = ERDDAP(server=self.server_url,
                        protocol='tabledap',
                        response='csv',
                    )
                    e.dataset_id=row['Dataset ID']
                    e.constraints=self.constraints
                    e.variables=self.variables[row['Dataset ID']]
                except HTTPError:
                    print('Failed to generate url {}'.format(row['Dataset ID']))
                    continue
                self.dfs.update({row['Dataset ID']: e.to_pandas(
                                        index_col='time (UTC)',
                                        parse_dates=True,
                                        skiprows=(1,)  # units information can be dropped.
                                        )})  
                
        return(self.dfs)
    
    def plot_timeseries(self, df, var=None,varstr='',cmap=cmocean.cm.thermal,vmin=None,vmax=None):
        fig, ax = plt.subplots(figsize=(17, 2))
        if vmin:
            cs = ax.scatter(df.index, df['ctd_depth (meters)'], s=15, c=df[var], marker='o', edgecolor='none',cmap=cmap,vmin=vmin,vmax=vmax)
        else:
            cs = ax.scatter(df.index, df['ctd_depth (meters)'], s=15, c=df[var], marker='o', edgecolor='none',cmap=cmap)

        ax.invert_yaxis()
        ax.set_xlim(df.index[0], df.index[-1])
        xfmt = mdates.DateFormatter('%d-%b\n%H:%M')
        ax.xaxis.set_major_formatter(xfmt)

        cbar = fig.colorbar(cs, orientation='vertical', extend='both')
        cbar.ax.set_ylabel(varstr)
        ax.set_ylabel('Depth (m)')
        
        return(fig,ax)
    
    def plot_waterfall(self, dfg, var=None,varstr='',delta=1):
        

        fig, ax = plt.subplots(figsize=(8, 12))
        shift = 0
        count = 0
        for g in dfg.groups:
            color = cmocean.cm.phase(np.linspace(0.1,0.9,len(dfg.groups))) # This returns RGBA; convert:
            df = dfg.get_group(g)
            if (count%5==0):
                cs = ax.plot(df[var]+shift, df['ctd_depth (meters)'], color=color[count],label=g)
            else:
                cs = ax.plot(df[var]+shift, df['ctd_depth (meters)'], color=color[count],label='')

            shift=shift+delta
            count+=1

        ax.legend()
        ax.invert_yaxis()
        ax.set_ylabel('Depth (m)')
        ax.set_xlabel(varstr)

        return(fig,ax)
