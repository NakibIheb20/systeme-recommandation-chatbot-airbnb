#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Démarrage Rapide - Système de Recommandation & Chatbot
===============================================================

Ce script permet de lancer facilement les différents composants du projet
avec la nouvelle organisation des fichiers.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Affiche la bannière du projet"""
    banner = """
🏠 SYSTÈME DE RECOMMANDATION & CHATBOT AIRBNB
=============================================
    
🎯 Projet: Aide à la sélection d'hébergements
📊 Données: 14,629 avis analysés | 1,015 hébergements
🌍 Zones: Hammamet & Jerba, Tunisie
🤖 IA: Analyse de sentiment BERT + Recommandations hybrides
"""
    print(banner)

def show_menu():
    """Affiche le menu principal"""
    menu = """
🚀 QUE VOULEZ-VOUS LANCER ?

1️⃣  Chatbot - Interface Jupyter (Recommandé)
2️⃣  Chatbot - Console Interactive  
3️⃣  Système de Recommandation - Application Web
4️⃣  Démonstration du Chatbot
5️⃣  Tests du Système
6️⃣  Exploration des Données
7️⃣  Documentation
8️⃣  Configuration et Installation
9️⃣  Structure du Projet
0️⃣  Quitter

"""
    print(menu)

def launch_chatbot_jupyter():
    """Lance l'interface Jupyter du chatbot"""
    print("🚀 Lancement du Chatbot - Interface Jupyter...")
    notebook_path = "03_CHATBOT/notebooks/chatbot_hebergement.ipynb"
    
    if Path(notebook_path).exists():
        try:
            subprocess.run(["jupyter", "notebook", notebook_path], check=True)
        except subprocess.CalledProcessError:
            print("❌ Erreur: Jupyter n'est pas installé ou accessible")
            print("💡 Installez avec: pip install jupyter")
        except FileNotFoundError:
            print("❌ Erreur: Jupyter non trouvé dans le PATH")
    else:
        print(f"❌ Fichier non trouvé: {notebook_path}")

def launch_chatbot_console():
    """Lance le chatbot en console"""
    print("🚀 Lancement du Chatbot - Console Interactive...")
    script_path = "03_CHATBOT/scripts/chatbot_hebergement.py"
    
    if Path(script_path).exists():
        try:
            subprocess.run([sys.executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors du lancement: {e}")
    else:
        print(f"❌ Fichier non trouvé: {script_path}")

def launch_recommender_app():
    """Lance l'application web du système de recommandation"""
    print("🚀 Lancement du Système de Recommandation...")
    script_path = "02_SYSTEME_RECOMMANDATION/scripts/app.py"
    
    if Path(script_path).exists():
        try:
            subprocess.run([sys.executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors du lancement: {e}")
    else:
        print(f"❌ Fichier non trouvé: {script_path}")

def launch_demo():
    """Lance la démonstration du chatbot"""
    print("🚀 Lancement de la Démonstration...")
    script_path = "03_CHATBOT/scripts/demo_chatbot.py"
    
    if Path(script_path).exists():
        try:
            subprocess.run([sys.executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors du lancement: {e}")
    else:
        print(f"❌ Fichier non trouvé: {script_path}")

def run_tests():
    """Lance les tests du système"""
    print("🧪 Lancement des Tests...")
    
    test_files = [
        "06_TESTS/test_chatbot.py",
        "06_TESTS/test_final.py"
    ]
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"\n🔍 Test: {test_file}")
            try:
                subprocess.run([sys.executable, test_file], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Erreur dans {test_file}: {e}")
        else:
            print(f"❌ Test non trouvé: {test_file}")

def explore_data():
    """Lance l'exploration des données"""
    print("📊 Exploration des Données...")
    notebook_path = "02_SYSTEME_RECOMMANDATION/notebooks/data_exploration.ipynb"
    
    if Path(notebook_path).exists():
        try:
            subprocess.run(["jupyter", "notebook", notebook_path], check=True)
        except subprocess.CalledProcessError:
            print("❌ Erreur: Jupyter n'est pas installé")
        except FileNotFoundError:
            print("❌ Erreur: Jupyter non trouvé")
    else:
        print(f"❌ Fichier non trouvé: {notebook_path}")

def show_documentation():
    """Affiche la documentation disponible"""
    print("📚 DOCUMENTATION DISPONIBLE")
    print("=" * 40)
    
    docs = [
        ("README_ORGANISATION.md", "Organisation du projet"),
        ("04_DOCUMENTATION/README_CHATBOT.md", "Documentation technique du chatbot"),
        ("04_DOCUMENTATION/GUIDE_UTILISATION.md", "Guide d'utilisation rapide"),
        ("04_DOCUMENTATION/CHATBOT_RESUME.md", "Résumé exécutif"),
        ("04_DOCUMENTATION/DOCUMENTATION_RAPPORT.md", "Rapport complet")
    ]
    
    for doc_file, description in docs:
        if Path(doc_file).exists():
            print(f"✅ {doc_file} - {description}")
        else:
            print(f"❌ {doc_file} - Non trouvé")
    
    print("\n💡 Ouvrez ces fichiers avec votre éditeur de texte préféré")

def show_config():
    """Affiche les informations de configuration"""
    print("⚙️  CONFIGURATION ET INSTALLATION")
    print("=" * 40)
    
    # Vérification de l'environnement virtuel
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Environnement virtuel activé")
    else:
        print("⚠️  Environnement virtuel non activé")
        print("💡 Activez avec: venv\\Scripts\\activate (Windows)")
    
    # Vérification des dépendances
    req_file = "05_CONFIGURATION/requirements.txt"
    if Path(req_file).exists():
        print(f"✅ Fichier de dépendances trouvé: {req_file}")
        print("💡 Installez avec: pip install -r 05_CONFIGURATION/requirements.txt")
    else:
        print("❌ Fichier requirements.txt non trouvé")
    
    # Vérification du dataset principal
    dataset = "01_DONNEES/final/all_reviews_final.csv"
    if Path(dataset).exists():
        print(f"✅ Dataset principal trouvé: {dataset}")
    else:
        print(f"❌ Dataset principal non trouvé: {dataset}")

def show_structure():
    """Affiche la structure du projet"""
    print("📁 STRUCTURE DU PROJET")
    print("=" * 40)
    
    structure = """
📦 systéme_recommandation_and_chatbot/
├── 📁 01_DONNEES/                    # Données du projet
│   ├── 📁 raw/                       # Données brutes
│   ├── 📁 processed/                 # Données traitées
│   └── 📁 final/                     # Données finales
├── 📁 02_SYSTEME_RECOMMANDATION/     # Système de recommandation
│   ├── 📁 notebooks/                 # Notebooks d'analyse
│   └── 📁 scripts/                   # Scripts Python
├── 📁 03_CHATBOT/                    # Chatbot intelligent
│   ├── 📁 notebooks/                 # Interface Jupyter
│   ├── 📁 scripts/                   # Scripts du chatbot
│   └── 📁 config/                    # Configuration
├── 📁 04_DOCUMENTATION/              # Documentation
├── 📁 05_CONFIGURATION/              # Configuration projet
├── 📁 06_TESTS/                      # Tests et validation
├── 📁 07_MODELES/                    # Modèles ML
└── 📁 08_RESULTATS/                  # Résultats et visualisations
"""
    print(structure)

def main():
    """Fonction principale"""
    print_banner()
    
    while True:
        show_menu()
        
        try:
            choice = input("👉 Votre choix (0-9): ").strip()
            
            if choice == "1":
                launch_chatbot_jupyter()
            elif choice == "2":
                launch_chatbot_console()
            elif choice == "3":
                launch_recommender_app()
            elif choice == "4":
                launch_demo()
            elif choice == "5":
                run_tests()
            elif choice == "6":
                explore_data()
            elif choice == "7":
                show_documentation()
            elif choice == "8":
                show_config()
            elif choice == "9":
                show_structure()
            elif choice == "0":
                print("👋 Au revoir ! Merci d'avoir utilisé le système.")
                break
            else:
                print("❌ Choix invalide. Veuillez sélectionner un nombre entre 0 et 9.")
            
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrompue. Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()