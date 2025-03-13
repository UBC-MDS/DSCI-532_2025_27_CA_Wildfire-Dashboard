import pandas as pd

def make_summary_chart(calfire_df):
     
     if "Assessed Improved Value" not in calfire_df.columns or calfire_df.empty:
         return 0

     total_cost = calfire_df["Assessed Improved Value"].sum()/ 1e9 #convert the values to Billion

     return total_cost
