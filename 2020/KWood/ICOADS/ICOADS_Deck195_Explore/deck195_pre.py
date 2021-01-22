import sys
import pandas as pd
import geopandas as gpd
import fiona 
import geoviews as gv
import geoviews.feature as gf
import holoviews as hv
from bokeh.models import HoverTool
# Adds %%opts line magic for bokeh plot config
hv.extension('bokeh')
import hvplot.pandas
from holoviews import streams
from holoviews import opts
import panel as pn
pn.extension()
#import utility as u
import numpy as np
import datetime
import colorcet as cc
import param
#import cartopy
#from cartopy import crs
import datetime

hv.output(widget_location='bottom')

df = pd.read_csv('~/in_and_outbox/2020/wood/IMMA_1940s/datasets_IMMA_ICOADS_ncei_1940s_e044_89bd_5d26.csv',
                 header=0,skiprows=[1],parse_dates=True,dtype={'ID':str})

allkeys =df.groupby('ID').groups.keys()
allkeys= list(allkeys)

#subgroup = df.groupby('ID').get_group('10009')
# or

grouped = df.groupby('ID')
# build list of relevant keys
groups = []
#prefix = ['22','32','41','43','51','59','61','89','94']
prefix = [str(sys.argv[1])]
print(f'You passed prefix {prefix} into be plotted')
for key in allkeys:
    for oprefix in prefix:
        try:
            if oprefix in key[0:2]:
                groups = groups + [str(key)]
        except:
            pass
subgroup = pd.concat([grouped.get_group(name) for name in groups])
