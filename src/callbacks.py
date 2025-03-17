"""
Dash Callbacks for Wildfire Data Visualization

This module contains server-side callbacks for updating various charts and 
visualizations in the California wildfire dashboard.

Functions
---------
update_charts(county, year, incident_number, selectedData)
    Filters the wildfire dataset based on user input and updates visualizations 
    such as roof type distribution, damage severity, structure counts, 
    economic loss summary, time series trends, and the interactive map.
    
toggle_button(n, is_open)
    Controls the visibility of the information modal when the info button is clicked.

Callbacks
---------
- Updates:
    - `roof_chart` (Vega visualization)
    - `damage_chart` (Vega visualization)
    - `structure_chart` (Vega visualization)
    - `summary_card` (Economic loss information)
    - `timeseries_chart` (Vega visualization)
    - `fire_damage_map` (Plotly map)
    - `county` (User-selected counties)
    - `fire_damage_map.selectedData` (Selection state reset)

Parameters
----------
county : list or None
    The selected counties for filtering the wildfire dataset.
year : list
    The range of years for filtering the dataset.
incident_number : list or None
    The selected incident numbers for filtering specific wildfire events.
selectedData : dict or None
    The selected data points from the map visualization.

Returns
-------
tuple
    A tuple containing updated versions of:
    - `roof_chart` (dict): Vega visualization of roof types.
    - `damage_chart` (dict): Vega visualization of damage severity.
    - `structure_chart` (dict): Vega visualization of affected structures.
    - `summary_card_update` (list): Dash component for displaying total economic loss.
    - `timeseries_chart` (dict): Vega visualization of time-series wildfire trends.
    - `fire_damage_map` (dict): Updated wildfire impact map.
    - `county` (list or None): Updated county selection.
    - `selectedData` (None): Reset selected data points.

Usage
-----
This script is part of a Dash app and should be run within a Dash context.

Example:
    >>> from callbacks import update_charts, toggle_button
    >>> update_charts(["Los Angeles"], [2015, 2020], None, None)
"""

from dash import Output, Input, callback, State, html, ctx, no_update
import dash_bootstrap_components as dbc
import pandas as pd

from .data import calfire_df, county_boundaries
from .roof_chart import make_roof_chart
from .damage_chart import make_damage_chart
from .structure_chart import make_structure_chart
from .summary_chart import make_summary_chart
from .timeseries_chart import make_time_series_chart
from .create_map import make_fire_damage_map
from .components import main_font_size, main_font_color, theme_color, min_year, max_year

import pickle
from flask_caching import Cache
from flask import Flask

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Cache original dataframe
@cache.memoize()
def load_data():
    with open('data/processed/processed_cal_fire.pkl', 'rb') as f:
        return pickle.load(f)
    
calfire_df = load_data()

@callback(
    [Output('county', 'value'),
     Output('year', 'value'),
     Output('incident_name', 'value')],
    [Input('submit', 'n_clicks'),
     Input('reset', 'n_clicks')],
    [State('county', 'value'),
     State('year', 'value'),
     State('incident_name', 'value'),
     State('fire_damage_map', 'selectedData')],
    prevent_initial_call=True
)
def update_filters(n_clicks_s, n_clicks_r, county, year, incident_name, selectedData):
    min_year, max_year = calfire_df['Year'].min(), calfire_df['Year'].max()
    # Reset filters
    if 'reset' == ctx.triggered_id:
        return None, [min_year, max_year], None

    # Update filters based on map selection
    if selectedData:
        selected_counties = [point["hovertext"] for point in selectedData["points"]]
        county = list(set(selected_counties + (county or [])))

    return county, year, incident_name

# Server side callbacks/reactivity
@callback(
    [Output('roof_chart', 'spec'),
     Output('damage_chart', 'spec'),
     Output('structure_chart', 'spec'),
     Output('timeseries_chart', 'spec')],
    [Input('submit', 'n_clicks')],
    [State('county', 'value'),
     State('year', 'value'),
     State('incident_name', 'value')],
    prevent_initial_call=True
)
def update_charts(n_clicks, county, year, incident_name):
    filtered_df = calfire_df.copy()

    # Filter data based on the selected year range
    if year:
        filtered_df = filtered_df[filtered_df["Year"].between(year[0], year[1])]

    # Filter data based on selected counties and incident names
    if county:
        filtered_df = filtered_df[filtered_df['County'].isin(list(county))]
    if incident_name:
        filtered_df = filtered_df[filtered_df['Incident Name'].isin(list(incident_name))]

    # Generate charts
    roof_chart = make_roof_chart(filtered_df).to_dict(format="vega")
    damage_chart = make_damage_chart(filtered_df).to_dict(format="vega")
    structure_chart = make_structure_chart(filtered_df).to_dict(format="vega")
    timeseries_chart = make_time_series_chart(filtered_df).to_dict(format="vega")

    return roof_chart, damage_chart, structure_chart, timeseries_chart

@callback(
    Output('summary_card', 'children'),
    [Input('submit', 'n_clicks')],
    [State('county', 'value'),
     State('year', 'value'),
     State('incident_name', 'value')],
    prevent_initial_call=True
)
def update_summary(n_clicks, county, year, incident_name):
    filtered_df = calfire_df.copy()

    # Filter data
    if year:
        filtered_df = filtered_df[filtered_df["Year"].between(year[0], year[1])]
    if county:
        filtered_df = filtered_df[filtered_df['County'].isin(list(county))]
    if incident_name:
        filtered_df = filtered_df[filtered_df['Incident Name'].isin(list(incident_name))]

    # Calculate total cost
    total_cost = make_summary_chart(filtered_df)

    summary_card_update = [
        dbc.CardHeader(
            "Total Economic Loss",
            style={
                "textAlign": "center",
                "fontWeight": "bold",
                "background-color": theme_color,
                "fontSize": main_font_size,
                "color": main_font_color,
            },
        ),
        dbc.CardBody(
            f'{total_cost} USD' if total_cost else "No Data Available",
            style={"textAlign": "center", "fontSize": "21px"},
        ),
    ]
    return summary_card_update

@callback(
    Output("info", "is_open"),
    [Input("info-button", "n_clicks")],
    [State("info", "is_open")],  
)
def toggle_button(n, is_open):
    print(n)  
    print(is_open)  
    if n:
        return not is_open
    return is_open


