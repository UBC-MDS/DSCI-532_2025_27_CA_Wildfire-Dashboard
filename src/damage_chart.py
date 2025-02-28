import pandas as pd
import altair as alt

def make_damage_chart(calfire_df):
    calfire_damage = calfire_df.copy()
    calfire_damage = calfire_damage[calfire_damage['Damage'] != 'Unknown']
    calfire_damage = calfire_damage.groupby(['Damage'])['Damage'].count().reset_index(name="Count")

    alt.data_transformers.enable("vegafusion")
    # Defines a mapping for renaming damage categories. This is a workaround to an existing altair bug https://github.com/vega/vega-lite/issues/5366
    damage_rename = {
        "No Damage": "A. No Damage",
        "Affected (1-9%)": "B. Affected (1-9%)",
        "Minor (10-25%)": "C. Minor (10-25%)",
        "Major (26-50%)": "D. Major (26-50%)",
        "Destroyed (>50%)": "E. Destroyed (>50%)"
    }

    calfire_damage["Damage_Renamed"] = calfire_damage["Damage"].map(damage_rename)

    damage_chart = alt.Chart(calfire_damage).mark_arc(innerRadius=50).encode(
    theta="Count",
    color=alt.Color("Damage_Renamed:N",
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
    tooltip=["Damage", "Count"]).properties(
        title="Damage Category"
    ).interactive()

    return damage_chart