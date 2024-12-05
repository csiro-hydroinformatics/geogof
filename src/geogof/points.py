"""Utilities for point data."""

from typing import Any, Dict  # noqa: UP035

import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs

# import mapclassify as mc
# import numpy as np
# import imageio
import pandas as pd
import xarray as xr
from branca.colormap import LinearColormap
from cartopy.mpl.geoaxes import GeoAxes
from ipyleaflet import GeoData

# import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# Acknowledgment: https://towardsdatascience.com/visualizing-geospatial-data-in-python-e070374fe621


class PointData:
    """Class for handling point data."""

    def __init__(
        self,
        data: pd.DataFrame | xr.DataArray,
        lat_name: str = "lat",
        lon_name: str = "lon",
        obj_name: str = "obj",
        lower_clip: float|None = None,
        upper_clip: float|None = None,
        fill_na_value: float=0,
    ) -> None:
        """Initialize the class.

        Args:
            data (pd.DataFrame | xr.DataArray): The point data.
            lat_name (str): The name of the latitude column.
            lon_name (str): The name of the longitude column.
            obj_name (str): The name of the objective column.
            lower_clip (float): The lower clipping value.
            upper_clip (float): The upper clipping value.
            fill_na_value (float): The value to fill NaNs with.
        """
        # Step 1: Convert the DataFrame to a GeoDataFrame
        gdf = data.to_dataframe().reset_index() if isinstance(data, xr.DataArray) else data.copy()

        for x in (lat_name, lon_name, obj_name):
            if x not in gdf.columns:
                raise ValueError(f"Column {x} not found in the DataFrame")
        self._lat_name = lat_name
        self._lon_name = lon_name
        self._obj_name = obj_name

        obj_clipped = gdf[self._obj_name].fillna(fill_na_value)
        if lower_clip is not None:
            obj_clipped = obj_clipped.clip(lower=lower_clip)
        if upper_clip is not None:
            obj_clipped = obj_clipped.clip(upper=upper_clip)
        gdf[self._obj_name] = obj_clipped
        self._gof_dataframe = gdf
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
        """Create a GeoData layer for use in ipyleaflet maps with color based on obj_value."""
        gdf = self._gdf

        # Create a color map
        objvals = gdf[self._obj_name]
        min_value = float(objvals.min())
        max_value = float(objvals.max())
        colormap = LinearColormap(colors=["blue", "yellow", "red"], vmin=min_value, vmax=max_value)

        def style_function(feature: Dict[str, Any]) -> dict:  # noqa: UP006
            """Function to get color based on obj_value."""
            obj_value = feature["properties"]["obj_value"]
            return {
                "fillColor": colormap(obj_value),
                "color": "black",
                "weight": 1.9,
                "dashArray": "2",
                "fillOpacity": 0.6,
                "radius": 8,
            }

        return GeoData(
            geo_dataframe=gdf,
            style_function=style_function,
            hover_style={"fillColor": "red", "fillOpacity": 0.2},
            point_style={"radius": 5, "color": "red", "fillOpacity": 0.8, "weight": 3},
            name="Release",
        )
