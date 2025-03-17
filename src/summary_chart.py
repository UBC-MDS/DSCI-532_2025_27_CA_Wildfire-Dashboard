import pandas as pd
from .millions_billions import millions_billions

def make_summary_chart(calfire_df):
    """
    Calculate and return the total economic loss from wildfire data, 
    formatted as millions or billions.

    Parameters
    ----------
    calfire_df : pd.DataFrame
        DataFrame containing wildfire economic data. Must include a column named 'Total Economic Loss'.

    Returns
    -------
    total_cost : int or float
        Total economic loss aggregated across the DataFrame, converted to a human-readable
        format (millions or billions). Returns 0 if the required column is missing or if
        the DataFrame is empty.

    Examples
    --------
    >>> data = pd.DataFrame({'Total Economic Loss': [1000000, 2000000, 5000000]})
    >>> make_summary_chart(data)
    '8.0M'

    >>> empty_df = pd.DataFrame()
    >>> make_summary_chart(empty_df)
    0
    """
    
    if "Total Economic Loss" not in calfire_df.columns or calfire_df.empty:
         return 0

    total_cost = millions_billions(calfire_df["Total Economic Loss"].sum()) #convert the values to Millions or Billions

    return total_cost
