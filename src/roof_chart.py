import pandas as pd
import altair as alt

def make_roof_chart(calfire_df):
    
    alt.data_transformers.enable("vegafusion")

    # Compute total count per Roof Construction for sorting
    roof_order = (
        calfire_df.groupby("Roof Construction")
        .size()
        .reset_index(name="Total Houses")
        .sort_values("Total Houses", ascending=False)["Roof Construction"]
        .tolist()
    )

    roof_chart = alt.Chart(calfire_df).mark_bar().encode(
        y=alt.Y("Roof Construction:N", 
                title=None, 
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
        tooltip=["Roof Construction", "count()", "Damage_Renamed"]
    ).properties(
        width='container',
        height=200
    )

    return roof_chart