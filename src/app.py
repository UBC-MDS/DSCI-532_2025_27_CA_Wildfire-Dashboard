from dash import Dash, dcc, callback, Output, Input, html
import altair as alt
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import plotly.express as px
from vega_datasets import data


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

df = pd.read_csv("../data/raw/California Wildfire Damage.csv", parse_dates=["Date"])


# Layout
app.layout = dbc.Container([


## Title
    dcc.Markdown('''

    # California Wildfires Dashboard

    A one-stop shop for gleaning insights from California Wildfires data

'''),

html.Br(),


## Dropdown / filter
dcc.Markdown('''
Select a location to see its associated scatter plot:
'''),
dcc.Dropdown(
    id='location',
    options=[{'label': loc, 'value': loc} for loc in df['Location'].unique()],
    placeholder = "Select a location"
),

html.Br(),


## Chart
    dvc.Vega(
        id='scatter',
        spec={},
        ),

html.Br(),


## TODO
    dcc.Markdown('''
##### To be added:
                 - Map
                 - Charts
                 - Filter
                 ''')
])


# Server side callbacks/reactivity
@callback(
    Output('scatter', 'spec'),
    Input('location', 'value')
)

def create_chart(location="Butte County"):
#   brush = alt.selection_point(fields=['Miles_per_Gallon', x_col], name='selection')
#   Later we'll use brushes for better interactivity with charts

    df = pd.read_csv("../data/raw/California Wildfire Damage.csv", parse_dates=True)
    df = df[df['Location'] == location]
    
    chart = alt.Chart(df).mark_point().encode(
        x='Injuries',
        y='Fatalities',
        tooltip='Incident_ID',
    ).interactive()

    return chart.to_dict()

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)