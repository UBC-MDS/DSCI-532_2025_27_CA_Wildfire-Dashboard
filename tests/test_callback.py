from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
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


# Test submit button
def test_update_charts():

    def run_callback(trigger):
        context_value.set(AttributeDict(**{"triggered_inputs": [trigger]}))
        return update_charts(1, 0)
    
    ctx = copy_context()
    trigger={"prop_id": "reset.n_clicks"}

    output = ctx.run(run_callback, trigger)

    assert output == (1,0)

# Test reset filter 

# Test county input

# Test year range input
# test incident name input