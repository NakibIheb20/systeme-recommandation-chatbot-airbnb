#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration du Chatbot d'Hébergements
=======================================

Ce fichier contient tous les paramètres configurables du chatbot
"""

# Configuration des données
DATA_CONFIG = {
    'data_file': 'all_reviews_final.csv',
    'encoding': 'utf-8',
    'required_columns': [
        'id_listing', 'title', 'city_listing', 'rating_listing',
        'sentiment_score', 'localizedText', 'price/label'
    ]
}

# Configuration du scoring de qualité
QUALITY_SCORING = {
    'weights': {
        'rating_listing': 0.3,      # Poids du rating global
        'sentiment_score': 0.3,     # Poids du sentiment des avis
        'avg_review_rating': 0.2,   # Poids de la note moyenne des avis
        'cleanliness_rating': 0.2   # Poids de la propreté
    },
    'min_score': 0.0,
    'max_score': 5.0
}

# Configuration des mots-clés pour l'analyse NLP
KEYWORDS_CONFIG = {
    'location_keywords': {
        'hammamet': ['hammamet', 'hammamat', 'hammet', 'hamam'],
        'jerba': ['jerba', 'djerba', 'gerba', 'jerb', 'djerb']
    },
    
    'quality_keywords': {
        'propre': [
            'propre', 'propreté', 'clean', 'cleanliness', 'hygiène',
            'nickel', 'impeccable', 'spotless'
        ],
        'communication': [
            'communication', 'réactif', 'responsive', 'contact', 'hôte',
            'disponible', 'joignable', 'accessible', 'serviable'
        ],
        'localisation': [
            'localisation', 'location', 'plage', 'beach', 'centre',
            'proche', 'situé', 'emplacement', 'position'
        ],
        'prix': [
            'prix', 'price', 'budget', 'cher', 'économique', 'abordable',
            'rapport qualité-prix', 'value', 'coût', 'tarif'
        ],
        'moderne': [
            'moderne', 'modern', 'neuf', 'nouveau', 'récent',
            'contemporain', 'design', 'stylé', 'tendance'
        ],
        'confort': [
            'confort', 'comfortable', 'lit', 'bed', 'équipé',
            'cosy', 'douillet', 'agréable', 'spacieux'
        ]
    },
    
    'sentiment_keywords': {
        'positif': [
            'bon', 'excellent', 'parfait', 'recommande', 'super', 'génial',
            'fantastique', 'merveilleux', 'top', 'formidable', 'magnifique'
        ],
        'négatif': [
            'mauvais', 'décevant', 'problème', 'sale', 'bruyant',
            'horrible', 'nul', 'catastrophique', 'inacceptable'
        ]
    },
    
    'rating_keywords': {
        'excellent': ['meilleur', 'top', 'excellent', 'exceptionnel', 'parfait'],
        'good': ['bon', 'bien', 'qualité', 'correct', 'satisfaisant']
    }
}

# Configuration des seuils de filtrage
FILTERING_CONFIG = {
    'rating_thresholds': {
        'excellent': 3.5,  # Seuil pour "meilleur/excellent"
        'good': 3.0,       # Seuil pour "bon/bien"
        'minimum': 1.0     # Score minimum acceptable
    },
    
    'sentiment_thresholds': {
        'positive': 0.7,   # Seuil pour sentiment positif
        'negative': 0.3,   # Seuil pour sentiment négatif
        'neutral_min': 0.3,
        'neutral_max': 0.7
    },
    
    'review_count_min': 1,  # Nombre minimum d'avis requis
    'price_range': {
        'min': 0,
        'max': 1000
    }
}

# Configuration de l'affichage des résultats
DISPLAY_CONFIG = {
    'max_results_default': 5,
    'max_results_advanced': 10,
    'max_description_length': 200,
    'max_title_length': 50,
    'max_review_preview': 150,
    
    'quality_badges': {
        4.5: {'badge': '🏆 EXCELLENT', 'color': '#28a745'},
        4.0: {'badge': '⭐ TRÈS BON', 'color': '#17a2b8'},
        3.5: {'badge': '👍 BON', 'color': '#ffc107'},
        0.0: {'badge': '📍 CORRECT', 'color': '#6c757d'}
    }
}

# Configuration des réponses du chatbot
RESPONSE_CONFIG = {
    'no_results_messages': [
        "😔 Aucun hébergement trouvé avec ces critères spécifiques.",
        "🔍 Aucun résultat ne correspond à votre recherche.",
        "😕 Désolé, aucun hébergement ne correspond à vos critères."
    ],
    
    'suggestions': [
        "💡 Suggestions :",
        "- Essayez d'élargir vos critères",
        "- Demandez les 'meilleurs hébergements' sans spécifier de ville",
        "- Posez une question plus générale",
        "- Utilisez des mots-clés comme 'propre', 'moderne', 'communication'"
    ],
    
    'greeting_messages': [
        "🤖 Bonjour ! Je suis votre assistant pour trouver l'hébergement parfait.",
        "👋 Salut ! Prêt à découvrir les meilleurs hébergements ?",
        "🏠 Bienvenue ! Comment puis-je vous aider à choisir votre hébergement ?"
    ]
}

# Configuration des exports
EXPORT_CONFIG = {
    'csv_encoding': 'utf-8',
    'json_indent': 2,
    'filename_format': 'recherche_hebergements_%Y%m%d_%H%M%S',
    'include_columns': [
        'title', 'city_listing', 'quality_score', 'review_count',
        'price/label', 'rating/cleanliness', 'rating/communication',
        'rating/location', 'sentiment_score'
    ]
}

# Configuration du logging
LOGGING_CONFIG = {
    'log_conversations': True,
    'log_file': 'chatbot_conversations.log',
    'log_level': 'INFO',
    'max_log_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Configuration de performance
PERFORMANCE_CONFIG = {
    'cache_results': True,
    'cache_size': 100,
    'max_processing_time': 30,  # secondes
    'batch_size': 1000,
    'memory_limit': 512 * 1024 * 1024  # 512MB
}

# Messages d'aide
HELP_MESSAGES = {
    'welcome': """
🤖 CHATBOT D'AIDE À LA SÉLECTION D'HÉBERGEMENTS
==============================================

💬 Posez vos questions en langage naturel !

💡 EXEMPLES DE QUESTIONS :
   • "Trouve-moi un appartement propre à Hammamet"
   • "Quels sont les hébergements avec la meilleure communication ?"
   • "Je veux un logement près de la plage à Jerba"
   • "Montre-moi les avis les plus positifs"
   • "Quel hébergement a le meilleur rapport qualité-prix ?"

🔧 COMMANDES SPÉCIALES :
   • 'help' ou 'aide' : Affiche l'aide
   • 'history' : Montre l'historique
   • 'stats' : Statistiques du dataset
   • 'quit' : Quitter le chatbot
""",
    
    'commands': """
🆘 COMMANDES DISPONIBLES :
========================

💬 QUESTIONS NATURELLES :
   Posez vos questions comme vous le feriez à un ami !

🔧 COMMANDES SPÉCIALES :
   • help, aide, h          → Affiche cette aide
   • history, historique    → Historique des conversations
   • stats, statistiques    → Statistiques du dataset
   • clear, effacer         → Efface l'historique
   • export                 → Exporte les derniers résultats
   • quit, exit, q          → Quitte le chatbot

💡 CONSEILS :
   • Soyez naturel dans vos questions
   • Combinez plusieurs critères
   • Spécifiez la ville pour des résultats localisés
   • Utilisez des mots-clés comme 'propre', 'moderne'
""",
    
    'examples': """
💡 EXEMPLES DE QUESTIONS EFFICACES :
===================================

🏠 RECHERCHE PAR VILLE :
   • "Hébergements à Hammamet"
   • "Logements disponibles à Jerba"
   • "Appartements dans le centre de Hammamet"

⭐ CRITÈRES DE QUALITÉ :
   • "Hébergement très propre"
   • "Logement avec bonne communication"
   • "Appartement moderne et confortable"

💰 BUDGET ET PRIX :
   • "Hébergement économique mais de qualité"
   • "Logement avec bon rapport qualité-prix"
   • "Options haut de gamme disponibles"

🎭 SENTIMENT ET AVIS :
   • "Hébergements avec avis positifs"
   • "Logements les mieux notés"
   • "Appartements recommandés par les clients"

🔄 REQUÊTES COMBINÉES :
   • "Appartement propre et moderne à Hammamet"
   • "Logement près de la plage avec bonne communication"
   • "Hébergement familial avec excellent rating à Jerba"
"""
}

# Validation de la configuration
def validate_config():
    """Valide la cohérence de la configuration"""
    errors = []
    
    # Vérification des seuils
    if FILTERING_CONFIG['rating_thresholds']['excellent'] <= FILTERING_CONFIG['rating_thresholds']['good']:
        errors.append("Le seuil 'excellent' doit être supérieur au seuil 'good'")
    
    # Vérification des poids de scoring
    total_weight = sum(QUALITY_SCORING['weights'].values())
    if abs(total_weight - 1.0) > 0.01:
        errors.append(f"La somme des poids de scoring doit être 1.0 (actuel: {total_weight})")
    
    # Vérification des seuils de sentiment
    if FILTERING_CONFIG['sentiment_thresholds']['positive'] <= FILTERING_CONFIG['sentiment_thresholds']['negative']:
        errors.append("Le seuil de sentiment positif doit être supérieur au négatif")
    
    return errors

# Test de la configuration
if __name__ == "__main__":
    print("🔧 VALIDATION DE LA CONFIGURATION")
    print("=" * 40)
    
    errors = validate_config()
    if errors:
        print("❌ ERREURS DÉTECTÉES :")
        for error in errors:
            print(f"   • {error}")
    else:
        print("✅ Configuration valide !")
        
    print(f"\n📊 RÉSUMÉ DE LA CONFIGURATION :")
    print(f"   🏠 Fichier de données : {DATA_CONFIG['data_file']}")
    print(f"   🎯 Résultats par défaut : {DISPLAY_CONFIG['max_results_default']}")
    print(f"   ⭐ Seuil excellent : {FILTERING_CONFIG['rating_thresholds']['excellent']}")
    print(f"   😊 Seuil positif : {FILTERING_CONFIG['sentiment_thresholds']['positive']}")
    print(f"   🌍 Villes supportées : {list(KEYWORDS_CONFIG['location_keywords'].keys())}")