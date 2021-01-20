#!/usr/bin/env python

"""
 Background:
 --------
 time_helper.py
 
 
 Purpose:
 --------
 Various Routines and Classes related to time manipulation
 
 History:
 --------

 2016-12-16: Broken out from instr_data_ingest.py

"""
import datetime
import numpy as np
from io import BytesIO
from netCDF4 import num2date


def linear_clock_adjust(
    time_orig=datetime.datetime.now(), date_time=datetime.datetime.now(), add_seconds=0
):
    r"""
		add clock offset to datetime values
	"""
    return (
        datetime.timedelta(seconds=(date_time - time_orig).seconds * add_seconds)
        + date_time
    )


def roundTime(dt=None, roundTo=60):
    """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.

   http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python/10854034#10854034
   """
    if dt == None:
        dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


def interp2hour(interp_time, data_time, data, vlist=[None]):
    """ starting with minimum value, grid data to hourly on the hour"""

    def to_float(d, epoch=datetime.datetime(1970, 1, 1)):
        return (d - epoch).total_seconds()

    data_interp = {}

    data_interp["time"] = interp_time
    for variable_name in vlist:
        try:
            data_interp[variable_name] = np.interp(
                map(to_float, interp_time),
                map(to_float, data_time),
                data[variable_name],
            )
            ind = data_interp[variable_name] >= 1e10
            data_interp[variable_name][ind] = 1e35
        except ValueError:  # empty variable
            data_interp[variable_name] = np.ones_like(interp_time) * 1e35
        except IOError:
            data_interp[variable_name] = np.ones_like(interp_time) * 1e35
        except TypeError:
            data_interp[variable_name] = np.ones_like(interp_time) * 1e35

    return data_interp
