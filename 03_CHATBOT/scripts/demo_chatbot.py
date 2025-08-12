#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration du Chatbot d'Hébergements Airbnb
==============================================

Ce script montre les capacités du chatbot avec des exemples concrets
"""

from chatbot_hebergement import ChatbotHebergement
import pandas as pd

def demo_chatbot():
    """Démonstration complète du chatbot"""
    
    print("🎭 DÉMONSTRATION DU CHATBOT D'HÉBERGEMENTS")
    print("=" * 60)
    
    # Initialisation
    print("🚀 Initialisation du chatbot...")
    chatbot = ChatbotHebergement('all_reviews_final.csv')
    
    if chatbot.listings is None:
        print("❌ Impossible de charger les données")
        return
    
    # Statistiques initiales
    stats = chatbot.get_statistics()
    print(f"\n📊 DONNÉES DISPONIBLES :")
    print(f"   🏠 {stats['total_listings']:,} hébergements")
    print(f"   💬 {stats['total_reviews']:,} avis analysés")
    print(f"   🌍 Villes : {', '.join(stats['cities'])}")
    print(f"   ⭐ Score moyen : {stats['avg_quality_score']:.2f}/5")
    
    # Exemples de requêtes
    demo_queries = [
        {
            'query': "Trouve-moi les meilleurs hébergements à Hammamet",
            'description': "🏆 Recherche des hébergements de qualité dans une ville spécifique"
        },
        {
            'query': "Je veux un appartement très propre",
            'description': "🧹 Filtrage par critère de propreté"
        },
        {
            'query': "Hébergement avec excellente communication",
            'description': "📞 Focus sur la qualité de communication de l'hôte"
        },
        {
            'query': "Logement moderne près de la plage à Jerba",
            'description': "🏖️ Requête combinée : style + localisation + ville"
        },
        {
            'query': "Quel hébergement a les avis les plus positifs ?",
            'description': "😊 Analyse basée sur le sentiment des avis"
        }
    ]
    
    print(f"\n🎯 DÉMONSTRATION AVEC {len(demo_queries)} EXEMPLES :")
    print("=" * 60)
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n📝 EXEMPLE #{i} : {demo['description']}")
        print(f"❓ Question : \"{demo['query']}\"")
        print("-" * 50)
        
        # Génération de la réponse
        response, results = chatbot.generate_response(demo['query'], top_n=3)
        
        print("🤖 RÉPONSE DU CHATBOT :")
        print(response)
        
        # Affichage des résultats
        if not results.empty:
            print("🏠 TOP 3 RECOMMANDATIONS :")
            for idx, (_, listing) in enumerate(results.iterrows(), 1):
                # Informations essentielles
                title = listing['title'][:50] + "..." if len(listing['title']) > 50 else listing['title']
                city = listing['city_listing']
                quality = listing['quality_score']
                reviews = listing['review_count']
                price = listing['price/label'] if pd.notna(listing['price/label']) else "Prix N/A"
                
                print(f"   #{idx} {title}")
                print(f"       📍 {city} | ⭐ {quality:.2f}/5 | 💬 {reviews} avis | 💰 {price}")
        else:
            print("😔 Aucun résultat trouvé avec ces critères")
        
        print("\n" + "="*60)
    
    # Analyse des critères détectés
    print("\n🔍 ANALYSE DES CAPACITÉS DE COMPRÉHENSION :")
    print("-" * 50)
    
    test_analysis = [
        "appartement moderne à Hammamet avec bonne communication",
        "hébergement économique mais propre à Jerba",
        "villa de luxe avec piscine et vue mer"
    ]
    
    for query in test_analysis:
        criteria = chatbot.analyze_query(query)
        print(f"\n📝 \"{query}\"")
        print(f"   🎯 Critères détectés :")
        if criteria['city']:
            print(f"      📍 Ville : {criteria['city']}")
        if criteria['quality_focus']:
            print(f"      🎨 Focus qualité : {', '.join(criteria['quality_focus'])}")
        if criteria['min_rating']:
            print(f"      ⭐ Rating minimum : {criteria['min_rating']}")
        if criteria['sentiment_filter']:
            print(f"      😊 Filtre sentiment : {criteria['sentiment_filter']}")
        
        if not any([criteria['city'], criteria['quality_focus'], criteria['min_rating'], criteria['sentiment_filter']]):
            print("      ℹ️ Requête générale sans critères spécifiques")
    
    # Recommandations d'utilisation
    print(f"\n💡 CONSEILS D'UTILISATION :")
    print("-" * 30)
    print("✅ Soyez naturel dans vos questions")
    print("✅ Combinez plusieurs critères pour plus de précision")
    print("✅ Utilisez des mots-clés comme 'propre', 'moderne', 'communication'")
    print("✅ Spécifiez la ville (Hammamet/Jerba) pour des résultats localisés")
    print("✅ Demandez des 'meilleurs' ou 'excellents' pour du haut de gamme")
    
    print(f"\n🎉 DÉMONSTRATION TERMINÉE !")
    print("💬 Vous pouvez maintenant utiliser le chatbot de manière interactive")
    print("🚀 Lancez 'python chatbot_hebergement.py' pour commencer")

if __name__ == "__main__":
    demo_chatbot()