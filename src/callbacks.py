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
import dask.dataframe as dd

from .data import calfire_df, county_boundaries
from .roof_chart import make_roof_chart
from .damage_chart import make_damage_chart
from .structure_chart import make_structure_chart
from .summary_chart import make_summary_chart
from .timeseries_chart import make_time_series_chart
from .create_map import make_fire_damage_map
from .components import main_font_size, main_font_color, theme_color, min_year, max_year

first_run_complete = False

# Server side callbacks/reactivity
@callback(
    [Output('roof_chart', 'spec'),
     Output('damage_chart', 'spec'),
     Output('structure_chart', 'spec'),
     Output('summary_card', 'children'),
     Output('timeseries_chart', 'spec'),
     Output('county', 'value'),
     Output('year', 'value'),
     Output('incident_name', 'value'),
    ],
    [Input('submit', 'n_clicks'),
     Input('reset', 'n_clicks'),
     State('county', 'value'),
     State('year', 'value'),
     State('incident_name', 'value'),
     State('fire_damage_map', 'selectedData'),
    ],
    # prevent_initial_call=True
)

def update_charts(n_clicks_s, n_clicks_r, county, year, incident_name, selectedData):
    global first_run_complete

    calfire_df = dd.read_parquet('data/processed/processed_cal_fire.parquet')

    # Reset filters 
    if 'reset' == ctx.triggered_id:
        county, year, incident_name, selectedData = None, [min_year, max_year], None, None

    else:
        calfire_df = calfire_df[(calfire_df["Incident Start Date"].dt.year.between(year[0], year[1]))]

        if selectedData:
            selected_counties = [point["hovertext"] for point in selectedData["points"]]
            county = list(set(selected_counties + county)) if county else selected_counties
            
        if county:
            calfire_df = calfire_df[calfire_df['County'].isin(list(county))]
        
        if incident_name:
            calfire_df = calfire_df[calfire_df['Incident Name'].isin(list(incident_name))]

    # Compute the filtered Dask DataFrame on the first run. It is lazy.
    if not first_run_complete:
        calfire_df = calfire_df.compute()
        first_run_complete = True

    roof_chart = make_roof_chart(calfire_df)
    damage_chart = make_damage_chart(calfire_df)
    structure_chart = make_structure_chart(calfire_df)
    total_cost = make_summary_chart(calfire_df)  

    # selectedData = None # To avoid filter being constantly overridden by map selection. Downside is map selection does not persist after filtering.

    summary_card_update = [  
        dbc.CardHeader("Total Economic Loss",
                       style={"textAlign": "center",
                              "fontWeight": "bold",
                              "background-color": theme_color,
                                "fontSize": main_font_size,
                              'color':main_font_color}),
        dbc.CardBody(
            f'{total_cost} USD' if total_cost else "No Data Available",
            style={"textAlign": "center", "fontSize": "21px"}
        )
    ]
    

    timeseries_chart = make_time_series_chart(calfire_df)
    # fire_damage_map = make_fire_damage_map(county_boundaries, selectedData)

    return (
        roof_chart.to_dict(format="vega"),
        damage_chart.to_dict(format="vega"),
        structure_chart.to_dict(format="vega"),
        summary_card_update, 
        timeseries_chart.to_dict(format="vega"),
        county,
        year,
        incident_name,
    )

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