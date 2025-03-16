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

    damage_table = pd.DataFrame(calfire_df.columns[:47].to_list(), columns=[ "Roof Construction", "Damage Category"])

    damage_count = pd.DataFrame(calfire_df.iloc[:, :47].sum(axis=0).values, columns=["Count"])

    roof_damage = pd.concat([damage_table, damage_count], axis=1)

    # Compute total count per Roof Construction for sorting
    roof_order = (
        roof_damage.groupby("Roof Construction")['Count']
        .sum().sort_values(ascending=False).index.tolist()
    )

    roof_chart = alt.Chart(roof_damage).mark_bar().encode(
        y=alt.Y("Roof Construction:N", 
                title=None, 
                sort=roof_order  # Sort by total house count (descending)
            ),  
        x=alt.X("Count", title="Number of Houses"),
        color=alt.Color("Damage Category:N",  # Use renamed categories for sorting
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
        tooltip=["Roof Construction:N", "count():Q", "Damage Category:O"]
    ).properties(
        width='container',
        height=200
    )

    return roof_chart