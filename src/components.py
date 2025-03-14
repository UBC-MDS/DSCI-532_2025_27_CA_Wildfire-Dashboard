"""
California Wildfire Dashboard Components

This module defines the layout components for the California Wildfire Dashboard using Dash and Dash Bootstrap Components. 
It includes global filters, interactive charts, and an information section to provide insights into wildfire incidents in California.

Global Variables
----------------
counties : list
    A sorted list of unique counties from the wildfire dataset.
min_year : int
    The earliest year in the wildfire dataset.
max_year : int
    The latest year in the wildfire dataset.
theme_color : str
    Primary theme color for dashboard styling.
main_font_size : str
    Default font size for text elements.
main_font_color : str
    Primary text color for labels and headings.

Components
----------
- **Global Filters**: Dropdowns and sliders for filtering wildfire data by county, year, and incident number.
- **Dashboard Charts**:
    - Map of wildfire damage by county.
    - Summary of total economic loss.
    - Damage category distribution.
    - Top 10 counties with maximum loss over time.
    - Structural damage by county.
    - Damage by roof type.
- **Info Section**: A collapsible section providing an overview of dashboard functionality.
- **Footer**: Contains contributor names, GitHub repository link, and last updated date.

Dependencies
------------
- dash
- dash_bootstrap_components
- dash_vega_components
- pandas

References
----------
GitHub Repository: https://github.com/UBC-MDS/DSCI-532_2025_27_CA_Wildfire-Dashboard

Last updated: March 5th, 2025
"""




import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Dash, dcc, html
import pickle

from .roof_chart import make_roof_chart
from .damage_chart import make_damage_chart
from .structure_chart import make_structure_chart
from .summary_chart import make_summary_chart
from .timeseries_chart import make_time_series_chart
from .create_map import make_fire_damage_map

from .data import calfire_df

# Declare global variables
theme_color = "#d1d6de"
main_font_size = "18px"
main_font_color= "black"

# Getting the global variables:
with open('data/processed/global_vars.pkl', 'rb') as f:
    counties, min_year, max_year, incidents = pickle.load(f)

# Components
# Top matter
info_button = dbc.Button(
    "Learn More!",
    id="info-button",
    outline=False,
    style={
        'width': '150px',
        'background-color': 'steelblue',
        "font-weight": "bold",
        'color': 'white'
    }
)

title = dbc.Row([
                dbc.Col([html.H1('California Wildfire Dashboard',
                 style={'color':main_font_color})]),
                dbc.Col(html.Div(info_button),
                        className="text-right",
                        width="auto",
                        style={'background-color':'transparent',
                               'padding-right': '24px',
                               'padding-top': '12px',
                               'padding-bottom': '12px'})
                ],
                style={'background-color': theme_color,
                       'padding': 10})
app_info = [
    html.Div(
        "Welcome to the California Wildfire Dashboard! A one-stop shop for gleaning insights from California Wildfires data.",
        style={'font-size': '16px',
            'max-width': '1500px'}
    ),
    html.Div(
        "Here you can explore the impact of wildfires across different counties in California for the past decade!",
        style={'font-size': '16px',
            'max-width': '1500px'}
    ),
    html.Div(
        "On the left, you can filter by specific or multiple counties and select a year range of interest. If you are curious about a specific fire, you can also filter by the name of the fire as well.",
        style={'font-size': '16px',
            'max-width': '1500px'}
    ),
    html.Div("On the right, you'll find a map of California. Hovering over a county will display a wildfire damage summary, selecting counties on the map will also filter for them.",
             style={'font-size': '16px',
            'max-width': '1500px'}),
    html.Div("Below the map, explore in detail the financial impact of wildfires on different counties, the extent of building damage, and the types of building materials affected.", style={'font-size': '16px',
            'max-width': '1500px'})   
]

info_section = dbc.Row(
    dbc.Collapse(
    app_info,
    id="info",
    style ={'background-color':theme_color,
    'padding-left': '30px',
    'padding-bottom': '12px',
    'color':main_font_color}
    ),
    style={"margin-top": "0px"})


# Global filters
global_widgets = dbc.Col(
            [
                
    html.Br(),
    html.Label("County", 
               style={'display': 'block','textAlign': 'center', 'fontWeight': 'bold'}),        
    dcc.Dropdown(id='county',
                 options = counties,
                 multi = True),

    html.Br(),
    html.Br(),
    html.Label("Incident Name",
                 style={'display': 'block','textAlign': 'center', 'fontWeight': 'bold'}),
    dcc.Dropdown(id="incident_name", options=incidents, value = 'id', multi= True),

    html.Br(),
    html.Br(),
    html.Label("Year",
                 style={'display': 'block','textAlign': 'center', 'fontWeight': 'bold'}),
    dcc.RangeSlider(id='year',
                    min=min_year,
                    max=max_year,
                    step=1,
                    value=[min_year, max_year],
                    marks={year: str(year) for year in range(min_year, max_year+1, 2)},
                    updatemode='mouseup'), # Using mouseup instead of drag to reduce update calls and improve performance
    html.Br(),
    dbc.Row(
        [dbc.Col(
            dbc.Button('Submit', id='submit'),
            width={'size':3, 'offset': 3}
            ),
        dbc.Col(
            dbc.Button('Reset All Filters', id='reset')
            )]
            ),
                ], 
            style={"background-color":theme_color,
                    "margin-left": "10px"},
                md=3)
 
# Dashboard charts
# Wilfire map
cali_map = dbc.Row(
                dbc.Card(
                    [dbc.CardHeader("California Wildfire Damage by County",
                                style={"textAlign": "center",
                                       "fontWeight": "bold",
                                        "fontSize": main_font_size,
                                        'background-color': theme_color,
                                        'color':main_font_color}),
                    dcc.Graph(id="fire_damage_map",
                              figure=make_fire_damage_map(calfire_df, None),
                              style={'width': '800px',
                                    "display": "flex",
                                    "justify-content": "center",
                                    "margin": "0 auto"})],
                style={'border':'none'}))

# total lost value 
summary_card = dbc.Row([
                dbc.Col(dbc.Card(
                [dbc.CardHeader("Total Economic Loss",
                                style={"textAlign": "center",
                                       "fontWeight": "bold",
                                       "background-color": theme_color,
                                        "fontSize": main_font_size,
                                        'color':main_font_color}),
                dbc.CardBody(f'${make_summary_chart(calfire_df):.2f} Billion USD',
                             style={"textAlign": "center",
                                    "fontSize": "21px"})],
                id='summary_card'),
                    width={"size": 3, "offset": 0}, 
                    style={"marginTop":"10px",
                           "position": "absolute",
                            "bottom": 0,
                            "left": 0,}
                        )
                    ],
                className="position-relative"   
            )

hover_info = dbc.Row(
                    [
                        html.P(
                            ["*Hover for details. Click county to select, hold ",
                              html.Code("Shift",
                                        style={"border": "1px solid #ccc"}),
                              " for multiple, click submit to apply filter*"],
                            style={"text-align": "center",
                                   "font-size": "16px",
                                   "position": "absolute",
                                    "bottom": 0,
                                    "right": 0},
                        )
                    ],
                    className="position-relative" 
                    )
            

# donut chart of count of damage level
damage_level=dbc.Col([
                    dbc.Card(
                        [dbc.CardHeader("Distribution of Damage Category",
                                        style={"textAlign": "center",
                                               "fontWeight": "bold",
                                               "background-color": theme_color,
                                               "fontSize": main_font_size,
                                               'color':main_font_color}),
                        dbc.CardBody(dcc.Loading(id="loading-damage-chart", children=[dvc.Vega(id='damage_chart', 
                      spec=make_damage_chart(calfire_df).to_dict(format="vega"))]),
                                     style={"height": "280px"})],
                        id="damage_card"
            )],
            md=6)

# time series of cost of incidents
timeseries_chart = dbc.Col([
                    dbc.Card(
                        [dbc.CardHeader("Counties with the Highest Economic Loss Over Time",
                                style={"textAlign": "center",
                                       "fontWeight": "bold",
                                       "background-color": theme_color,
                                        "fontSize": main_font_size,
                                        'color':main_font_color}),
                        dbc.CardBody(dcc.Loading(id="loading-timeseries-chart", children=[
                            dvc.Vega(id='timeseries_chart', spec=make_time_series_chart(calfire_df).to_dict(format="vega"))
                        ]),
                             style={"height": "280px"})]
                )],
                md=6)


# bar chart of damage by stucture category and county
structure_count=dbc.Col([
                    dbc.Card(
                        [dbc.CardHeader("Counties with the Most Damaged Structures by Category",
                                style={"textAlign": "center",
                                       "fontWeight": "bold",
                                       "background-color": theme_color,
                                        "fontSize": main_font_size,
                                        'color':main_font_color}),
                        dbc.CardBody(dcc.Loading(id="loading-structure-chart", children=[
                            dvc.Vega(id='structure_chart',
                         spec=make_structure_chart(calfire_df).to_dict(format="vega"))
                         ]),
                                    style={"height": "280px"})
                        ])],
                        md=6)



# house characteristic vs Damage level
roof_chart = dbc.Col([
                    dbc.Card(
                        [dbc.CardHeader("Houses Damaged by Roof Type",
                                        style={"textAlign": "center",
                                               "fontWeight": "bold",
                                               "background-color": theme_color,
                                               "fontSize": main_font_size,
                                               'color':main_font_color}),
                        dbc.CardBody(dcc.Loading(id="loading-roof-chart", children=[dvc.Vega(id='roof_chart', spec=make_roof_chart(calfire_df).to_dict(format="vega"))]),
                                     style={"height": "280px"})],
                                     id="roof_card"
                                     )],
                    md=6)

# Bottom matters
reference_info = dbc.Row(
    dbc.Col([
        html.Hr(),
        html.P("Developed by Gunisha Kaur, Thamer Aldawood, Elaine Chu and Forgive Agbesi."),
        html.P([
            "GitHub Repository: ",
            html.A("View on GitHub", href="https://github.com/UBC-MDS/DSCI-532_2025_27_CA_Wildfire-Dashboard", target="_blank")
        ]),
        html.P(f"Last updated: March 5th, 2025")
    ], style={"text-align": "center", "margin-top": "20px"}))

