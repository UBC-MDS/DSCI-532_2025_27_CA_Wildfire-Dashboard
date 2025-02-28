import pandas as pd

def load_calfire_df():
    '''
    Imports the CAL FIRE Damage Inspection (DINS) Data CSV from data folder and converts it to a Pandas DataFrame and saves it in data folder. Also applies some simple data cleaning.

    Usage:
    from data_import import load_calfire_df
    load_calfire_df()
    '''    

    csv_file_path = '../data/raw/California_wildfire_2013-2025.csv'
    calfire_df = pd.read_csv(csv_file_path)

    columns = ['* Damage', '* City', 'County', '* Incident Name', 'Incident Number (e.g. CAAEU 123456)', 'Incident Start Date', '* Structure Type',
       'Structure Category', '* Roof Construction', '* Eaves', '* Vent Screen', '* Exterior Siding', '* Window Pane',
       '* Deck/Porch On Grade', '* Deck/Porch Elevated', '* Patio Cover/Carport Attached to Structure',
       '* Fence Attached to Structure', 'Distance - Propane Tank to Structure',
       'Distance - Residence to Utility/Misc Structure &gt; 120 SQFT', 'Fire Name (Secondary)',
       'Assessed Improved Value (parcel)', 'Year Built (parcel)']
    
    # Selecting relevant columns
    calfire_df = calfire_df[columns]

    # Minor data cleaning
    calfire_df.loc[calfire_df["* City"].isin(["A", "#31"]), "* City"] = "Other"
    calfire_df.loc[calfire_df["* Damage"] == "Inaccessible", "* Damage"] = "Unknown"

    new_columns = ["Damage", "City", "County", "Incident Name", "Incident Number", "Incident Start Date", "Structure Type", "Structure Category",
                    "Roof Construction", "Eaves", "Vent Screen", "Exterior Siding", 'Window Pane',
        'Deck/Porch On Grade', 'Deck/Porch Elevated',
        'Patio Cover/Carport Attached to Structure',
        'Fence Attached to Structure', 'Distance - Propane Tank to Structure',
        'Distance - Residence to Utility/Misc Structure',
        'Fire Name (Secondary)',
        'Assessed Improved Value', 'Year Built']

    # Renaming columns
    calfire_df.columns = new_columns

    # Save cleaned up dataframe into data folder
    calfire_df.to_csv('../data/processed/cleaned_cal_fire.csv', index=False)