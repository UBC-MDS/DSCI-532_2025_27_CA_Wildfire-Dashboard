import pandas as pd
import pickle

def load_calfire_df():
    '''
    Imports the CAL FIRE Damage Inspection (DINS) Data CSV from data folder and converts it to a Pandas DataFrame and saves it in data folder. Also applies some simple data cleaning.

    Usage:
    from data_import import load_calfire_df
    load_calfire_df()
    '''    

    relevant_columns = ["* Damage", "County", "* Incident Name", "Incident Start Date", "Structure Category", "* Roof Construction", "Assessed Improved Value (parcel)"]
    renamed_columns = ["Damage", "County", "Incident Name", "Incident Start Date", "Structure Category", "Roof Construction", "Assessed Improved Value"]

    csv_file_path = 'data/raw/California_wildfire_2013-2025.csv'
    calfire_df = pd.read_csv(csv_file_path, usecols=relevant_columns)
    calfire_df["Incident Start Date"] = pd.to_datetime(calfire_df["Incident Start Date"], format="%m/%d/%Y %I:%M:%S %p")
    # Reading file, selecting and renaming relevant columns

    # Rename columns
    calfire_df.columns = renamed_columns


    # Data cleaning

    ## General data cleaning
    calfire_df.loc[calfire_df["Damage"] == "Inaccessible", "Damage"] = None
    calfire_df.loc[calfire_df["Roof Construction"] == " ", "Roof Construction"] =  None

    calfire_df = calfire_df.dropna()

    ## For correct sorting of damage types. This is a workaround to an existing altair bug https://github.com/vega/vega-lite/issues/5366
    damage_rename = {
    "No Damage": "A. No Damage",
    "Affected (1-9%)": "B. Affected (1-9%)",
    "Minor (10-25%)": "C. Minor (10-25%)",
    "Major (26-50%)": "D. Major (26-50%)",
    "Destroyed (>50%)": "E. Destroyed (>50%)"
}

    ## For correct sorting of structure types.
    calfire_df["Damage_Renamed"] = calfire_df["Damage"].map(damage_rename)

    structure_rename = {
    "Single Residence": "A",
    "Multiple Residence": "B",
    "Mixed Commercial/Residential": "C",
    "Nonresidential Commercial": "D",
    "Infrastructure": "E",
    "Agriculture": "F",
    "Other Minor Structure": "G"
    }

    calfire_df["Structure_Renamed"] = calfire_df["Structure Category"].map(structure_rename)

    # Save processed dataframe into data folder
    calfire_df.to_csv('data/processed/processed_cal_fire.csv', index=False)


    # Global variables are created here (Should be updated whenever dataset is updated)
    counties = sorted(calfire_df["County"].dropna().unique())
    min_year = calfire_df['Incident Start Date'].min().year
    max_year = calfire_df['Incident Start Date'].max().year
    incidents = sorted(calfire_df["Incident Name"].dropna().unique())

    # Saving the global variables:
    with open('data/processed/global_vars.pkl', 'wb') as f:
        pickle.dump([counties, min_year, max_year, incidents], f)

if __name__ == '__main__':
    load_calfire_df()

    # columns = ['* Damage', '* City', 'County', '* Incident Name', 'Incident Number (e.g. CAAEU 123456)', 'Incident Start Date', '* Structure Type',
    #    'Structure Category', '* Roof Construction', '* Eaves', '* Vent Screen', '* Exterior Siding', '* Window Pane',
    #    '* Deck/Porch On Grade', '* Deck/Porch Elevated', '* Patio Cover/Carport Attached to Structure',
    #    '* Fence Attached to Structure', 'Distance - Propane Tank to Structure',
    #    'Distance - Residence to Utility/Misc Structure &gt; 120 SQFT', 'Fire Name (Secondary)',
    #    'Assessed Improved Value (parcel)', 'Year Built (parcel)']

    # renamed_columns = ["Damage", "City", "County", "Incident Name", "Incident Number", "Incident Start Date", "Structure Type", "Structure Category",
    #                 "Roof Construction", "Eaves", "Vent Screen", "Exterior Siding", 'Window Pane',
    #     'Deck/Porch On Grade', 'Deck/Porch Elevated',
    #     'Patio Cover/Carport Attached to Structure',
    #     'Fence Attached to Structure', 'Distance - Propane Tank to Structure',
    #     'Distance - Residence to Utility/Misc Structure',
    #     'Fire Name (Secondary)',
    #     'Assessed Improved Value', 'Year Built']

    # I'm keeping these as comments in case we find a use for one of these columns in the future so we can easily add them back in.