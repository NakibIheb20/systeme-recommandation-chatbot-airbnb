# 📊 Données du Projet - Système de Recommandation & Chatbot Airbnb

## 🚨 **Note Importante**

Les fichiers de données volumineux (CSV) ne sont pas inclus dans ce repository GitHub pour des raisons de taille. 

### 📈 **Statistiques des Données**

- **14,629 avis clients** analysés
- **1,015 hébergements uniques** 
- **Zones géographiques** : Hammamet & Jerba, Tunisie
- **Période** : Données collectées en juillet 2025
- **Taille totale** : ~280 MB de données CSV

### 📁 **Structure des Données**

#### **📂 raw/** - Données Brutes
```
dataset_airbnb-scraper_hammamet_2025-07-13_23-14-54-881.csv
dataset_airbnb-scraper_jerba_2025-07-14_09-40-14-380.csv  
dataset_airbnb-reviews-scraper_2025-07-13_23-48-03-281.csv
dataset_airbnb-reviews-scraper_jerba_2025-07-14_09-56-44-640.csv
```

#### **📂 processed/** - Données Traitées
```
all_reviews.csv                    # Tous les avis consolidés
all_reviews_df.csv                 # DataFrame structuré
all_reviews_with_anomalies.csv     # Avec détection d'anomalies
all_reviews_with_listings.csv      # Enrichi avec infos hébergements
listings.csv                       # Informations hébergements
review_cleaned.csv                 # Avis nettoyés
users2.csv                         # Données utilisateurs
reviews_with_users.json            # Format JSON enrichi
```

#### **📂 final/** - Données Finales
```
all_reviews_final.csv              # Dataset principal pour le chatbot
```

### 🔄 **Comment Obtenir les Données**

#### **Option 1 : Génération Automatique**
Les scripts du projet peuvent régénérer les données :
```bash
# Lancer le système de recommandation
python 02_SYSTEME_RECOMMANDATION/scripts/app.py

# Ou utiliser les notebooks d'analyse
jupyter notebook 02_SYSTEME_RECOMMANDATION/notebooks/
```

#### **Option 2 : Données d'Exemple**
Pour tester le système, vous pouvez créer des données d'exemple :
```python
import pandas as pd

# Créer un dataset d'exemple
sample_data = {
    'review_id': range(1, 101),
    'listing_id': [f'listing_{i%20}' for i in range(100)],
    'reviewer_name': [f'User_{i}' for i in range(100)],
    'review_text': ['Great place to stay!'] * 100,
    'rating': [4.5] * 100,
    'sentiment_score': [0.8] * 100
}

df = pd.DataFrame(sample_data)
df.to_csv('01_DONNEES/final/all_reviews_final.csv', index=False)
```

#### **Option 3 : Contact**
Pour obtenir les données complètes, contactez l'auteur du projet.

### 🛠️ **Traitement des Données**

Le projet inclut des scripts complets pour :
- **Collecte** via scraping Airbnb
- **Nettoyage** et normalisation
- **Enrichissement** avec analyse de sentiment BERT
- **Détection d'anomalies**
- **Création de matrices** de similarité

### 📋 **Format des Données**

#### **Colonnes Principales**
```
review_id          : Identifiant unique de l'avis
listing_id         : Identifiant de l'hébergement  
reviewer_name      : Nom du reviewer
review_text        : Texte de l'avis
rating            : Note donnée (1-5)
sentiment_score   : Score de sentiment BERT (-1 à 1)
location          : Localisation (Hammamet/Jerba)
price             : Prix par nuit
amenities         : Équipements disponibles
host_info         : Informations sur l'hôte
```

### 🔒 **Confidentialité**

- Toutes les données personnelles ont été anonymisées
- Seules les informations publiques Airbnb sont utilisées
- Respect des conditions d'utilisation des plateformes

### 📞 **Support**

Pour toute question sur les données :
- Consultez la documentation dans `04_DOCUMENTATION/`
- Utilisez les notebooks d'exploration dans `02_SYSTEME_RECOMMANDATION/notebooks/`
- Contactez l'équipe de développement

---

**💡 Ce projet démontre les capacités d'analyse même sans les données complètes grâce à sa structure modulaire et ses scripts de génération.**