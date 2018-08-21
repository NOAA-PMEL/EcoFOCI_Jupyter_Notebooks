#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 12:48:11 2018

@author: chu
"""
import numpy as np
import datetime
import cmocean
from scipy.interpolate import griddata

import matplotlib.pyplot as plt

import pickle

with open('objs.pickle','rb') as f:  # Python 3 open(..., 'rb')
    df = pickle.load(f)
    
    
    
df_drop=df
df_10min = df_drop.resample('10min').mean()
df_interp = df_10min.interpolate (method='time', limit=1)


# data coordinates and values
df_interp = df_interp.reset_index()

#
#remove nan rows
df_interp = df_interp.dropna()


x = df_interp.index
y = df_interp.Depth
zt = df_interp.meantemp_lastminsampling
zs = df_interp.meansal_lastminsampling
zp = df_interp.pco2_corrected_osmotic
zo = df_interp.meano2_lastminsampling
zd = df_interp.sigmatheta_kgm_3
zpmod = df_interp.pco2_calculated_0_100


xi=np.arange(0,7460, 6)

yi = np.arange(0,90,2)

xi,yi = np.meshgrid(xi,yi)

k=1

# interpolate
zti = griddata((x,y/k),zt,(xi,yi),method='linear')
zsi = griddata((x,y/k),zs,(xi,yi),method='linear')
zpi = griddata((x,y/k),zp,(xi,yi),method='linear')
zoi = griddata((x,y/k),zo,(xi,yi),method='linear')
zdi = griddata((x,y/k),zd,(xi,yi),method='linear')
zpmodi = griddata((x,y/k),zpmod,(xi,yi),method='linear')

#make plot
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1)

im1 = ax1.contourf(xi,yi*k,zti,np.arange(7,17,1), cmap=cmocean.cm.thermal)
ax1.invert_yaxis()
cb1=fig.colorbar(im1, ax=ax1)
cb1.set_label('Temp. ($^oC$)')

im2 = ax2.contourf(xi,yi*k,zsi,np.arange(30.5,34,0.3), cmap=cmocean.cm.haline)
ax2.invert_yaxis()
cb2=fig.colorbar(im2, ax=ax2)
cb2.set_label('Sal. (PSS)')

im3=ax3.contourf(xi,yi*k,zoi,np.arange(0,525,50), cmap=cmocean.cm.oxy)
ax3.invert_yaxis()
cb3=fig.colorbar(im3, ax=ax3)
cb3.set_label('$O_2$ (uM)')

df_interp.index = df_interp.datetime64_ns

im4 = ax4.scatter(df_interp.index, df_interp.Depth, s=10, c=df_interp.meano2_lastminsampling, cmap=cmocean.cm.oxy,vmin=0, vmax=525)
ax4.invert_yaxis()
cb4=fig.colorbar(im4, ax=ax4)
dstop = datetime.datetime(2017,9,17, 18, 40)
dstart = datetime.datetime(2017,7,11, 21, 20)
ax4.set_xlim([dstart,dstop])

#fig.autofmt_xdate()
fig.set_size_inches(10.5, 5.5)


# Set common labels
ax1.set_ylabel('Depth (m)')
ax2.set_ylabel('Depth (m)')
ax3.set_ylabel('Depth (m)')
ax4.set_ylabel('Depth (m)')

ax1.annotate("A", xy=(-0.05, 1.05), xycoords="axes fraction", weight='bold')
ax2.annotate("B", xy=(-0.05, 1.05), xycoords="axes fraction", weight='bold')
ax3.annotate("C", xy=(-0.05, 1.05), xycoords="axes fraction", weight='bold')
ax4.annotate("D", xy=(-0.05, 1.05), xycoords="axes fraction", weight='bold')

plt.tight_layout()
plt.savefig('interpolatedprawler_TSDO.png',dpi=100)