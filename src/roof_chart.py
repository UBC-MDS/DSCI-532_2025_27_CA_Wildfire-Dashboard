import pandas as pd
import altair as alt

def make_roof_chart(calfire_df):
    """
    Creates a bar chart showing the number of houses by roof construction type,
    categorized by wildfire damage severity.

    Parameters
    ----------
    calfire_df : pd.DataFrame
        A DataFrame containing wildfire damage data with at least the following columns:
        - "Roof Construction": Type of roof construction.
        - "Damage": Damage severity category.

    Returns
    -------
    alt.Chart
        An Altair bar chart displaying the count of houses for each roof construction type,
        colored by damage severity.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {"Roof Construction": ["Tile", "Shingle", "Tile", "Metal"],
    ...         "Damage": ["No Damage", "Minor (10-25%)", "Destroyed (>50%)", "Major (26-50%)"]}
    >>> df = pd.DataFrame(data)
    >>> chart = make_roof_chart(df)
    >>> chart.show()
    """
    alt.data_transformers.enable("vegafusion")

    # Compute total count per Roof Construction for sorting
    roof_order = (
        calfire_df.groupby("Roof Construction")
        .size()
        .reset_index(name="Total Houses")
        .sort_values("Total Houses", ascending=False)["Roof Construction"]
        .tolist()
    )

    roof_chart = alt.Chart(calfire_df).mark_bar().encode(
        y=alt.Y("Roof Construction:N", 
                title=None, 
                sort=roof_order  # Sort by total house count (descending)
            ),  
        x=alt.X("count()", title="Number of Houses"),
        color=alt.Color("Damage_Renamed:N",  # Use renamed categories for sorting
                        title="Damage Category",
                        scale=alt.Scale(scheme="reds"),
                        legend=alt.Legend(
                            title="Damage Category",
                            labelExpr="{'A. No Damage': 'No Damage', " 
                                    "'B. Affected (1-9%)': 'Affected (1-9%)', " 
                                    "'C. Minor (10-25%)': 'Minor (10-25%)', " 
                                    "'D. Major (26-50%)': 'Major (26-50%)', " 
                                    "'E. Destroyed (>50%)': 'Destroyed (>50%)'}[datum.label]"  
                        )  # Show original labels in legend
                    ),  
        tooltip=["Roof Construction", "count()", "Damage_Renamed"]
    ).properties(
        width='container',
        height=200
    )

    return roof_chart