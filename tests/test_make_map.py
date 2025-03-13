import pytest
import pandas as pd
import geopandas as gpd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.create_map import make_fire_damage_map, plot_map  

# Sample county boundary GeoDataFrame (mocked)
county_boundaries = gpd.GeoDataFrame({
    "CountyName": ["Los Angeles", "San Diego", "San Francisco"],
    "geometry": [None, None, None]  # Normally, these would be geometries
})

# Mock data for wildfires
sample_data = pd.DataFrame({
    "County": ["Los Angeles", "San Diego", "San Francisco", "Los Angeles"],
    "Damage": [1, 1, 1, 1],  # Counts how many fires occurred
    "Assessed Improved Value": [500000000, 200000000, 100000000, 700000000]  # In dollars
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
    fig = make_fire_damage_map(sample_data, mock_selected_data)

    # Validate output
    assert fig is not None, "Function should return a Plotly figure"
    assert len(fig.data) > 0, "Figure should contain data"
    
    # Restore global county_boundaries
    county_boundaries = county_boundaries_backup


def test_make_fire_damage_map_empty():
    """Test behavior when input DataFrame is empty."""
    empty_df = pd.DataFrame(columns=["County", "Damage", "Assessed Improved Value"])
    fig = make_fire_damage_map(empty_df, None)

    assert fig is not None, "Function should return a figure even for empty input"
    assert len(fig.data) == 1, "Figure should still be valid with no fire data"


def test_plot_map():
    """Test the generation of a choropleth map."""
    # Mock GeoDataFrame for plotting
    mock_gdf = gpd.GeoDataFrame({
        "CountyName": ["Los Angeles", "San Diego"],
        "geometry": [None, None],
        "Fire_Count": [5, 10],
        "Assessed_Value_B": ["$1.2B", "$0.8B"]
    })

    fig = plot_map(mock_gdf)

    assert fig is not None, "Function should return a valid Plotly figure"
    assert len(fig.data) > 0, "Figure should contain data"


def test_plot_map_with_selection():
    """Test highlighting selected counties in the choropleth map."""
    mock_gdf = gpd.GeoDataFrame({
        "CountyName": ["Los Angeles", "San Diego"],
        "geometry": [None, None],
        "Fire_Count": [5, 10],
        "Assessed_Value_B": ["$1.2B", "$0.8B"]
    })

    selected_data = {"points": [{"pointIndex": 1}]}

    fig = plot_map(mock_gdf, selected_data)

    assert fig is not None, "Function should return a valid Plotly figure"
    assert list(fig.data[0].selectedpoints) == [1], "Selection should be applied correctly"


if __name__ == "__main__":
    pytest.main()
