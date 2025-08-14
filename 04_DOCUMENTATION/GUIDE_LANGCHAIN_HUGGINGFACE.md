# 🤖 Guide Chatbot LangChain + HuggingFace

## 📋 **Vue d'Ensemble**

Ce guide vous explique comment utiliser le **chatbot avancé** intégrant **LangChain** et **HuggingFace** pour des recommandations Airbnb intelligentes.

### 🎯 **Fonctionnalités Principales**
- **🧠 Mémoire conversationnelle** : Se souvient du contexte
- **🔍 RAG (Retrieval-Augmented Generation)** : Recherche dans une base de connaissances
- **🤗 Modèles HuggingFace** : Utilise des modèles de langage pré-entraînés
- **🎨 Interface Gradio** : Interface web interactive
- **📊 Métriques de performance** : Évaluation automatique

---

## 📦 **Installation**

### **1. Dépendances Requises**
```bash
# Installation complète
pip install -r 05_CONFIGURATION/requirements.txt

# Ou installation manuelle des composants LangChain
pip install langchain langchain-community langchain-huggingface
pip install transformers torch sentence-transformers
pip install faiss-cpu chromadb gradio
```

### **2. Vérification de l'Installation**
```python
# Test rapide
python -c "import langchain, transformers, gradio; print('✅ Toutes les dépendances installées')"
```

---

## 🚀 **Utilisation**

### **Option 1 : Notebook Jupyter (Recommandé)**
```bash
# Lancer Jupyter
jupyter notebook 03_CHATBOT/notebooks/chatbot_langchain_huggingface.ipynb
```

**Avantages :**
- Interface interactive complète
- Visualisation des résultats
- Tests étape par étape
- Documentation intégrée

### **Option 2 : Script Python**
```bash
# Exécution directe
python 03_CHATBOT/scripts/chatbot_langchain_advanced.py
```

**Avantages :**
- Exécution rapide
- Mode production
- Interface Gradio automatique

---

## 💬 **Exemples d'Utilisation**

### **Questions Types Supportées**

#### **🏖️ Destinations**
```
"Que peux-tu me dire sur Hammamet ?"
"Quels sont les avantages de Jerba ?"
"Compare Hammamet et Jerba pour moi"
```

#### **👨‍👩‍👧‍👦 Recommandations Familiales**
```
"Je voyage avec ma famille, que me conseilles-tu ?"
"Hébergements avec piscine pour enfants ?"
"Villas familiales à Hammamet ?"
```

#### **💑 Recommandations Couples**
```
"Hébergements romantiques pour couple ?"
"Riads avec terrasse privée ?"
"Appartements vue sur mer ?"
```

#### **📅 Conseils Voyage**
```
"Quelle est la meilleure période pour visiter ?"
"Conseils pour éviter la haute saison ?"
"Météo en avril à Jerba ?"
```

---

## 🧠 **Architecture Technique**

### **Composants Principaux**

#### **1. LangChain Framework**
- Chaîne conversationnelle avec mémoire
- Gestion automatique du contexte
- Intégration transparente avec HuggingFace

#### **2. Base de Connaissances FAISS**
- Documents vectorisés pour RAG
- Recherche sémantique rapide
- Embeddings multilingues

#### **3. Modèles HuggingFace**
- Pipeline de génération de texte
- Support multiple modèles
- Optimisation mémoire automatique

---

## 🎨 **Interface Gradio**

### **Fonctionnalités Interface**
- **💬 Chat en temps réel** : Conversation fluide
- **📊 Onglet statistiques** : Métriques d'utilisation
- **🗑️ Bouton effacer** : Reset de la conversation
- **💡 Exemples prédéfinis** : Questions suggérées

### **Lancement Interface**
```python
# Dans le notebook ou script
interface = create_gradio_interface(chatbot)
interface.launch(share=True, debug=True)
```

**URL d'accès :** `http://localhost:7860`

---

## 🔄 **Mode Fallback**

### **Fonctionnement Sans LangChain**
Si LangChain n'est pas disponible, le chatbot utilise un **mode dégradé** :

**Avantages du fallback :**
- ✅ Fonctionnement garanti même sans dépendances
- ✅ Réponses pertinentes basées sur mots-clés
- ✅ Transition transparente pour l'utilisateur

---

## 🚀 **Déploiement**

### **Option 1 : Local**
```bash
python 03_CHATBOT/scripts/chatbot_langchain_advanced.py
```

### **Option 2 : Hugging Face Spaces**
1. Créer un Space sur huggingface.co
2. Uploader les fichiers du projet
3. Configurer `app.py` avec le chatbot
4. Déploiement automatique

### **Option 3 : Streamlit Cloud**
```python
# Créer app_streamlit.py
import streamlit as st
from chatbot_langchain_advanced import AirbnbLangChainChatbot

chatbot = AirbnbLangChainChatbot()
# Interface Streamlit...
```

---

## 🐛 **Dépannage**

### **Problèmes Courants**

#### **Erreur : Module 'langchain' not found**
```bash
pip install langchain langchain-community langchain-huggingface
```

#### **Erreur : CUDA out of memory**
```python
# Forcer utilisation CPU
device = -1  # Au lieu de 0 pour GPU
```

#### **Modèle trop lent**
```python
# Utiliser modèle plus petit
chatbot = AirbnbLangChainChatbot(model_size='small')
```

---

## 📈 **Optimisations**

### **Performance**
- **Cache des embeddings** : Évite recalculs
- **Modèles quantifiés** : Réduction mémoire
- **Batch processing** : Traitement groupé

### **Qualité des Réponses**
- **Fine-tuning** : Adapter aux données Airbnb
- **Prompt engineering** : Optimiser les instructions
- **Feedback loop** : Apprentissage continu

---

## 🎯 **Prochaines Étapes**

### **Améliorations Suggérées**
1. **🔗 API Airbnb réelle** : Données en temps réel
2. **🌍 Support multilingue étendu** : Plus de langues
3. **📱 Application mobile** : Interface native
4. **🧪 A/B Testing** : Optimisation continue
5. **📊 Analytics avancés** : Métriques détaillées

### **Intégrations Possibles**
- **🗺️ Cartes interactives** : Visualisation géographique
- **💰 Comparateur de prix** : Analyse tarifaire
- **📸 Galerie photos** : Recommandations visuelles
- **⭐ Système de notation** : Feedback utilisateur

---

## 📞 **Support**

### **Ressources**
- **📚 Documentation LangChain** : [docs.langchain.com](https://docs.langchain.com)
- **🤗 HuggingFace Hub** : [huggingface.co](https://huggingface.co)
- **🎨 Gradio Docs** : [gradio.app](https://gradio.app)

### **Contact**
- **GitHub** : [@NakibIheb20](https://github.com/NakibIheb20)
- **Repository** : [systeme-recommandation-chatbot-airbnb](https://github.com/NakibIheb20/systeme-recommandation-chatbot-airbnb)

---

**🎉 Votre chatbot LangChain + HuggingFace est maintenant prêt à impressionner avec ses capacités d'IA avancées !**