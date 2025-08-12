#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Vérification des Fichiers pour GitHub
==============================================

Vérifie quels fichiers seront inclus dans le repository GitHub optimisé.
"""

import os
import subprocess
from pathlib import Path

def get_file_size(file_path):
    """Retourne la taille d'un fichier en MB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)  # Convertir en MB
    except:
        return 0

def main():
    """Fonction principale"""
    print("📁 VÉRIFICATION DES FICHIERS POUR GITHUB")
    print("=" * 50)
    
    # Obtenir la liste des fichiers trackés par Git
    try:
        result = subprocess.run(['git', 'ls-files'], 
                              capture_output=True, text=True, check=True)
        tracked_files = result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        print("❌ Erreur: Impossible d'obtenir la liste des fichiers Git")
        return
    
    # Analyser les fichiers
    total_size = 0
    file_types = {}
    large_files = []
    
    print(f"\n📊 ANALYSE DE {len(tracked_files)} FICHIERS TRACKÉS")
    print("-" * 50)
    
    for file_path in tracked_files:
        if not file_path.strip():
            continue
            
        full_path = Path(file_path)
        if not full_path.exists():
            continue
            
        size_mb = get_file_size(full_path)
        total_size += size_mb
        
        # Compter par type de fichier
        extension = full_path.suffix.lower()
        if extension not in file_types:
            file_types[extension] = {'count': 0, 'size': 0}
        file_types[extension]['count'] += 1
        file_types[extension]['size'] += size_mb
        
        # Identifier les gros fichiers
        if size_mb > 1:  # Plus de 1MB
            large_files.append((file_path, size_mb))
    
    # Afficher les résultats
    print(f"📦 TAILLE TOTALE: {total_size:.2f} MB")
    print(f"📄 NOMBRE DE FICHIERS: {len(tracked_files)}")
    
    print(f"\n📊 RÉPARTITION PAR TYPE DE FICHIER:")
    print("-" * 50)
    for ext, data in sorted(file_types.items(), key=lambda x: x[1]['size'], reverse=True):
        if ext == '':
            ext = '(sans extension)'
        print(f"{ext:15} | {data['count']:3} fichiers | {data['size']:8.2f} MB")
    
    if large_files:
        print(f"\n⚠️  FICHIERS VOLUMINEUX (>1MB):")
        print("-" * 50)
        for file_path, size in sorted(large_files, key=lambda x: x[1], reverse=True):
            print(f"{size:8.2f} MB | {file_path}")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    print("-" * 50)
    if total_size < 50:
        print("✅ Taille excellente pour GitHub (<50MB)")
    elif total_size < 100:
        print("✅ Taille acceptable pour GitHub (<100MB)")
    else:
        print("⚠️  Taille importante - considérez Git LFS pour gros fichiers")
    
    # Vérifier les types de fichiers essentiels
    essential_types = ['.py', '.ipynb', '.md', '.txt', '.json', '.yml', '.yaml']
    code_files = sum(data['count'] for ext, data in file_types.items() if ext in essential_types)
    
    print(f"📝 Fichiers de code/doc: {code_files}")
    print(f"🎯 Repository optimisé pour le code source: {'✅' if code_files > len(tracked_files) * 0.7 else '⚠️'}")

if __name__ == "__main__":
    main()