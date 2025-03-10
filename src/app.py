from dash import Dash, html
import dash_bootstrap_components as dbc
import sys
import os

# Enables importing from src
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from src import callbacks
from src.components import title, global_widgets, cali_map, summary_card, damage_level, timeseries_chart, structure_count, roof_chart, info_section, reference_info, hover_info

# Initiatlize the app
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Layout
app.layout = dbc.Container([
    title, 
    info_section, 
     dbc.Row([
        global_widgets, 
        dbc.Col(
            [cali_map, 
            summary_card, 
            hover_info, 
            dbc.Row([
                roof_chart,
                damage_level],
            style={"marginTop": "20px"}),
            dbc.Row([
                structure_count,
                timeseries_chart],
            style={"marginTop": "20px"})])
            ]),
    reference_info],
    fluid=True,
    style={'margin': 0,
           'padding': 0,
           'overflow-x': 'hidden'}
    )
      


# Run the app/dashboard
if __name__ == '__main__':
    app.server.run(debug=True)
