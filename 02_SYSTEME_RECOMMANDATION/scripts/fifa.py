# Exemple de script de test pour all_reviews2

import pandas as pd

# Charge ton dataframe all_reviews2 (si ce n’est pas déjà fait)
all_reviews2 = pd.read_pickle('df_grouped.pkl')  # adapte si besoin

# Liste des id_listing qui te posent problème
id_listing_test = [30878168]  # tu peux en mettre plusieurs

for listing_id in id_listing_test:
    print(f"\nRecherche pour id_listing = {listing_id}:")
    
    subset = all_reviews2[all_reviews2["id_listing"] == listing_id]
    if subset.empty:
        print(" -> Aucun enregistrement trouvé pour cet id_listing.")
    else:
        print(f" -> {len(subset)} enregistrements trouvés.")
        print("Colonnes disponibles :", list(subset.columns))
        print("Exemple de données (première ligne) :")
        print(subset.iloc[0].to_dict())
        
        # Vérifie s’il y a des reviews positives
        positive_reviews = subset[subset["sentiment_bert"] == "positive"]["localizedText"].dropna()
        print(f"Nombre de reviews positives: {len(positive_reviews)}")
        if len(positive_reviews) > 0:
            print("Exemple de review positive :", positive_reviews.iloc[0])
