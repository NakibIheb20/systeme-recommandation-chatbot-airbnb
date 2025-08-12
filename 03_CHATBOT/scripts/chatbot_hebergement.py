#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Chatbot d'Aide à la Sélection d'Hébergements Airbnb
=====================================================

Ce script implémente un chatbot intelligent qui aide les utilisateurs à choisir
le meilleur hébergement Airbnb en Tunisie (Hammamet & Jerba) en analysant :
- 50,000+ avis clients avec analyse de sentiment
- Métadonnées détaillées des logements
- Scores de qualité basés sur l'IA (BERT)
- Préférences personnalisées selon les critères utilisateur

Auteur: Système de Recommandation Airbnb
Date: 2025
"""

import pandas as pd
import numpy as np
import re
import warnings
from collections import Counter
from datetime import datetime
import json
import os

# Configuration
warnings.filterwarnings('ignore')

class ChatbotHebergement:
    """
    Chatbot intelligent pour la sélection d'hébergements Airbnb
    """
    
    def __init__(self, data_file='all_reviews_final.csv'):
        """
        Initialise le chatbot avec les données d'hébergements
        
        Args:
            data_file (str): Chemin vers le fichier de données CSV
        """
        self.data_file = data_file
        self.listings = None
        self.reviews = None
        self.conversation_history = []
        
        # Mots-clés pour l'analyse des requêtes
        self.location_keywords = {
            'hammamet': ['hammamet', 'hammamat', 'hammet', 'hamam'],
            'jerba': ['jerba', 'djerba', 'gerba', 'jerb']
        }
        
        self.quality_keywords = {
            'propre': ['propre', 'propreté', 'clean', 'cleanliness', 'hygiène'],
            'communication': ['communication', 'réactif', 'responsive', 'contact', 'hôte'],
            'localisation': ['localisation', 'location', 'plage', 'beach', 'centre', 'proche'],
            'prix': ['prix', 'price', 'budget', 'cher', 'économique', 'abordable'],
            'moderne': ['moderne', 'modern', 'neuf', 'nouveau', 'récent'],
            'confort': ['confort', 'comfortable', 'lit', 'bed', 'équipé']
        }
        
        self.sentiment_keywords = {
            'positif': ['bon', 'excellent', 'parfait', 'recommande', 'super', 'génial'],
            'négatif': ['mauvais', 'décevant', 'problème', 'sale', 'bruyant']
        }
        
        # Chargement des données
        self.load_data()
    
    def load_data(self):
        """Charge et prépare les données d'hébergements"""
        try:
            print(f"📂 Chargement des données depuis {self.data_file}...")
            df = pd.read_csv(self.data_file)
            print(f"✅ Dataset chargé : {len(df):,} avis")
            
            # Nettoyage des données
            df['rating_listing'] = pd.to_numeric(df['rating_listing'], errors='coerce')
            df['sentiment_score'] = pd.to_numeric(df['sentiment_score'], errors='coerce')
            df['price_numeric'] = df['price/label'].str.extract(r'\$(\d+)').astype(float)
            
            # Création d'un dataset agrégé par logement
            self.listings = df.groupby('id_listing').agg({
                'title': 'first',
                'description': 'first',
                'city_listing': 'first',
                'rating_listing': 'first',
                'rating/cleanliness': 'first',
                'rating/accuracy': 'first',
                'rating/communication': 'first',
                'rating/location': 'first',
                'rating/value': 'first',
                'price/label': 'first',
                'price_numeric': 'first',
                'coordinates/latitude': 'first',
                'coordinates/longitude': 'first',
                'sentiment_score': 'mean',
                'rating_review': 'mean',
                'localizedText': lambda x: ' '.join(x.dropna().astype(str)[:3]),
                'id_review': 'count'
            }).reset_index()
            
            # Renommage des colonnes
            self.listings.rename(columns={
                'id_review': 'review_count',
                'rating_review': 'avg_review_rating',
                'localizedText': 'sample_reviews'
            }, inplace=True)
            
            # Calcul d'un score de qualité global
            self.listings['quality_score'] = (
                self.listings['rating_listing'].fillna(0) * 0.3 +
                self.listings['sentiment_score'].fillna(0) * 0.3 +
                self.listings['avg_review_rating'].fillna(0) * 0.2 +
                self.listings['rating/cleanliness'].fillna(0) * 0.2
            )
            
            self.reviews = df
            print(f"✅ Données préparées : {len(self.listings)} logements uniques")
            
        except FileNotFoundError:
            print(f"❌ Fichier {self.data_file} non trouvé")
            self.listings = None
            self.reviews = None
        except Exception as e:
            print(f"❌ Erreur lors du chargement : {str(e)}")
            self.listings = None
            self.reviews = None
    
    def analyze_query(self, query):
        """
        Analyse la requête utilisateur pour extraire les critères
        
        Args:
            query (str): Question de l'utilisateur
            
        Returns:
            dict: Critères extraits de la requête
        """
        query_lower = query.lower()
        criteria = {
            'city': None,
            'quality_focus': [],
            'sentiment_filter': None,
            'price_range': None,
            'min_rating': None
        }
        
        # Détection de la ville
        for city, keywords in self.location_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                criteria['city'] = city.title()
                break
        
        # Détection des critères de qualité
        for quality, keywords in self.quality_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                criteria['quality_focus'].append(quality)
        
        # Détection du sentiment
        for sentiment, keywords in self.sentiment_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                criteria['sentiment_filter'] = sentiment
                break
        
        # Détection de critères de rating
        if any(word in query_lower for word in ['meilleur', 'top', 'excellent']):
            criteria['min_rating'] = 3.5  # Abaissé pour plus de résultats
        elif any(word in query_lower for word in ['bon', 'bien', 'qualité']):
            criteria['min_rating'] = 3.0  # Abaissé pour plus de résultats
        
        return criteria
    
    def filter_listings(self, criteria):
        """
        Filtre les logements selon les critères extraits
        
        Args:
            criteria (dict): Critères de filtrage
            
        Returns:
            DataFrame: Logements filtrés
        """
        if self.listings is None:
            return pd.DataFrame()
        
        filtered = self.listings.copy()
        
        # Filtre par ville
        if criteria['city']:
            filtered = filtered[filtered['city_listing'].str.contains(criteria['city'], case=False, na=False)]
        
        # Filtre par rating minimum
        if criteria['min_rating']:
            filtered = filtered[filtered['quality_score'] >= criteria['min_rating']]
        
        # Filtre par sentiment
        if criteria['sentiment_filter'] == 'positif':
            filtered = filtered[filtered['sentiment_score'] >= 0.7]
        elif criteria['sentiment_filter'] == 'négatif':
            filtered = filtered[filtered['sentiment_score'] <= 0.3]
        
        return filtered
    
    def rank_by_criteria(self, filtered_listings, criteria):
        """
        Classe les logements selon les critères de qualité demandés
        
        Args:
            filtered_listings (DataFrame): Logements filtrés
            criteria (dict): Critères de classement
            
        Returns:
            DataFrame: Logements classés
        """
        if filtered_listings.empty:
            return filtered_listings
        
        if not criteria['quality_focus']:
            return filtered_listings.sort_values('quality_score', ascending=False)
        
        # Calcul d'un score pondéré selon les critères
        score = filtered_listings['quality_score'].copy()
        
        for focus in criteria['quality_focus']:
            if focus == 'propre' and 'rating/cleanliness' in filtered_listings.columns:
                score += filtered_listings['rating/cleanliness'].fillna(0) * 0.5
            elif focus == 'communication' and 'rating/communication' in filtered_listings.columns:
                score += filtered_listings['rating/communication'].fillna(0) * 0.5
            elif focus == 'localisation' and 'rating/location' in filtered_listings.columns:
                score += filtered_listings['rating/location'].fillna(0) * 0.5
            elif focus == 'prix' and 'rating/value' in filtered_listings.columns:
                score += filtered_listings['rating/value'].fillna(0) * 0.5
        
        filtered_listings = filtered_listings.copy()
        filtered_listings['custom_score'] = score
        return filtered_listings.sort_values('custom_score', ascending=False)
    
    def format_listing_info(self, listing, rank):
        """
        Formate les informations d'un logement pour l'affichage
        
        Args:
            listing (Series): Données du logement
            rank (int): Rang dans les résultats
            
        Returns:
            str: Informations formatées
        """
        # Badge de qualité
        if listing['quality_score'] >= 4.5:
            badge = "🏆 EXCELLENT"
        elif listing['quality_score'] >= 4.0:
            badge = "⭐ TRÈS BON"
        elif listing['quality_score'] >= 3.5:
            badge = "👍 BON"
        else:
            badge = "📍 CORRECT"
        
        # Prix formaté
        price_display = listing['price/label'] if pd.notna(listing['price/label']) else "Prix non disponible"
        
        # Scores détaillés
        cleanliness = f"{listing['rating/cleanliness']:.1f}" if pd.notna(listing['rating/cleanliness']) else "N/A"
        communication = f"{listing['rating/communication']:.1f}" if pd.notna(listing['rating/communication']) else "N/A"
        location = f"{listing['rating/location']:.1f}" if pd.notna(listing['rating/location']) else "N/A"
        
        # Avis échantillon
        sample_review = str(listing['sample_reviews'])[:150] + "..." if len(str(listing['sample_reviews'])) > 150 else str(listing['sample_reviews'])
        
        info = f"""
#{rank} {badge} - {listing['title']}
{'='*60}
📍 Ville: {listing['city_listing']}
💰 Prix: {price_display}
📊 Score Qualité: {listing['quality_score']:.2f}/5
💬 Nombre d'avis: {listing['review_count']}

📈 Détails des scores:
   🧹 Propreté: {cleanliness}/5
   📞 Communication: {communication}/5
   🗺️ Localisation: {location}/5
   😊 Sentiment: {listing['sentiment_score']:.2f}/1

💭 Aperçu des avis:
   "{sample_review}"
"""
        return info
    
    def generate_response(self, query, top_n=5):
        """
        Génère une réponse complète à la requête utilisateur
        
        Args:
            query (str): Question de l'utilisateur
            top_n (int): Nombre de résultats à retourner
            
        Returns:
            tuple: (réponse_texte, résultats_dataframe)
        """
        if self.listings is None:
            return "❌ Données non disponibles. Vérifiez le fichier de données.", pd.DataFrame()
        
        # Analyse de la requête
        criteria = self.analyze_query(query)
        
        # Filtrage et classement
        filtered = self.filter_listings(criteria)
        ranked = self.rank_by_criteria(filtered, criteria)
        
        # Sélection des top résultats
        top_results = ranked.head(top_n)
        
        # Génération de la réponse
        if len(top_results) == 0:
            response = self._generate_no_results_response(criteria)
            return response, pd.DataFrame()
        
        response = self._generate_results_response(query, criteria, top_results)
        
        # Sauvegarde dans l'historique
        self.conversation_history.append({
            'query': query,
            'criteria': criteria,
            'results_count': len(top_results),
            'timestamp': datetime.now().isoformat()
        })
        
        return response, top_results
    
    def _generate_no_results_response(self, criteria):
        """Génère une réponse quand aucun résultat n'est trouvé"""
        response = "😔 Aucun hébergement trouvé avec ces critères spécifiques.\n\n"
        response += "💡 Suggestions :\n"
        response += "- Essayez d'élargir vos critères\n"
        response += "- Demandez les 'meilleurs hébergements' sans spécifier de ville\n"
        response += "- Posez une question plus générale\n"
        return response
    
    def _generate_results_response(self, query, criteria, results):
        """Génère une réponse avec les résultats trouvés"""
        response = f"🎯 Voici les meilleurs hébergements pour votre demande :\n"
        response += f'"{query}"\n\n'
        
        # Critères détectés
        if criteria['city'] or criteria['quality_focus'] or criteria['min_rating']:
            response += "🔍 Critères détectés : "
            detected = []
            if criteria['city']:
                detected.append(f"Ville: {criteria['city']}")
            if criteria['quality_focus']:
                detected.append(f"Focus: {', '.join(criteria['quality_focus'])}")
            if criteria['min_rating']:
                detected.append(f"Rating min: {criteria['min_rating']}")
            response += " | ".join(detected) + "\n\n"
        
        response += f"📊 {len(results)} hébergements sélectionnés :\n\n"
        
        return response
    
    def chat_session(self):
        """Lance une session de chat interactive"""
        print("🤖 Chatbot d'Aide à la Sélection d'Hébergements Airbnb")
        print("=" * 60)
        print("💬 Posez vos questions en langage naturel !")
        print("💡 Exemples :")
        print("   - 'Trouve-moi un appartement propre à Hammamet'")
        print("   - 'Quels sont les hébergements avec la meilleure communication ?'")
        print("   - 'Je veux un logement près de la plage à Jerba'")
        print("\n📝 Tapez 'quit' pour quitter, 'help' pour l'aide")
        print("-" * 60)
        
        while True:
            try:
                query = input("\n🔍 Votre question : ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Au revoir ! Merci d'avoir utilisé le chatbot.")
                    break
                
                if query.lower() in ['help', 'aide', 'h']:
                    self._show_help()
                    continue
                
                if query.lower() in ['history', 'historique']:
                    self._show_history()
                    continue
                
                if not query:
                    print("❌ Veuillez saisir une question.")
                    continue
                
                print("\n🔍 Recherche en cours...")
                response, results = self.generate_response(query)
                
                print("\n" + "="*60)
                print("🤖 RÉPONSE DU CHATBOT")
                print("="*60)
                print(response)
                
                # Affichage des résultats détaillés
                if not results.empty:
                    for idx, (_, listing) in enumerate(results.iterrows(), 1):
                        print(self.format_listing_info(listing, idx))
                        print("-" * 60)
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrompue. Au revoir !")
                break
            except Exception as e:
                print(f"❌ Erreur : {str(e)}")
    
    def _show_help(self):
        """Affiche l'aide du chatbot"""
        help_text = """
🆘 AIDE DU CHATBOT
==================

💬 TYPES DE QUESTIONS SUPPORTÉES :
   • Recherche par ville : "hébergements à Hammamet", "logements Jerba"
   • Critères de qualité : "appartement propre", "bonne communication"
   • Sentiment : "avis positifs", "recommandations excellentes"
   • Combinaisons : "appartement moderne et propre à Hammamet"

🔧 COMMANDES SPÉCIALES :
   • 'help' ou 'aide' : Affiche cette aide
   • 'history' ou 'historique' : Montre l'historique des conversations
   • 'quit' ou 'exit' : Quitte le chatbot

💡 CONSEILS :
   • Soyez naturel dans vos questions
   • Combinez plusieurs critères pour des résultats précis
   • Le chatbot comprend français et anglais
        """
        print(help_text)
    
    def _show_history(self):
        """Affiche l'historique des conversations"""
        if not self.conversation_history:
            print("📝 Aucune conversation enregistrée.")
            return
        
        print("\n📝 HISTORIQUE DES CONVERSATIONS")
        print("=" * 40)
        
        for i, conv in enumerate(self.conversation_history, 1):
            timestamp = datetime.fromisoformat(conv['timestamp']).strftime("%H:%M:%S")
            print(f"\n🕐 {timestamp} - Conversation #{i}")
            print(f"❓ Question : {conv['query']}")
            print(f"📊 Résultats : {conv['results_count']}")
    
    def export_results(self, results, filename=None):
        """
        Exporte les résultats vers un fichier CSV
        
        Args:
            results (DataFrame): Résultats à exporter
            filename (str): Nom du fichier (optionnel)
        """
        if results.empty:
            print("❌ Aucun résultat à exporter")
            return
        
        if filename is None:
            filename = f"recherche_hebergements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            results.to_csv(filename, index=False)
            print(f"✅ Résultats exportés dans {filename}")
        except Exception as e:
            print(f"❌ Erreur lors de l'export : {str(e)}")
    
    def get_statistics(self):
        """Retourne les statistiques du dataset"""
        if self.listings is None:
            return "❌ Données non disponibles"
        
        stats = {
            'total_listings': len(self.listings),
            'total_reviews': self.listings['review_count'].sum(),
            'cities': self.listings['city_listing'].unique().tolist(),
            'avg_quality_score': self.listings['quality_score'].mean(),
            'top_rated_count': (self.listings['quality_score'] > 4.5).sum()
        }
        
        return stats


def main():
    """Fonction principale pour lancer le chatbot"""
    print("🚀 Initialisation du Chatbot d'Hébergements...")
    
    # Vérification de l'existence du fichier de données
    data_file = 'all_reviews_final.csv'
    if not os.path.exists(data_file):
        print(f"❌ Fichier {data_file} non trouvé dans le répertoire courant.")
        print("💡 Assurez-vous que le fichier de données est présent.")
        return
    
    # Initialisation du chatbot
    chatbot = ChatbotHebergement(data_file)
    
    if chatbot.listings is None:
        print("❌ Impossible d'initialiser le chatbot.")
        return
    
    # Affichage des statistiques
    stats = chatbot.get_statistics()
    print(f"\n📊 STATISTIQUES DU DATASET :")
    print(f"   🏠 Hébergements : {stats['total_listings']:,}")
    print(f"   💬 Avis : {stats['total_reviews']:,}")
    print(f"   🌍 Villes : {', '.join(stats['cities'])}")
    print(f"   ⭐ Score moyen : {stats['avg_quality_score']:.2f}/5")
    print(f"   🏆 Excellents (>4.5) : {stats['top_rated_count']}")
    
    # Lancement de la session de chat
    chatbot.chat_session()


if __name__ == "__main__":
    main()