from dash import Dash, dcc, callback, Output, Input, html, State
import altair as alt
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import geopandas as gpd
import plotly.express as px
try:
    from roof_chart import make_roof_chart
    from damage_chart import make_damage_chart
    from structure_chart import make_structure_chart
    from summary_chart import make_summary_chart
    from timeseries_chart import make_time_series_chart
    from create_map import make_fire_damage_map
except ModuleNotFoundError:
    from src.roof_chart import make_roof_chart
    from src.damage_chart import make_damage_chart
    from src.structure_chart import make_structure_chart
    from src.summary_chart import make_summary_chart
    from src.timeseries_chart import make_time_series_chart
    from src.create_map import make_fire_damage_map

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Load wildfire data
calfire_df = pd.read_csv("data/processed/cleaned_cal_fire.csv")
counties = sorted(calfire_df["County"].dropna().unique())
calfire_df["Incident Start Date"] = pd.to_datetime(calfire_df["Incident Start Date"], format="%m/%d/%Y %I:%M:%S %p")
min_year = calfire_df['Incident Start Date'].min().year
max_year = calfire_df['Incident Start Date'].max().year
theme_color = "#e88b10"
main_font_size = "18px"
main_font_color= "white"

# Filters
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



# Components
cali_map = dcc.Graph(id="fire_damage_map")#,spec= make_fire_damage_map(calfire_df)) # map of california with
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
    html.Div("On the right, you'll find a map of California. Hovering over a county will display a wildfire damage summary, and you can also use the map to select counties of interest.",
             style={'font-size': '16px'}),
    html.Div("Below the map, you can explore the different charts that contains information on the financial loss and the degree of damage based on the structure types", style={'font-size': '16px'})   
]

info_section = dbc.Collapse(
        app_info,
        id="info",
        style ={'background-color':theme_color,
        'padding-left': '30px',
        'padding-bottom': '12px',
        'color':main_font_color}
)

# Layout
app.layout = dbc.Container([
    dbc.Row([
                dbc.Col(title),
                dbc.Col(html.Div(info_button),
                        className="text-right",
                        width="auto",
                        style={'background-color':'transparent',
                               'padding-right': '24px',
                               'padding-top': '12px',
                               'padding-bottom': '12px'})
                ],
                style={'background-color': theme_color,
                       'padding': 10}),

    dbc.Row(info_section,
            style={"margin-top": "0px"}),

     dbc.Row([
        dbc.Col(
            global_widgets, 
            style={"background-color":"lightgrey",
                    "padding": "10px"},
                md=3),
        dbc.Col(
            [dbc.Row(
                dbc.Card(
                    [dbc.CardHeader("California Wildfire Damage by County",
                                style={"textAlign": "center",
                                       "fontWeight": "bold",
                                        "fontSize": main_font_size,
                                        # 'border':'none',
                                        'background-color': theme_color,
                                        'color':main_font_color}),
                    dcc.Loading(id="loading-cali-map", children=[cali_map])],
                style={'border':'none'})),
            dbc.Row([
                dbc.Col(summary_card,
                    width={"size": 3, "offset": 0}, 
                    style={"marginTop":"10px",
                           "position": "absolute",
                            "bottom": 0,
                            "left": 0,}
                        )
                    ],
                className="position-relative"   
            ),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        [dbc.CardHeader("House Damaged by Roof Type",
                                        style={"textAlign": "center",
                                               "fontWeight": "bold",
                                               "background-color": theme_color,
                                               "fontSize": main_font_size,
                                               'color':main_font_color}),
                        dbc.CardBody(dcc.Loading(id="loading-roof-chart", children=[roof_chart]),
                                     style={"height": "280px"})],
                                     id="roof_card"
                                     )],
                    md=6),
                dbc.Col([
                    dbc.Card(
                        [dbc.CardHeader("Distribution of Damage Category",
                                        style={"textAlign": "center",
                                               "fontWeight": "bold",
                                               "background-color": theme_color,
                                               "fontSize": main_font_size,
                                               'color':main_font_color}),
                        dbc.CardBody(dcc.Loading(id="loading-damage-chart", children=[damage_level]),
                                     style={"height": "280px"})],
                        id="damage_card"
            )])],
            style={"marginTop": "20px"}),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        [dbc.CardHeader("Top 10 Counties with Most Structures Damaged",
                                style={"textAlign": "center",
                                       "fontWeight": "bold",
                                       "background-color": theme_color,
                                        "fontSize": main_font_size,
                                        'color':main_font_color}),
                        dbc.CardBody(dcc.Loading(id="loading-structure-chart", children=[structure_count]),
                                    style={"height": "280px"})
                        ]
                        )
                        ]),
                dbc.Col([
                    dbc.Card(
                        [dbc.CardHeader("Top 10 Counties with Maximum Economic Loss Over Time",
                                style={"textAlign": "center",
                                       "fontWeight": "bold",
                                       "background-color": theme_color,
                                        "fontSize": main_font_size,
                                        'color':main_font_color}),
                        dbc.CardBody(dcc.Loading(id="loading-timeseries-chart", children=[timeseries_chart]),
                             style={"height": "280px"})]
                )])],
            style={"marginTop": "20px"})])
            ]),
    dbc.Row(
    dbc.Col([
        html.Hr(),
        html.P("This dashboard provides insights into California wildfires, including their impact, trends, and affected areas."),
        html.P("Developed by Gunisha Kaur, Thamer Aldawood, Elaine Chu and Forgive Agbesi."),
        html.P([
            "GitHub Repository: ",
            html.A("View on GitHub", href="https://github.com/UBC-MDS/DSCI-532_2025_27_CA_Wildfire-Dashboard", target="_blank")
        ]),
        html.P(f"Last updated: March 5th, 2025")
    ], style={"text-align": "center", "margin-top": "20px"}))],
    fluid=True,
    style={'margin': 0,
           'padding': 0,
           'overflow-x': 'hidden'}
    )
      
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
    [Input('county', 'value'),
    Input('year', 'value'),
    Input('incident_number', 'value'),
    Input('fire_damage_map', 'selectedData')
    ]
)

def update_charts(county, year, incident_number, selectedData):

    filtered_df = calfire_df[(calfire_df["Incident Start Date"].dt.year.between(year[0], year[1]))]

    if selectedData:
        selected_counties = [point["hovertext"] for point in selectedData["points"]]
        county = selected_counties
        
    if county:
        filtered_df = filtered_df[filtered_df['County'].isin(list(county))]
    
    if incident_number:
        filtered_df = filtered_df[filtered_df['Incident Number'].isin(list(incident_number))]
         
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

# Run the app/dashboard
if __name__ == '__main__':
    app.server.run(debug=False)
