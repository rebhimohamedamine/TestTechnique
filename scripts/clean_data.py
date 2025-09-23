import pandas as pd
import os

# List of dataset filenames
datasets = [
    "commission-du-vieux-paris-adresses-instruites.csv",
    "les-1000-titres-les-plus-reserves-dans-les-bibliotheques-de-pret.csv",
    "les-titres-les-plus-pretes.csv",
    "lieux-de-tournage-a-paris.csv",
    "plaques_commemoratives_1939-1945.csv",
    "plaques_commemoratives.csv",
    "postes-publics-des-bibliotheques.csv",
    "postes-publics-logiciels-disponibles.csv",
    "que-faire-a-paris-.csv",
    "referentiel-archeologique-de-paris.csv",
    "statistiques-des-documents-numerises-des-bibliotheques-patrimoniales.csv",
    "tous-les-documents-des-bibliotheques-de-pret.csv",
    "touspe3.csv"
]

input_dir = "../data/raw"
output_dir = "../data/cleaned"
os.makedirs(output_dir, exist_ok=True)
input_path = '../data/raw/que-faire-a-paris-.csv'
output_path = '../data/cleaned/que-faire-a-paris-.csv'

def clean_que_faire_a_paris(input_path, output_path):
    df = pd.read_csv(input_path)
    # Remove duplicate rows
    df = df.drop_duplicates()
    # Remove columns with all missing values
    df = df.dropna(axis=1, how='all')
    # Remove rows missing geospatial data
    df = df.dropna(subset=['lat_lon.lat', 'lat_lon.lon'])
    # Remove rows with out-of-range coordinates (Paris bounds)
    df = df[(df['lat_lon.lat'] >= 48.8) & (df['lat_lon.lat'] <= 48.9) &
            (df['lat_lon.lon'] >= 2.25) & (df['lat_lon.lon'] <= 2.42)]
    # Remove events not in Paris (zip code not starting with '75')
    df['address_zipcode'] = df['address_zipcode'].astype(str).str.strip()
    df = df[df['address_zipcode'].str.startswith('75')]
    # Standardize address columns
    df['address_street'] = df['address_street'].str.lower().str.strip()
    df['address_city'] = df['address_city'].str.lower().str.strip()
    # Fill remaining missing values with empty string
    df = df.fillna("")
    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to {output_path}")

clean_que_faire_a_paris(input_path, output_path)