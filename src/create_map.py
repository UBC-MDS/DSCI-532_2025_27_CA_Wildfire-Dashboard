import plotly.express as px
import geopandas as gpd
import pandas as pd

def make_fire_damage_map(county_boundaries):
    """
    Generates a choropleth map of California counties with wildfire damage data.

    Parameters
    ----------
    county_boundaries : geopandas.GeoDataFrame
        A GeoDataFrame containing county boundaries with precomputed columns "Fire Count" and "Economic Loss".
    selectedData : dict, optional
        Data from a previous selection event, used to highlight selected counties (default is None).

    Returns
    -------
    plotly.graph_objects.Figure
        A choropleth map displaying wildfire damage across California counties.
        
    Examples
    --------
    >>> create_fire_damage_map( county_boundaries)
    """

    fig = px.choropleth(
        county_boundaries,
        geojson=county_boundaries.geometry,
        locations=county_boundaries.index,
        color="Assessed Improved Value",
        labels={"Assessed Improved Value": "Economic Loss (Billion $)"},
        projection="mercator",
        hover_name="County", 
        color_continuous_scale="Reds",
        hover_data={"County": False, "Economic Loss": True, "Fire Count": True},
        custom_data=["Economic Loss", "Fire Count"],
    )
    
    fig.update_layout(clickmode='event+select')

    fig.update_geos(fitbounds="locations", visible=False)

    # Remove index from tooltip
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Economic Loss: %{customdata[0]}<br>Number of Fires: %{customdata[1]}<extra></extra>")

    return fig