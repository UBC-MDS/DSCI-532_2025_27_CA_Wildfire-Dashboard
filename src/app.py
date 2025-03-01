from dash import Dash, dcc, callback, Output, Input, html
import altair as alt
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import geopandas as gpd
import plotly.express as px
from data_import import load_calfire_df
from roof_chart import make_roof_chart
from damage_chart import make_damage_chart
from structure_chart import make_structure_chart
from summary_chart import make_summary_chart
from timeseries_chart import make_time_series_chart


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Load wildfire data
calfire_df = pd.read_csv("data/processed/cleaned_cal_fire.csv")
counties = sorted(calfire_df["County"].dropna().unique())
calfire_df["Incident Start Date"] = pd.to_datetime(calfire_df["Incident Start Date"], format="mixed")
min_year = calfire_df['Incident Start Date'].min().year
max_year = calfire_df['Incident Start Date'].max().year


# Load geojson data on county boundaries
geojson_file_path = 'data/raw/California_County_Boundaries.geojson'
county_boundaries = gpd.read_file(geojson_file_path)

# Components
title = [html.H1('California Wildfire Dashboard'),
         html.H6('A one-stop shop for gleaning insights from California Wildfires data')]
global_widgets = [
    dbc.Label("County"),
    dcc.Dropdown(id='county',
                 options = counties,
                 multi = True),

    dbc.Label("Incident Number"),
    dcc.Dropdown(id="incident_number", options=sorted(calfire_df["Incident Number"].dropna().unique()), value = 'id', multi= True),
    dbc.Label("Year"),
    dcc.RangeSlider(id='year',
                    min=min_year,
                    max=max_year,
                    value=[2013, 2025],
                    marks={year: str(year) for year in range(min_year, max_year+2, 2)},
                    updatemode='drag')
] # inputs
cali_map = [html.H3('California map')] # map of california with
summary_chart = dvc.Vega(id='summary_chart', spec=make_summary_chart(calfire_df).to_dict(format="vega"))
# total lost value 
damage_level=dvc.Vega(id='damage_chart', 
                      spec=make_damage_chart(calfire_df).to_dict(format="vega")) # donut chart of count of damage level
timeseries_chart = dvc.Vega(id='timeseries_chart', spec=make_time_series_chart(calfire_df).to_dict(format="vega"))# time series of cost of incidents
structure_count=dvc.Vega(id='structure_chart',
                         spec=make_structure_chart(calfire_df).to_dict(format="vega")) # bar chart of damage by stucture category and county
house_damage =[html.H3('house characteristic vs damage')]# house characteristic vs Damage level

roof_chart = dvc.Vega(id='roof_chart', spec=make_roof_chart(calfire_df).to_dict(format="vega"))

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        dbc.Col(global_widgets, md=3),
        dbc.Col(cali_map, md=6),
        dbc.Col([
         dbc.Row(
                dbc.Col(html.Div(summary_chart, style={"text-align": "center", "margin-bottom": "5px"}))  # Moves Up
            ),
            dbc.Row(
                dbc.Col(damage_level, style={"text-align": "center", "margin-top": "-30px"})  # Moves Up
            )
        ], md=3)
    ]),
  dbc.Row([
        dbc.Col(roof_chart),
        dbc.Col(timeseries_chart),
        dbc.Col(structure_count)
    ])
])

# Server side callbacks/reactivity
@callback(
    [Output('roof_chart', 'spec'),
     Output('damage_chart', 'spec'),
     Output('structure_chart', 'spec'),
     Output('summary_chart', 'spec'),
     Output('timeseries_chart', 'spec')],
    [Input('county', 'value'),
    Input('year', 'value'),
    Input('incident_number', 'value')]
)
def update_charts(county, year, incident_number):
    filtered_df = calfire_df[(calfire_df["Incident Start Date"].dt.year
                                  .between(year[0], year[1]))]

    if county:
        filtered_df = filtered_df[filtered_df['County'].isin(county)]
    
    if incident_number:
        filtered_df = filtered_df[filtered_df['Incident Number'].isin(incident_number)]

    roof_chart = make_roof_chart(filtered_df)
    damage_chart = make_damage_chart(filtered_df)
    structure_chart = make_structure_chart(filtered_df)
    summary_chart = make_summary_chart(filtered_df)
    timeseries_chart = make_time_series_chart(filtered_df)
    return roof_chart.to_dict(format="vega"), damage_chart.to_dict(format="vega"), structure_chart.to_dict(format="vega"), summary_chart.to_dict(format="vega"), timeseries_chart.to_dict(format="vega")

# Run the app/dashboard
if __name__ == '__main__':
    app.server.run(debug=True)
