import pandas as pd
import altair as alt

def make_structure_chart(calfire_df):
    """
    Creates a bar chart showing the number of damaged structures by county,
    categorized by structure type.

    Parameters
    ----------
    calfire_df : pd.DataFrame
        A DataFrame containing wildfire damage data with at least the following columns:
        - "County": The county where the wildfire occurred.
        - "Structure Category": The type of structure affected.

    Returns
    -------
    alt.Chart
        An Altair bar chart displaying the number of damaged structures for 
        the top 10 counties most affected, categorized by structure type.

    Notes
    -----
    - Groups data by County and Structure Category to calculate structure counts.
    - Renames structure categories using single-letter codes to work around Altair sorting issues.
    - Filters to display only the top 10 counties with the most damaged structures.
    - Uses a color scheme to differentiate structure categories.
    - Enables interactive tooltips for better user insights.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {"County": ["Los Angeles", "San Diego", "Los Angeles", "Orange"],
    ...         "Structure Category": ["Single Residence", "Infrastructure", "Agriculture", "Nonresidential Commercial"]}
    >>> df = pd.DataFrame(data)
    >>> chart = make_structure_chart(df)
    >>> chart.show()
    """

    calfire_structure = calfire_df.groupby(['County', 'Structure_Renamed'])['Structure_Renamed'].count().reset_index(name="Count")

    top_10 = (calfire_structure
          .groupby(['County'])['Count'].sum()
          .sort_values(ascending=False)
          .reset_index()
          .iloc[:10, 0])
    
    calfire_structure = calfire_structure[calfire_structure['County'].isin(top_10)]

    alt.data_transformers.enable("vegafusion")

    structure_chart = alt.Chart(calfire_structure).mark_bar().encode(
        y=alt.Y("County:N",
                title=None,
                sort=top_10
                ), 
                x=alt.X("Count", title="Number of Structures Damaged"),
                color=alt.Color("Structure_Renamed:N",
                                title="Structure Category",
                                scale=alt.Scale(scheme="paired"),
                                legend=alt.Legend(
                                    title="Structure Category",
                                    labelExpr="{'A':'Single Residence', "
                                                "'B': 'Multiple Residence', "
                                                "'C': 'Mixed Commercial/Residential', "
                                                "'D': 'Nonresidential Commercial', "
                                                "'E': 'Infrastructure', "
                                                "'F': 'Agriculture', "
                                                "'G': 'Other Minor Structure'}[datum.label]"
                                                )
                                ),
                tooltip=["Structure_Renamed", "Count"]
                ).properties(
        width='container',
        height=200
    )
    
    return structure_chart