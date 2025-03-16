import pandas as pd
import altair as alt
import pickle
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.structure_chart import make_structure_chart

with open('data/processed/processed_cal_fire.pkl', 'rb') as f:
    calfire_df = pickle.load(f)
expected_categories = {
    'name': 'data_0_color_domain_Structure Category',
    'values': [{'Structure Category': 'A. Single Residence'},
    {'Structure Category': 'B. Multiple Residence'},
    {'Structure Category': 'C. Mixed Commercial/Residential'},
    {'Structure Category': 'D. Nonresidential Commercial'},
    {'Structure Category': 'E. Infrastructure'},
    {'Structure Category': 'F. Agriculture'},
    {'Structure Category': 'G. Other Minor Structure'}]}

def test_structure_chart():
    output = make_structure_chart(calfire_df)
    output_data = output.to_dict(format="vega")

    # check that output is an altair chart
    assert isinstance(output, alt.Chart), "Output should be an altair chart" 

    # check that the output is a donut chart
    assert output_data['marks'][0]["type"] == 'rect', "Damage chart should be a bar chart"

    # Check that the data are transformed correctly
    assert output_data['data'][3] == expected_categories, "Data not grouped correctly"