import pandas as pd
import altair as alt

def make_roof_chart(calfire_df):
    calfire_roof = calfire_df.copy()
    calfire_roof = calfire_roof[calfire_roof["Roof Construction"].notnull()]
    calfire_roof = calfire_roof[calfire_roof["Roof Construction"] != ' ']
    calfire_roof = calfire_roof[calfire_roof["Roof Construction"] != 'Unknown']

    calfire_roof = calfire_roof[calfire_roof["Damage"] != 'Unknown']

    alt.data_transformers.enable("vegafusion")
    # Defines a mapping for renaming damage categories. This is a workaround to an existing altair bug https://github.com/vega/vega-lite/issues/5366
    damage_rename = {
        "No Damage": "A. No Damage",
        "Affected (1-9%)": "B. Affected (1-9%)",
        "Minor (10-25%)": "C. Minor (10-25%)",
        "Major (26-50%)": "D. Major (26-50%)",
        "Destroyed (>50%)": "E. Destroyed (>50%)"
    }

    calfire_roof["Damage_Renamed"] = calfire_roof["Damage"].map(damage_rename)

    # Compute total count per Roof Construction for sorting
    roof_order = (
        calfire_roof.groupby("Roof Construction")
        .size()
        .reset_index(name="Total Houses")
        .sort_values("Total Houses", ascending=False)["Roof Construction"]
        .tolist()
    )

    roof_chart = alt.Chart(calfire_roof).mark_bar().encode(
        y=alt.Y("Roof Construction:N", 
                title="Roof Type", 
                sort=roof_order  # Sort by total house count (descending)
            ),  
        x=alt.X("count()", title="Number of Houses"),
        color=alt.Color("Damage_Renamed:N",  # Use renamed categories for sorting
                        title="Damage Category",
                        scale=alt.Scale(scheme="reds"),
                        legend=alt.Legend(
                            title="Damage Category",
                            labelExpr="{'A. No Damage': 'No Damage', " 
                                    "'B. Affected (1-9%)': 'Affected (1-9%)', " 
                                    "'C. Minor (10-25%)': 'Minor (10-25%)', " 
                                    "'D. Major (26-50%)': 'Major (26-50%)', " 
                                    "'E. Destroyed (>50%)': 'Destroyed (>50%)'}[datum.label]"  
                        )  # Show original labels in legend
                    ),  
        tooltip=["Roof Construction", "count()", "Damage"]
    ).properties(
        title="House Damage by Roof Type"
    ).interactive()

    return roof_chart