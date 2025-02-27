from dash import Dash, dcc, callback, Output, Input, html
import altair as alt
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import plotly.express as px
from data_import import load_calfire_df
from roof_chart import make_roof_chart


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Load wildfire data
calfire_df = load_calfire_df()
counties = sorted(calfire_df["County"].dropna().unique())

# Components
title = [html.H1('California Wildfire Dashboard'),
         html.H6('A one-stop shop for gleaning insights from California Wildfires data')]
global_widgets = [
    dbc.Label("County"),
    dcc.Dropdown(id='county',
                 options = counties,
                 multi = True),

    dbc.Label("Incident Number"),
    dcc.Dropdown(id="Incident Number", options=sorted(calfire_df["Incident Number"].dropna().unique()), value = 'id'),
    dbc.Label("Year"),
    dcc.RangeSlider(id='year',
                    min=2013,
                    max=2025,
                    value=[2013, 2025],
                    marks={year: str(year) for year in range(2013, 2026, 2)},
                    updatemode='drag')
] # inputs
cali_map = [html.H3('California map')] # map of california with
sum_cost=[html.H3('summary cost')]# total lost value 
damage_level=[html.H3('damage level')]# pie chart of count of damage level
time_cost=[html.H3('time series of cost')]# time series of cost of incidents
structure_count=[html.H3('bar chart structure count')]# bar chart of damage by stucture category and county
house_damage =[html.H3('house characteristic vs damage')]# house characteristic vs Damage level

roof_chart = dvc.Vega(id='roof_chart', spec=make_roof_chart(calfire_df).to_dict(format="vega"))

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        dbc.Col(global_widgets, md=3),
        dbc.Col(cali_map),
        dbc.Col([
            dbc.Row(sum_cost),
            dbc.Row(damage_level)
        ],
        md=3)
    ]),
    dbc.Row([
        dbc.Col(roof_chart),
        dbc.Col(time_cost),
        dbc.Col(structure_count)
    ])
])

# Server side callbacks/reactivity
@callback(
    Output('roof_chart', 'spec'),
    Input('county', 'value')
)
def create_roof_chart(county):
    if not county:  # If no county is selected, use all counties
        filtered_df = calfire_df
    else:
        filtered_df = calfire_df[calfire_df['County'].isin(county)]
    roof_chart = make_roof_chart(filtered_df)
    return roof_chart.to_dict(format="vega")

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)
