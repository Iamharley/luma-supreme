#!/usr/bin/env python3
"""
🔥 LUMA BUSINESS PRO - N8N WHATSAPP INTEGRATION
===============================================
Architecture complète pour réponses WhatsApp automatiques
N8N (Webhook) → LUMA (IA Response) → WhatsApp (Reply)
===============================================
FICHIER POUR CURSOR - modules/whatsapp_n8n_service.py
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from flask import Flask, request, jsonify
import requests
import re
from dataclasses import dataclass
import os
from dotenv import load_dotenv
import random

# Charger configuration
load_dotenv('config/.env')

# ==================================================================
# 🔗 N8N WEBHOOK RECEIVER - POINT D'ENTRÉE WHATSAPP
# ==================================================================

class N8NWebhookReceiver:
    """
    📱 Récepteur webhook N8N pour messages WhatsApp
    Point d'entrée de tous les messages clients
    """
    
    def __init__(self, luma_processor):
        self.app = Flask(__name__)
        self.luma_processor = luma_processor
        self.setup_routes()
        
    def setup_routes(self):
        """Configuration des routes Flask"""
        
        @self.app.route('/webhook/whatsapp', methods=['POST'])
        def handle_whatsapp_message():
            """
            📨 Réception message WhatsApp depuis N8N
            Format attendu depuis N8N workflow
            """
            try:
                data = request.get_json()
                
                # Extraction données message
                message_data = {
                    'phone': data.get('from', ''),
                    'message': data.get('message', ''),
                    'timestamp': data.get('timestamp', datetime.now().isoformat()),
                    'message_id': data.get('id', ''),
                    'contact_name': data.get('contact_name', 'Client'),
                    'media_type': data.get('media_type', 'text')
                }
                
                logging.info(f"📱 Message WhatsApp reçu: {message_data['phone']} - {message_data['message'][:50]}...")
                
                # Traitement par LUMA (synchrone pour Flask)
                response = asyncio.run(self.luma_processor.process_whatsapp_message(message_data))
                
                return jsonify({
                    'status': 'success',
                    'luma_response': response,
                    'processed_at': datetime.now().isoformat()
                })
                
            except Exception as e:
                logging.error(f"❌ Erreur webhook WhatsApp: {e}")
                return jsonify({
                    'status': 'error',
                    'error': str(e)
                }), 500
        
        @self.app.route('/webhook/whatsapp/status', methods=['POST'])
        def handle_delivery_status():
            """📋 Gestion statuts de livraison messages"""
            try:
                data = request.get_json()
                status = data.get('status', 'unknown')
                message_id = data.get('message_id', '')
                
                logging.info(f"📊 Statut message {message_id}: {status}")
                
                return jsonify({'status': 'acknowledged'})
                
            except Exception as e:
                logging.error(f"❌ Erreur statut: {e}")
                return jsonify({'status': 'error'}), 500
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """💚 Health check pour monitoring"""
            return jsonify({
                'status': 'healthy',
                'service': 'LUMA WhatsApp',
                'timestamp': datetime.now().isoformat()
            })
    
    def start_server(self, host='localhost', port=5000):
        """🚀 Démarrage serveur webhook"""
        logging.info(f"🔗 Serveur webhook N8N démarré sur {host}:{port}")
        self.app.run(host=host, port=port, debug=False)

# ==================================================================
# 🧠 LUMA WHATSAPP PROCESSOR - INTELLIGENCE RÉPONSE
# ==================================================================

@dataclass
class WhatsAppContext:
    """Contexte client WhatsApp"""
    phone: str
    name: str
    last_interaction: Optional[datetime] = None
    interaction_count: int = 0
    preferred_language: str = "fr"
    vip_status: bool = False
    notes: str = ""

class LumaWhatsAppProcessor:
    """
    🤖 Processeur LUMA pour messages WhatsApp
    Analyse + Contexte + Génération réponse + Envoi N8N
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.n8n_webhook_url = config.get('n8n_send_webhook', '')
        
        # Import modules LUMA existants
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from core.luma_personality import LumaPersonality
            self.personality = LumaPersonality()
            logging.info("✅ Personnalité LUMA chargée")
        except ImportError as e:
            logging.error(f"❌ Erreur import LUMA: {e}")
            self.personality = None
        
        # Cache contexte clients
        self.client_contexts = {}
        
        # Historique conversations pour détection transfert
        self.conversation_histories = {}
        
        # Templates WhatsApp spécialisés
        self.whatsapp_templates = self._load_whatsapp_templates()
    
    def _load_whatsapp_templates(self) -> Dict:
        """📱 Templates WhatsApp spécialisés (style Lulu)"""
        return {
            "welcome_new_client": {
                "template": "Bonjour {name} ! 👋\nMerci de contacter Harley Vape !\n\nJe suis LUMA, l'assistante digitale d'Anne-Sophie. Comment puis-je vous aider aujourd'hui ? 😊\n\n🛒 Commandes\n📦 Suivi livraison\n❓ Questions produits\n\nRépondez simplement !",
                "tone": "chaleureux_professionnel"
            },
            
            "order_inquiry": {
                "template": "📦 Commande en cours !\n\nBonjour {name}, je vérifie votre commande immédiatement.\n\nVotre demande est prise en compte et notre équipe vous recontacte très rapidement avec toutes les infos ! 😊\n\nAutre chose pour vous aider ?",
                "tone": "informatif_rassurant"
            },
            
            "product_question": {
                "template": "🛒 Questions produits !\n\nSalut {name} ! Excellente question sur nos produits Harley Vape.\n\nNotre équipe spécialisée analyse votre demande et vous répond avec tous les détails dans les plus brefs délais !\n\nVoulez-vous que je vous mette en contact direct avec Anne-Sophie ? 📞",
                "tone": "expert_conseil"
            },
            
            "urgent_support": {
                "template": "🚨 URGENT - Pris en charge !\n\nBonjour {name}, je comprends l'urgence de votre situation.\n\nJe transmets immédiatement à Anne-Sophie qui vous recontacte sous 30 minutes maximum.\n\nVotre demande urgente est notre priorité absolue ! 💙",
                "tone": "urgent_rassurant"
            },
            
            "after_hours": {
                "template": "🌙 Harley Vape - Hors horaires\n\nBonsoir {name} !\n\nIl est {time} et notre équipe est en repos bien mérité 😴\n\nVotre message est enregistré et nous vous répondons dès demain matin (9h-18h).\n\nBonne soirée ! 🌟",
                "tone": "bienveillant_informatif"
            },
            
            "general_response": {
                "template": "Salut {name} ! 😊\n\nMerci pour votre message ! Je suis LUMA, l'assistante d'Anne-Sophie pour Harley Vape.\n\nComment puis-je vous aider ?\n\n🛒 Commandes et produits\n📞 Contact direct\n❓ Questions diverses\n\nJe suis là pour vous ! 💙",
                "tone": "chaleureux_disponible"
            }
        }
    
    async def process_whatsapp_message(self, message_data: Dict) -> str:
        """
        ⚡ Traitement principal message WhatsApp
        Pipeline complet: Analyse → Contexte → Réponse → Envoi
        """
        
        phone = message_data['phone']
        message = message_data['message']
        contact_name = message_data.get('contact_name', 'Client')
        
        try:
            # 1. Récupérer/créer contexte client
            context = await self._get_client_context(phone, contact_name)
            
            # 2. Analyser intention message
            intent_analysis = await self._analyze_message_intent(message, context)
            
            # 3. Générer réponse contextuelle
            logging.info("🧠 Tentative génération réponse...")
            try:
                response = await self._generate_contextual_response(
                    message, context, intent_analysis
                )
                logging.info("✅ Réponse générée avec succès")
            except Exception as e:
                logging.error(f"❌ Erreur génération réponse: {e}")
                import traceback
                logging.error(f"❌ Traceback: {traceback.format_exc()}")
                # Fallback simple
                response = f"Bonjour {contact_name} ! Merci pour votre message. Notre équipe Harley Vape vous répond très rapidement ! 😊"
            
            # 4. Envoyer via N8N webhook (si configuré)
            if self.n8n_webhook_url:
                await self._send_via_n8n(phone, response, message_data)
            
            # 5. Mettre à jour contexte client
            await self._update_client_context(context, message, response)
            
            # 6. Log pour monitoring
            await self._log_interaction(phone, message, response, intent_analysis)
            
            return response
            
        except Exception as e:
            logging.error(f"❌ Erreur traitement WhatsApp {phone}: {e}")
            import traceback
            logging.error(f"❌ Traceback: {traceback.format_exc()}")
            
            # Réponse de fallback
            fallback_response = f"Bonjour {contact_name} ! Merci pour votre message. Notre équipe Harley Vape vous répond très rapidement ! 😊"
            
            if self.n8n_webhook_url:
                await self._send_via_n8n(phone, fallback_response, message_data)
            
            return fallback_response
    
    async def _analyze_message_intent(self, message: str, context: WhatsAppContext) -> Dict:
        """
        🔍 Analyse intention du message client
        Classification automatique pour réponse adaptée
        """
        
        message_lower = message.lower()
        
        # Mots-clés par intention
        intent_keywords = {
            "order_inquiry": ["commande", "order", "suivi", "tracking", "livraison", "delivery", "référence", "ref"],
            "product_question": ["produit", "product", "prix", "price", "disponible", "stock", "conseil", "recommande"],
            "urgent_support": ["urgent", "problème", "problem", "help", "aide", "bug", "erreur", "réclamation"],
            "greeting": ["bonjour", "hello", "salut", "hi", "bonsoir", "coucou"],
            "thanks": ["merci", "thank", "parfait", "super", "génial", "top"],
            "complaint": ["déçu", "mécontent", "nul", "mauvais", "insatisfait", "remboursement", "annuler"]
        }
        
        # Analyse sentiment
        positive_words = ["bien", "parfait", "merci", "super", "génial", "top", "excellent"]
        negative_words = ["problème", "déçu", "nul", "mauvais", "erreur", "bug", "urgent"]
        
        sentiment = "neutral"
        if any(word in message_lower for word in positive_words):
            sentiment = "positive"
        elif any(word in message_lower for word in negative_words):
            sentiment = "negative"
        
        # Détection intention principale
        detected_intent = "general"
        max_matches = 0
        
        for intent, keywords in intent_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            if matches > max_matches:
                max_matches = matches
                detected_intent = intent
        
        # Contexte temporel
        current_hour = datetime.now().hour
        is_business_hours = 9 <= current_hour <= 18
        
        # Urgence détectée
        urgency_level = "normal"
        if any(word in message_lower for word in ["urgent", "immédiat", "tout de suite", "maintenant"]):
            urgency_level = "high"
        elif not is_business_hours:
            urgency_level = "low"
        
        return {
            "intent": detected_intent,
            "sentiment": sentiment,
            "urgency": urgency_level,
            "is_business_hours": is_business_hours,
            "confidence": min(max_matches / 3, 1.0),
            "keywords_found": max_matches
        }
    
    async def _generate_contextual_response(self, 
                                          message: str, 
                                          context: WhatsAppContext,
                                          intent_analysis: Dict) -> str:
        """
        🧠 Génération réponse IA conversationnelle
        Utilise la vraie IA LUMA pour des réponses personnalisées
        """
        logging.info(f"🧠 _generate_contextual_response appelée avec message: {message[:50]}...")
        
        # Utiliser la vraie IA LUMA si disponible
        logging.info(f"🧠 Personality disponible: {self.personality is not None}")
        if self.personality:
            try:
                # Contexte pour l'IA
                ai_context = {
                    "client_name": context.name,
                    "from": context.phone,  # Pour détection premier contact
                    "client_phone": context.phone,
                    "interaction_count": context.interaction_count,
                    "preferred_language": context.preferred_language,
                    "business_hours": intent_analysis["is_business_hours"],
                    "urgency": intent_analysis["urgency"],
                    "intent": intent_analysis["intent"],
                    "sentiment": intent_analysis["sentiment"],
                    "business": "Harley Vape",
                    "owner": "Anne-Sophie",
                    "conversation_history": self._get_conversation_history(context.phone)
                }
                
                # Générer réponse avec IA + OpenRouter
                logging.info("🧠 Tentative OpenRouter...")
                
                try:
                    # Appeler OpenRouter via la personnalité LUMA
                    ai_response = await self.personality.generate_whatsapp_response_with_openrouter(message, ai_context)
                    logging.info("✅ OpenRouter utilisé avec succès!")
                    return ai_response
                    
                except Exception as e:
                    logging.warning(f"⚠️ OpenRouter non disponible, fallback templates: {e}")
                    # Fallback vers templates naturels
                    return await self.personality.generate_whatsapp_response(message, ai_context)
                
            except Exception as e:
                logging.error(f"❌ Erreur IA LUMA: {e}")
                # Fallback vers templates basiques
        
        # 🎯 UTILISER LES TEMPLATES NATURELS DIRECTEMENT
        # (solution temporaire pendant qu'on corrige Ollama)
        
        # Détection de langue
        message_lower = message.lower()
        if any(word in message_lower for word in ["hello", "hi", "hey", "what", "how", "can", "you", "help", "thanks", "price", "cost", "open", "hours"]):
            lang = "en"
        elif any(word in message_lower for word in ["bonjour", "salut", "quoi", "comment", "peux", "aide", "merci", "prix", "combien", "ouvert", "horaires"]):
            lang = "fr"
        else:
            lang = "fr"  # défaut français
        
        # Analyse du contexte
        if any(word in message_lower for word in ['price', 'cost', 'precio', 'prix', 'preço', 'cuánto', 'combien', 'quanto']):
            context_type = 'prices'
        elif any(word in message_lower for word in ['open', 'hours', 'horaire', 'abierto', 'aberto', 'fermé', 'closed', 'horas', 'ore']):
            context_type = 'hours'
        elif any(word in message_lower for word in ['product', 'vape', 'disponible', 'available', 'producto', 'produit', 'geekbar']):
            context_type = 'products'
        elif any(word in message_lower for word in ['hi', 'hello', 'hola', 'salut', 'ciao', 'oi', 'hey']):
            context_type = 'greeting'
        else:
            context_type = 'general'
        
        # Templates naturels
        templates = {
            'en': {
                'greeting_new': ["Hey! What can I help you with?", "Hi there! What do you need?"],
                'greeting_return': ["What's up?", "How can I help?", "Need anything?"],
                'products': ["What are you looking for?", "Which product interests you?"],
                'hours': ["We're open 12pm-9pm daily. Coming by?", "Open until 9pm. What do you need?"],
                'prices': ["Depends what you want. What are you interested in?"],
                'general': ["What do you need?", "How can I help?", "What's up?"]
            },
            'fr': {
                'greeting_new': ["Salut ! Je peux t'aider ?", "Hey ! Qu'est-ce qu'il te faut ?"],
                'greeting_return': ["Salut !", "Je peux t'aider ?", "Tu veux quoi ?"],
                'products': ["Tu cherches quoi ?", "Quel produit t'intéresse ?"],
                'hours': ["Ouvert 12h-21h tous les jours. Tu passes ?", "Jusqu'à 21h. Tu veux quoi ?"],
                'prices': ["Ça dépend de quoi. Dis-moi ce qui t'intéresse ?"],
                'general': ["Tu veux quoi ?", "Je peux t'aider ?", "Qu'est-ce qu'il te faut ?"]
            }
        }
        
        # Déterminer la catégorie de template
        is_first_contact = context.interaction_count == 0
        if context_type == 'greeting':
            template_category = 'greeting_new' if is_first_contact else 'greeting_return'
        else:
            template_category = context_type
        
        # Sélectionner réponse aléatoire
        response_templates = templates[lang][template_category]
        response = random.choice(response_templates)
        
        # Ajouter la signature
        signature = "\n\n– L'équipe Harley Vape 🧡" if lang == 'fr' else "\n\n– Team Harley Vape 🧡"
        
        return response + signature
    
    async def _send_via_n8n(self, phone: str, response: str, original_data: Dict):
        """
        📤 Envoi réponse via webhook N8N
        N8N se charge de l'envoi WhatsApp effectif
        """
        
        if not self.n8n_webhook_url:
            logging.info("⚠️ N8N webhook URL non configurée - réponse générée uniquement")
            return
        
        payload = {
            "phone": phone,
            "message": response,
            "timestamp": datetime.now().isoformat(),
            "original_message_id": original_data.get('message_id', ''),
            "luma_processed": True,
            "priority": "normal"
        }
        
        try:
            response_n8n = requests.post(
                self.n8n_webhook_url,
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            if response_n8n.status_code == 200:
                logging.info(f"✅ Message envoyé via N8N: {phone}")
            else:
                logging.warning(f"⚠️ N8N response {response_n8n.status_code}: {response_n8n.text}")
                
        except Exception as e:
            logging.error(f"❌ Erreur envoi N8N: {e}")
    
    async def _get_client_context(self, phone: str, name: str) -> WhatsAppContext:
        """📋 Récupération/création contexte client"""
        
        if phone in self.client_contexts:
            context = self.client_contexts[phone]
            context.interaction_count += 1
            context.last_interaction = datetime.now()
        else:
            context = WhatsAppContext(
                phone=phone,
                name=name,
                last_interaction=datetime.now(),
                interaction_count=1,
                preferred_language="fr",
                vip_status=False,
                notes=""
            )
            self.client_contexts[phone] = context
        
        return context
    
    async def _update_client_context(self, context: WhatsAppContext, message: str, response: str):
        """📝 Mise à jour contexte après interaction"""
        
        # Détection langue
        if any(word in message.lower() for word in ["hello", "hi", "english", "thank you"]):
            context.preferred_language = "en"
        
        # Mise à jour notes (apprentissage)
        if len(context.notes) < 200:
            context.notes += f" {datetime.now().strftime('%d/%m')}: {message[:50]}..."
    
    def _get_conversation_history(self, phone: str) -> list:
        """Récupère l'historique des conversations pour un client"""
        return self.conversation_histories.get(phone, [])
    
    def _add_to_conversation_history(self, phone: str, message: str, response: str):
        """Ajoute un échange à l'historique des conversations"""
        if phone not in self.conversation_histories:
            self.conversation_histories[phone] = []
        
        self.conversation_histories[phone].append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "response": response
        })
        
        # Garder seulement les 10 derniers échanges
        if len(self.conversation_histories[phone]) > 10:
            self.conversation_histories[phone] = self.conversation_histories[phone][-10:]
    
    def _notify_human_transfer(self, context: WhatsAppContext, message: str, reason: str):
        """Notifie Anne-Sophie d'un transfert vers humain"""
        notification = {
            "type": "human_transfer",
            "client_name": context.name,
            "client_phone": context.phone,
            "message": message,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "urgency": "high"
        }
        
        logging.warning(f"🚨 NOTIFICATION TRANSFERT HUMAIN: {json.dumps(notification)}")
        
        # Ici on pourrait envoyer une notification à Anne-Sophie
        # Par exemple via email, SMS, ou webhook vers son téléphone
        # Pour l'instant, on log juste
    
    async def _log_interaction(self, phone: str, message: str, response: str, intent_analysis: Dict):
        """📊 Log interaction pour analytics"""
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "phone": phone[-4:],  # Seulement 4 derniers chiffres pour privacy
            "message_length": len(message),
            "response_length": len(response), 
            "intent": intent_analysis["intent"],
            "sentiment": intent_analysis["sentiment"],
            "confidence": intent_analysis["confidence"]
        }
        
        logging.info(f"📊 WhatsApp interaction: {json.dumps(log_data)}")
        
        # Ajouter à l'historique des conversations
        self._add_to_conversation_history(phone, message, response)

# ==================================================================
# 🚀 LUMA WHATSAPP SERVICE - ORCHESTRATEUR PRINCIPAL
# ==================================================================

class LumaWhatsAppService:
    """
    🎯 Service principal WhatsApp pour LUMA Business Pro
    Combine webhook receiver + processor + monitoring
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.processor = LumaWhatsAppProcessor(config)
        self.webhook_receiver = N8NWebhookReceiver(self.processor)
        
    def start_service(self):
        """🚀 Démarrage service WhatsApp complet"""
        
        logging.info("📱 LUMA WhatsApp Service - Démarrage")
        logging.info(f"🔗 Webhook: {self.config.get('webhook_host', 'localhost')}:{self.config.get('webhook_port', 5000)}")
        logging.info(f"📤 N8N Send: {self.config.get('n8n_send_webhook', 'Non configuré')}")
        
        # Démarrage serveur webhook
        self.webhook_receiver.start_server(
            host=self.config.get('webhook_host', 'localhost'),
            port=self.config.get('webhook_port', 5000)
        )

# ==================================================================
# 🔧 CONFIGURATION & LANCEMENT
# ==================================================================

def create_whatsapp_config() -> Dict:
    """⚙️ Configuration WhatsApp + N8N pour LUMA"""
    
    return {
        # Webhook configuration
        'webhook_host': os.getenv('LUMA_WEBHOOK_HOST', 'localhost'),
        'webhook_port': int(os.getenv('LUMA_WEBHOOK_PORT', 5001)),
        
        # N8N webhooks
        'n8n_send_webhook': os.getenv('N8N_SEND_WEBHOOK', ''),
        
        # Business info
        'business_name': 'Harley Vape',
        'business_phone': os.getenv('BUSINESS_PHONE', '+33123456789'),
        'business_hours': {'start': 9, 'end': 18},
        
        # LUMA config
        'response_delay': 2,
        'max_message_length': 1000,
        'auto_response_enabled': True,
        
        # APIs
        'whatsapp_access_token': os.getenv('WHATSAPP_ACCESS_TOKEN', ''),
        'whatsapp_phone_number_id': os.getenv('WHATSAPP_PHONE_NUMBER_ID', ''),
        'openai_key': os.getenv('OPENAI_API_KEY', ''),
        'claude_key': os.getenv('CLAUDE_API_KEY', ''),
        'openrouter_api_key': os.getenv('OPENROUTER_API_KEY', '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'),
        'openrouter_model': os.getenv('OPENROUTER_MODEL', 'openai/gpt-4-turbo')
    }

def main():
    """🎯 Point d'entrée principal service WhatsApp"""
    
    # Configuration logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Configuration
    config = create_whatsapp_config()
    
    # Initialisation service
    whatsapp_service = LumaWhatsAppService(config)
    
    print("🔥 LUMA BUSINESS PRO - WHATSAPP SERVICE")
    print("📱 Réponses automatiques clients via N8N")
    print("💙 Templates Lulu intégrés")
    print("⚡ Intelligence contextuelle activée")
    print(f"🔗 Webhook: http://{config['webhook_host']}:{config['webhook_port']}/webhook/whatsapp")
    print("\n🚀 Service démarré ! En attente messages...")
    
    try:
        # Démarrage service
        whatsapp_service.start_service()
    except KeyboardInterrupt:
        print("\n👋 Service WhatsApp LUMA arrêté")
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        logging.error(f"Erreur service WhatsApp: {e}")

if __name__ == "__main__":
    main() 