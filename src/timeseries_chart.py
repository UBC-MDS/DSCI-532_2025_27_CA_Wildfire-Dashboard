import pandas as pd
import altair as alt

def make_time_series_chart(calfire_df, selected_counties=None):
    if calfire_df.empty:
        return {}
    
    calfire_time_series = calfire_df.groupby(
        [calfire_df["Incident Start Date"].dt.year, "County"]
    )["Assessed Improved Value"].sum().reset_index()
    calfire_time_series.rename(columns={"Incident Start Date": "Year", "Assessed Improved Value": "Total Economic Loss (Billions of USD)"}, inplace=True)
    calfire_time_series["Total Economic Loss (Billions of USD)"] /= 1e9

    top_5_counties = (
        calfire_time_series.groupby("County")["Total Economic Loss (Billions of USD)"]
        .sum()
        .nlargest(5)
        .index.tolist()
    )

    if not selected_counties:
        filtered_df = calfire_time_series[calfire_time_series["County"].isin(top_5_counties)]
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
    title="Total Economic Loss (Billions of USD)",  
    scale=alt.Scale(zero=False),
    axis=alt.Axis(format="$,.0f")  
        ),
        color=alt.Color(
            "County:N",
            title="Click Legend to Filter" if not selected_counties else "Selected Counties",
            scale=color_scale,
            legend=alt.Legend(
                title="Click a County to Filter" if not selected_counties else "Selected Counties",
                orient="right"
            )
        ),
        opacity=opacity_rule,
        tooltip=["Year:O", "County", alt.Tooltip("Total Economic Loss (Billions of USD):Q", title="Total Economic Loss (Billions of USD)", format="$,.0f")]
    ).properties(
        title="Economic Loss Over Time",
        width=250,
        height=200
    ).add_selection(zoom)
    if not selected_counties:
        timeseries_chart = timeseries_chart.add_selection(selection)
    return timeseries_chart
       