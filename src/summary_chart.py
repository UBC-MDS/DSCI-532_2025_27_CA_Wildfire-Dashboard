from .millions_billions import millions_billions

def make_summary_chart(calfire_df):

     """
    Creates a summary chart displaying the total assessed economic loss due to wildfire damage.

    Parameters
    ----------
    calfire_df : DataFrame
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
     if "Assessed Improved Value" not in calfire_df.columns: # Had to adjust condition after switching to dask 
         return 0

     calfire_df = calfire_df.compute()

     total_cost = millions_billions(calfire_df["Assessed Improved Value"].sum()) #convert the values to Millions or Billions

     return total_cost
