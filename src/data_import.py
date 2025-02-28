import pandas as pd

def load_calfire_df():
    '''
    Imports the CAL FIRE Damage Inspection (DINS) Data CSV from the California Open Data Portal and converts it to a Pandas DataFrame and returns it. Also applies some simple data cleaning.

    Returns: pandas dataframe

    Usage:
    from data_import import load_calfire_df
    calfire_df = load_calfire_df()
    '''    

    csv_url = 'https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::cal-fire-damage-inspection-dins-data.csv'
    calfire_df = pd.read_csv(csv_url)

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

    return calfire_df