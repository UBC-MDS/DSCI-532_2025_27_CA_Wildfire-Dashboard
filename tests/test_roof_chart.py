import unittest
import pandas as pd
import altair as alt
from src.roof_chart import make_roof_chart
import pickle
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

with open('data/processed/processed_cal_fire.pkl', 'rb') as f:
    calfire_df = pickle.load(f)

def test_roof_chart():

    output = make_roof_chart(calfire_df)
    output_data = output.to_dict(format="vega")

    # check that output is an altair chart
    assert isinstance(output, alt.Chart), "Output should be an altair chart" 

    # check that the output is a donut chart
    assert output_data['marks'][0]["type"] == 'rect', "Damage chart should be a bar chart"

    # Check that the counts are correct
    assert output['data']["Count"][2] == 466, "Data not counted correctly"


if __name__ == '__main__':
    unittest.main()