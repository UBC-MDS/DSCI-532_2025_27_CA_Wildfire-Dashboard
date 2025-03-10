
# Description: This script creates a choropleth map of California counties with wildfire damage data.
#
# The make_fire_damage_map function takes in a filtered dataframe and selectedData as input and returns a choropleth map of California counties with wildfire damage data.
# The function first aggregates the fire damage count per county using the groupby method.
# It then merges the aggregated data with the county boundaries data to create a GeoDataFrame.
# The plot_map function is called to create the choropleth map using the GeoDataFrame and selectedData.
# The function returns the choropleth map.
#
# The plot_map function takes in county_data and selectedData as input and returns a choropleth map of California counties with wildfire damage data.
# The function uses the plotly express choropleth method to create the map.
# It sets the color scale, hover data, and custom data for the map.
# The function updates the layout of the map to enable clickmode and select mode.
# If selectedData is provided, the function updates the selected points on the map.
# The function returns the choropleth map.

import plotly.express as px
from .data import county_boundaries
    
def plot_map(county_data, selectedData=None):
    county_data = county_data.reset_index(drop=True)
    
    fig = px.choropleth(
        county_data,
        geojson=county_data.geometry,
        locations=county_data.index,
        color="Fire_Count",
        labels={"Fire_Count": "Number of Fires", "Assessed_Value_B": "Economic Loss"},
        projection="mercator",
        hover_name="CountyName", 
        color_continuous_scale="Reds",
        hover_data={"CountyName": False, "Assessed_Value_B": True, "Fire_Count": True},
        custom_data=["Assessed_Value_B"]   
    )
    
    fig.update_layout(clickmode='event+select')

    if selectedData:
        selected_indices = [point['pointIndex'] for point in selectedData['points']]
        fig.update_traces(selectedpoints=selected_indices)

    fig.update_geos(fitbounds="locations", visible=False)

     # Remove index from tooltip
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Economic Loss: %{customdata[0]}<br>Number of Fires: %{z}<extra></extra>")

    return fig


def make_fire_damage_map(filtered_df, selectedData):
    
    # Aggregate fire damage count per county
    fire_count = filtered_df.groupby("County").agg(
        Fire_Count=("Damage", "count"),
        Assessed_Value=("Assessed Improved Value", "sum") 
    ).reset_index() 
    fire_count["Assessed_Value"] = fire_count["Assessed_Value"] / 1e9

    # Merge with county boundaries
    county_fire_data = county_boundaries.merge(fire_count, left_on="CountyName", right_on="County", 
                                               how="left").infer_objects(copy=False).fillna(0)
    
    county_fire_data["Assessed_Value_B"] = county_fire_data["Assessed_Value"].apply(lambda x: f"${x:,.2f}B")
    
    return plot_map(county_fire_data, selectedData)
