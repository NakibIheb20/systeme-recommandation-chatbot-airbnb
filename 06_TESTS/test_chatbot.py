#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du chatbot d'hébergements
"""

import pandas as pd
import os

def test_chatbot():
    """Test complet du chatbot"""
    print("🧪 TEST DU CHATBOT D'HÉBERGEMENTS")
    print("=" * 50)
    
    # Vérification de l'existence du fichier de données
    if os.path.exists('all_reviews_final.csv'):
        df = pd.read_csv('all_reviews_final.csv')
        print(f"✅ Fichier de données trouvé : {len(df):,} lignes")
        print(f"📊 Colonnes disponibles : {len(df.columns)}")
        print(f"🏠 Logements uniques : {df['id_listing'].nunique():,}")
        print(f"🌍 Villes : {list(df['city_listing'].unique())}")
        
        # Test du chatbot
        print("\n🤖 Test du chatbot...")
        try:
            from chatbot_hebergement import ChatbotHebergement
            
            chatbot = ChatbotHebergement('all_reviews_final.csv')
            if chatbot.listings is not None:
                print("✅ Chatbot initialisé avec succès")
                
                # Test de plusieurs requêtes
                test_queries = [
                    "meilleurs hébergements à Hammamet",
                    "appartement propre",
                    "logement avec bonne communication à Jerba",
                    "hébergement moderne"
                ]
                
                for query in test_queries:
                    print(f"\n🔍 Test : '{query}'")
                    response, results = chatbot.generate_response(query, top_n=3)
                    print(f"   ✅ {len(results)} résultats trouvés")
                
                # Statistiques
                stats = chatbot.get_statistics()
                print(f"\n📊 STATISTIQUES :")
                print(f"   🏠 Hébergements : {stats['total_listings']:,}")
                print(f"   💬 Avis : {stats['total_reviews']:,}")
                print(f"   🌍 Villes : {', '.join(stats['cities'])}")
                print(f"   ⭐ Score moyen : {stats['avg_quality_score']:.2f}/5")
                print(f"   🏆 Excellents : {stats['top_rated_count']}")
                
                print("\n✅ TOUS LES TESTS RÉUSSIS !")
                return True
                
            else:
                print("❌ Erreur d'initialisation du chatbot")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du test : {str(e)}")
            return False
    else:
        print("❌ Fichier all_reviews_final.csv non trouvé")
        return False

if __name__ == "__main__":
    test_chatbot()