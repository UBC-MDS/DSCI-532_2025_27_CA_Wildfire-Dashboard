import pandas as pd

def load_calfire_df():
    '''
    Imports the CAL FIRE Damage Inspection (DINS) Data CSV from data folder and converts it to a Pandas DataFrame and saves it in data folder. Also applies some simple data cleaning.

    Usage:
    from data_import import load_calfire_df
    load_calfire_df()
    '''    

    csv_file_path = '../data/raw/CAL_FIRE_Damage_Inspection_(DINS)_Data.csv'
    calfire_df = pd.read_csv(csv_file_path)

    columns = ['DAMAGE', 'CITY', 'COUNTY', 'INCIDENTNAME', 'INCIDENTNUM', 'INCIDENTSTARTDATE', 'STRUCTURETYPE',
       'STRUCTURECATEGORY', 'ROOFCONSTRUCTION', 'EAVES', 'VENTSCREEN', 'EXTERIORSIDING', 'WINDOWPANE',
       'DECKPORCHONGRADE', 'DECKPORCHELEVATED', 'PATIOCOVERCARPORT',
       'FENCEATTACHEDTOSTRUCTURE', 'PROPANETANKDISTANCE',
       'UTILITYMISCSTRUCTUREDISTANCE', 'FIRENAME',
       'ASSESSEDIMPROVEDVALUE', 'YEARBUILT']
    
    # Selecting relevant columns
    calfire_df = calfire_df[columns]

    # Minor data cleaning
    calfire_df.loc[calfire_df["CITY"].isin(["A", "#31"]), "CITY"] = "Other"
    calfire_df.loc[calfire_df["DAMAGE"] == "Inaccessible", "DAMAGE"] = "Unknown"

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