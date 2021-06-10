#!/usr/bin/env python
# coding: utf-8

# # netcdf creation with fill values
# 
# Is it a:
# - python issue (2.7 vs 3.6+)
# - netcdf issue (NETCDF3_CLASSIC vs NETCDF4_CLASSIC vs ?)
# 

# In[24]:


import netCDF4

import numpy as np


# In[25]:


rootgrp = netCDF4.Dataset('test.nc', 'w', format='NETCDF3_CLASSIC')


# In[26]:


timedim = rootgrp.createDimension('TIME', None)
depthdim = rootgrp.createDimension('DEPTH', 1)
latitudedim = rootgrp.createDimension('LATITUDE', 1)
longitudedim = rootgrp.createDimension('LONGITUDE', 1)
posqualdim = rootgrp.createDimension('POSITION', 1)
wind2heightdim = rootgrp.createDimension('HEIGHT_WIND2',1)

times = rootgrp.createVariable('TIME','f8',('TIME',))


# In[27]:


wind2sspd = rootgrp.createVariable('WSSPD2','f4',('TIME',),fill_value=np.NaN)
wind2gust = rootgrp.createVariable('WGUST2','f4',('TIME',),fill_value=np.NaN)
wind2spdq = rootgrp.createVariable('WSPD2_QC','f4',('TIME','HEIGHT_WIND2','LATITUDE','LONGITUDE'),fill_value=4)
wind2dirq = rootgrp.createVariable('WDIR2_QC','i1',('TIME','HEIGHT_WIND2','LATITUDE','LONGITUDE'),fill_value=4)


# In[ ]:




