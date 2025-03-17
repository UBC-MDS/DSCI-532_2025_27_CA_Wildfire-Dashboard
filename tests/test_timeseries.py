import pytest
import pandas as pd
import altair as alt
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from timeseries_chart import make_time_series_chart


# Sample wildfire dataset
sample_data = pd.DataFrame({
    "Year": pd.to_datetime(["2015", "2016", "2017", "2018"]),
    "County": ["Los Angeles", "San Diego", "Los Angeles", "San Francisco"],
    "Total Economic Loss": [100000000, 50000000, 75000000, 20000000]
})


def test_make_time_series_chart():
    """Test normal case with multiple counties."""
    result = make_time_series_chart(sample_data)
    chart_dict = result.to_dict()

   
    if "datasets" in chart_dict:
        dataset_keys = list(chart_dict["datasets"].keys())
        assert len(chart_dict["datasets"][dataset_keys[0]]) > 0, "Chart should contain data points"
    else:
        pytest.fail("Chart data structure is different than expected: " + str(chart_dict))


def test_make_time_series_chart_empty():
    """Test behavior when input DataFrame is empty."""
    empty_df = pd.DataFrame(columns=["Incident Start Date", "County", "Assessed Improved Value"])
    result = make_time_series_chart(empty_df)

    assert result == {}, "Function should return an empty dictionary for empty input"


def test_make_time_series_chart_single_county():
    """Test filtering with a single county."""
    result = make_time_series_chart(sample_data, selected_counties=["Los Angeles"])
    chart_dict = result.to_dict()


    if "datasets" in chart_dict:
        dataset_keys = list(chart_dict["datasets"].keys())
        chart_data = chart_dict["datasets"][dataset_keys[0]]
        counties_in_chart = set(entry["County"] for entry in chart_data)
        assert counties_in_chart == {"Los Angeles"}, "Only selected county should be in the chart"
    else:
        pytest.fail("Chart data structure is different than expected: " + str(chart_dict))


def test_make_time_series_chart_large_values():
    """Test correct handling of large values (billions)."""
    large_data = pd.DataFrame({
        "Year": pd.to_datetime(["2015", "2016", "2017"]),
        "County": ["Los Angeles", "San Diego", "San Francisco"],
        "Total Economic Loss": [2e9, 1.5e9, 3.2e9]  # Values in billions
    })

    result = make_time_series_chart(large_data)
    chart_dict = result.to_dict()

    assert isinstance(result, alt.Chart), "Function should return an Altair Chart"
    assert "Billions of USD" in chart_dict["encoding"]["y"]["title"], "Y-axis should be in billions format"


def test_make_time_series_chart_with_selection():
    """Test filtering multiple selected counties."""
    result = make_time_series_chart(sample_data, selected_counties=["Los Angeles", "San Francisco"])
    chart_dict = result.to_dict()

    if "datasets" in chart_dict:
        dataset_keys = list(chart_dict["datasets"].keys())
        chart_data = chart_dict["datasets"][dataset_keys[0]]
        counties_in_chart = set(entry["County"] for entry in chart_data)
        assert counties_in_chart == {"Los Angeles", "San Francisco"}, "Chart should only contain selected counties"
    else:
        pytest.fail("Chart data structure is different than expected: " + str(chart_dict))


if __name__ == "__main__":
    pytest.main()
