#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de mise à jour des chemins après réorganisation
====================================================

Ce script met à jour automatiquement tous les chemins dans les fichiers
pour qu'ils correspondent à la nouvelle organisation des dossiers.
"""

import os
import re
from pathlib import Path

def update_file_paths(file_path, old_patterns, new_patterns):
    """Met à jour les chemins dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remplacement des patterns
        for old_pattern, new_pattern in zip(old_patterns, new_patterns):
            content = re.sub(old_pattern, new_pattern, content)
        
        # Sauvegarde si des changements ont été faits
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Mis à jour: {file_path}")
            return True
        else:
            print(f"ℹ️  Aucun changement: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {str(e)}")
        return False

def main():
    """Fonction principale de mise à jour"""
    print("🔄 MISE À JOUR DES CHEMINS APRÈS RÉORGANISATION")
    print("=" * 60)
    
    # Répertoire racine
    root_dir = Path("c:/Users/DELL/Desktop/stage d'été 2/systéme_recommandation_and_chatbot")
    
    # Patterns à remplacer
    old_patterns = [
        r"'all_reviews_final\.csv'",
        r'"all_reviews_final\.csv"',
        r"all_reviews_final\.csv",
        r"'config_chatbot\.py'",
        r'"config_chatbot\.py"',
        r"from config_chatbot import",
        r"'chatbot_hebergement\.py'",
        r'"chatbot_hebergement\.py"',
        r"'test_.*\.py'",
        r'"test_.*\.py"',
        r"'.*\.pkl'",
        r'".*\.pkl"',
        r"'.*\.npy'",
        r'".*\.npy"',
    ]
    
    new_patterns = [
        "'01_DONNEES/final/all_reviews_final.csv'",
        '"01_DONNEES/final/all_reviews_final.csv"',
        "01_DONNEES/final/all_reviews_final.csv",
        "'03_CHATBOT/config/config_chatbot.py'",
        '"03_CHATBOT/config/config_chatbot.py"',
        "from 03_CHATBOT.config.config_chatbot import",
        "'03_CHATBOT/scripts/chatbot_hebergement.py'",
        '"03_CHATBOT/scripts/chatbot_hebergement.py"',
        "'06_TESTS/test_*.py'",
        '"06_TESTS/test_*.py"',
        "'07_MODELES/*.pkl'",
        '"07_MODELES/*.pkl"',
        "'07_MODELES/*.npy'",
        '"07_MODELES/*.npy"',
    ]
    
    # Fichiers à mettre à jour
    files_to_update = []
    
    # Recherche des fichiers Python et Jupyter
    for pattern in ["**/*.py", "**/*.ipynb"]:
        files_to_update.extend(root_dir.glob(pattern))
    
    print(f"📁 Fichiers trouvés à mettre à jour: {len(files_to_update)}")
    print("-" * 60)
    
    updated_count = 0
    
    for file_path in files_to_update:
        # Ignorer certains dossiers
        if any(ignore in str(file_path) for ignore in ['venv', '__pycache__', '.git', '.ipynb_checkpoints']):
            continue
            
        if update_file_paths(file_path, old_patterns, new_patterns):
            updated_count += 1
    
    print("-" * 60)
    print(f"✅ Mise à jour terminée: {updated_count} fichiers modifiés")
    
    # Création d'un fichier de configuration des nouveaux chemins
    create_path_config()

def create_path_config():
    """Crée un fichier de configuration des chemins"""
    config_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration des chemins après réorganisation
==============================================
"""

import os
from pathlib import Path

# Répertoire racine du projet
ROOT_DIR = Path(__file__).parent

# Chemins des données
DATA_PATHS = {
    'raw': ROOT_DIR / '01_DONNEES' / 'raw',
    'processed': ROOT_DIR / '01_DONNEES' / 'processed',
    'final': ROOT_DIR / '01_DONNEES' / 'final',
    'main_dataset': ROOT_DIR / '01_DONNEES' / 'final' / 'all_reviews_final.csv'
}

# Chemins du système de recommandation
RECOMMENDER_PATHS = {
    'notebooks': ROOT_DIR / '02_SYSTEME_RECOMMANDATION' / 'notebooks',
    'scripts': ROOT_DIR / '02_SYSTEME_RECOMMANDATION' / 'scripts',
    'app': ROOT_DIR / '02_SYSTEME_RECOMMANDATION' / 'scripts' / 'app.py'
}

# Chemins du chatbot
CHATBOT_PATHS = {
    'notebooks': ROOT_DIR / '03_CHATBOT' / 'notebooks',
    'scripts': ROOT_DIR / '03_CHATBOT' / 'scripts',
    'config': ROOT_DIR / '03_CHATBOT' / 'config',
    'main_script': ROOT_DIR / '03_CHATBOT' / 'scripts' / 'chatbot_hebergement.py',
    'main_notebook': ROOT_DIR / '03_CHATBOT' / 'notebooks' / 'chatbot_hebergement.ipynb',
    'config_file': ROOT_DIR / '03_CHATBOT' / 'config' / 'config_chatbot.py'
}

# Chemins de la documentation
DOC_PATHS = {
    'root': ROOT_DIR / '04_DOCUMENTATION',
    'chatbot_readme': ROOT_DIR / '04_DOCUMENTATION' / 'README_CHATBOT.md',
    'guide': ROOT_DIR / '04_DOCUMENTATION' / 'GUIDE_UTILISATION.md',
    'resume': ROOT_DIR / '04_DOCUMENTATION' / 'CHATBOT_RESUME.md'
}

# Chemins de configuration
CONFIG_PATHS = {
    'root': ROOT_DIR / '05_CONFIGURATION',
    'requirements': ROOT_DIR / '05_CONFIGURATION' / 'requirements.txt',
    'package_json': ROOT_DIR / '05_CONFIGURATION' / 'package.json'
}

# Chemins des tests
TEST_PATHS = {
    'root': ROOT_DIR / '06_TESTS',
    'chatbot_test': ROOT_DIR / '06_TESTS' / 'test_chatbot.py',
    'final_test': ROOT_DIR / '06_TESTS' / 'test_final.py'
}

# Chemins des modèles
MODEL_PATHS = {
    'root': ROOT_DIR / '07_MODELES',
    'knn_model': ROOT_DIR / '07_MODELES' / 'knn_model.pkl',
    'similarity_matrix': ROOT_DIR / '07_MODELES' / 'similarity_matrix_bert.npy',
    'user_item_matrix': ROOT_DIR / '07_MODELES' / 'user_item_matrix.pkl'
}

# Chemins des résultats
RESULT_PATHS = {
    'root': ROOT_DIR / '08_RESULTATS',
    'heatmap': ROOT_DIR / '08_RESULTATS' / 'avis_positifs_heatmap.html'
}

def get_path(category, key):
    """Récupère un chemin spécifique"""
    paths_dict = {
        'data': DATA_PATHS,
        'recommender': RECOMMENDER_PATHS,
        'chatbot': CHATBOT_PATHS,
        'doc': DOC_PATHS,
        'config': CONFIG_PATHS,
        'test': TEST_PATHS,
        'model': MODEL_PATHS,
        'result': RESULT_PATHS
    }
    
    return paths_dict.get(category, {}).get(key)

def ensure_path_exists(path):
    """S'assure qu'un chemin existe"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    print("📁 CONFIGURATION DES CHEMINS")
    print("=" * 40)
    print(f"Répertoire racine: {ROOT_DIR}")
    print(f"Dataset principal: {DATA_PATHS['main_dataset']}")
    print(f"Script chatbot: {CHATBOT_PATHS['main_script']}")
    print(f"Notebook chatbot: {CHATBOT_PATHS['main_notebook']}")
'''
    
    with open('path_config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("📁 Fichier path_config.py créé")

if __name__ == "__main__":
    main()