import pandas as pd
import altair as alt

def make_summary_chart(calfire_df):
     """
    Creates a summary chart displaying the total assessed economic loss due to wildfire damage.

    Parameters
    ----------
    calfire_df : pd.DataFrame
        A DataFrame containing wildfire damage data with at least the following column:
        - "Assessed Improved Value": The monetary value of assessed improvements to structures.

    Returns
    -------
    float or alt.Chart
        - If the required column is missing or the DataFrame is empty, returns `0`.
        - Otherwise, returns an Altair text chart displaying the total economic loss in billions of USD.

    Notes
    -----
    - Converts the total assessed value from USD to billions for readability.
    - Uses a mouse-over interaction to change the text color dynamically.
    - If no valid data exists, the function returns `0` instead of a chart.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {"Assessed Improved Value": [50000000, 200000000, 150000000]}
    >>> df = pd.DataFrame(data)
    >>> chart = make_summary_chart(df)
    >>> chart.show()  # Displays the total economic loss chart.
    """
     calfire_summary = calfire_df.copy()
     if "Assessed Improved Value" not in calfire_df.columns or calfire_df.empty:
         return 0

     total_cost = calfire_summary["Assessed Improved Value"].sum()/ 1e9 #convert the values to Billion

     selection = alt.selection_single(on='mouseover', fields=['Total Economic Loss (Billions of USD)'], empty='none')

     summary_chart = alt.Chart(pd.DataFrame({"Total Economic Loss (Billions of USD)": [total_cost]})).mark_text(
         size=24, align='center', baseline='middle'
     ).encode(
         text=alt.Text("Total Economic Loss (Billions of USD):Q", format=".0f"),
         color=alt.condition(selection, alt.value('blue'), alt.value('red'))
     ).properties(
         title="Total Economic Loss (Billions of USD)",
         width=400,
         height=100
     ).add_selection(selection)

     return total_cost
