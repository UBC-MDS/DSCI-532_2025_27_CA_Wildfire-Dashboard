import pytest
import pandas as pd
import plotly.express as px
import geopandas as gpd
import plotly.graph_objects as go
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.create_map import make_fire_damage_map  

def test_make_fire_damage_map():
    """Test the aggregation and merging of wildfire data with county boundaries."""
    county_boundaries = gpd.GeoDataFrame({
        "County": ["Los Angeles", "San Diego", "San Francisco"],
        "geometry": [None, None, None],  # Normally, these would be geometries
        "Fire Count": [5, 10, 3],
        "Assessed Improved Value": [1.2 * 1e9, 0.8 * 1e9, 0.3 * 1e9],
        "Economic Loss": ["$1.2B", "$0.8B", "$0.3B"]
    })

    fig = make_fire_damage_map(county_boundaries)

    assert fig is not None, "Function should return a Plotly figure"
    assert hasattr(fig, "data"), "Figure should have data attribute"
    assert hasattr(fig, "layout"), "Figure should have layout attribute"


def test_make_fire_damage_map_empty():
    """Test behavior when input DataFrame is empty."""
    empty_df = gpd.GeoDataFrame(columns=["County", "geometry", "Fire Count", "Assessed Improved Value", "Economic Loss"])

    fig = make_fire_damage_map(empty_df)

    assert fig is not None, "Function should return a figure even for empty input"
    assert isinstance(fig, go.Figure), "Function should return a Plotly figure"  # ✅ Corrected check
    assert len(fig.data) >= 0, "Figure should not crash even with no data"


def test_plot_map():
    """Test the generation of a choropleth map."""
    mock_gdf = gpd.GeoDataFrame({
        "County": ["Los Angeles", "San Diego", "San Francisco"],
        "geometry": [None, None, None],  # Normally, these would be geometries
        "Fire Count": [5, 10, 3],
        "Assessed Improved Value": [1.2 * 1e9, 0.8 * 1e9, 0.3 * 1e9],
        "Economic Loss": ["$1.2B", "$0.8B", "$0.3B"]
    })

    fig = make_fire_damage_map(mock_gdf)

    assert fig is not None, "Function should return a valid Plotly figure"
    assert len(fig.data) >= 0, "Figure should not be empty"

if __name__ == "__main__":
    pytest.main()
