import pandas as pd
import geopandas as gpd
import pickle

# Load wildfire data
# calfire_df = pd.read_csv("data/processed/processed_cal_fire.csv", parse_dates=["Incident Start Date"])
with open('data/processed/processed_cal_fire.pkl', 'rb') as f:
    calfire_df = pickle.load(f)

calfire_df["Incident Start Date"] = pd.to_datetime(calfire_df["Incident Start Date"], format="ISO8601") # check if needed

# Load geojson file
geojson_file_path = "data/raw/California_County_Boundaries.geojson"
county_boundaries = gpd.read_file(geojson_file_path)[["CountyName", "geometry"]]
county_boundaries["CountyName"] = county_boundaries["CountyName"].str.strip()
