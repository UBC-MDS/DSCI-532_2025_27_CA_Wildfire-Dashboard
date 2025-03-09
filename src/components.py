import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Dash, dcc, html

from .roof_chart import make_roof_chart
from .damage_chart import make_damage_chart
from .structure_chart import make_structure_chart
from .summary_chart import make_summary_chart
from .timeseries_chart import make_time_series_chart

from .data import calfire_df

# Declre global variables
counties = sorted(calfire_df["County"].dropna().unique())
min_year = calfire_df['Incident Start Date'].min().year
max_year = calfire_df['Incident Start Date'].max().year
theme_color = "#e88b10"
main_font_size = "18px"
main_font_color= "white"

# Components

title = [html.H1('California Wildfire Dashboard',
                 style={'color':main_font_color})]

global_widgets = [
    html.H4('Filters',
            style={"textAlign":"center"}),
    dcc.Markdown("**County**",
                 style={"textAlign":"center"}),
    dcc.Dropdown(id='county',
                 options = counties,
                 multi = True),

    dcc.Markdown("**Incident Number**",
                 style={"textAlign":"center"}),
    dcc.Dropdown(id="incident_number", options=sorted(calfire_df["Incident Number"].dropna().unique()), value = 'id', multi= True),
    dcc.Markdown("**Year**",
                 style={"textAlign":"center"}),
    dcc.RangeSlider(id='year',
                    min=min_year,
                    max=max_year,
                    step=1,
                    value=[min_year, max_year],
                    marks={year: str(year) for year in range(min_year, max_year+1, 2)},
                    updatemode='mouseup') # Using mouseup instead of drag to reduce update calls and improve performance
] 

cali_map = dcc.Graph(id="fire_damage_map")
summary_card = dbc.Card(
                [dbc.CardHeader("Total Economic Loss",
                                style={"textAlign": "center",
                                       "fontWeight": "bold",
                                       "background-color": theme_color,
                                        "fontSize": main_font_size,
                                        'color':main_font_color}),
                dbc.CardBody(f'${make_summary_chart(calfire_df):.2f} Billions USD',
                             style={"textAlign": "center",
                                    "fontSize": "21px"})],
                id='summary_card')
# total lost value 
damage_level=dvc.Vega(id='damage_chart', 
                      spec=make_damage_chart(calfire_df).to_dict(format="vega")) # donut chart of count of damage level
timeseries_chart = dvc.Vega(id='timeseries_chart', spec=make_time_series_chart(calfire_df).to_dict(format="vega"))# time series of cost of incidents
structure_count=dvc.Vega(id='structure_chart',
                         spec=make_structure_chart(calfire_df).to_dict(format="vega")) # bar chart of damage by stucture category and county
roof_chart = dvc.Vega(id='roof_chart', spec=make_roof_chart(calfire_df).to_dict(format="vega")) # house characteristic vs Damage level
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

app_info = [
    html.Div(
        "Welcome to the California Wildfire Dashboard! A one-stop shop for gleaning insights from California Wildfires data. Here you can explore the impact of wildfires across different counties in California for the past decade!", style={'font-size': '16px'}
    ),
    html.Div(
        "On the left, you can filter by specific or multiple counties and select a year range of interest. If you know the fire's incident ID, you can filter by that as well.", style={'font-size': '16px'}
    ),
    html.Div("On the right, you'll find a map of California. Hovering over a county will display a wildfire damage summary, selecting counties on the map will also filter for them.",
             style={'font-size': '16px'}),
    html.Div("Below the map, explore in detail the financial impact of wildfires on different counties, the extent of building damage, and the types of building materials affected.", style={'font-size': '16px'})   
]

info_section = dbc.Collapse(
        app_info,
        id="info",
        style ={'background-color':theme_color,
        'padding-left': '30px',
        'padding-bottom': '12px',
        'color':main_font_color}
)