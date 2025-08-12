# 📁 Organisation du Projet - Système de Recommandation & Chatbot

## 🏗️ Structure des Dossiers

```
📦 systéme_recommandation_and_chatbot/
├── 📁 01_DONNEES/                    # Toutes les données du projet
│   ├── 📁 raw/                       # Données brutes (datasets originaux)
│   ├── 📁 processed/                 # Données traitées intermédiaires
│   └── 📁 final/                     # Données finales prêtes à l'usage
│
├── 📁 02_SYSTEME_RECOMMANDATION/     # Système de recommandation
│   ├── 📁 notebooks/                 # Notebooks Jupyter d'analyse
│   └── 📁 scripts/                   # Scripts Python du système
│
├── 📁 03_CHATBOT/                    # Chatbot intelligent
│   ├── 📁 notebooks/                 # Interface Jupyter du chatbot
│   ├── 📁 scripts/                   # Scripts Python du chatbot
│   └── 📁 config/                    # Configuration du chatbot
│
├── 📁 04_DOCUMENTATION/              # Documentation complète
│
├── 📁 05_CONFIGURATION/              # Fichiers de configuration
│
├── 📁 06_TESTS/                      # Tests et validation
│
├── 📁 07_MODELES/                    # Modèles ML et matrices
│
├── 📁 08_RESULTATS/                  # Résultats et visualisations
│
├── 📁 venv/                          # Environnement virtuel Python
│
└── 📄 README_ORGANISATION.md         # Ce fichier d'organisation
```

---

## 📂 Détail des Dossiers

### 📁 01_DONNEES - Gestion des Données
```
01_DONNEES/
├── raw/                              # Données brutes
│   ├── dataset_airbnb-reviews-scraper_*.csv
│   └── dataset_airbnb-scraper_*.csv
├── processed/                        # Données intermédiaires
│   ├── all_reviews.csv
│   ├── all_reviews_df.csv
│   ├── all_reviews_with_*.csv
│   ├── listings.csv
│   ├── review_cleaned.csv
│   ├── users2.csv
│   └── reviews_with_users.json
└── final/                           # Données finales
    └── all_reviews_final.csv        # Dataset principal pour le chatbot
```

### 📁 02_SYSTEME_RECOMMANDATION - Système de Recommandation
```
02_SYSTEME_RECOMMANDATION/
├── notebooks/                       # Analyses et développement
│   ├── recommandationsystéme_final.ipynb
│   ├── recommandation_systeme_gatehouses.ipynb
│   ├── data_exploration.ipynb
│   └── data_preparation.ipynb
└── scripts/                         # Scripts de production
    ├── app.py                       # Application Flask
    └── fifa.py                      # Script utilitaire
```

### 📁 03_CHATBOT - Chatbot Intelligent
```
03_CHATBOT/
├── notebooks/                       # Interface interactive
│   └── chatbot_hebergement.ipynb   # Interface Jupyter du chatbot
├── scripts/                         # Scripts du chatbot
│   ├── chatbot_hebergement.py       # Script principal
│   └── demo_chatbot.py              # Démonstration
└── config/                          # Configuration
    └── config_chatbot.py            # Paramètres du chatbot
```

### 📁 04_DOCUMENTATION - Documentation
```
04_DOCUMENTATION/
├── README_CHATBOT.md                # Documentation technique du chatbot
├── GUIDE_UTILISATION.md             # Guide d'utilisation rapide
├── CHATBOT_RESUME.md                # Résumé exécutif
└── DOCUMENTATION_RAPPORT.md         # Rapport complet du projet
```

### 📁 05_CONFIGURATION - Configuration
```
05_CONFIGURATION/
├── requirements.txt                 # Dépendances Python
├── package.json                     # Configuration Node.js
└── package-lock.json               # Verrouillage des versions
```

### 📁 06_TESTS - Tests et Validation
```
06_TESTS/
├── test_chatbot.py                  # Tests du chatbot
└── test_final.py                    # Tests complets du système
```

### 📁 07_MODELES - Modèles et Matrices
```
07_MODELES/
├── knn_model.pkl                    # Modèle KNN
├── similarity_matrix_bert.npy       # Matrice de similarité BERT
├── user_item_matrix.pkl             # Matrice utilisateur-item
├── df_grouped.pkl                   # Données groupées
├── id_to_index.pkl                  # Mapping des IDs
└── metadata.pkl                     # Métadonnées des modèles
```

### 📁 08_RESULTATS - Résultats et Visualisations
```
08_RESULTATS/
└── avis_positifs_heatmap.html       # Visualisation des avis positifs
```

---

## 🚀 Comment Utiliser Cette Organisation

### 🎯 **Pour le Système de Recommandation**
1. **Données** : Utilisez `01_DONNEES/final/all_reviews_final.csv`
2. **Notebooks** : Ouvrez `02_SYSTEME_RECOMMANDATION/notebooks/`
3. **Application** : Lancez `02_SYSTEME_RECOMMANDATION/scripts/app.py`

### 🤖 **Pour le Chatbot**
1. **Interface Jupyter** : `03_CHATBOT/notebooks/chatbot_hebergement.ipynb`
2. **Script Console** : `03_CHATBOT/scripts/chatbot_hebergement.py`
3. **Configuration** : Modifiez `03_CHATBOT/config/config_chatbot.py`

### 📚 **Pour la Documentation**
- Consultez `04_DOCUMENTATION/` pour tous les guides et rapports

### 🧪 **Pour les Tests**
- Exécutez les scripts dans `06_TESTS/` pour valider le système

---

## 🔧 Commandes Utiles

### **Activation de l'environnement virtuel**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### **Installation des dépendances**
```bash
pip install -r 05_CONFIGURATION/requirements.txt
```

### **Lancement du chatbot**
```bash
# Interface console
python 03_CHATBOT/scripts/chatbot_hebergement.py

# Interface Jupyter
jupyter notebook 03_CHATBOT/notebooks/chatbot_hebergement.ipynb
```

### **Lancement du système de recommandation**
```bash
python 02_SYSTEME_RECOMMANDATION/scripts/app.py
```

---

## 📋 Avantages de Cette Organisation

### ✅ **Clarté**
- Chaque composant a son dossier dédié
- Séparation claire entre données, code et documentation

### ✅ **Maintenabilité**
- Structure logique et intuitive
- Facile à naviguer et comprendre

### ✅ **Évolutivité**
- Ajout facile de nouveaux composants
- Structure extensible

### ✅ **Collaboration**
- Organisation professionnelle
- Facile pour les nouveaux développeurs

---

## 🎯 Prochaines Étapes

1. **Vérifiez** que tous les chemins dans le code pointent vers les nouveaux emplacements
2. **Testez** le système avec la nouvelle organisation
3. **Mettez à jour** les imports si nécessaire
4. **Documentez** les changements spécifiques à votre équipe

---

**📁 Votre projet est maintenant parfaitement organisé et prêt pour le développement professionnel !**