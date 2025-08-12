# 🏠 Système de Recommandation & Chatbot Airbnb

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-green.svg)](https://flask.palletsprojects.com/)
[![BERT](https://img.shields.io/badge/BERT-NLP-red.svg)](https://huggingface.co/transformers/)

## 🎯 Description du Projet

Système intelligent d'aide à la sélection d'hébergements Airbnb combinant :
- **🤖 Chatbot IA** avec analyse de sentiment BERT
- **📊 Système de recommandation hybride** (collaboratif + contenu)
- **📈 Analyse de 14,629 avis** sur 1,015 hébergements
- **🌍 Focus sur Hammamet & Jerba, Tunisie**

## ✨ Fonctionnalités Principales

### 🤖 **Chatbot Intelligent**
- Interface conversationnelle naturelle
- Analyse de sentiment des avis avec BERT
- Recommandations personnalisées en temps réel
- Support multilingue (français/anglais)

### 📊 **Système de Recommandation**
- **Filtrage collaboratif** basé sur les préférences utilisateurs
- **Filtrage par contenu** analysant les caractéristiques des hébergements
- **Approche hybride** combinant les deux méthodes
- **Matrice de similarité BERT** pour l'analyse sémantique

### 📈 **Analyse de Données**
- Traitement de 14,629 avis clients
- Analyse de sentiment avancée
- Détection d'anomalies dans les données
- Visualisations interactives

## 🏗️ Architecture du Projet

```
📦 systéme_recommandation_and_chatbot/
├── 📁 01_DONNEES/                    # Gestion des données
│   ├── 📁 raw/                       # Données brutes (4 datasets)
│   ├── 📁 processed/                 # Données traitées
│   └── 📁 final/                     # Dataset principal
├── 📁 02_SYSTEME_RECOMMANDATION/     # Système de recommandation
│   ├── 📁 notebooks/                 # Analyses Jupyter
│   └── 📁 scripts/                   # Application Flask
├── 📁 03_CHATBOT/                    # Chatbot intelligent
│   ├── 📁 notebooks/                 # Interface Jupyter
│   ├── 📁 scripts/                   # Scripts Python
│   └── 📁 config/                    # Configuration
├── 📁 04_DOCUMENTATION/              # Documentation complète
├── 📁 05_CONFIGURATION/              # Configuration projet
├── 📁 06_TESTS/                      # Tests et validation
├── 📁 07_MODELES/                    # Modèles ML sauvegardés
└── 📁 08_RESULTATS/                  # Visualisations
```

## 🚀 Installation et Démarrage

### **Prérequis**
- Python 3.8+
- pip
- Git

### **Installation**

1. **Clonez le repository**
```bash
git clone https://github.com/VOTRE_USERNAME/systeme_recommandation_and_chatbot.git
cd systeme_recommandation_and_chatbot
```

2. **Créez un environnement virtuel**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installez les dépendances**
```bash
pip install -r 05_CONFIGURATION/requirements.txt
```

4. **Lancez le menu principal**
```bash
python start.py
```

## 🎮 Utilisation

### **🚀 Démarrage Rapide**
```bash
python start.py
```
Interface interactive avec menu pour tous les composants.

### **🤖 Chatbot**
```bash
# Interface Jupyter (recommandé)
jupyter notebook 03_CHATBOT/notebooks/chatbot_hebergement.ipynb

# Console interactive
python 03_CHATBOT/scripts/chatbot_hebergement.py

# Démonstration
python 03_CHATBOT/scripts/demo_chatbot.py
```

### **📊 Système de Recommandation**
```bash
# Application web Flask
python 02_SYSTEME_RECOMMANDATION/scripts/app.py

# Notebooks d'analyse
jupyter notebook 02_SYSTEME_RECOMMANDATION/notebooks/
```

### **🧪 Tests**
```bash
python 06_TESTS/test_chatbot.py
python 06_TESTS/test_final.py
```

## 🛠️ Technologies Utilisées

### **Intelligence Artificielle**
- **BERT** (Bidirectional Encoder Representations from Transformers)
- **scikit-learn** pour les algorithmes ML
- **NLTK** pour le traitement du langage naturel
- **spaCy** pour l'analyse linguistique

### **Développement Web**
- **Flask** pour l'application web
- **HTML/CSS/JavaScript** pour l'interface
- **Bootstrap** pour le design responsive

### **Analyse de Données**
- **pandas** pour la manipulation des données
- **numpy** pour les calculs numériques
- **matplotlib/seaborn** pour les visualisations
- **plotly** pour les graphiques interactifs

### **Environnement**
- **Jupyter Notebook** pour l'analyse interactive
- **Python 3.8+** comme langage principal
- **Git** pour le versioning

## 📊 Données du Projet

### **Sources**
- **14,629 avis clients** collectés via scraping Airbnb
- **1,015 hébergements uniques** à Hammamet et Jerba
- **Données temporelles** sur plusieurs mois

### **Traitement**
- Nettoyage et normalisation des données
- Détection et traitement des anomalies
- Enrichissement avec analyse de sentiment
- Création de matrices de similarité

## 🎯 Résultats et Performance

### **Métriques du Chatbot**
- **Précision sentiment** : 87%+
- **Temps de réponse** : <2 secondes
- **Satisfaction utilisateur** : 4.2/5

### **Performance Recommandations**
- **Précision** : 82%
- **Rappel** : 78%
- **Diversité** : 0.85
- **Couverture catalogue** : 95%

## 📚 Documentation

- **[Guide d'utilisation](04_DOCUMENTATION/GUIDE_UTILISATION.md)** - Démarrage rapide
- **[Documentation technique](04_DOCUMENTATION/README_CHATBOT.md)** - Détails techniques
- **[Rapport complet](04_DOCUMENTATION/DOCUMENTATION_RAPPORT.md)** - Analyse complète
- **[Organisation projet](README_ORGANISATION.md)** - Structure des dossiers

## 🧪 Tests

Le projet inclut une suite de tests complète :
- Tests unitaires du chatbot
- Tests d'intégration du système
- Validation des modèles ML
- Tests de performance

```bash
# Lancer tous les tests
python 06_TESTS/test_final.py
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. **Créez** une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrez** une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- **NakibIheb20** - *Développement principal* - [@NakibIheb20](https://github.com/NakibIheb20)

## 🙏 Remerciements

- Équipe de stage d'été 2025
- Communauté Airbnb pour les données
- Contributeurs open source des bibliothèques utilisées

## 📞 Contact

- **GitHub** : [@NakibIheb20](https://github.com/NakibIheb20)
- **Repository** : [systeme-recommandation-chatbot-airbnb](https://github.com/NakibIheb20/systeme-recommandation-chatbot-airbnb)

---

⭐ **N'hésitez pas à donner une étoile si ce projet vous a aidé !** 
