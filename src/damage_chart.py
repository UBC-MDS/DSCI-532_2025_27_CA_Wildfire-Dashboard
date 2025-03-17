import pandas as pd
import altair as alt

def make_damage_chart(calfire_df):
    """
    Generates a donut chart displaying the distribution of damage categories in the given dataset.

    Parameters
    ----------
    calfire_df : pd.DataFrame
        A DataFrame containing wildfire damage data with the following columns:
        - "('Asphalt', 'A. No Damage')": Count of "Ashphalt" roof type with "no damage" damage level.
        - "('Asphalt', 'B. Affected (1-9%)')": Count of "Ashphalt" roof type with "Affect (1-9%)" damage level.
        - "('Asphalt', 'C. Minor (10-25%)')": Count of "Ashphalt" roof type with with "Minor (10-25%)" damage level.
        - "('Asphalt', 'D. Major (26-50%)')": Count of "Ashphalt" roof type with "Major (26-50%)" damage level.
        - "('Asphalt', 'E. Destroyed (>50%)')": Count of "Ashphalt" roof type with "Destroyed (>50%)" damage level.
        - "('Combustible', 'A. No Damage')": Count of "Combustible" roof type with "no damage" damage level.
        - "('Combustible', 'B. Affected (1-9%)')": Count of "Combustible" roof type with "Affect (1-9%)" damage level.
        - "('Combustible', 'C. Minor (10-25%)')": Count of "Combustible" roof type with "Minor (10-25%)" damage level.
        - "('Combustible', 'D. Major (26-50%)')": Count of "Combustible" roof type with "Major (26-50%)" damage level.
        - "('Combustible', 'E. Destroyed (>50%)')": Count of "Combustible" roof type with "Destroyed (>50%)" damage level.
        - "('Concrete', 'A. No Damage')": Count of "Concrete" roof type with "no damage" damage level.
        - "('Concrete', 'B. Affected (1-9%)')": Count of "Concrete" roof type with "Affect (1-9%)" damage level.
        - "('Concrete', 'C. Minor (10-25%)')": Count of concrete roof type with "Minor (10-25%)" damage level.
        - "('Concrete', 'D. Major (26-50%)')": Count of "Concrete" roof type with "Major (26-50%)" damage level.
        - "('Concrete', 'E. Destroyed (>50%)')": Count of "Concrete" roof type with "Destroyed (>50%)" damage level.
        - "('Fire Resistant', 'A. No Damage')": Count of "Fire Resistant" roof type with "no damage" damage level.
        - "('Fire Resistant', 'B. Affected (1-9%)')": Count of "Fire Resistant" roof type with "Affect (1-9%)" damage level.
        - "('Fire Resistant', 'C. Minor (10-25%)')": Count of "Fire Resistant" roof type with "Minor (10-25%)" damage level.
        - "('Fire Resistant', 'D. Major (26-50%)')": Count of "Fire Resistant" roof type with "Major (26-50%)" damage level.
        - "('Fire Resistant', 'E. Destroyed (>50%)')": Count of "Fire Resistant" roof type with "Destroyed (>50%)" damage level.
        - "('Metal', 'A. No Damage')": Count of "Metal" roof type with "no damage" damage level.
        - "('Metal', 'B. Affected (1-9%)')": Count of "Metal" roof type with "Affect (1-9%)" damage level.
        - "('Metal', 'C. Minor (10-25%)')": Count of "Metal" roof type with "Minor (10-25%)" damage level.
        - "('Metal', 'D. Major (26-50%)')": Count of "Metal" roof type with "Major (26-50%)" damage level.
        - "('Metal', 'E. Destroyed (>50%)')": Count of "Metal" roof type with "Destroyed (>50%)" damage level.
        - "('No Deck/Porch', 'A. No Damage')": Count of "No Deck/Porch" roof type with "no damage" damage level.
        - "('Non Combustible', 'E. Destroyed (>50%)')": Count of "Non Combustible" roof type with "Destroyed (>50%)" damage level.
        - "('Other', 'A. No Damage')": Count of "Other" roof type with "no damage" damage level.
        - "('Other', 'B. Affected (1-9%)')": Count of "Other" roof type with "Affect (1-9%)" damage level.
        - "('Other', 'C. Minor (10-25%)')": Count of "Other" roof type with "Minor (10-25%)" damage level.
        - "('Other', 'D. Major (26-50%)')": Count of "Other" roof type with "Major (26-50%)" damage level.
        - "('Other', 'E. Destroyed (>50%)')": Count of "Other" roof type with "Destroyed (>50%)" damage level.
        - "('Tile', 'A. No Damage')": Count of "Tile" roof type with "no damage" damage level
        - "('Tile', 'B. Affected (1-9%)')": Count of "Tile" roof type with "Affect (1-9%)" damage level.
        - "('Tile', 'C. Minor (10-25%)')": Count of "Tile" roof type with "Minor (10-25%)" damage level.
        - "('Tile', 'D. Major (26-50%)')": Count of "Tile" roof type with "Major (26-50%)" damage level.
        - "('Tile', 'E. Destroyed (>50%)')": Count of "Tile" roof type with "Destroyed (>50%)" damage level.
        - "('Unknown', 'A. No Damage')": Count of "Unknown" roof type with "no damage" damage level.
        - "('Unknown', 'B. Affected (1-9%)')": Count of "Unknown" roof type with "Affect (1-9%)" damage level.
        - "('Unknown', 'C. Minor (10-25%)')": Count of "Unknown" roof type with "Minor (10-25%)" damage level.
        - "('Unknown', 'D. Major (26-50%)')": Count of "Unknown" roof type with "Major (26-50%)" damage level.
        - "('Unknown', 'E. Destroyed (>50%)')": Count of "Unknown" roof type with "Destroyed (>50%)" damage level.
        - "('Wood', 'A. No Damage')": Count of "Wood" roof type with "no damage" damage level.
        - "('Wood', 'B. Affected (1-9%)')": Count of "Wood" roof type with "Affect (1-9%)" damage level.
        - "('Wood', 'C. Minor (10-25%)')": Count of "Wood" roof type with "Minor (10-25%)" damage level.
        - "('Wood', 'D. Major (26-50%)')": Count of "Wood" roof type with "Major (26-50%)" damage level.
        - "('Wood', 'E. Destroyed (>50%)')": Count of "Wood" roof type with "Destroyed (>50%)" damage level.
        - "A. Single Residence": Count of "Single Residence" damaged by wildfire.
        - "B. Multiple Residence": Count of "Multiple Residence" damaged by wildfire.
        - "C. Mixed Commercial/Residential": Count of "Mixed Commercial/Residential" damaged by wildfire.
        - "D. Nonresidential Commercial": Count of "Nonresidential Commercial" damaged by wildfire.
        - "E. Infrastructure": Count of "Infrastructure" damaged by wildfire.
        - "F. Agriculture": Count of "Agriculture" damaged by wildfire.
        - "G. Other Minor Structure": Count of "Other Minor Structure" damaged by wildfire.
        - "Incident Name": Incident name of the wildfire.
        - "Year": Year of the wildfire occurance.
        - "County": The county where the wildfire occurred.
        - "Total Economic Loss": Total economic loss caused by the wildfire.
    Returns
    -------
    alt.Chart
        An Altair donut chart visualizing the count of each damage category.
    Examples
    -------
    >>> make_damage_chart(calfire_df)
    """
    alt.data_transformers.enable("vegafusion")

    damage_table = pd.DataFrame(calfire_df.columns[:47].to_list(), columns=[ "Roof Construction", "Damage Category"])

    damage_count = pd.DataFrame(calfire_df.iloc[:, :47].sum(axis=0).values, columns=["Count"])

    calfire_damage = (pd.concat([damage_table, damage_count], axis=1)
                      .groupby(['Damage Category'])['Count']
                      .sum().reset_index(name="Count"))

    damage_chart = alt.Chart(calfire_damage).mark_arc(innerRadius=50).encode(
    theta="Count",
    color=alt.Color("Damage Category:N",
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
    tooltip=["Damage Category:O", "Count:Q"]).properties(
        width='container',
        height=200
    )

    return damage_chart