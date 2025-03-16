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
    alt.data_transformers.enable("vegafusion")

    damage_table = pd.DataFrame(calfire_df.columns[:47].to_list(), columns=[ "Roof Construction", "Damage Category"])

    damage_count = pd.DataFrame(calfire_df.iloc[:, :47].sum(axis=0).values, columns=["Count"])

    calfire_damage = (pd.concat([damage_table, damage_count], axis=1)
                      .groupby(['Damage Category'])['Count']
                      .sum().reset_index(name="Count"))

    damage_chart = alt.Chart(calfire_damage).mark_arc(innerRadius=50).encode(
    theta="Count",
    color=alt.Color("Damage Category:N",
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
    tooltip=["Damage Category:O", "Count:Q"]).properties(
        width='container',
        height=200
    )

    return damage_chart