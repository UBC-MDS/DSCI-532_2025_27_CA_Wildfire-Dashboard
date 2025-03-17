import pandas as pd
import altair as alt
import pickle
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.damage_chart import make_damage_chart

with open('data/processed/processed_cal_fire.pkl', 'rb') as f:
    calfire_df = pickle.load(f)

expected_transformed_df = [{'name': 'source_0',
  'values': [{'Count': 45540,
    'Count_end': 45540.0,
    'Count_start': 0.0,
    'Damage Category': 'A. No Damage'},
   {'Count': 4732,
    'Count_end': 50272.0,
    'Count_start': 45540.0,
    'Damage Category': 'B. Affected (1-9%)'},
   {'Count': 1242,
    'Count_end': 51514.0,
    'Count_start': 50272.0,
    'Damage Category': 'C. Minor (10-25%)'},
   {'Count': 614,
    'Count_end': 52128.0,
    'Count_start': 51514.0,
    'Damage Category': 'D. Major (26-50%)'},
   {'Count': 66949,
    'Count_end': 119077.0,
    'Count_start': 52128.0,
    'Damage Category': 'E. Destroyed (>50%)'}]},
 {'name': 'source_0_color_domain_Damage Category',
  'values': [{'Damage Category': 'A. No Damage'},
   {'Damage Category': 'B. Affected (1-9%)'},
   {'Damage Category': 'C. Minor (10-25%)'},
   {'Damage Category': 'D. Major (26-50%)'},
   {'Damage Category': 'E. Destroyed (>50%)'}]}]


def test_damage_chart():
    output = make_damage_chart(calfire_df)
    output_data = output.to_dict(format="vega")

    # check that output is an altair chart
    assert isinstance(output, alt.Chart), "Output should be an altair chart" 

    # check that the output is a donut chart
    assert output_data['marks'][0]["type"] == 'arc', "Damage chart should be a donut chart"

    # Check that the data are transformed correctly
    assert output_data['data'] == expected_transformed_df, "Data not summarized correctly"