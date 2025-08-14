#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chatbot Avancé avec LangChain et HuggingFace
==========================================

Chatbot intelligent pour recommandations Airbnb utilisant :
- LangChain pour la gestion des conversations
- HuggingFace Transformers pour les modèles de langage
- FAISS pour la recherche vectorielle
- RAG (Retrieval-Augmented Generation)

Auteur: NakibIheb20
Date: 2025
"""

import os
import sys
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    # LangChain imports (versions mises à jour)
    try:
        from langchain_community.llms import HuggingFacePipeline
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        from langchain_community.document_loaders import DataFrameLoader
    except ImportError:
        # Fallback vers les anciens imports
        from langchain.llms import HuggingFacePipeline
        from langchain.embeddings import HuggingFaceEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.document_loaders import DataFrameLoader
    
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationalRetrievalChain
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.prompts import PromptTemplate
    
    # HuggingFace imports
    from transformers import (
        AutoTokenizer, AutoModelForCausalLM,
        pipeline
    )
    import torch
    
    # BitsAndBytesConfig optionnel (pour quantification)
    try:
        from transformers import BitsAndBytesConfig
    except ImportError:
        BitsAndBytesConfig = None
    
    # Interface utilisateur
    import gradio as gr
    
    LANGCHAIN_AVAILABLE = True
    print("✅ LangChain et HuggingFace disponibles")
    
except ImportError as e:
    print(f"⚠️ Certaines dépendances manquent : {e}")
    print("📦 Installez avec : pip install langchain transformers torch gradio")
    LANGCHAIN_AVAILABLE = False


class AirbnbChatbotConfig:
    """Configuration pour le chatbot Airbnb avec LangChain"""
    
    # Modèles HuggingFace recommandés
    MODELS = {
        'small': 'microsoft/DialoGPT-small',  # Rapide, léger
        'medium': 'microsoft/DialoGPT-medium',  # Équilibré
        'french': 'dbmdz/bert-base-french-europeana-cased',  # Français
        'multilingual': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        'gpt2': 'gpt2'  # Fallback simple
    }
    
    # Configuration par défaut
    DEFAULT_MODEL = 'small'
    MAX_LENGTH = 512
    TEMPERATURE = 0.7
    TOP_P = 0.9
    
    # Embeddings pour la recherche sémantique
    EMBEDDING_MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    
    # Prompts en français
    SYSTEM_PROMPT = """
    Tu es un assistant intelligent spécialisé dans les recommandations d'hébergements Airbnb 
    pour la Tunisie, particulièrement Hammamet et Jerba.
    
    Tes responsabilités :
    - Recommander des hébergements basés sur les préférences utilisateur
    - Analyser les avis clients pour donner des conseils
    - Fournir des informations sur les destinations
    - Être amical, professionnel et informatif
    
    Réponds toujours en français et sois concis mais complet.
    """


class AirbnbLangChainChatbot:
    """
    Chatbot Airbnb utilisant LangChain et HuggingFace
    """
    
    def __init__(self, model_size: str = 'small'):
        """
        Initialise le chatbot
        
        Args:
            model_size (str): Taille du modèle à utiliser
        """
        self.config = AirbnbChatbotConfig()
        self.conversation_history = []
        self.model_size = model_size
        
        if LANGCHAIN_AVAILABLE:
            self._initialize_components()
        else:
            print("❌ LangChain non disponible - Mode dégradé")
            self.conversation_chain = None
    
    def _initialize_components(self):
        """Initialise tous les composants du chatbot"""
        print("🔄 Initialisation du chatbot LangChain...")
        
        try:
            # 1. Initialiser le modèle LLM
            self.llm = self._initialize_huggingface_model()
            
            # 2. Créer la base de connaissances
            self.vectorstore = self._create_knowledge_base()
            
            # 3. Configurer la chaîne conversationnelle
            self.conversation_chain = self._create_conversation_chain()
            
            print("✅ Chatbot LangChain initialisé avec succès !")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation : {e}")
            self.conversation_chain = None
    
    def _initialize_huggingface_model(self) -> Optional[HuggingFacePipeline]:
        """
        Initialise le modèle HuggingFace
        
        Returns:
            HuggingFacePipeline: Pipeline LangChain configuré
        """
        print(f"🔄 Chargement du modèle {self.model_size}...")
        
        model_name = self.config.MODELS.get(self.model_size, self.config.MODELS['gpt2'])
        
        try:
            # Configuration pour optimiser la mémoire
            device = 0 if torch.cuda.is_available() else -1
            
            # Créer le pipeline de génération de texte
            text_generation_pipeline = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=model_name,
                max_length=self.config.MAX_LENGTH,
                temperature=self.config.TEMPERATURE,
                top_p=self.config.TOP_P,
                device=device,
                do_sample=True,
                pad_token_id=50256  # Pour éviter les warnings
            )
            
            # Wrapper LangChain
            llm = HuggingFacePipeline(
                pipeline=text_generation_pipeline,
                model_kwargs={
                    "temperature": self.config.TEMPERATURE,
                    "max_length": self.config.MAX_LENGTH
                }
            )
            
            print(f"✅ Modèle {model_name} chargé avec succès !")
            return llm
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle : {e}")
            print("🔄 Tentative avec GPT-2...")
            
            # Fallback vers GPT-2
            try:
                simple_pipeline = pipeline(
                    "text-generation",
                    model="gpt2",
                    max_length=256,
                    device=device
                )
                
                return HuggingFacePipeline(pipeline=simple_pipeline)
            except Exception as e2:
                print(f"❌ Impossible de charger un modèle : {e2}")
                return None
    
    def _create_knowledge_base(self) -> Optional[FAISS]:
        """
        Crée une base de connaissances vectorielle pour le RAG
        
        Returns:
            FAISS: Base de données vectorielle
        """
        print("📚 Création de la base de connaissances...")
        
        try:
            # Données d'exemple sur les hébergements Airbnb Tunisie
            knowledge_data = [
                {
                    "content": "Hammamet est une destination balnéaire populaire en Tunisie, connue pour ses plages de sable fin et sa médina historique. Les hébergements Airbnb y offrent souvent des vues sur mer et un accès facile aux attractions touristiques.",
                    "location": "Hammamet",
                    "type": "destination_info"
                },
                {
                    "content": "Jerba est une île tunisienne réputée pour son climat doux, ses plages magnifiques et son patrimoine culturel riche. Les hébergements traditionnels avec architecture locale sont très appréciés des visiteurs.",
                    "location": "Jerba", 
                    "type": "destination_info"
                },
                {
                    "content": "Pour un séjour familial, privilégiez les hébergements avec piscine, cuisine équipée et proximité des plages. Les villas avec jardin sont idéales pour les groupes.",
                    "location": "Général",
                    "type": "recommendation"
                },
                {
                    "content": "Les couples apprécient les riads traditionnels avec terrasse privée, les appartements avec vue sur mer et les hébergements dans les médinas pour une expérience authentique.",
                    "location": "Général",
                    "type": "recommendation"
                },
                {
                    "content": "La meilleure période pour visiter la Tunisie est d'avril à juin et de septembre à novembre. Les prix des hébergements sont plus avantageux hors saison estivale.",
                    "location": "Général",
                    "type": "travel_tips"
                }
            ]
            
            # Créer un DataFrame
            df = pd.DataFrame(knowledge_data)
            
            # Charger avec LangChain
            loader = DataFrameLoader(df, page_content_column="content")
            documents = loader.load()
            
            # Diviser les documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            texts = text_splitter.split_documents(documents)
            
            # Créer les embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name=self.config.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'}  # Utiliser CPU pour la compatibilité
            )
            
            # Créer la base vectorielle FAISS
            vectorstore = FAISS.from_documents(texts, embeddings)
            
            print(f"✅ Base de connaissances créée avec {len(texts)} documents")
            return vectorstore
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de la base de connaissances : {e}")
            return None
    
    def _create_conversation_chain(self) -> Optional[ConversationalRetrievalChain]:
        """
        Crée une chaîne conversationnelle avec mémoire et RAG
        
        Returns:
            ConversationalRetrievalChain: Chaîne conversationnelle
        """
        if not self.llm or not self.vectorstore:
            print("❌ Impossible de créer la chaîne conversationnelle")
            return None
        
        print("🔗 Configuration de la chaîne conversationnelle...")
        
        try:
            # Mémoire conversationnelle
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
            
            # Créer la chaîne conversationnelle
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 3}  # Récupérer les 3 documents les plus pertinents
                ),
                memory=memory,
                return_source_documents=True,
                verbose=True
            )
            
            print("✅ Chaîne conversationnelle configurée")
            return qa_chain
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de la chaîne : {e}")
            return None
    
    def chat(self, user_input: str) -> Dict[str, Any]:
        """
        Traite une question utilisateur et retourne une réponse
        
        Args:
            user_input (str): Question de l'utilisateur
        
        Returns:
            Dict: Réponse avec métadonnées
        """
        if not self.conversation_chain:
            return self._fallback_response(user_input)
        
        try:
            # Obtenir la réponse de la chaîne conversationnelle
            result = self.conversation_chain({
                "question": user_input
            })
            
            # Extraire la réponse
            answer = result.get("answer", "Désolé, je n'ai pas pu traiter votre demande.")
            source_docs = result.get("source_documents", [])
            
            # Ajouter à l'historique
            self.conversation_history.append({
                "user": user_input,
                "bot": answer,
                "sources": len(source_docs)
            })
            
            return {
                "answer": answer,
                "sources": source_docs,
                "confidence": self._calculate_confidence(answer, source_docs),
                "method": "langchain"
            }
            
        except Exception as e:
            print(f"❌ Erreur lors du traitement : {e}")
            return self._fallback_response(user_input)
    
    def _fallback_response(self, user_input: str) -> Dict[str, Any]:
        """
        Réponse de secours quand LangChain n'est pas disponible
        
        Args:
            user_input (str): Question de l'utilisateur
        
        Returns:
            Dict: Réponse de base
        """
        # Réponses prédéfinies simples
        responses = {
            "hammamet": "Hammamet est une excellente destination avec de belles plages et une médina historique. Je recommande les hébergements avec vue sur mer.",
            "jerba": "Jerba est parfaite pour des vacances relaxantes avec son climat doux et ses plages magnifiques. Les hébergements traditionnels sont très appréciés.",
            "famille": "Pour les familles, je conseille les villas avec piscine et cuisine équipée, proche des plages et des activités pour enfants.",
            "couple": "Les couples apprécient les riads avec terrasse privée et les appartements romantiques avec vue sur mer.",
            "période": "La meilleure période est d'avril à juin et de septembre à novembre pour éviter la forte chaleur estivale."
        }
        
        user_lower = user_input.lower()
        
        # Recherche de mots-clés
        for keyword, response in responses.items():
            if keyword in user_lower:
                return {
                    "answer": response,
                    "sources": [],
                    "confidence": 0.6,
                    "method": "fallback"
                }
        
        # Réponse par défaut
        return {
            "answer": "Bonjour ! Je suis votre assistant pour les hébergements Airbnb en Tunisie. Posez-moi vos questions sur Hammamet, Jerba, ou vos préférences de voyage !",
            "sources": [],
            "confidence": 0.5,
            "method": "fallback"
        }
    
    def _calculate_confidence(self, answer: str, sources: List) -> float:
        """
        Calcule un score de confiance basé sur la réponse et les sources
        
        Args:
            answer (str): Réponse générée
            sources (List): Sources utilisées
        
        Returns:
            float: Score de confiance (0-1)
        """
        if not answer or "désolé" in answer.lower():
            return 0.2
        
        # Plus il y a de sources, plus la confiance est élevée
        source_score = min(len(sources) * 0.3, 0.9)
        
        # Longueur de la réponse (réponses plus détaillées = plus de confiance)
        length_score = min(len(answer) / 200, 0.5)
        
        return min(source_score + length_score + 0.3, 1.0)
    
    def get_conversation_history(self) -> List[Dict]:
        """Retourne l'historique de conversation"""
        return self.conversation_history
    
    def clear_history(self):
        """Efface l'historique de conversation"""
        self.conversation_history = []
        if self.conversation_chain and hasattr(self.conversation_chain, 'memory'):
            self.conversation_chain.memory.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques du chatbot
        
        Returns:
            Dict: Statistiques d'utilisation
        """
        history = self.get_conversation_history()
        
        if not history:
            return {
                "total_conversations": 0,
                "avg_confidence": 0.0,
                "total_sources_used": 0,
                "langchain_enabled": LANGCHAIN_AVAILABLE
            }
        
        confidences = [conv.get("confidence", 0) for conv in history if "confidence" in conv]
        sources = [conv.get("sources", 0) for conv in history if "sources" in conv]
        
        return {
            "total_conversations": len(history),
            "avg_confidence": np.mean(confidences) if confidences else 0.0,
            "total_sources_used": sum(sources),
            "langchain_enabled": LANGCHAIN_AVAILABLE and self.conversation_chain is not None
        }


def create_gradio_interface(chatbot: AirbnbLangChainChatbot):
    """
    Crée une interface Gradio pour le chatbot
    
    Args:
        chatbot: Instance du chatbot
    
    Returns:
        gr.Blocks: Interface Gradio
    """
    def chat_interface(message, history):
        """Interface de chat pour Gradio"""
        if not message.strip():
            return history, ""
        
        # Obtenir la réponse du chatbot
        response = chatbot.chat(message)
        
        # Ajouter à l'historique Gradio
        history.append([message, response['answer']])
        
        return history, ""
    
    def clear_chat():
        """Efface l'historique de chat"""
        chatbot.clear_history()
        return [], ""
    
    def show_stats():
        """Affiche les statistiques"""
        stats = chatbot.get_stats()
        return f"""
        📊 **Statistiques du Chatbot**
        - Conversations: {stats['total_conversations']}
        - Confiance moyenne: {stats['avg_confidence']:.2f}
        - Sources utilisées: {stats['total_sources_used']}
        - LangChain actif: {'✅' if stats['langchain_enabled'] else '❌'}
        """
    
    # Créer l'interface Gradio
    with gr.Blocks(
        title="🏠 Chatbot Airbnb Tunisie - LangChain + HuggingFace",
        theme=gr.themes.Soft()
    ) as interface:
        
        gr.Markdown("""
        # 🤖 Assistant Airbnb Intelligent
        
        Powered by **LangChain** + **HuggingFace** 🚀
        
        Posez-moi vos questions sur les hébergements Airbnb en Tunisie !
        """)
        
        with gr.Tab("💬 Chat"):
            chatbot_interface = gr.Chatbot(
                label="Conversation",
                height=400,
                show_label=True
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Votre message",
                    placeholder="Tapez votre question ici...",
                    scale=4
                )
                send_btn = gr.Button("Envoyer 📤", scale=1)
            
            with gr.Row():
                clear_btn = gr.Button("Effacer 🗑️")
                
            # Exemples de questions
            gr.Examples(
                examples=[
                    "Recommande-moi un hébergement à Hammamet",
                    "Quels sont les avantages de Jerba ?",
                    "Je voyage en famille, que conseilles-tu ?",
                    "Quelle est la meilleure période pour visiter ?"
                ],
                inputs=msg
            )
        
        with gr.Tab("📊 Statistiques"):
            stats_btn = gr.Button("Actualiser les statistiques")
            stats_output = gr.Markdown()
        
        # Événements
        send_btn.click(
            chat_interface,
            inputs=[msg, chatbot_interface],
            outputs=[chatbot_interface, msg]
        )
        
        msg.submit(
            chat_interface,
            inputs=[msg, chatbot_interface],
            outputs=[chatbot_interface, msg]
        )
        
        clear_btn.click(
            clear_chat,
            outputs=[chatbot_interface, msg]
        )
        
        stats_btn.click(
            show_stats,
            outputs=stats_output
        )
    
    return interface


def main():
    """Fonction principale"""
    print("🚀 Démarrage du Chatbot Airbnb LangChain...")
    print("=" * 50)
    
    # Initialiser le chatbot
    chatbot = AirbnbLangChainChatbot(model_size='small')
    
    # Tests rapides
    print("\n🧪 Tests du chatbot...")
    test_questions = [
        "Bonjour !",
        "Recommande-moi un hébergement à Hammamet",
        "Je voyage en famille"
    ]
    
    for question in test_questions:
        print(f"\n🙋 {question}")
        response = chatbot.chat(question)
        print(f"🤖 {response['answer'][:100]}...")
        print(f"📊 Confiance: {response['confidence']:.2f} | Méthode: {response['method']}")
    
    # Afficher les statistiques
    stats = chatbot.get_stats()
    print(f"\n📊 Statistiques finales:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Créer l'interface Gradio
    if LANGCHAIN_AVAILABLE:
        print("\n🎨 Création de l'interface Gradio...")
        interface = create_gradio_interface(chatbot)
        
        print("✅ Interface prête !")
        print("💡 Décommentez la ligne suivante pour lancer l'interface web:")
        print("# interface.launch(share=True, debug=True)")
        
        # Décommentez pour lancer l'interface
        # interface.launch(share=True, debug=True)
    else:
        print("⚠️ Interface Gradio non disponible sans LangChain")
    
    return chatbot


if __name__ == "__main__":
    chatbot = main()