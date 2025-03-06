from dash import dcc
import plotly.express as px
import altair as alt
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import geopandas as gpd

geojson_file_path = "data/raw/California_County_Boundaries.geojson"
county_boundaries = gpd.read_file(geojson_file_path)[["CountyName", "geometry"]]
county_boundaries["CountyName"] = county_boundaries["CountyName"].str.strip()
    
def plot_map(county_data, selectedData=None):
    fig = px.choropleth(
        county_data,
        geojson=county_data.geometry,
        locations=county_data.index,
        color="Fire_Count",
        title="California Wildfire Damage by County",
        labels={"Fire_Count": "Number of Fires"},
        projection="mercator",
        hover_name="CountyName",
        color_continuous_scale="Reds",
    )

    fig.update_layout(clickmode='event+select') # For map selection

    if selectedData: # For persistent map selection
        selected_indices = [point['pointIndex'] for point in selectedData['points']]
        fig.update_traces(selectedpoints=selected_indices)

    fig.update_geos(fitbounds="locations", visible=False)

    return fig

def make_fire_damage_map(filtered_df, selectedData):
    
    # Aggregate fire damage count per county
    fire_count = filtered_df.groupby("County")["Damage"].count().reset_index(name="Fire_Count")

    # Merge with county boundaries
    county_fire_data = county_boundaries.merge(fire_count, left_on="CountyName", right_on="County", 
                                               how="left").infer_objects(copy=False).fillna(0)

    return plot_map(county_fire_data, selectedData)