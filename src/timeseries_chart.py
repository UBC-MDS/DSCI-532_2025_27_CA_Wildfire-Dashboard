import pandas as pd
import altair as alt

def make_time_series_chart(calfire_df, selected_counties=None):
    """
    Creates an interactive time-series chart showing the total economic loss due to wildfires over the years.

    Parameters
    ----------
    calfire_df : pd.DataFrame
        A DataFrame containing wildfire damage data with at least the following columns:
        - "Incident Start Date": A datetime column representing the start date of each wildfire incident.
        - "County": The county where the wildfire occurred.
        - "Assessed Improved Value": The monetary value of assessed improvements to structures.

    selected_counties : list, optional
        A list of county names to filter the chart to specific counties. If None, the function selects
        the top 10 counties with the highest economic loss.

    Returns
    -------
    alt.Chart or dict
        - If the input DataFrame is empty, returns an empty dictionary `{}`.
        - Otherwise, returns an Altair line chart showing the total economic loss over time.

    Notes
    -----
    - The function aggregates the total assessed economic loss per year and county.
    - If `selected_counties` is provided, the chart only includes data for those counties.
    - If `selected_counties` is None, the top 10 counties with the highest total economic loss are selected.
    - Users can zoom into the chart and filter by clicking on the legend.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {
    ...     "Incident Start Date": pd.to_datetime(["2015-06-01", "2016-07-15", "2016-09-10"]),
    ...     "County": ["Los Angeles", "San Diego", "San Diego"],
    ...     "Assessed Improved Value": [100000000, 50000000, 75000000]
    ... }
    >>> df = pd.DataFrame(data)
    >>> chart = make_time_series_chart(df)
    >>> chart.show()  # Displays the interactive time-series chart.
    """
    if calfire_df.empty:
        return {}
    
    calfire_time_series = calfire_df.groupby(
        [calfire_df["Incident Start Date"].dt.year, "County"]
    )["Assessed Improved Value"].sum().reset_index()
    calfire_time_series.rename(columns={"Incident Start Date": "Year", "Assessed Improved Value": "Total Economic Loss (Billions of USD)"}, inplace=True)
    calfire_time_series["Total Economic Loss (Billions of USD)"] /= 1e9

    top_10_counties = (
        calfire_time_series.groupby("County")["Total Economic Loss (Billions of USD)"]
        .sum()
        .nlargest(10)
        .index.tolist()
    )

    if not selected_counties:
        filtered_df = calfire_time_series[calfire_time_series["County"].isin(top_10_counties)]
        selection = alt.selection_multi(fields=["County"], bind="legend", name="Select")
        opacity_rule = alt.condition(selection, alt.value(1), alt.value(0.2))
    else:
        filtered_df = calfire_time_series[calfire_time_series["County"].isin(selected_counties)]
        selection = None
        opacity_rule = alt.value(1)
    color_scale = alt.Scale(scheme="category20")
    zoom = alt.selection_interval(bind="scales")
    timeseries_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X(
            "Year:O",
            title="Year",
            axis=alt.Axis(labelAngle=45, tickMinStep=1)
        ),
        y=alt.Y(
    "Total Economic Loss (Billions of USD):Q",
    title=None,  
    scale=alt.Scale(zero=False),
    axis=alt.Axis(format=",.0f")  
        ),
        color=alt.Color(
            "County:N",
            title="Click Legend to Filter" if not selected_counties else "Selected Counties",
            scale=color_scale,
            legend=alt.Legend(
                title="County" if not selected_counties else "Selected Counties",
                orient="right"
            )
        ),
        opacity=opacity_rule,
        tooltip=["Year:O", "County", alt.Tooltip("Total Economic Loss (Billions of USD):Q", title="Total Economic Loss (Billions of USD)", format="$,.2f")]
    ).properties(
        width='container',
        height=200
    ).add_selection(zoom)
    if not selected_counties:
        timeseries_chart = timeseries_chart.add_selection(selection)
    return timeseries_chart
       