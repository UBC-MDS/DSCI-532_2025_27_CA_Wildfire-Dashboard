import pandas as pd
import json
import urllib.request

def load_calfire_df():
    '''
    Imports the CAL FIRE Damage Inspection (DINS) Data CSV from the California Open Data Portal and converts it to a Pandas DataFrame and returns it. Also applies some simple data cleaning.

    Returns: pandas dataframe

    Usage:
    from data_import import load_calfire_df
    calfire_df = load_calfire_df()
    '''    

    url = 'https://data.ca.gov/api/3/action/datastore_search?resource_id=b8aeb030-140d-43d2-aa29-1a80862e3d62'  
    fileobj = urllib.request.urlopen(url)
    response_dict = json.loads(fileobj.read())
    calfire_df = pd.DataFrame(response_dict["result"]["records"])

    columns = ['* Damage', '* City', 'County', '* Incident Name', 'Incident Number (e.g. CAAEU 123456)', 'Incident Start Date', '* Structure Type',
       'Structure Category',  '* Eaves', '* Vent Screen', '* Exterior Siding', '* Window Pane',
       '* Deck/Porch On Grade', '* Deck/Porch Elevated',
       '* Patio Cover/Carport Attached to Structure',
       '* Fence Attached to Structure', 'Distance - Propane Tank to Structure',
       'Distance - Residence to Utility/Misc Structure &gt; 120 SQFT',
       'Fire Name (Secondary)', 'APN (parcel)',
       'Assessed Improved Value (parcel)', 'Year Built (parcel)']
    
    # Selecting relevant columns
    calfire_df = calfire_df[columns]

    # Minor data cleaning
    calfire_df.loc[calfire_df["* City"].isin(["A", "#31"]), "* City"] = "Other"
    calfire_df.loc[calfire_df["* Damage"] == "Inaccessible", "* Damage"] = "Unknown"

    new_columns = ["Damage", "City", "County", "Incident Name", "Incident Number", "Incident Start Date", "Structure Type", "Structure Category",
                    "Eaves", "Vent Screen", "Exterior Siding", 'Window Pane',
        'Deck/Porch On Grade', 'Deck/Porch Elevated',
        'Patio Cover/Carport Attached to Structure',
        'Fence Attached to Structure', 'Distance - Propane Tank to Structure',
        'Distance - Residence to Utility/Misc Structure',
        'Fire Name (Secondary)', 'APN',
        'Assessed Improved Value', 'Year Built']

    # Renaming columns
    calfire_df.columns = new_columns

    return calfire_df

df = load_calfire_df()

df.to_csv("data/raw/California_Wildfire.csv", index=False)
