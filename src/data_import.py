import pandas as pd

def load_calfire_df():
    '''
    Imports the CAL FIRE Damage Inspection (DINS) Data CSV from data folder and converts it to a Pandas DataFrame and saves it in data folder. Also applies some simple data cleaning.

    Usage:
    from data_import import load_calfire_df
    load_calfire_df()
    '''    

    relevant_columns = ["* Damage", "County", "Incident Number (e.g. CAAEU 123456)", "Incident Start Date", "Structure Category", "* Roof Construction", "Assessed Improved Value (parcel)"]
    renamed_columns = ["Damage", "County", "Incident Number", "Incident Start Date", "Structure Category", "Roof Construction", "Assessed Improved Value"]

    csv_file_path = 'data/raw/California_wildfire_2013-2025.csv'
    calfire_df = pd.read_csv(csv_file_path, usecols=relevant_columns)
    # Reading file, selecting and renaming relevant columns

    # Rename columns
    calfire_df.columns = renamed_columns


    # Minor data cleaning
    calfire_df.loc[calfire_df["Damage"] == "Inaccessible", "Damage"] = "Unknown"
    calfire_df.loc[calfire_df["Assessed Improved Value"].isna(), "Assessed Improved Value"] = 0
    calfire_df.loc[calfire_df["County"].isna(), "County"] =  "Unknown"
    calfire_df.loc[calfire_df["Roof Construction"].isna(), "Roof Construction"] =  "Unknown"
    calfire_df.loc[calfire_df["Roof Construction"] == " ", "Roof Construction"] =  "Unknown"

    # calfire_df.loc[calfire_df["City"].isin(["A", "#31"]), "City"] = "Other" # Keeping this as a comment in case we use the city column in the future

    # Save cleaned up dataframe into data folder
    calfire_df.to_csv('data/processed/cleaned_cal_fire.csv', index=False)

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