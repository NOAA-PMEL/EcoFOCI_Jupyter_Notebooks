"""
ArgosDrifters.py

Using Anaconda packaged Python 
"""

#System Stack
import os

#Science Stack
import numpy as np
from netCDF4 import Dataset

# Plotting Stack
import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap, shiftgrid
import matplotlib.pyplot as plt
import matplotlib as mpl
import cmocean


"""------------------------------------- MAPS -----------------------------------------"""

def find_nearest(a, a0):
    "Element in nd array `a` closest to the scalar value `a0`"
    idx = np.abs(a - a0).argmin()
    return idx
        
"""------------------------------------- Main -----------------------------------------"""


class ArgosPlot(object):

    def __init__(self,df=None):
        self.df = df

    def set_region(self,region='bering'):
        if region == 'arctic':
            self.etopo_levels=[-1000, -100, -50, -25, ]  #chuckchi
        else:
            self.etopo_levels=[-1000, -200, -100, -70, ]  #berring

    def etopo5(self,file='data/etopo5.nc'):
        """ read in etopo5 topography/bathymetry. """

        etopodata = Dataset(file)
        
        self.topoin = etopodata.variables['bath'][:]
        self.elons = etopodata.variables['X'][:]
        self.elats = etopodata.variables['Y'][:]

        etopodata.close()
        
        self.topoin,self.elons = shiftgrid(0.,self.topoin,self.elons,start=False) # -360 -> 0
 
    def set_region_bounds(self,etopofile='data/etopo5.nc',lat='latitude',lon='longitude'): 
        """
        df=dataframe

        """

        ### load etopo data
        self.etopo5(file=etopofile)

        #build regional subset of data
        self.topoin = self.topoin[find_nearest(self.elats,self.df[lat].min()-5):find_nearest(self.elats,self.df[lat].max()+5),find_nearest(self.elons,-1*(self.df[lon].max()+5)):find_nearest(self.elons,-1*(self.df[lon].min()-5))]
        self.elons = self.elons[find_nearest(self.elons,-1*(self.df[lon].max()+5)):find_nearest(self.elons,-1*(self.df[lon].min()-5))]
        self.elats = self.elats[find_nearest(self.elats,self.df[lat].min()-5):find_nearest(self.elats,self.df[lat].max()+5)]

        #determine regional bounding
        y1 = np.floor(self.df[lat].min()-1)
        y2 = np.ceil(self.df[lat].max()+1)
        x1 = np.ceil(-1*(self.df[lon].max()+2))
        x2 = np.floor(-1*(self.df[lon].min()-2))

        return({'x1':x1,'x2':x2,'y1':y1,'y2':y2})

    def make_map(self,bounds=None,param='doy',etopofile='data/etopo5.nc',lat='latitude',lon='longitude'):

        bounds = self.set_region_bounds(etopofile=etopofile)
        self.set_region(region='bering')

        fig1 = plt.figure(1)
        #Custom adjust of the subplots
        ax = plt.subplot(1,1,1)
        
                
        m = Basemap(resolution='i',projection='merc', llcrnrlat=bounds['y1'], \
                    urcrnrlat=bounds['y2'],llcrnrlon=bounds['x1'],urcrnrlon=bounds['x2'],\
                    lat_ts=45)
        
        self.elons, self.elats = np.meshgrid(self.elons, self.elats)

        x, y = m(-1. * self.df[lon].values,self.df[lat].values)
        ex, ey = m(self.elons, self.elats)

        m.drawcountries(linewidth=0.5)
        m.drawcoastlines(linewidth=0.5)
        m.drawparallels(np.arange(bounds['y1'],bounds['y2'],2.),labels=[1,0,0,0],color='black',dashes=[1,1],labelstyle='+/-',linewidth=0.2) # draw parallels
        m.drawmeridians(np.arange(bounds['x1']-20,bounds['x2'],4.),labels=[0,0,0,1],color='black',dashes=[1,1],labelstyle='+/-',linewidth=0.2) # draw meridians
        m.fillcontinents(color='white')

    
        m.contourf(ex,ey,self.topoin, levels=self.etopo_levels, colors=('#737373','#969696','#bdbdbd','#d9d9d9','#f0f0f0'), extend='both', alpha=.75)
        if param=='sst':
            m.scatter(x,y,20,marker='.', edgecolors='none', c=self.df.sst.values, vmin=-2, vmax=15, cmap=cmocean.cm.thermal)
        elif param == 'julian_day':
            m.scatter(x,y,20,marker='.', edgecolors='none', c=self.df.index.dayofyear, vmin=0, vmax=365, cmap=cmocean.cm.phase)
        else:
            m.scatter(x,y,20,marker='.', edgecolors='none', c=self.df.index.dayofyear, vmin=0, vmax=365, cmap=cmocean.cm.phase)
        c = plt.colorbar()
        
        return(ax,fig1)

    def output_type(self,ending='png'):
        if ending == 'png':
            self.filetype = ending
        else:
            self.filetype = 'svg'


