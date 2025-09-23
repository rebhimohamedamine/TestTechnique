import os
import requests
import pandas as pd

# Dossier de sortie
output_dir = "../data/raw"
os.makedirs(output_dir, exist_ok=True)

# Liste des datasets à récupérer
datasets = [
    "que-faire-a-paris-",
    "plaques-commemoratives",
    "referentiel-archeologique-de-paris",
    "les-titres-les-plus-pretes-dans-les-bibliotheques-de-pret",
    "les-1000-titres-les-plus-reserves-dans-les-bibliotheques-de-pret",
    "postes-publics-des-bibliotheques-logiciels-disponibles",
    "postes-publics-des-bibliotheques",
    "statistiques-des-documents-numerises-des-bibliotheques-patrimoniales",
    "commission-du-vieux-paris-adresses-instruites",
    "lieux-de-tournage-a-paris",
    "tous-les-documents-des-bibliotheques-de-pret",
    "touspe3",
    "plaques_commemoratives_1939-1945"
]

# Fonction pour récupérer un dataset via l'API Open Data Paris
def fetch_dataset(dataset_id):
    print(f"Téléchargement du dataset : {dataset_id}")
    base_url = f"https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/{dataset_id}/records"
    params = {
        "offset": 0,
        "limit": 100,
        "timezone": "UTC",
        "include_links": False,
        "include_app_metas": False
    }
    all_results = []
    while True:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Erreur {response.status_code} pour {dataset_id}")
            break

        data = response.json()
        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)

        # Pagination
        params["offset"] += params["limit"]
        if params["offset"] >= data.get("total_count", 0):
            break

    if all_results:
        df = pd.json_normalize(all_results)
        output_file = os.path.join(output_dir, f"{dataset_id}.csv")
        df.to_csv(output_file, index=False)
        print(f"{len(df)} enregistrements sauvegardés dans {output_file}\n")
    else:
        print(f"Aucun enregistrement trouvé pour {dataset_id}\n")

# Récupération de tous les datasets
for ds in datasets:
    fetch_dataset(ds)
