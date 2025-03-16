from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash import callback_context
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.callbacks import update_charts, toggle_button

def test_toggle_button():
    output = toggle_button(1, False)
    assert output is True

    output = toggle_button(1, True)
    assert output is False
    
    output = toggle_button(0, False)
    assert output is False


# Test reset button
def test_reset_button():

    def run_callback(trigger):
        context_value.set(AttributeDict(**{"triggered_inputs": [trigger]}))
        return update_charts(0, 1, None, ["Butte"], [2017, 2020], None)
    
    ctx = copy_context()
    trigger={"prop_id": "reset.n_clicks"}

    output = ctx.run(run_callback, trigger)

    (roof_chart, damage_chart, structure_chart, summary_card_update, 
     timeseries_chart, county, year, incident_name) = output
    
    assert isinstance(roof_chart, dict), "Returned roof chart should be a dicionary"
    assert isinstance(damage_chart, dict), "Returned damage chart should be a dictionary"
    assert isinstance(structure_chart, dict), "Returned structure chart should be a dictionary"
    assert isinstance(timeseries_chart, dict), "Returned timeseries chart should be a dictionary"
    assert isinstance(summary_card_update, list), "Returned summary card should be a dictionary"
    assert county is None, "County input should be cleared"
    assert year == [2014, 2025], "Year input should reset to min and max years"
    assert incident_name is None, "Incident name should be cleared"

# Test year imput
def test_submit_button():

    def run_callback(trigger):
        context_value.set(AttributeDict(**{"triggered_inputs": [trigger]}))
        return update_charts(1, 0, None, [2017, 2020], None, None)
    
    ctx = copy_context()
    trigger={"prop_id": "submit.n_clicks"}

    output = ctx.run(run_callback, trigger)


    (roof_chart, damage_chart, structure_chart, summary_card_update, 
     timeseries_chart, county, year, incident_name) = output
    print(county),
    print(incident_name)
    print(year)
    assert isinstance(roof_chart, dict), "Returned roof chart should be a dicionary"
    assert isinstance(damage_chart, dict), "Returned damage chart should be a dictionary"
    assert isinstance(structure_chart, dict), "Returned structure chart should be a dictionary"
    assert isinstance(timeseries_chart, dict), "Returned timeseries chart should be a dictionary"
    assert isinstance(summary_card_update, list), "Returned summary card should be a dictionary"
    assert county is None
    assert year == [2017, 2020], "Returned year should be the same as input"
    assert incident_name is None 

# Test county input
def test_county_input():

    def run_callback(trigger):
        context_value.set(AttributeDict(**{"triggered_inputs": [trigger]}))
        return update_charts(1, 0, ["Butte"], [2017, 2020], None, None)
    
    ctx = copy_context()
    trigger={"prop_id": "submit.n_clicks"}

    output = ctx.run(run_callback, trigger)


    (roof_chart, damage_chart, structure_chart, summary_card_update, 
     timeseries_chart, county, year, incident_name) = output
    print(county),
    print(incident_name)
    print(year)
    assert isinstance(roof_chart, dict), "Returned roof chart should be a dicionary"
    assert isinstance(damage_chart, dict), "Returned damage chart should be a dictionary"
    assert isinstance(structure_chart, dict), "Returned structure chart should be a dictionary"
    assert isinstance(timeseries_chart, dict), "Returned timeseries chart should be a dictionary"
    assert isinstance(summary_card_update, list), "Returned summary card should be a dictionary"
    assert county == ["Butte"], "Returned County should be same as input"
    assert year == [2017, 2020], "Returned year should be the same as input"
    assert incident_name is None, "Returned incident should be none" 