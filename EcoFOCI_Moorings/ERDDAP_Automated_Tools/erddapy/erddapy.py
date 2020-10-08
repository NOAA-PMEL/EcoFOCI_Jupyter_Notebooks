"""
Pythonic way to access ERDDAP data

"""

import copy
import functools

from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import quote_plus

import pandas as pd

from erddapy.utilities import (
    _nc_dataset,
    _tempnc,
    parse_dates,
    quote_string_constraints,
    servers,
    urlopen,
)


ListLike = Union[List[str], Tuple[str]]
OptionalStr = Optional[str]


def _distinct(url: str, **kwargs: Dict) -> str:
    """
    Sort all of the rows in the results table
    (starting with the first requested variable,
    then using the second requested variable if the first variable has a tie, ...),
    then remove all non-unique rows of data.

    For example, a query for the variables ["stationType", "stationID"] with `distinct=True`
    will return a sorted list of "stationIDs" associated with each "stationType".

    See https://coastwatch.pfeg.noaa.gov/erddap/tabledap/documentation.html#distinct

    """
    distinct = kwargs.pop("distinct", False)
    if distinct is True:
        return f"{url}&distinct()"
    return url


class ERDDAP(object):
    """Creates an ERDDAP instance for a specific server endpoint.

    Args:
        server: an ERDDAP server URL or an acronym for one of the builtin servers.
        protocol: tabledap or griddap.

    Attributes:
        dataset_id: a dataset unique id.
        variables: a list variables to download.
        response: default is HTML.
        constraints: download constraints, default None (opendap-like url)
        params and requests_kwargs: `request.get` options

    Returns:
        instance: the ERDDAP URL builder.

    Examples:
        Specifying the server URL

        >>> e = ERDDAP(server="https://gliders.ioos.us/erddap")

        let's search for glider `ru29` and read the csv response with pandas.

        >>> import pandas as pd
        >>> url = e.get_search_url(search_for="ru29", response="csv")
        >>> pd.read_csv(url)["Dataset ID"]
        0    ru29-20150623T1046
        1    ru29-20161105T0131
        Name: Dataset ID, dtype: object

        there are "shortcuts" for some servers

        >>> e = ERDDAP(server="SECOORA")
        >>> e.server
        'http://erddap.secoora.org/erddap'

        to get a list of the shortcuts available servers:

        >>> from erddapy import servers
        >>> {k: v.url for k, v in servers.items()}
        {'MDA': 'https://bluehub.jrc.ec.europa.eu/erddap/',
         'MII': 'https://erddap.marine.ie/erddap/',
         'CSCGOM': 'http://cwcgom.aoml.noaa.gov/erddap/',
         'CSWC': 'https://coastwatch.pfeg.noaa.gov/erddap/',
         'CeNCOOS': 'http://erddap.axiomalaska.com/erddap/',
         'NERACOOS': 'http://www.neracoos.org/erddap/',
         'NGDAC': 'https://gliders.ioos.us/erddap/',
         'PacIOOS': 'http://oos.soest.hawaii.edu/erddap/',
         'SECOORA': 'http://erddap.secoora.org/erddap/',
         'NCEI': 'https://ecowatch.ncddc.noaa.gov/erddap/',
         'OSMC': 'http://osmc.noaa.gov/erddap/',
         'UAF': 'https://upwell.pfeg.noaa.gov/erddap/',
         'ONC': 'http://dap.onc.uvic.ca/erddap/',
         'BMLSC': 'http://bmlsc.ucdavis.edu:8080/erddap/',
         'RTECH': 'https://meteo.rtech.fr/erddap/',
         'IFREMER': 'http://www.ifremer.fr/erddap/',
         'UBC': 'https://salishsea.eos.ubc.ca/erddap/'}

    """

    def __init__(
        self, server: str, protocol: OptionalStr = None, response: str = "html",
    ):
        if server in servers.keys():
            server = servers[server].url
        self.server = server
        self.protocol = protocol
        self.response = response

        # Initialized only via properties.
        self.constraints: Optional[Dict] = None
        self.dataset_id: OptionalStr = None
        self.requests_kwargs: Dict = {}
        self.auth: Optional[tuple] = None
        self.variables: Optional[ListLike] = None

        # Caching the last `dataset_id` and `variables` list request for quicker multiple accesses,
        # will be overridden when requesting a new `dataset_id`.
        self._dataset_id: OptionalStr = None
        self._variables: Dict = {}

    def get_search_url(
        self,
        response: OptionalStr = None,
        search_for: OptionalStr = None,
        protocol: OptionalStr = None,
        items_per_page: int = 1000,
        page: int = 1,
        **kwargs,
    ) -> str:

        """The search URL for the `server` endpoint provided.

        Args:
            search_for: "Google-like" search of the datasets' metadata.

                - Type the words you want to search for, with spaces between the words.
                    ERDDAP will search for the words separately, not as a phrase.
                - To search for a phrase, put double quotes around the phrase
                    (for example, `"wind speed"`).
                - To exclude datasets with a specific word, use `-excludedWord`.
                - To exclude datasets with a specific phrase, use `-"excluded phrase"`
                - Searches are not case-sensitive.
                - You can search for any part of a word. For example,
                    searching for `spee` will find datasets with `speed` and datasets with
                    `WindSpeed`
                - The last word in a phrase may be a partial word. For example,
                    to find datasets from a specific website (usually the start of the datasetID),
                    include (for example) `"datasetID=erd"` in your search.

            response: default is HTML.
            items_per_page: how many items per page in the return,
                default is 1000.
            page: which page to display, default is the first page (1).
            kwargs: extra search constraints based on metadata and/or coordinates ke/value.
                metadata: `cdm_data_type`, `institution`, `ioos_category`,
                `keywords`, `long_name`, `standard_name`, and `variableName`.
                coordinates: `minLon`, `maxLon`, `minLat`, `maxLat`, `minTime`, and `maxTime`.

        Returns:
            url: the search URL.

        """
        base = (
            "{server}/search/advanced.{response}"
            "?page={page}"
            "&itemsPerPage={itemsPerPage}"
            "&protocol={protocol}"
            "&cdm_data_type={cdm_data_type}"
            "&institution={institution}"
            "&ioos_category={ioos_category}"
            "&keywords={keywords}"
            "&long_name={long_name}"
            "&standard_name={standard_name}"
            "&variableName={variableName}"
            "&minLon={minLon}"
            "&maxLon={maxLon}"
            "&minLat={minLat}"
            "&maxLat={maxLat}"
            "&minTime={minTime}"
            "&maxTime={maxTime}"
        )
        if search_for:
            search_for = quote_plus(search_for)
            base += "&searchFor={searchFor}"

        # Convert dates from datetime to `seconds since 1970-01-01T00:00:00Z`.
        min_time = kwargs.pop("min_time", None)
        max_time = kwargs.pop("max_time", None)
        if min_time:
            kwargs.update({"min_time": parse_dates(min_time)})
        if max_time:
            kwargs.update({"max_time": parse_dates(max_time)})

        protocol = protocol if protocol else self.protocol
        response = response if response else self.response
        if protocol:
            kwargs.update({"protocol": protocol})

        default = "(ANY)"
        url = base.format(
            server=self.server,
            response=response,
            page=page,
            itemsPerPage=items_per_page,
            protocol=kwargs.get("protocol", default),
            cdm_data_type=kwargs.get("cdm_data_type", default),
            institution=kwargs.get("institution", default),
            ioos_category=kwargs.get("ioos_category", default),
            keywords=kwargs.get("keywords", default),
            long_name=kwargs.get("long_name", default),
            standard_name=kwargs.get("standard_name", default),
            variableName=kwargs.get("variableName", default),
            minLon=kwargs.get("min_lon", default),
            maxLon=kwargs.get("max_lon", default),
            minLat=kwargs.get("min_lat", default),
            maxLat=kwargs.get("max_lat", default),
            minTime=kwargs.get("min_time", default),
            maxTime=kwargs.get("max_time", default),
            searchFor=search_for,
        )

        return url

    def get_info_url(
        self, dataset_id: OptionalStr = None, response: OptionalStr = None
    ) -> str:
        """The info URL for the `server` endpoint.

        Args:
            dataset_id: a dataset unique id.
            response: default is HTML.

        Returns:
            url: the info URL for the `response` chosen.

        """
        dataset_id = dataset_id if dataset_id else self.dataset_id
        response = response if response else self.response

        if not dataset_id:
            raise ValueError(f"You must specify a valid dataset_id, got {dataset_id}")

        url = f"{self.server}/info/{dataset_id}/index.{response}"
        return url

    def get_categorize_url(
        self,
        categorize_by: str,
        value: OptionalStr = None,
        response: OptionalStr = None,
    ) -> str:
        """The categorize URL for the `server` endpoint.

        Args:
            categorize_by: a valid attribute, e.g.: ioos_category or standard_name.
            value: an attribute value.
            response: default is HTML.

        Returns:
            url: the categorized URL for the `response` chosen.

        """
        response = response if response else self.response
        if value:
            url = f"{self.server}/categorize/{categorize_by}/{value}/index.{response}"
        else:
            url = f"{self.server}/categorize/{categorize_by}/index.{response}"
        return url

    def get_download_url(
        self,
        dataset_id: OptionalStr = None,
        protocol: OptionalStr = None,
        variables: Optional[ListLike] = None,
        response=None,
        constraints=None,
        **kwargs,
    ) -> str:
        """The download URL for the `server` endpoint.

        Args:
            dataset_id: a dataset unique id.
            protocol: tabledap or griddap.
            variables (list/tuple): a list of the variables to download.
            response (str): default is HTML.
            constraints (dict): download constraints, default None (opendap-like url)
            example: constraints = {'latitude<=': 41.0,
                                    'latitude>=': 38.0,
                                    'longitude<=': -69.0,
                                    'longitude>=': -72.0,
                                    'time<=': '2017-02-10T00:00:00+00:00',
                                    'time>=': '2016-07-10T00:00:00+00:00',}

        Returns:
            url (str): the download URL for the `response` chosen.

        """
        dataset_id = dataset_id if dataset_id else self.dataset_id
        protocol = protocol if protocol else self.protocol
        variables = variables if variables else self.variables
        response = response if response else self.response
        constraints = constraints if constraints else self.constraints

        if not dataset_id:
            raise ValueError(f"Please specify a valid `dataset_id`, got {dataset_id}")

        if not protocol:
            raise ValueError(f"Please specify a valid `protocol`, got {protocol}")

        # This is an unconstrained OPeNDAP response b/c
        # the integer based constrained version is just not worth supporting ;-p
        if response == "opendap":
            return f"{self.server}/{protocol}/{dataset_id}"
        else:
            url = f"{self.server}/{protocol}/{dataset_id}.{response}?"

        if variables:
            url += ",".join(variables)

        if constraints:
            _constraints = copy.copy(constraints)
            for k, v in _constraints.items():
                if k.startswith("time"):
                    _constraints.update({k: parse_dates(v)})
            _constraints = quote_string_constraints(_constraints)
            _constraints = "".join([f"&{k}{v}" for k, v in _constraints.items()])

            url += f"{_constraints}"
        url = _distinct(url, **kwargs)
        return url

    def to_pandas(self, **kw):
        """Save a data request to a pandas.DataFrame.

        Accepts any `pandas.read_csv` keyword arguments.

        This method uses the .csvp [1] response as the default for simplicity,
        please check ERDDAP's documentation for the other csv options available.

        [1] Download a ISO-8859-1 .csv file with line 1: name (units). Times are ISO 8601 strings.

        """
        response = kw.pop("response", "csvp")
        url = self.get_download_url(response=response, **kw)
        return pd.read_csv(urlopen(url, auth=self.auth, **self.requests_kwargs), **kw)

    def to_ncCF(self, **kw):
        """Load the data request into a Climate and Forecast compliant netCDF4-python object.

        """
        url = self.get_download_url(response="ncCF", **kw)
        nc = _nc_dataset(url, auth=self.auth, **self.requests_kwargs)
        return nc

    def to_xarray(self, **kw):
        """Load the data request into a xarray.Dataset.

        Accepts any `xr.open_dataset` keyword arguments.
        """
        import xarray as xr

        url = self.get_download_url(response="nc")
        nc = _nc_dataset(url, auth=self.auth, **self.requests_kwargs)
        return xr.open_dataset(xr.backends.NetCDF4DataStore(nc), **kw)

    def to_iris(self, **kw):
        """Load the data request into an iris.CubeList.

        Accepts any `iris.load_raw` keyword arguments.
        """
        import iris

        url = self.get_download_url(response="ncCF", **kw)
        data = urlopen(url, auth=self.auth, **self.requests_kwargs).read()
        with _tempnc(data) as tmp:
            cubes = iris.load_raw(tmp, **kw)
            try:
                cubes.realise_data()
            except ValueError:
                iris.cube.CubeList([cube.data for cube in cubes])
            return cubes

    @functools.lru_cache(maxsize=None)
    def _get_variables(self, dataset_id: OptionalStr = None) -> Dict:
        if not dataset_id:
            dataset_id = self.dataset_id

        if dataset_id is None:
            raise ValueError(f"You must specify a valid dataset_id, got {dataset_id}")

        url = self.get_info_url(dataset_id=dataset_id, response="csv")

        variables = {}
        _df = pd.read_csv(urlopen(url, auth=self.auth, **self.requests_kwargs))
        self._dataset_id = dataset_id
        for variable in set(_df["Variable Name"]):
            attributes = (
                _df.loc[_df["Variable Name"] == variable, ["Attribute Name", "Value"]]
                .set_index("Attribute Name")
                .to_dict()["Value"]
            )
            variables.update({variable: attributes})
        return variables

    def get_var_by_attr(self, dataset_id: OptionalStr = None, **kwargs) -> List[str]:
        """Similar to netCDF4-python `get_variables_by_attributes` for an ERDDAP
        `dataset_id`.

        The `get_var_by_attr` method will create an info `csv` return,
        for the `dataset_id`, and the variables attribute dictionary.

        Examples:
            >>> e = ERDDAP(server_url="https://gliders.ioos.us/erddap")
            >>> dataset_id = "whoi_406-20160902T1700"

            Get variables with x-axis attribute.

            >>> e.get_var_by_attr(dataset_id, axis="X")
            ['longitude']

            Get variables with matching "standard_name" attribute

            >>> e.get_var_by_attr(
            ...     dataset_id, standard_name="northward_sea_water_velocity"
            ... )
            ['v']

            Get Axis variables

            >>> e.get_var_by_attr(dataset_id, axis=lambda v: v in ["X", "Y", "Z", "T"])
            ['latitude', 'longitude', 'time', 'depth']

        """
        variables = self._get_variables(dataset_id=dataset_id)
        # Virtually the same code as the netCDF4 counterpart.
        vs = []
        has_value_flag = False
        for vname in variables:
            var = variables[vname]
            for k, v in kwargs.items():
                if callable(v):
                    has_value_flag = v(var.get(k, None))
                    if has_value_flag is False:
                        break
                elif var.get(k) and var.get(k) == v:
                    has_value_flag = True
                else:
                    has_value_flag = False
                    break
            if has_value_flag is True:
                vs.append(vname)
        return vs
