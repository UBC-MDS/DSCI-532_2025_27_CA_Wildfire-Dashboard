import pandas as pd
import altair as alt

def make_structure_chart(calfire_df):
    calfire_structure = calfire_df.copy()
    calfire_structure = calfire_structure.groupby(['County', 'Structure Category'])['Structure Category'].count().reset_index(name="Count")

    structure_rename = {
    "Single Residence": "A",
    "Multiple Residence": "B",
    "Mixed Commercial/Residential": "C",
    "Nonresidential Commercial": "D",
    "Infrastructure": "E",
    "Agriculture": "F",
    "Other Minor Structure": "G"
    }

    calfire_structure["Structure_Renamed"] = calfire_structure["Structure Category"].map(structure_rename)

    top_10 = (calfire_structure
          .groupby(['County'])['Count'].sum()
          .sort_values(ascending=False)
          .reset_index()
          .iloc[:10, 0])
    
    calfire_structure = calfire_structure[calfire_structure['County'].isin(top_10)]

    alt.data_transformers.enable("vegafusion")

    structure_chart = alt.Chart(calfire_structure).mark_bar().encode(
        y=alt.Y("County:N",
                title="County",
                sort=top_10
                ), 
                x=alt.X("Count", title="Number of Structures damaged"),
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
                tooltip=["Structure Category", "Count"]
                ).properties(
                    title="Structure Damaged by Category in the Top 10 Most Affected Counties"
                    ).interactive()
    
    return structure_chart