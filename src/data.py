import pandas as pd
import geopandas as gpd

# Load wildfire data
calfire_df = pd.read_csv("data/processed/cleaned_cal_fire.csv")

calfire_df["Incident Start Date"] = pd.to_datetime(calfire_df["Incident Start Date"], format="%m/%d/%Y %I:%M:%S %p")

# Load geojson file
geojson_file_path = "data/raw/California_County_Boundaries.geojson"
county_boundaries = gpd.read_file(geojson_file_path)[["CountyName", "geometry"]]
county_boundaries["CountyName"] = county_boundaries["CountyName"].str.strip()