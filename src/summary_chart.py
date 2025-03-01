import pandas as pd
import altair as alt

def make_summary_chart(calfire_df):
     calfire_summary = calfire_df.copy()
     if "Assessed Improved Value" not in calfire_df.columns or calfire_df.empty:
         return {}

     total_cost = calfire_summary["Assessed Improved Value"].sum()/ 1e9

     selection = alt.selection_single(on='mouseover', fields=['Total Economic Loss (in Billion)'], empty='none')

     summary_chart = alt.Chart(pd.DataFrame({"Total Economic Loss (in Billion)": [total_cost]})).mark_text(
         size=24, align='center', baseline='middle'
     ).encode(
         text=alt.Text("Total Economic Loss (in Billion):Q", format="$,.2f"),
         color=alt.condition(selection, alt.value('blue'), alt.value('red'))
     ).properties(
         title="Total Economic Loss (in Billion)",
         width=400,
         height=100
     ).add_selection(selection)

     return summary_chart 
