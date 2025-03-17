import pandas as pd
import altair as alt

def make_time_series_chart(calfire_df, selected_counties=None):
    """
    Generate an Altair time-series line chart visualizing total economic losses from wildfires by county and year.

    The chart aggregates total economic loss per county per year, automatically adjusting units to billions, millions,
    or dollars depending on the magnitude of the maximum loss. If no counties are explicitly selected, the chart defaults
    to displaying the top 10 counties by total economic loss and includes interactive filtering through the legend.

    Parameters
    ----------
    calfire_df : pd.DataFrame
        DataFrame containing wildfire data. Required columns include:
        - 'County': County names.
        - 'Year': Year of the reported economic loss.
        - 'Total Economic Loss': Numeric economic losses per event or year.

    selected_counties : list of str, optional
        Specific counties to visualize. If `None`, defaults to showing the top 10 counties.

    Returns
    -------
    alt.Chart or dict
        An Altair line chart object visualizing economic losses over time, or an empty dictionary `{}` if
        `calfire_df` is empty.

    Examples
    --------
    >>> data = pd.DataFrame({
    ...     'County': ['Los Angeles', 'Los Angeles', 'San Diego', 'San Diego'],
    ...     'Year': [2019, 2020, 2019, 2020],
    ...     'Total Economic Loss': [1.2e9, 1.5e9, 500e6, 800e6]
    ... })
    >>> chart = make_time_series_chart(data)
    >>> type(chart)
    <class 'altair.vegalite.v5.api.Chart'>

    Notes
    -----
    - The chart includes interactive elements that allow users to filter data by clicking on counties in the legend.
    - Numeric formatting automatically adapts based on the magnitude of the economic loss data.
    """
    
    if calfire_df.empty:
        return {}
    
    calfire_time_series = (calfire_df
                           .groupby(['County', 'Year'])["Total Economic Loss"]
                           .sum().reset_index())

    #calfire_time_series["Total Economic Loss (Billions of USD)"] /= 1e9

    max_loss = calfire_time_series["Total Economic Loss"].max()
    if max_loss >= 1e9:
        calfire_time_series["Total Economic Loss"] /= 1e9
        y_axis_title = "Total Economic Loss (Billions of USD)"
        y_axis_format = ",.0f"
    elif max_loss >= 1e6:
        calfire_time_series["Total Economic Loss"] /= 1e6
        y_axis_title = "Total Economic Loss (Millions of USD)"
        y_axis_format = ",.0f"
    else:
        y_axis_title = "Total Economic Loss (USD)"
        y_axis_format = ",.0f"

    top_10_counties = (
        calfire_time_series.groupby("County")["Total Economic Loss"]
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
    timeseries_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X(
            "Year:O",
            title="Year",
            axis=alt.Axis(labelAngle=45, tickMinStep=1)
        ),
       y=alt.Y(
            "Total Economic Loss:Q",
            title=y_axis_title,
            scale=alt.Scale(zero=False),
            axis=alt.Axis(format=y_axis_format)
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
        tooltip=["Year:O", "County", alt.Tooltip("Total Economic Loss:Q", title=y_axis_title, format=y_axis_format)]

    ).properties(
        width='container',
        height=200
    )
    if not selected_counties:
        timeseries_chart = timeseries_chart.add_selection(selection)
    return timeseries_chart
       