#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de tous les composants du chatbot
"""

def test_final():
    """Test complet de tous les composants"""
    print("🧪 TEST FINAL DU CHATBOT")
    print("=" * 40)
    
    try:
        # 1. Test de la configuration
        print("🔧 Test de la configuration...")
        from config_chatbot import validate_config, DATA_CONFIG
        errors = validate_config()
        if not errors:
            print("✅ Configuration valide")
        else:
            print(f"❌ Erreurs de configuration: {errors}")
            return False
        
        # 2. Test du chatbot principal
        print("🤖 Test du chatbot principal...")
        from chatbot_hebergement import ChatbotHebergement
        chatbot = ChatbotHebergement(DATA_CONFIG['data_file'])
        
        if chatbot.listings is None:
            print("❌ Erreur d'initialisation du chatbot")
            return False
        
        print("✅ Chatbot initialisé avec succès")
        
        # 3. Test de requêtes variées
        print("💬 Test de requêtes...")
        test_queries = [
            "hébergements à Hammamet",
            "appartement propre",
            "meilleurs logements"
        ]
        
        for query in test_queries:
            response, results = chatbot.generate_response(query, top_n=2)
            print(f"   ✅ '{query}': {len(results)} résultats")
        
        # 4. Test des statistiques
        print("📊 Test des statistiques...")
        stats = chatbot.get_statistics()
        print(f"   ✅ {stats['total_listings']} hébergements disponibles")
        print(f"   ✅ {stats['total_reviews']} avis analysés")
        print(f"   ✅ Villes: {', '.join(stats['cities'])}")
        
        # 5. Test de l'analyse de requête
        print("🔍 Test de l'analyse NLP...")
        criteria = chatbot.analyze_query("appartement moderne à Hammamet avec bonne communication")
        print(f"   ✅ Ville détectée: {criteria['city']}")
        print(f"   ✅ Critères détectés: {criteria['quality_focus']}")
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("=" * 40)
        print("🚀 CHATBOT PRÊT À UTILISER !")
        print("💬 Commandes disponibles:")
        print("   • python chatbot_hebergement.py (interface console)")
        print("   • jupyter notebook chatbot_hebergement.ipynb (interface graphique)")
        print("   • python demo_chatbot.py (démonstration)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_final()
    if success:
        print("\n✅ Système opérationnel !")
    else:
        print("\n❌ Des problèmes ont été détectés.")