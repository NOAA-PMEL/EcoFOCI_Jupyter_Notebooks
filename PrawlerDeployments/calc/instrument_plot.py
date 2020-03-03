#!/usr/bin/env

"""
class definitions for standard 1 variable plots
class definitions for standard 2 variable plots
class definitions for standard 3 variable plots

 History:
 --------
 2019-05-21: error in calculation used corrected udata to correct vdata 

"""

# System Stack
import datetime

# science stack
import numpy as np

# Visual Stack

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.dates import (
    YearLocator,
    WeekdayLocator,
    MonthLocator,
    DayLocator,
    HourLocator,
    DateFormatter,
)
import matplotlib.ticker as ticker


class Timeseries1varPlot(object):

    mpl.rcParams["svg.fonttype"] = "none"
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["pdf.fonttype"] = 42

    def __init__(self, fontsize=10, labelsize=10, plotstyle="k-.", stylesheet="bmh"):
        """Initialize the timeseries with items that do not change.

        This sets up the axes and station locations. The `fontsize` and `spacing`
        are also specified here to ensure that they are consistent between individual
        station elements.

        Parameters
        ----------
        fontsize : int
            The fontsize to use for drawing text
        labelsize : int
          The fontsize to use for labels
        stylesheet : str
          Choose a mpl stylesheet [u'seaborn-darkgrid', 
          u'seaborn-notebook', u'classic', u'seaborn-ticks', 
          u'grayscale', u'bmh', u'seaborn-talk', u'dark_background', 
          u'ggplot', u'fivethirtyeight', u'seaborn-colorblind', 
          u'seaborn-deep', u'seaborn-whitegrid', u'seaborn-bright', 
          u'seaborn-poster', u'seaborn-muted', u'seaborn-paper', 
          u'seaborn-white', u'seaborn-pastel', u'seaborn-dark', 
          u'seaborn-dark-palette']
        """

        self.fontsize = fontsize
        self.labelsize = labelsize
        self.plotstyle = plotstyle
        plt.style.use(stylesheet)

    @staticmethod
    def add_title(mooringid="", lat=-99.9, lon=-99.9, depth=9999, instrument=""):
        """Pass parameters to annotate the title of the plot

      This sets the standard plot title using common meta information from PMEL/EPIC style netcdf files

      Parameters
      ----------
      mooringid : str
        Mooring Identifier
      lat : float
        The latitude of the mooring
      lon : float
        The longitude of the mooring
      depth : int
        Nominal depth of the instrument
      instrument : str
        Name/identifier of the instrument plotted
      """

        ptitle = (
            "Plotted on: {time:%Y/%m/%d %H:%M} \n from {mooringid} Lat: {latitude:3.3f}  Lon: {longitude:3.3f}"
            " Depth: {depth}\n : {instrument}"
        ).format(
            time=datetime.datetime.now(),
            mooringid=mooringid,
            latitude=lat,
            longitude=lon,
            depth=depth,
            instrument=instrument,
        )

        return ptitle

    def plot(self, xdata=None, ydata=None, ylabel=None, **kwargs):
        fig = plt.figure(1)
        ax1 = plt.subplot2grid((1, 1), (0, 0), colspan=1, rowspan=1)
        p1 = ax1.plot(xdata, ydata, self.plotstyle, markersize=2)
        ax1.set_ylim([np.nanmin(ydata), np.nanmax(ydata)])
        ax1.set_xlim([np.nanmin(xdata), np.nanmax(xdata)])
        plt.ylabel(ylabel)
        ax1.xaxis.set_major_locator(MonthLocator())
        ax1.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax1.xaxis.set_major_formatter(ticker.NullFormatter())
        ax1.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax1.tick_params(axis="both", which="minor", labelsize=self.labelsize)

        return plt, fig


class Timeseries2varPlot(object):

    mpl.rcParams["svg.fonttype"] = "none"
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["pdf.fonttype"] = 42

    def __init__(self, fontsize=10, labelsize=10, plotstyle="k-.", stylesheet="bmh"):
        """Initialize the timeseries with items that do not change.

        This sets up the axes and station locations. The `fontsize` and `spacing`
        are also specified here to ensure that they are consistent between individual
        station elements.

        Parameters
        ----------
        fontsize : int
            The fontsize to use for drawing text
        labelsize : int
          The fontsize to use for labels
        stylesheet : str
          Choose a mpl stylesheet [u'seaborn-darkgrid', 
          u'seaborn-notebook', u'classic', u'seaborn-ticks', 
          u'grayscale', u'bmh', u'seaborn-talk', u'dark_background', 
          u'ggplot', u'fivethirtyeight', u'seaborn-colorblind', 
          u'seaborn-deep', u'seaborn-whitegrid', u'seaborn-bright', 
          u'seaborn-poster', u'seaborn-muted', u'seaborn-paper', 
          u'seaborn-white', u'seaborn-pastel', u'seaborn-dark', 
          u'seaborn-dark-palette']
        """

        self.fontsize = fontsize
        self.labelsize = labelsize
        self.plotstyle = plotstyle
        plt.style.use(stylesheet)

    @staticmethod
    def add_title(mooringid="", lat=-99.9, lon=-99.9, depth=9999, instrument=""):
        """Pass parameters to annotate the title of the plot

      This sets the standard plot title using common meta information from PMEL/EPIC style netcdf files

      Parameters
      ----------
      mooringid : str
        Mooring Identifier
      lat : float
        The latitude of the mooring
      lon : float
        The longitude of the mooring
      depth : int
        Nominal depth of the instrument
      instrument : str
        Name/identifier of the instrument plotted
      """
        ptitle = (
            "Plotted on: {time:%Y/%m/%d %H:%M} \n from {mooringid} Lat: {latitude:3.3f}  Lon: {longitude:3.3f}"
            " Depth: {depth}\n : {instrument}"
        ).format(
            time=datetime.datetime.now(),
            mooringid=mooringid,
            latitude=lat,
            longitude=lon,
            depth=depth,
            instrument=instrument,
        )

        return ptitle

    def plot(
        self, xdata=None, ydata=None, ydata2=None, ylabel=None, ylabel2=None, **kwargs
    ):
        fig = plt.figure(1)
        ax1 = plt.subplot2grid((2, 1), (0, 0), colspan=1, rowspan=1)
        p1 = ax1.plot(xdata, ydata, self.plotstyle, markersize=2)
        ax1.set_ylim([np.nanmin(ydata), np.nanmax(ydata)])
        ax1.set_xlim([np.nanmin(xdata), np.nanmax(xdata)])
        plt.ylabel(ylabel)
        ax1.xaxis.set_major_locator(MonthLocator())
        ax1.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax1.xaxis.set_major_formatter(ticker.NullFormatter())
        ax1.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax1.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax1.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax1.spines["bottom"].set_visible(False)

        ax2 = plt.subplot2grid((2, 1), (1, 0), colspan=1, rowspan=1)
        p2 = ax2.plot(xdata, ydata2, self.plotstyle, markersize=2)
        ax2.set_ylim([np.nanmin(ydata2), np.nanmax(ydata2)])
        ax2.set_xlim([np.nanmin(xdata), np.nanmax(xdata)])
        plt.ylabel(ylabel2)
        ax2.xaxis.set_major_locator(MonthLocator())
        ax2.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax2.xaxis.set_major_formatter(ticker.NullFormatter())
        ax2.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax2.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax2.tick_params(axis="x", which="both", top="off")
        ax2.spines["top"].set_visible(False)

        return plt, fig


class Timeseries3varPlot(object):

    mpl.rcParams["svg.fonttype"] = "none"
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["pdf.fonttype"] = 42

    def __init__(self, fontsize=10, labelsize=10, plotstyle="k-.", stylesheet="bmh"):
        """Initialize the timeseries with items that do not change.

        This sets up the axes and station locations. The `fontsize` and `spacing`
        are also specified here to ensure that they are consistent between individual
        station elements.

        Parameters
        ----------
        fontsize : int
            The fontsize to use for drawing text
        labelsize : int
          The fontsize to use for labels
        stylesheet : str
          Choose a mpl stylesheet [u'seaborn-darkgrid', 
          u'seaborn-notebook', u'classic', u'seaborn-ticks', 
          u'grayscale', u'bmh', u'seaborn-talk', u'dark_background', 
          u'ggplot', u'fivethirtyeight', u'seaborn-colorblind', 
          u'seaborn-deep', u'seaborn-whitegrid', u'seaborn-bright', 
          u'seaborn-poster', u'seaborn-muted', u'seaborn-paper', 
          u'seaborn-white', u'seaborn-pastel', u'seaborn-dark', 
          u'seaborn-dark-palette']
        """

        self.fontsize = fontsize
        self.labelsize = labelsize
        self.plotstyle = plotstyle
        plt.style.use(stylesheet)

    @staticmethod
    def add_title(mooringid="", lat=-99.9, lon=-99.9, depth=9999, instrument=""):
        """Pass parameters to annotate the title of the plot

      This sets the standard plot title using common meta information from PMEL/EPIC style netcdf files

      Parameters
      ----------
      mooringid : str
        Mooring Identifier
      lat : float
        The latitude of the mooring
      lon : float
        The longitude of the mooring
      depth : int
        Nominal depth of the instrument
      instrument : str
        Name/identifier of the instrument plotted
      """
        ptitle = (
            "Plotted on: {time:%Y/%m/%d %H:%M} \n from {mooringid} Lat: {latitude:3.3f}  Lon: {longitude:3.3f}"
            " Depth: {depth}\n : {instrument}"
        ).format(
            time=datetime.datetime.now(),
            mooringid=mooringid,
            latitude=lat,
            longitude=lon,
            depth=depth,
            instrument=instrument,
        )

        return ptitle

    def plot(
        self,
        xdata=None,
        ydata=None,
        ydata2=None,
        ydata3=None,
        ylabel=None,
        ylabel2=None,
        ylabel3=None,
        **kwargs
    ):
        fig = plt.figure(1)
        ax1 = plt.subplot2grid((3, 1), (0, 0), colspan=1, rowspan=1)
        p1 = ax1.plot(xdata, ydata, self.plotstyle, markersize=2)
        ax1.set_ylim([np.nanmin(ydata), np.nanmax(ydata)])
        ax1.set_xlim([np.nanmin(xdata), np.nanmax(xdata)])
        plt.ylabel(ylabel)
        ax1.xaxis.set_major_locator(MonthLocator())
        ax1.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax1.xaxis.set_major_formatter(ticker.NullFormatter())
        ax1.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax1.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax1.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax1.spines["bottom"].set_visible(False)

        ax2 = plt.subplot2grid((3, 1), (1, 0), colspan=1, rowspan=1)
        p2 = ax2.plot(xdata, ydata2, self.plotstyle, markersize=2)
        ax2.set_ylim([np.nanmin(ydata2), np.nanmax(ydata2)])
        ax2.set_xlim([np.nanmin(xdata), np.nanmax(xdata)])
        plt.ylabel(ylabel2)
        ax2.xaxis.set_major_locator(MonthLocator())
        ax2.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax2.xaxis.set_major_formatter(ticker.NullFormatter())
        ax2.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax2.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax2.tick_params(
            axis="x", which="both", top="off", bottom="off", labelbottom="off"
        )
        ax2.spines["top"].set_visible(False)
        ax2.spines["bottom"].set_visible(False)

        ax3 = plt.subplot2grid((3, 1), (2, 0), colspan=1, rowspan=1)
        p2 = ax3.plot(xdata, ydata3, self.plotstyle, markersize=2)
        ax3.set_ylim([np.nanmin(ydata3), np.nanmax(ydata3)])
        ax3.set_xlim([np.nanmin(xdata), np.nanmax(xdata)])
        plt.ylabel(ylabel3)
        ax3.xaxis.set_major_locator(MonthLocator())
        ax3.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax3.xaxis.set_major_formatter(ticker.NullFormatter())
        ax3.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax3.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax3.tick_params(axis="x", which="both", top="off")
        ax3.spines["top"].set_visible(False)

        return plt, fig


class Timeseries1dStickPlot(object):

    mpl.rcParams["svg.fonttype"] = "none"
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["pdf.fonttype"] = 42

    def __init__(self, fontsize=10, labelsize=10, plotstyle="k-.", stylesheet="bmh"):
        """Initialize the timeseries with items that do not change.

        This sets up the axes and station locations. The `fontsize` and `spacing`
        are also specified here to ensure that they are consistent between individual
        station elements.

        Parameters
        ----------
        fontsize : int
            The fontsize to use for drawing text
        labelsize : int
          The fontsize to use for labels
        stylesheet : str
          Choose a mpl stylesheet [u'seaborn-darkgrid', 
          u'seaborn-notebook', u'classic', u'seaborn-ticks', 
          u'grayscale', u'bmh', u'seaborn-talk', u'dark_background', 
          u'ggplot', u'fivethirtyeight', u'seaborn-colorblind', 
          u'seaborn-deep', u'seaborn-whitegrid', u'seaborn-bright', 
          u'seaborn-poster', u'seaborn-muted', u'seaborn-paper', 
          u'seaborn-white', u'seaborn-pastel', u'seaborn-dark', 
          u'seaborn-dark-palette']
        """

        self.fontsize = fontsize
        self.labelsize = labelsize
        self.plotstyle = plotstyle
        plt.style.use(stylesheet)

    @staticmethod
    def add_title(mooringid="", lat=-99.9, lon=-99.9, depth=9999, instrument=""):
        """Pass parameters to annotate the title of the plot

      This sets the standard plot title using common meta information from PMEL/EPIC style netcdf files

      Parameters
      ----------
      mooringid : str
        Mooring Identifier
      lat : float
        The latitude of the mooring
      lon : float
        The longitude of the mooring
      depth : int
        Nominal depth of the instrument
      instrument : str
        Name/identifier of the instrument plotted
      """
        ptitle = (
            "Plotted on: {time:%Y/%m/%d %H:%M} \n from {mooringid} Lat: {latitude:3.3f}  Lon: {longitude:3.3f}"
            " Depth: {depth}\n : {instrument}"
        ).format(
            time=datetime.datetime.now(),
            mooringid=mooringid,
            latitude=lat,
            longitude=lon,
            depth=depth,
            instrument=instrument,
        )

        return ptitle

    def plot(self, timedata=None, udata=None, vdata=None, ylabel=None, **kwargs):

        if kwargs["rotate"] != 0.0:
            # when rotating vectors - positive(+) rotation is equal to ccw of the axis (cw of vector)
            #                      - negative(-) rotation is equal to cw of the axis (ccw of the vector)
            print("rotating vectors {} degrees".format(kwargs["rotate"]))
            angle_offset_rad = np.deg2rad(kwargs["rotate"])
            # error in calculation used corrected udata to correct vdata 2019/05
            uprime = udata * np.cos(angle_offset_rad) + vdata * np.sin(angle_offset_rad)
            vprime = -1.0 * udata * np.sin(angle_offset_rad) + vdata * np.cos(
                angle_offset_rad
            )
            udata = uprime
            vdata = vprime

        magnitude = np.sqrt(udata ** 2 + vdata ** 2)

        fig = plt.figure(1)
        ax1 = plt.subplot2grid((2, 1), (0, 0), colspan=1, rowspan=1)
        ax2 = plt.subplot2grid((2, 1), (1, 0), colspan=1, rowspan=1)

        # Plot u and v components
        # Plot quiver
        ax1.set_ylim(-1 * np.nanmax(magnitude), np.nanmax(magnitude))
        fill1 = ax1.fill_between(timedata, magnitude, 0, color="k", alpha=0.1)

        # Fake 'box' to be able to insert a legend for 'Magnitude'
        p = ax1.add_patch(plt.Rectangle((1, 1), 1, 1, fc="k", alpha=0.1))
        leg1 = ax1.legend([p], ["Current magnitude [cm/s]"], loc="lower right")
        leg1._drawFrame = False

        # 1D Quiver plot
        q = ax1.quiver(
            timedata,
            0,
            udata,
            vdata,
            color="r",
            units="y",
            scale_units="y",
            scale=1,
            headlength=1,
            headaxislength=1,
            width=0.04,
            alpha=0.95,
        )
        qk = plt.quiverkey(
            q,
            0.2,
            0.05,
            5,
            r"$5 \frac{cm}{s}$",
            labelpos="W",
            fontproperties={"weight": "bold"},
        )

        # Plot u and v components
        ax1.set_xticklabels(ax1.get_xticklabels(), visible=False)
        ax2.set_xticklabels(ax2.get_xticklabels(), visible=True)
        ax1.axes.get_xaxis().set_visible(False)
        ax1.set_xlim(timedata.min() - 0.5, timedata.max() + 0.5)
        ax1.set_ylabel("Velocity (cm/s)")
        ax2.plot(timedata, vdata, "b-", linewidth=0.25)
        ax2.plot(timedata, udata, "g-", linewidth=0.25)
        ax2.set_xlim(timedata.min() - 0.5, timedata.max() + 0.5)
        ax2.set_xlabel("Date (UTC)")
        ax2.set_ylabel("Velocity (cm/s)")
        ax2.xaxis.set_major_locator(MonthLocator())
        ax2.xaxis.set_minor_locator(MonthLocator(bymonth=range(1, 13), bymonthday=15))
        ax2.xaxis.set_major_formatter(ticker.NullFormatter())
        ax2.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax1.spines["bottom"].set_visible(False)
        ax2.spines["top"].set_visible(False)
        ax1.xaxis.set_ticks_position("top")
        ax2.xaxis.set_ticks_position("bottom")
        ax2.yaxis.set_ticks_position("both")
        ax2.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax1.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        # manual time limit sets
        # ax1.set_xlim([datetime.datetime(2016,2,1),datetime.datetime(2016,9,15)])
        # ax2.set_xlim([datetime.datetime(2016,2,1),datetime.datetime(2016,9,15)])
        # Set legend location - See: http://matplotlib.org/Volumes/WDC_internal/users/legend_guide.html#legend-location
        leg2 = plt.legend(["v", "u"], loc="upper left")
        leg2._drawFrame = False

        return plt, fig


class Timeseries1dStickPlot_2params(object):

    mpl.rcParams["svg.fonttype"] = "none"
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["pdf.fonttype"] = 42

    def __init__(self, fontsize=10, labelsize=10, plotstyle="k-.", stylesheet="bmh"):
        """Initialize the timeseries with items that do not change.

        This sets up the axes and station locations. The `fontsize` and `spacing`
        are also specified here to ensure that they are consistent between individual
        station elements.

        Parameters
        ----------
        fontsize : int
            The fontsize to use for drawing text
        labelsize : int
          The fontsize to use for labels
        stylesheet : str
          Choose a mpl stylesheet [u'seaborn-darkgrid', 
          u'seaborn-notebook', u'classic', u'seaborn-ticks', 
          u'grayscale', u'bmh', u'seaborn-talk', u'dark_background', 
          u'ggplot', u'fivethirtyeight', u'seaborn-colorblind', 
          u'seaborn-deep', u'seaborn-whitegrid', u'seaborn-bright', 
          u'seaborn-poster', u'seaborn-muted', u'seaborn-paper', 
          u'seaborn-white', u'seaborn-pastel', u'seaborn-dark', 
          u'seaborn-dark-palette']
        """

        self.fontsize = fontsize
        self.labelsize = labelsize
        self.plotstyle = plotstyle
        plt.style.use(stylesheet)

    @staticmethod
    def add_title(mooringid="", lat=-99.9, lon=-99.9, depth=9999, instrument=""):
        """Pass parameters to annotate the title of the plot

      This sets the standard plot title using common meta information from PMEL/EPIC style netcdf files

      Parameters
      ----------
      mooringid : str
        Mooring Identifier
      lat : float
        The latitude of the mooring
      lon : float
        The longitude of the mooring
      depth : int
        Nominal depth of the instrument
      instrument : str
        Name/identifier of the instrument plotted
      """
        ptitle = (
            "Plotted on: {time:%Y/%m/%d %H:%M} \n from {mooringid} Lat: {latitude:3.3f}  Lon: {longitude:3.3f}"
            " Depth: {depth}\n : {instrument}"
        ).format(
            time=datetime.datetime.now(),
            mooringid=mooringid,
            latitude=lat,
            longitude=lon,
            depth=depth,
            instrument=instrument,
        )

        return ptitle

    def plot(self, timedata=None, udata=None, vdata=None, ylabel=None, **kwargs):

        if kwargs["rotate"] != 0.0:
            print("rotating vectors")
            angle_offset_rad = np.deg2rad(kwargs["rotate"])
            udata = udata * np.cos(angle_offset_rad) + vdata * np.sin(angle_offset_rad)
            vdata = -1 * udata * np.sin(angle_offset_rad) + vdata * np.cos(
                angle_offset_rad
            )

        magnitude = np.sqrt(udata ** 2 + vdata ** 2)

        fig = plt.figure(1)
        ax2 = plt.subplot2grid((2, 1), (0, 0), colspan=1, rowspan=1)
        ax1 = plt.subplot2grid((2, 1), (1, 0), colspan=1, rowspan=1)

        # Plot u and v components
        # Plot quiver
        ax1.set_ylim(-1 * np.nanmax(magnitude), np.nanmax(magnitude))
        fill1 = ax1.fill_between(timedata, magnitude, 0, color="k", alpha=0.1)

        # Fake 'box' to be able to insert a legend for 'Magnitude'
        p = ax1.add_patch(plt.Rectangle((1, 1), 1, 1, fc="k", alpha=0.1))
        leg1 = ax1.legend([p], ["Current magnitude [cm/s]"], loc="lower right")
        leg1._drawFrame = False

        # 1D Quiver plot
        q = ax1.quiver(
            timedata,
            0,
            udata,
            vdata,
            color="r",
            units="y",
            scale_units="y",
            scale=1,
            headlength=1,
            headaxislength=1,
            width=0.04,
            alpha=0.95,
        )
        qk = plt.quiverkey(
            q,
            0.2,
            0.05,
            25,
            r"$25 \frac{cm}{s}$",
            labelpos="W",
            fontproperties={"weight": "bold"},
        )

        # Plot u and v components
        ax1.set_xticklabels(ax1.get_xticklabels(), visible=True)
        ax2.set_xticklabels(ax2.get_xticklabels(), visible=True)
        ax1.axes.get_xaxis().set_visible(True)
        ax1.set_xlim(timedata.min() - 0.5, timedata.max() + 0.5)
        ax1.set_ylabel("Velocity (cm/s)")
        ax2.plot(kwargs["timedata2"], kwargs["data2"][:, 0, 0, 0], "k-", linewidth=1)
        ax2.set_xlim(timedata.min() - 0.5, timedata.max() + 0.5)
        ax2.set_xlabel("Date (UTC)")
        ax2.set_ylabel("Salinity (PSU)")
        ax2.xaxis.set_major_locator(MonthLocator())
        ax2.xaxis.set_minor_locator(MonthLocator(bymonth=range(1, 13), bymonthday=15))
        ax2.xaxis.set_major_formatter(ticker.NullFormatter())
        ax2.xaxis.set_minor_formatter(ticker.NullFormatter())
        ax1.xaxis.set_major_locator(MonthLocator())
        ax1.xaxis.set_minor_locator(MonthLocator(bymonth=range(1, 13), bymonthday=15))
        ax1.xaxis.set_major_formatter(ticker.NullFormatter())
        ax1.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax2.spines["bottom"].set_visible(False)
        ax1.spines["top"].set_visible(False)
        ax1.xaxis.set_ticks_position("top")
        ax2.xaxis.set_ticks_position("bottom")
        ax2.yaxis.set_ticks_position("both")
        ax1.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax2.tick_params(axis="both", which="minor", labelsize=self.labelsize)

        return plt, fig


class Timeseries2dStickPlot(object):
    # TODO
    pass


class TimeseriesImagePlot(object):
    pass


class TimeseriesWPAK(object):

    mpl.rcParams["svg.fonttype"] = "none"
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["pdf.fonttype"] = 42

    def __init__(self, fontsize=10, labelsize=10, plotstyle="k-.", stylesheet="bmh"):
        """Initialize the timeseries with items that do not change.

        This sets up the axes and station locations. The `fontsize` and `spacing`
        are also specified here to ensure that they are consistent between individual
        station elements.

        Parameters
        ----------
        fontsize : int
            The fontsize to use for drawing text
        labelsize : int
          The fontsize to use for labels
        stylesheet : str
          Choose a mpl stylesheet [u'seaborn-darkgrid', 
          u'seaborn-notebook', u'classic', u'seaborn-ticks', 
          u'grayscale', u'bmh', u'seaborn-talk', u'dark_background', 
          u'ggplot', u'fivethirtyeight', u'seaborn-colorblind', 
          u'seaborn-deep', u'seaborn-whitegrid', u'seaborn-bright', 
          u'seaborn-poster', u'seaborn-muted', u'seaborn-paper', 
          u'seaborn-white', u'seaborn-pastel', u'seaborn-dark', 
          u'seaborn-dark-palette']
        """

        self.fontsize = fontsize
        self.labelsize = labelsize
        self.plotstyle = plotstyle
        plt.style.use(stylesheet)

    @staticmethod
    def add_title(mooringid="", lat=-99.9, lon=-99.9, depth=9999, instrument=""):
        """Pass parameters to annotate the title of the plot

      This sets the standard plot title using common meta information from PMEL/EPIC style netcdf files

      Parameters
      ----------
      mooringid : str
        Mooring Identifier
      lat : float
        The latitude of the mooring
      lon : float
        The longitude of the mooring
      depth : int
        Nominal depth of the instrument
      instrument : str
        Name/identifier of the instrument plotted
      """
        ptitle = (
            "Plotted on: {time:%Y/%m/%d %H:%M} \n from {mooringid} Lat: {latitude:3.3f}  Lon: {longitude:3.3f}"
            " Depth: {depth}\n : {instrument}"
        ).format(
            time=datetime.datetime.now(),
            mooringid=mooringid,
            latitude=lat,
            longitude=lon,
            depth=depth,
            instrument=instrument,
        )

        return ptitle

    def plot(self, xdata=None, ydata=None, **kwargs):

        """
      Purpose
      --------
      Plot all sfc met observations as one image
      """

        TC = ydata["AT_21"][:, 0, 0, 0]
        TD = ydata["RH_910"][:, 0, 0, 0]
        Press = ydata["BP_915"][:, 0, 0, 0]
        WindU = ydata["WU_422"][:, 0, 0, 0]
        WindV = ydata["WV_423"][:, 0, 0, 0]
        Rad = ydata["Qs_133"][:, 0, 0, 0]
        Teq = ydata["Teq_1800"][:, 0, 0, 0]
        bat = ydata["BAT_106"][:, 0, 0, 0]
        comp = ydata["comp_1404"][:, 0, 0, 0]

        fig = plt.figure()
        # text locations
        right = 0.05
        top = 0.95

        # TC, TD
        ax = fig.add_subplot(911)
        tplot = ax.plot(xdata, TC)
        ax.set_xlim(min(xdata), max(xdata))
        plt.setp(tplot, "color", "r", "linestyle", "-", "linewidth", 0.5)
        ax.text(
            right,
            top,
            "Air Temperature ",
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax.transAxes,
        )
        plt.ylabel("(Deg C)")
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        ax.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax.spines["bottom"].set_visible(False)
        ax.yaxis.set_ticks_position("both")

        # RH
        ax = fig.add_subplot(912)
        tplot = ax.plot(xdata, TD)
        ax.set_xlim(min(xdata), max(xdata))
        plt.setp(tplot, "color", "g", "linestyle", "-", "linewidth", 0.5)
        ax.text(
            right,
            top,
            "Relative Humidity ",
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax.transAxes,
        )
        plt.ylabel("%")
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        ax.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax.spines["bottom"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.yaxis.set_ticks_position("both")

        # Press
        ax = fig.add_subplot(913)
        tplot = ax.plot(xdata, Press)
        ax.set_xlim(min(xdata), max(xdata))
        plt.setp(tplot, "color", "k", "linestyle", "-", "linewidth", 0.5)
        ax.text(
            right,
            top,
            "Pressure ",
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax.transAxes,
        )
        plt.ylabel("(mb)")
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        ax.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax.spines["bottom"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.yaxis.set_ticks_position("both")

        # Plot quiver
        # WindU[WindU == np.nan] = 0
        # WindV[WindV == np.nan] = 0
        ax1 = fig.add_subplot(914)
        ax2 = fig.add_subplot(915)
        magnitude = (WindU ** 2 + WindV ** 2) ** 0.5
        ax1.set_ylim(-1 * np.nanmax(magnitude), np.nanmax(magnitude))
        ax1.set_xlim(min(xdata), max(xdata))

        fill1 = ax1.fill_between(xdata, magnitude, 0, color="k", alpha=0.1)

        # Fake 'box' to be able to insert a legend for 'Magnitude'
        p = ax1.add_patch(plt.Rectangle((1, 1), 1, 1, fc="k", alpha=0.5))
        leg1 = ax1.legend([p], ["Wind magnitude [m/s]"], loc="lower right")
        leg1._drawFrame = False

        # 1D Quiver plot
        q = ax1.quiver(
            xdata,
            0,
            WindU,
            WindV,
            color="r",
            units="y",
            scale_units="y",
            scale=1,
            headlength=1,
            headaxislength=1,
            width=0.04,
            alpha=0.75,
        )
        qk = plt.quiverkey(
            q,
            0.2,
            0.05,
            2,
            r"$2 \frac{m}{s}$",
            labelpos="W",
            fontproperties={"weight": "bold"},
        )

        # Plot u and v components
        ax1.set_ylabel("Velocity (m/s)")

        ax2.plot(xdata, WindV, "b-")
        ax2.plot(xdata, WindU, "g-")
        ax2.set_xlim(min(xdata), max(xdata))
        ax2.set_ylabel("Velocity (m/s)")
        ax2.yaxis.set_ticks_position("both")
        ax2.xaxis.set_major_locator(MonthLocator())
        ax2.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax2.xaxis.set_major_formatter(ticker.NullFormatter())
        ax2.xaxis.set_minor_formatter(ticker.NullFormatter())
        ax2.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax2.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax1.set_ylabel("Velocity (m/s)")
        ax1.yaxis.set_ticks_position("both")
        ax1.xaxis.set_major_locator(MonthLocator())
        ax1.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax1.xaxis.set_major_formatter(ticker.NullFormatter())
        ax1.xaxis.set_minor_formatter(ticker.NullFormatter())
        ax1.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax1.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax1.axes.get_xaxis().set_visible(False)
        ax1.spines["top"].set_visible(False)
        ax1.spines["bottom"].set_visible(False)
        ax2.axes.get_xaxis().set_visible(False)
        ax2.spines["top"].set_visible(False)
        ax2.spines["bottom"].set_visible(False)

        # Set legend location - See: http://matplotlib.org/users/legend_guide.html#legend-location
        leg2 = plt.legend(["v", "u"], loc="upper left")
        leg2._drawFrame = False

        # Rad
        ax = fig.add_subplot(916)
        tplot = ax.plot(xdata, Rad)
        ax.set_xlim(min(xdata), max(xdata))
        plt.setp(tplot, "color", "k", "linestyle", "-", "linewidth", 0.5)
        ax.fill_between(xdata, 0, Rad, facecolor="yellow")
        ax.text(
            right,
            top,
            "Shortwave Radiation  ",
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax.transAxes,
        )
        plt.ylabel("(W*m^-2)")
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        ax.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax.spines["bottom"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.yaxis.set_ticks_position("both")

        # system vars - equil temp, battery, compass
        ax = fig.add_subplot(917)
        tplot = ax.plot(xdata, Teq)
        ax.set_xlim(min(xdata), max(xdata))
        plt.setp(tplot, "color", "k", "linestyle", "-", "linewidth", 0.5)
        ax.text(
            right,
            top,
            "Teq ",
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax.transAxes,
        )
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        ax.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax.spines["bottom"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.yaxis.set_ticks_position("both")

        ax = fig.add_subplot(918)
        tplot = ax.plot(xdata, bat)
        ax.set_xlim(min(xdata), max(xdata))
        plt.setp(tplot, "color", "k", "linestyle", "-", "linewidth", 0.5)
        ax.text(
            right,
            top,
            "battery ",
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax.transAxes,
        )
        plt.ylabel("volts")
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        ax.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax.spines["bottom"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.yaxis.set_ticks_position("both")

        ax = fig.add_subplot(919)
        tplot = ax.plot(xdata, comp)
        ax.set_xlim(min(xdata), max(xdata))
        plt.setp(
            tplot, "color", "k", "linestyle", "None", "marker", ".", "markersize", 2.5
        )
        ax.text(
            right,
            top,
            "compass ",
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax.transAxes,
        )
        plt.ylabel("degrees")
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax.tick_params(axis="y", which="major", labelsize=self.labelsize)
        ax.tick_params(axis="x", which="both", top="off")
        ax.spines["top"].set_visible(False)
        ax.set_xlabel("Date (UTC)")

        return (plt, fig)

    def plot_rad(
        self,
        xdata=None,
        ydata=None,
        ydata2=None,
        ylabel=None,
        textlabel=None,
        textlabel2=None,
        **kwargs
    ):

        # Shortwave Radiation
        fig = plt.figure(1)
        ax1 = plt.subplot2grid((2, 1), (0, 0), colspan=1, rowspan=1)
        p1 = ax1.plot(xdata, ydata, "k", linewidth=0.25)
        ax1.fill_between(xdata, 0, ydata, facecolor="yellow")
        ax1.set_ylim([np.nanmin(ydata), np.nanmax(ydata)])
        ax1.set_xlim([np.nanmin(xdata), np.nanmax(xdata)])
        plt.ylabel(ylabel)
        ax1.xaxis.set_major_locator(MonthLocator())
        ax1.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax1.xaxis.set_major_formatter(ticker.NullFormatter())
        ax1.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax1.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax1.tick_params(axis="x", which="both", bottom="off", labelbottom="off")
        ax1.spines["bottom"].set_visible(False)
        ax1.text(
            0.05,
            0.95,
            textlabel,
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax1.transAxes,
        )

        # Shortwave Radiation Estimated (1000Wm^-2 incident)
        ax2 = plt.subplot2grid((2, 1), (1, 0), colspan=1, rowspan=1)
        p2 = ax2.plot(xdata, ydata2, "k", linewidth=0.25)
        ax2.fill_between(xdata, 0, ydata, facecolor="yellow")
        ax2.set_ylim([np.nanmin(ydata2), np.nanmax(ydata2)])
        ax2.set_xlim([np.nanmin(xdata), np.nanmax(xdata)])
        plt.ylabel(ylabel)
        ax2.xaxis.set_major_locator(MonthLocator())
        ax2.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        ax2.xaxis.set_major_formatter(ticker.NullFormatter())
        ax2.xaxis.set_minor_formatter(DateFormatter("%b %y"))
        ax2.tick_params(axis="both", which="minor", labelsize=self.labelsize)
        ax2.tick_params(axis="x", which="both", top="off")
        ax2.spines["top"].set_visible(False)
        ax2.text(
            0.05,
            0.95,
            textlabel2,
            horizontalalignment="left",
            verticalalignment="top",
            transform=ax2.transAxes,
        )

        ax2.set_xlabel("Date (UTC)")

        return (plt, fig)


class TimeseriesPorpertyPropertyPlot(object):
    """ class to plot property vs property plots with density iso-contours"""

    mpl.rcParams["svg.fonttype"] = "none"
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["pdf.fonttype"] = 42

    def __init__(
        self, fontsize=10, labelsize=10, plotstyle="k-.", stylesheet="seaborn-whitegrid"
    ):
        """Initialize the timeseries with items that do not change.

        This sets up the axes and station locations. The `fontsize` and `spacing`
        are also specified here to ensure that they are consistent between individual
        station elements.

        Parameters
        ----------
        fontsize : int
            The fontsize to use for drawing text
        labelsize : int
          The fontsize to use for labels
        stylesheet : str
          Choose a mpl stylesheet [u'seaborn-darkgrid', 
          u'seaborn-notebook', u'classic', u'seaborn-ticks', 
          u'grayscale', u'bmh', u'seaborn-talk', u'dark_background', 
          u'ggplot', u'fivethirtyeight', u'seaborn-colorblind', 
          u'seaborn-deep', u'seaborn-whitegrid', u'seaborn-bright', 
          u'seaborn-poster', u'seaborn-muted', u'seaborn-paper', 
          u'seaborn-white', u'seaborn-pastel', u'seaborn-dark', 
          u'seaborn-dark-palette']
        """

        self.fontsize = fontsize
        self.labelsize = labelsize
        self.plotstyle = plotstyle
        plt.style.use(stylesheet)

    @staticmethod
    def add_title(mooringid="", lat=-99.9, lon=-99.9, depth=9999, instrument=""):
        """Pass parameters to annotate the title of the plot

      This sets the standard plot title using common meta information from PMEL/EPIC style netcdf files

      Parameters
      ----------
      mooringid : str
        Mooring Identifier
      lat : float
        The latitude of the mooring
      lon : float
        The longitude of the mooring
      depth : int
        Nominal depth of the instrument
      instrument : str
        Name/identifier of the instrument plotted
      """

        ptitle = (
            "Plotted on: {time:%Y/%m/%d %H:%M} \n from {mooringid} Lat: {latitude:3.3f}  Lon: {longitude:3.3f}"
            " Depth: {depth}\n : {instrument}"
        ).format(
            time=datetime.datetime.now(),
            mooringid=mooringid,
            latitude=lat,
            longitude=lon,
            depth=depth,
            instrument=instrument,
        )

        return ptitle

    @staticmethod
    def plot(
        self, var1, var2, var3=None, var1range=[0, 1], var2range=[0, 10], ptitle=""
    ):

        # Calculate how many gridcells we need in the x and y dimensions
        xdim = round((var1range[1] - var1range[0]) / 0.1 + 1, 0)
        ydim = round((var2range[1] - var2range[0]) + 2, 0)

        # print 'ydim: ' + str(ydim) + ' xdim: ' + str(xdim) + ' \n'
        if (xdim > 10000) or (ydim > 10000):
            print(
                "To many dimensions for grid in "
                + cruise
                + cast
                + " file. Likely  missing data \n"
            )
            return

        # Create empty grid of zeros
        dens = np.zeros((int(ydim), int(xdim)))

        # Create temp and salt vectors of appropiate dimensions
        ti = np.linspace(0, ydim - 1, ydim) + var2range[0]
        si = np.linspace(0, xdim - 1, xdim) * 0.1 + var1range[0]

        # Loop to fill in grid with densities
        for j in range(0, int(ydim)):
            for i in range(0, int(xdim)):
                dens[j, i] = sw.dens0(si[i], ti[j])

        # Substract 1000 to convert to sigma-t
        dens = dens - 1000

        # Plot data ***********************************************
        fig = plt.figure(1)
        ax1 = plt.subplot2grid((1, 1), (0, 0), colspan=1, rowspan=1)
        CS = plt.contour(si, ti, dens, linestyles="dashed", colors="k")
        plt.clabel(CS, fontsize=12, inline=1, fmt="%1.1f")  # Label every second level

        ts = ax1.scatter(var1, var2, s=25, c=var3, marker=".", cmap="Blues")
        plt.colorbar(ts, label="DOY")
        plt.ylim(var2range[0], var2range[1])
        plt.xlim(var1range[0], var1range[1])

        ax1.set_xlabel("Salinity (PSU)")
        ax1.set_ylabel("Temperature (C)")

        return plt, fig
