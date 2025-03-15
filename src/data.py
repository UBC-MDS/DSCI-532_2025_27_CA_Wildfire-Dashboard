import pandas as pd
import geopandas as gpd
import pickle

# Load wildfire data
with open('data/processed/processed_cal_fire.pkl', 'rb') as f:
    calfire_df = pickle.load(f)

# calfire_df["Incident Start Date"] = pd.to_datetime(calfire_df["Incident Start Date"], format="ISO8601") # Not needed for now

# Load geospatial and county data
with open('data/processed/county_boundaries.pkl', 'rb') as f:
    county_boundaries = pickle.load(f)