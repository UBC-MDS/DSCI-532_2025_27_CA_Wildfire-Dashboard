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