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

Author
------
[Your Name]

Date
----
[YYYY-MM-DD]
"""



from dash import Output, Input, callback, State, html
import dash_bootstrap_components as dbc
import pandas as pd

from .data import calfire_df
from .roof_chart import make_roof_chart
from .damage_chart import make_damage_chart
from .structure_chart import make_structure_chart
from .summary_chart import make_summary_chart
from .timeseries_chart import make_time_series_chart
from .create_map import make_fire_damage_map
from .components import main_font_size, main_font_color, theme_color

# Server side callbacks/reactivity
@callback(
    [Output('roof_chart', 'spec'),
     Output('damage_chart', 'spec'),
     Output('structure_chart', 'spec'),
     Output('summary_card', 'children'),
     Output('timeseries_chart', 'spec'),
     Output('fire_damage_map', 'figure'),
     Output('county', 'value'),
     Output('fire_damage_map', 'selectedData')],
    [Input('submit', 'n_clicks'),
     State('county', 'value'),
     State('year', 'value'),
     State('incident_name', 'value'),
     State('fire_damage_map', 'selectedData'),
    ],
    prevent_initial_call=True
)

def update_charts(n_clicks, county, year, incident_name, selectedData):

    filtered_df = calfire_df[(calfire_df["Incident Start Date"].dt.year.between(year[0], year[1]))]

    if selectedData:
        selected_counties = [point["hovertext"] for point in selectedData["points"]]
        county = selected_counties
        
    if county:
        filtered_df = filtered_df[filtered_df['County'].isin(list(county))]
    
    if incident_name:
        filtered_df = filtered_df[filtered_df['Incident Name'].isin(list(incident_name))]
         
    roof_chart = make_roof_chart(filtered_df)
    damage_chart = make_damage_chart(filtered_df)
    structure_chart = make_structure_chart(filtered_df)
    total_cost = make_summary_chart(filtered_df)  

    summary_card_update = [  
        dbc.CardHeader("Total Economic Loss",
                       style={"textAlign": "center",
                              "fontWeight": "bold",
                              "background-color": theme_color,
                                "fontSize": main_font_size,
                              'color':main_font_color}),
        dbc.CardBody(
            f'${total_cost:.2f} Billions USD' if total_cost else "No Data Available",
            style={"textAlign": "center", "fontSize": "21px"}
        )
    ]
    

    timeseries_chart = make_time_series_chart(filtered_df)
    fire_damage_map = make_fire_damage_map(filtered_df, selectedData)

    selectedData = None # to avoid overriding new changes in filter by existing selected counties in map


    return (
        roof_chart.to_dict(format="vega"),
        damage_chart.to_dict(format="vega"),
        structure_chart.to_dict(format="vega"),
        summary_card_update, 
        timeseries_chart.to_dict(format="vega"),
        fire_damage_map,
        county,
        selectedData
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