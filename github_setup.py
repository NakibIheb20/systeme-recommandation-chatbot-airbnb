#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'Aide pour la Mise sur GitHub
====================================

Ce script vous guide pas à pas pour mettre votre projet sur GitHub.
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Affiche la bannière"""
    banner = """
🚀 ASSISTANT GITHUB - MISE EN LIGNE DE VOTRE PROJET
==================================================

Ce script va vous aider à mettre votre projet sur GitHub étape par étape.
"""
    print(banner)

def check_git_config():
    """Vérifie la configuration Git"""
    print("🔧 VÉRIFICATION DE LA CONFIGURATION GIT")
    print("=" * 50)
    
    try:
        # Vérifier le nom d'utilisateur
        result = subprocess.run(['git', 'config', 'user.name'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ Nom d'utilisateur Git : {result.stdout.strip()}")
        else:
            name = input("❓ Entrez votre nom pour Git : ")
            subprocess.run(['git', 'config', '--global', 'user.name', name])
            print(f"✅ Nom configuré : {name}")
        
        # Vérifier l'email
        result = subprocess.run(['git', 'config', 'user.email'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ Email Git : {result.stdout.strip()}")
        else:
            email = input("❓ Entrez votre email pour Git : ")
            subprocess.run(['git', 'config', '--global', 'user.email', email])
            print(f"✅ Email configuré : {email}")
            
    except FileNotFoundError:
        print("❌ Git n'est pas installé ou pas dans le PATH")
        return False
    
    return True

def show_github_instructions():
    """Affiche les instructions pour créer le repository GitHub"""
    instructions = """
🌐 CRÉATION DU REPOSITORY SUR GITHUB
===================================

1. 🌐 Allez sur https://github.com
2. 🔑 Connectez-vous à votre compte
3. ➕ Cliquez sur "New" ou "+" → "New repository"

4. 📝 Configuration du repository :
   ┌─────────────────────────────────────────────────┐
   │ Repository name: systeme-recommandation-chatbot │
   │ Description: 🏠 Système intelligent Airbnb     │
   │ ☑️ Public (recommandé pour portfolio)          │
   │ ☐ Add README (on a déjà le nôtre)             │
   │ ☐ Add .gitignore (on a déjà le nôtre)         │
   │ ☐ Choose license (on a déjà MIT)              │
   └─────────────────────────────────────────────────┘

5. 🚀 Cliquez "Create repository"

6. 📋 Copiez l'URL qui apparaît (ressemble à) :
   https://github.com/VOTRE_USERNAME/systeme-recommandation-chatbot.git
"""
    print(instructions)

def setup_github_remote():
    """Configure la connexion avec GitHub"""
    print("\n🔗 CONNEXION AVEC GITHUB")
    print("=" * 30)
    
    # Demander l'URL du repository
    repo_url = input("📋 Collez l'URL de votre repository GitHub : ").strip()
    
    if not repo_url:
        print("❌ URL vide. Opération annulée.")
        return False
    
    try:
        # Ajouter l'origine
        print("🔗 Ajout de l'origine GitHub...")
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
        print("✅ Origine ajoutée avec succès")
        
        # Renommer la branche
        print("🌿 Renommage de la branche en 'main'...")
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
        print("✅ Branche renommée")
        
        # Pousser vers GitHub
        print("🚀 Envoi du code vers GitHub...")
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("🎉 SUCCÈS ! Votre projet est maintenant sur GitHub !")
            print(f"🌐 Visitez : {repo_url.replace('.git', '')}")
            return True
        else:
            print(f"❌ Erreur lors du push : {result.stderr}")
            print("\n💡 Solutions possibles :")
            print("1. Vérifiez vos identifiants GitHub")
            print("2. Utilisez un Personal Access Token")
            print("3. Vérifiez que le repository existe")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur : {e}")
        return False

def show_next_steps():
    """Affiche les prochaines étapes"""
    next_steps = """
🎯 PROCHAINES ÉTAPES RECOMMANDÉES
===============================

1. 🏷️ AJOUTER DES TOPICS
   - Sur GitHub, cliquez ⚙️ à côté de "About"
   - Ajoutez : python, machine-learning, chatbot, airbnb, bert

2. 📸 AJOUTER DES SCREENSHOTS
   - Créez un dossier screenshots/
   - Ajoutez des captures de votre interface
   - Intégrez-les dans le README

3. 🏆 CRÉER UNE RELEASE
   - Onglet "Releases" → "Create new release"
   - Tag : v1.0.0
   - Titre : "🎉 Version 1.0 - Système Complet"

4. 📈 AMÉLIORER LA VISIBILITÉ
   - Partagez sur LinkedIn
   - Ajoutez à votre portfolio
   - Mentionnez dans votre CV

5. ⭐ DONNER UNE ÉTOILE
   - N'oubliez pas de "star" votre propre projet !
"""
    print(next_steps)

def show_git_commands():
    """Affiche les commandes Git utiles"""
    commands = """
🔄 COMMANDES GIT UTILES POUR LA SUITE
====================================

# Voir le statut
git status

# Ajouter des changements
git add .

# Créer un commit avec emoji
git commit -m "✨ Nouvelle fonctionnalité"

# Pousser vers GitHub
git push origin main

# Récupérer les changements
git pull origin main

# Voir l'historique
git log --oneline

🎨 EMOJIS POUR COMMITS :
✨ Nouvelle fonctionnalité    🐛 Correction bug
📚 Documentation            🔧 Configuration  
🧪 Tests                    ♻️ Refactoring
🚀 Déploiement              🎉 Version majeure
"""
    print(commands)

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérification de Git
    if not check_git_config():
        print("❌ Veuillez installer Git et relancer le script.")
        return
    
    print("\n" + "="*60)
    
    # Instructions GitHub
    show_github_instructions()
    
    # Attendre confirmation
    input("\n⏸️ Appuyez sur Entrée quand vous avez créé le repository sur GitHub...")
    
    # Configuration de la connexion
    if setup_github_remote():
        print("\n" + "="*60)
        show_next_steps()
        print("\n" + "="*60)
        show_git_commands()
        
        print("\n🎊 FÉLICITATIONS !")
        print("Votre projet est maintenant sur GitHub et prêt à impressionner !")
    else:
        print("\n❌ La mise sur GitHub a échoué.")
        print("📖 Consultez le fichier GUIDE_GITHUB.md pour plus d'aide.")

if __name__ == "__main__":
    main()