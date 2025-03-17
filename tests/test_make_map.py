import pytest
import pandas as pd
import geopandas as gpd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.create_map import make_fire_damage_map  

# Sample county boundary GeoDataFrame (mocked)
county_boundaries = gpd.GeoDataFrame({
    "County": ["Los Angeles", "San Diego", "San Francisco"],
    "geometry": [None, None, None],  # Normally, these would be geometries
    "Fire Count": [5, 10, 3],
    "Assessed Improved Value": [1.2 * 1e9, 0.8 * 1e9, 0.3 * 1e9],
    "Economic Loss": ["$1.2B", "$0.8B", "$0.3B"]
})

# Mock selected data for interactivity
mock_selected_data = {"points": [{"pointIndex": 0}, {"pointIndex": 2}]}


def test_make_fire_damage_map():
    """Test the aggregation and merging of wildfire data with county boundaries."""
    # Patch the county_boundaries within the function
    global county_boundaries
    county_boundaries_backup = county_boundaries
    county_boundaries = county_boundaries  # Use mock boundaries

    # Run function
    fig = make_fire_damage_map(county_boundaries)

    # Validate output
    assert fig is not None, "Function should return a Plotly figure"
    assert len(fig.data) > 0, "Figure should contain data"
    
    # Restore global county_boundaries
    county_boundaries = county_boundaries_backup


def test_make_fire_damage_map_empty():
    """Test behavior when input DataFrame is empty."""
    empty_df = pd.DataFrame(columns=["County", "geometry", "Fire Count", "Assessed Improved Value", "Economic Loss"])
    fig = make_fire_damage_map(empty_df)

    assert fig is not None, "Function should return a figure even for empty input"


def test_plot_map():
    """Test the generation of a choropleth map."""
    # Mock GeoDataFrame for plotting
    mock_gdf = gpd.GeoDataFrame({
    "County": ["Los Angeles", "San Diego", "San Francisco"],
    "geometry": [None, None, None],  # Normally, these would be geometries
    "Fire Count": [5, 10, 3],
    "Assessed Improved Value": [1.2 * 1e9, 0.8 * 1e9, 0.3 * 1e9],
    "Economic Loss": ["$1.2B", "$0.8B", "$0.3B"]
    })

    fig = make_fire_damage_map(mock_gdf)

    assert fig is not None, "Function should return a valid Plotly figure"
    assert len(fig.data) > 0, "Figure should contain data"

if __name__ == "__main__":
    pytest.main()
