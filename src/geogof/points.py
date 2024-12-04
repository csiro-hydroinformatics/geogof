"""Utilities for point data."""

from typing import Any

import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs

# import mapclassify as mc
# import numpy as np
# import imageio
import pandas as pd
import xarray as xr
from cartopy.mpl.geoaxes import GeoAxes
from ipyleaflet import GeoData

# import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# Acknowledgment: https://towardsdatascience.com/visualizing-geospatial-data-in-python-e070374fe621


class PointData:
    """Class for handling point data."""

    def __init__(
        self, data: pd.DataFrame | xr.DataArray, lat_name: str = "lat", lon_name: str = "lon", obj_name: str = "obj",
    ) -> None:
        """Initialize the class.

        Args:
            data (pd.DataFrame | xr.DataArray): The point data.
            lat_name (str): The name of the latitude column.
            lon_name (str): The name of the longitude column.
        """
        # Step 1: Convert the DataFrame to a GeoDataFrame
        self._gof_dataframe = data.to_dataframe().reset_index() if isinstance(data, xr.DataArray) else data.copy()

        for x in (lat_name, lon_name, obj_name):
            if x not in self._gof_dataframe.columns:
                raise ValueError(f"Column {x} not found in the DataFrame")
        self._lat_name = lat_name
        self._lon_name = lon_name
        self._obj_name = obj_name
        # Step 2: Create a GeoDataFrame
        df = self._gof_dataframe
        self._gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df.lon, df.lat),
            crs="EPSG:4326",  # WGS84 coordinate system
        )

    def pointplot(self, outline_shape: gpd.GeoDataFrame | None, projection: Any = None) -> tuple[Axes, GeoAxes]:
        """Plot the point data."""
        projection = projection or gcrs.LambertAzimuthalEqualArea()
        ax = None if outline_shape is None else gplt.polyplot(outline_shape, projection=projection)
        return gplt.pointplot(self._gof_dataframe, hue=self._obj_name, ax=ax, legend=True)

    def ipyleaflet_geodata_layer(self) -> GeoData:
        """Create a GeoData layer for use in ipyleaflet maps."""
        # https://ipyleaflet.readthedocs.io/en/latest/layers/geodata.html

        gdf = self._gof_dataframe

        return GeoData(geo_dataframe = gdf,
            style={"color": "black", "radius":8, "fillColor": "#3366cc", "opacity":0.5, "weight":1.9, "dashArray":"2", "fillOpacity":0.6},
            hover_style={"fillColor": "red" , "fillOpacity": 0.2},
            point_style={"radius": 5, "color": "red", "fillOpacity": 0.8, "fillColor": "blue", "weight": 3},
            name = "Release")
