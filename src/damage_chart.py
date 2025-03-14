import pandas as pd
import altair as alt

def make_damage_chart(calfire_df):
    """
    Generates a donut chart displaying the distribution of damage categories in the given dataset.

    Parameters
    ----------
    calfire_df : pd.DataFrame
        A DataFrame containing wildfire damage data with a column named 'Damage'.

    Returns
    -------
    alt.Chart
        An Altair donut chart visualizing the count of each damage category.
    Examples
    -------
    >>> make_damage_chart(calfire_df)
    """
    calfire_damage = calfire_df.groupby(['Damage_Category'])['Damage_Category'].count().reset_index(name="Count")

    damage_chart = alt.Chart(calfire_damage).mark_arc(innerRadius=50).encode(
    theta="Count",
    color=alt.Color("Damage_Category:N",
                    title="Damage Category",
                    scale=alt.Scale(scheme="reds"),
                    legend=alt.Legend(
                            title="Damage Category",
                            labelExpr="{'A. No Damage': 'No Damage', " 
                                    "'B. Affected (1-9%)': 'Affected (1-9%)', " 
                                    "'C. Minor (10-25%)': 'Minor (10-25%)', " 
                                    "'D. Major (26-50%)': 'Major (26-50%)', " 
                                    "'E. Destroyed (>50%)': 'Destroyed (>50%)'}[datum.label]"
                                    )
                                    ),
    tooltip=["Damage_Category", "Count"]).properties(
        width='container',
        height=200
    )

    return damage_chart