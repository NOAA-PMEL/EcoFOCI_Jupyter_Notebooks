#!/usr/bin/env

"""

class definitions for netcdf4 wrappers

"""

import datetime

# science stack
from netCDF4 import Dataset


class EcoFOCI_netCDF(object):
    def __init__(self, file_name=None):
        """Initialize opening of netcdf file.

        Parameters
        ----------
        file_name : str
            full path to file on disk

        """

        self.nchandle = Dataset(file_name, "a")
        self.file_name = file_name

    def _getnchandle_(self):
        return self.nchandle

    def get_global_atts(self):
        """get global attribute for specified name"""
        g_atts = {}
        att_names = self.nchandle.ncattrs()

        for name in att_names:
            g_atts[name] = self.nchandle.getncattr(name)

        return g_atts

    def set_global_atts(self, name=None, attribute=None):
        """set global attribute for specified name"""
        self.nchandle.setncattr(name, attribute)

    def get_vars(self):
        self.variables = self.nchandle.variables
        return self.variables

    """    
            def get_vars_attributes(self, var_name=None, var_type=None):
            r"get variable attributes for specified variable"
            return self.nchandle.variables[var_name].getncattr(var_type)
    """

    def get_vars_attributes(self, var_name=None):
        """get variable attributes for specified variable"""
        return self.nchandle.variables[var_name]

    def set_vars_attributes(self, var_name=None, var_type=None, attr_value=None):
        """get variable attributes for specified variable"""
        self.nchandle.variables[var_name].setncattr(var_type, attr_value)

    def ncreadfile_dic(self):

        data = {}
        for j, v in enumerate(self.nchandle.variables):
            if v in self.nchandle.variables.keys():  # check for nc variable
                data[v] = self.nchandle.variables[v][:]

            else:  # if parameter doesn't exist fill the array with zeros
                data[v] = None
        return data

    def update_epic_time(self, time=None, time2=None):
        self.nchandle.variables["time"][:] = time
        self.nchandle.variables["time2"][:] = time2

    def add_history(self, prev_history, new_history):
        """Adds timestamp (UTC time) and history to existing information"""
        self.nchandle.setncattr(
            "History",
            prev_history
            + "\n"
            + datetime.datetime.utcnow().strftime("%B %d, %Y %H:%M UTC")
            + " "
            + new_history,
        )

    def close(self):
        self.nchandle.close()
