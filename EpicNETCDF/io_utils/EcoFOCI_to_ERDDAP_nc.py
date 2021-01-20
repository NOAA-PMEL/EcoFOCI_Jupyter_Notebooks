#!/usr/bin/env python

"""
 EcoFOCI_to_ERDDAP_nc.py
 
 class for building netcdf files from specified instruments
 
 
  History:
 --------
 2016-12-19: Add a class for ragged arrays (1D and 2D) - 1D is continuous file
 2016-12-16: Add a class for CF time conventions (1D and 2D) TODO: merge into other classes
 2016-09-16: Add a class for copying the existing structure of a file 
 2016-09-12: Add a class for duplicating netcdf files (all parameters and attributes) 
    but with a new number of data points due to trimming pre/post deployment times

 2016-08-02: Migrate to EcoFOCI_MooringAnalysis pkg and unify netcdf creation code so
    that it is no longer instrument dependant

"""

# Standard library.
import datetime, os

# Scientific stack.
import numpy as np
from netCDF4 import Dataset

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2014, 01, 13)
__modified__ = datetime.datetime(2014, 12, 02)
__version__  = "0.4.0"
__status__   = "Development"


"""-------------------------------NCFile Creation--------------------------------------"""
class timeseries_to_ERDDAP_nc(object):
    """ Class instance to generate a NetCDF file.  

    Standards
    ---------
    EPICNetCDF (PMEL) Standards  


    Usage
    -----
    
    Order of routines matters and no error checking currently exists
    ToDo: Error Checking
    
    Use this to create a nc file with all default values
        ncinstance = timeseries_to_ERDDAP_nc()
        ncinstance.file_create()
        ncinstance.sbeglobal_atts()
        ncinstance.dimension_init()
        ncinstance.variable_init()
        ncinstance.add_coord_data()
        ncinstance.add_data()
        ncinstance.close()
    """ 
    
    
    nc_format = 'NETCDF3_CLASSIC'
    nc_read   = 'w'

    def __init__(self, savefile='data/test.nc'):
        """initialize output file path"""
        
        self.savefile = savefile
    
    def file_create(self):
            rootgrpID = Dataset(self.savefile, timeseries_to_ERDDAP_nc.nc_read, 
                                format=timeseries_to_ERDDAP_nc.nc_format)
            self.rootgrpID = rootgrpID
            return ( rootgrpID )
        
    def sbeglobal_atts(self, raw_data_file='', Water_Mass='', Water_Depth=9999, 
                       Experiment='', Station_Name='', SerialNumber='', 
                       Instrument_Type='', History='', Project='', featureType=''):
        """
        Assumptions
        -----------
        
        Format of DataFrame.name = 'dy1309l1_ctd001'
        
        seabird related global attributes found in DataFrame.header list
        
        """
        
        self.rootgrpID.CREATION_DATE = datetime.datetime.utcnow().strftime("%B %d, %Y %H:%M UTC")
        self.rootgrpID.INST_TYPE = Instrument_Type
        self.rootgrpID.DATA_CMNT = raw_data_file
        self.rootgrpID.NC_FILE_GENERATOR = __file__.split('/')[-1] + ' ' + __version__ 
        self.rootgrpID.WATER_DEPTH = Water_Depth
        self.rootgrpID.MOORING = Station_Name
        self.rootgrpID.WATER_MASS = Water_Mass
        self.rootgrpID.EXPERIMENT = Experiment
        self.rootgrpID.PROJECT = Project
        self.rootgrpID.SERIAL_NUMBER = SerialNumber
        self.rootgrpID.History = History
        self.rootgrpID.featureType = featureType

    def dimension_init(self, recnum_len=1, str_len=20):
        """
        Assumes
        -------
        Dimensions will be 'record_number'
        
        Todo
        ----
        User defined dimensions
        """

        self.dim_vars = ['row','id_strlen']
        
        self.rootgrpID.createDimension( self.dim_vars[0], recnum_len ) #recnumber
        self.rootgrpID.createDimension( self.dim_vars[1], str_len ) #recnumber
        
        
    def variable_init(self, nchandle):
        """
        built from knowledge about previous file
        """
        
        #build record variable attributes
        rec_vars, rec_var_name, rec_var_longname = [], [], []
        rec_var_generic_name, rec_var_FORTRAN, rec_var_units, rec_var_epic = [], [], [], []
        
        for v_name in nchandle.variables.keys():
            print "Copying attributes for {0}".format(v_name)
            rec_vars.append( v_name )
            rec_var_name.append( nchandle.variables[v_name].name )
            rec_var_longname.append( nchandle.variables[v_name].long_name )
            rec_var_generic_name.append( nchandle.variables[v_name].generic_name )
            rec_var_units.append( nchandle.variables[v_name].units )
            rec_var_FORTRAN.append( nchandle.variables[v_name].FORTRAN_format )
            rec_var_epic.append( nchandle.variables[v_name].epic_code )

        for i, v in enumerate(rec_vars[:]):  #1D coordinate variables
            var_class.append(self.rootgrpID.createVariable(rec_vars[i], rec_var_type[i], self.dim_vars[0]))
            
        ### add variable attributes
        for i, v in enumerate(var_class): #4dimensional for all vars
            print ("Adding Variable {0}").format(v)#
            v.setncattr('name',rec_var_name[i])
            v.long_name = rec_var_longname[i]
            v.generic_name = rec_var_generic_name[i]
            v.FORTRAN_format = rec_var_FORTRAN[i]
            v.units = rec_var_units[i]
            v.type = rec_var_strtype[i]
            v.epic_code = rec_epic_code[i]
            
        self.var_class = var_class
        self.rec_vars = rec_vars


        
    def add_coord_data(self, recnum=None):
        """ """
        self.var_class[0][:] = recnum

    def add_data(self, data=None):
        """ """
        
        for ind, varname in enumerate(data.keys()):
            di = self.rec_vars.index(varname)
            self.var_class[di][:] = data[varname][:,0,0,0]
    
      
        
    def add_history(self, new_history):
        """Adds timestamp (UTC time) and history to existing information"""
        self.rootgrpID.History = self.rootgrpID.History + '\n' + datetime.datetime.utcnow().strftime("%B %d, %Y %H:%M UTC")\
                    + ' ' + new_history
                    
    def close(self):
        self.rootgrpID.close()  
