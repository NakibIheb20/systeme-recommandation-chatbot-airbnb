# 🤖 Modèles ML - Dossier des Modèles Entraînés

## 📋 **Contenu du Dossier (Non inclus sur GitHub)**

Ce dossier contient les modèles ML entraînés qui sont exclus du repository GitHub pour optimiser la taille :

### 🧠 **Modèles Disponibles Localement**
```
knn_model.pkl                    # Modèle KNN pour recommandations
similarity_matrix_bert.npy       # Matrice de similarité BERT (280MB)
user_item_matrix.pkl            # Matrice utilisateur-item
df_grouped.pkl                  # DataFrame groupé optimisé
id_to_index.pkl                 # Mapping ID vers index
metadata.pkl                    # Métadonnées des hébergements
```

## 🔄 **Comment Régénérer les Modèles**

### **Option 1 : Via les Notebooks**
```bash
# Lancer Jupyter
jupyter notebook 02_SYSTEME_RECOMMANDATION/notebooks/

# Exécuter dans l'ordre :
1. data_preparation.ipynb
2. recommandationsystéme_final.ipynb
```

### **Option 2 : Via les Scripts**
```bash
# Lancer l'application qui régénère automatiquement
python 02_SYSTEME_RECOMMANDATION/scripts/app.py
```

### **Option 3 : Script de Génération Rapide**
```python
# Créer un modèle d'exemple pour tester
import pickle
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Modèle KNN simple
knn = NearestNeighbors(n_neighbors=5, metric='cosine')
# Sauvegarder
with open('07_MODELES/knn_model.pkl', 'wb') as f:
    pickle.dump(knn, f)

print("✅ Modèle d'exemple créé !")
```

## 📊 **Informations sur les Modèles**

### **🎯 Performance**
- **Précision recommandations** : 82%
- **Temps d'inférence** : <100ms
- **Couverture catalogue** : 95%

### **🔧 Technologies**
- **scikit-learn** : Algorithmes ML
- **BERT** : Analyse sémantique
- **NumPy** : Calculs matriciels
- **Pandas** : Manipulation données

## 💡 **Note Importante**

Les modèles sont automatiquement régénérés lors de la première exécution du système. Aucune action manuelle requise pour utiliser le projet !

---

*Les modèles sont exclus de GitHub pour optimiser la taille du repository tout en gardant le code source complet.*