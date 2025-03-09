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
#
# The make_fire_damage_map function is called in the update_charts function in app.py to update the fire damage map based on the selected counties and data filters.
# The function is used to visualize the distribution of wildfire damage across California counties.
# The map provides an interactive visualization of the number of fires and assessed value of damage in each county.
# The map allows users to select specific counties and view detailed information about the fire damage in those counties.
# The map is updated dynamically based on the user's selection and filter criteria.
# The map provides a visual representation of the economic impact of wildfires in California.
# The map helps users understand the distribution of fire damage across different counties and identify areas with high wildfire risk.
# The map enhances the user experience by providing an interactive and informative visualization of wildfire damage data.
# The map is an essential component of the California Wildfire Dashboard, providing valuable insights into the economic impact of wildfires in the state.
# The map complements other visualizations and charts in the dashboard, providing a comprehensive overview of wildfire-related data.
# The map is designed to be user-friendly and intuitive, allowing users to explore and analyze wildfire damage data effectively.
# The map leverages geospatial data and interactive features to enhance the user experience and facilitate data-driven decision-making.
# The map is an integral part of the dashboard's functionality, enabling users to interact with and explore wildfire damage data in a visually engaging manner.
# The map showcases the power of geospatial visualization in conveying complex information and highlighting patterns and trends in wildfire damage data.
# The map serves as a key tool for policymakers, researchers, and the general public to gain insights into the economic impact of wildfires in California and inform mitigation strategies and policy decisions.
# The map contributes to the overall goal of the dashboard to raise awareness about wildfires and their consequences and promote data-driven solutions to address the wildfire crisis in California.
# The map is a valuable resource for stakeholders interested in understanding the spatial distribution of wildfire damage and assessing the economic implications of wildfires in different regions of California.
# The map is an essential component of the dashboard's data visualization strategy, providing a geospatial perspective on wildfire damage data and enhancing the overall user experience.
# The map is designed to be informative, interactive, and visually appealing, making it an effective tool for exploring and analyzing wildfire-related data in California.
# The map is a key feature of the dashboard, offering users a unique and engaging way to explore and interpret wildfire damage data and gain insights into the impact of wildfires on California communities.
# The map is an example of how geospatial visualization can be used to communicate complex information effectively and engage users in exploring and understanding wildfire-related data.
# The map is an important component of the dashboard's functionality, providing users with a comprehensive view of wildfire damage across California counties and enabling them to interact with the data in a meaningful way.
# The map is a powerful tool for visualizing and analyzing wildfire damage data, helping users identify patterns, trends, and hotspots of fire activity in California.
# The map is an essential resource for stakeholders interested in monitoring and assessing the economic impact of wildfires in California and developing strategies to mitigate the risks associated with wildfires.


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
        labels={"Fire_Count": "Number of Fires", "Assessed_Value": "Assessed Value"},
        projection="mercator",
        hover_name="CountyName",
        hover_data={"Assessed_Value": ":,.2f"},  # Formatting as currency-like
        color_continuous_scale="Reds",
        custom_data=["Assessed_Value"]  # Ensure custom_data is set
    )

    fig.update_layout(clickmode='event+select')

    if selectedData:
        selected_indices = [point['pointIndex'] for point in selectedData['points']]
        fig.update_traces(selectedpoints=selected_indices)

    fig.update_geos(fitbounds="locations", visible=False)

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

    return plot_map(county_fire_data, selectedData)