import pytest
import pandas as pd
import altair as alt
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.timeseries_chart import make_time_series_chart
@pytest.fixture

def sample_data():
    """Fixture to provide a sample wildfire dataset."""
    return pd.DataFrame({
        "Year": [2015, 2016, 2017, 2018, 2019, 2020],
        "County": ["Los Angeles", "San Diego", "Los Angeles", "San Diego", "San Francisco", "Los Angeles"],
        "Total Economic Loss": [100000000, 50000000, 75000000, 120000000, 95000000, 80000000]
    })

def test_make_time_series_chart(sample_data):
    """Test normal case with multiple counties."""
    result = make_time_series_chart(sample_data)
    assert isinstance(result, alt.Chart), "Function should return an Altair Chart"

def test_make_time_series_chart_large_values():
    """Test correct handling of large values in billions."""
    large_data = pd.DataFrame({
        "Year": [2015, 2016, 2017],
        "County": ["Los Angeles", "San Diego", "San Francisco"],
        "Total Economic Loss": [2e9, 1.5e9, 3.2e9]  # Values in billions
    })
    result = make_time_series_chart(large_data)
    chart_dict = result.to_dict(format="vega")
    assert isinstance(result, alt.Chart), "Function should return an Altair Chart"
    assert "data" in chart_dict, "Chart should contain a 'data' section"

def test_make_time_series_chart_with_selection(sample_data):
    """Test filtering multiple selected counties."""
    result = make_time_series_chart(sample_data, selected_counties=["Los Angeles", "San Francisco"])
    chart_dict = result.to_dict(format="vega")
    assert isinstance(result, alt.Chart), "Function should return an Altair Chart"
    assert "data" in chart_dict, "Chart should contain a data section"
    if isinstance(chart_dict["data"], list) and "values" in chart_dict["data"][0]:
        data_values = chart_dict["data"][0]["values"]
    else:
        pytest.fail(f"Unexpected data structure: {chart_dict}")
    counties_in_chart = set(entry["County"] for entry in data_values)
    assert counties_in_chart == {"Los Angeles", "San Francisco"}, f"Chart should only contain selected counties, but found: {counties_in_chart}"

    
if __name__ == "__main__":
    pytest.main()






