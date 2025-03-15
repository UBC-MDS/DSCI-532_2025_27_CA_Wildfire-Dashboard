import pytest
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from summary_chart import make_summary_chart  

# Test cases
test_cases = [
    (pd.DataFrame({"Assessed Improved Value": [50000000, 200000000, 150000000]}), 0.4, "Normal case with multiple values"),
    (pd.DataFrame(columns=["Assessed Improved Value"]), 0, "Empty DataFrame"),
    (pd.DataFrame({"Other Column": [100, 200, 300]}), 0, "Missing required column"),
    (pd.DataFrame({"Assessed Improved Value": [1000000000]}), 1.0, "Single value"),
    (pd.DataFrame({"Assessed Improved Value": [1e10, 2e10, 3e10]}), 60.0, "Large values"),
    (pd.DataFrame({"Assessed Improved Value": [-50000000, 200000000, -150000000]}), 0.0, "Negative values"),
    (pd.DataFrame({"Assessed Improved Value": [0, 0, 0]}), 0, "Zero values")
]

@pytest.mark.parametrize("input_df, expected, test_name", test_cases)
def test_make_summary_chart(input_df, expected, test_name):
    """Test make_summary_chart function with various scenarios."""
    result = make_summary_chart(input_df)
    assert result == expected, f"{test_name} failed: expected {expected}, got {result}"

if __name__ == "__main__":
    pytest.main()
