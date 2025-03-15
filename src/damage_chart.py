import altair as alt

def make_damage_chart(calfire_df):
    """
    Generates a donut chart displaying the distribution of damage categories in the given dataset.

    Parameters
    ----------
    calfire_df : DataFrame
        A DataFrame containing wildfire damage data with a column named 'Damage'.

    Returns
    -------
    alt.Chart
        An Altair donut chart visualizing the count of each damage category.
    Examples
    -------
    >>> make_damage_chart(calfire_df)
    """
    # calfire_df = calfire_df.groupby(['Damage_Category'])['Damage_Category'].count().reset_index(name="Count")

    # Group by Damage_Category and count the number of records in each category
    calfire_df = calfire_df.groupby('Damage_Category').size().reset_index()

    # Compute the Dask DataFrame to get a Pandas DataFrame
    calfire_df = calfire_df.compute()

    calfire_df.columns = ["Damage_Category", "Count"]

    damage_chart = alt.Chart(calfire_df).mark_arc(innerRadius=50).encode(
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
    tooltip=["Damage_Category:O", "Count:Q"]).properties(
        width='container',
        height=200
    )

    return damage_chart