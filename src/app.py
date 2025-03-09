from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from . import callbacks
from .components import title, global_widgets, cali_map, summary_card, damage_level, timeseries_chart, structure_count, roof_chart, info_button, info_section, main_font_color, main_font_size, theme_color

# Initiatlize the app
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.FLATLY])
server = app.server

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
                    "margin-left": "10px"},
                md=3),
        dbc.Col(
            [dbc.Row(
                dbc.Card(
                    [dbc.CardHeader("California Wildfire Damage by County",
                                style={"textAlign": "center",
                                       "fontWeight": "bold",
                                        "fontSize": main_font_size,
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
            dbc.Row(
                    [
                        html.P(
                            "* Hover to view county summary; click to filter.",
                            style={"text-align": "center",
                                   "font-size": "16px",
                                   "position": "absolute",
                                    "bottom": 0,
                                    "right": 0},
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
      


# Run the app/dashboard
if __name__ == '__main__':
    app.server.run(debug=True)
