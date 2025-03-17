import pytest
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.summary_chart import make_summary_chart  

# Test cases
test_cases = [
    (pd.DataFrame({"Total Economic Loss": [50000000, 200000000, 150000000]}), "$400.00M", "Normal case with multiple values"),
    (pd.DataFrame(columns=["Total Economic Loss"]), 0, "Empty DataFrame"),
    (pd.DataFrame({"Other Column": [100, 200, 300]}), 0, "Missing required column"),
    (pd.DataFrame({"Total Economic Loss": [1000000000]}), "$1.00B", "Single value"),
    (pd.DataFrame({"Total Economic Loss": [1e10, 2e10, 3e10]}), "$60.00B", "Large values"),
    (pd.DataFrame({"Total Economic Loss": [-50000000, 200000000, -150000000]}), "$0.00M", "Negative values"),
    (pd.DataFrame({"Total Economic Loss": [0, 0, 0]}), "$0.00M", "Zero values")
]

@pytest.mark.parametrize("input_df, expected, test_name", test_cases)
def test_make_summary_chart(input_df, expected, test_name):
    """Test make_summary_chart function with various scenarios."""
    result = make_summary_chart(input_df)
    assert result == expected, f"{test_name} failed: expected {expected}, got {result}"

if __name__ == "__main__":
    pytest.main()
