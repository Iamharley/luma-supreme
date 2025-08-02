"""
🧬 LUMA Personality System
Personnalité et templates de conversation pour Anne-Sophie
"""

import random
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import subprocess
import json
import re
import logging
import os
import openai
from openai import OpenAI


class ConversationTemplate:
    """Templates de conversation personnalisés pour Anne-Sophie"""
    
    def __init__(self):
        self.templates = {
            "morning_briefing": {
                "greeting": [
                    "Bonjour Anne-Sophie 🌞",
                    "Salut ma belle ! ☀️",
                    "Hey Anne-Sophie, bonne journée ! 🌅"
                ],
                "structure": [
                    "Voici ton point du jour :",
                    "Résumé de la situation :",
                    "État des lieux :"
                ],
                "closing": [
                    "🧠 Tu veux que je gère un truc aujourd'hui ?",
                    "💪 Besoin d'aide sur quelque chose ?",
                    "🎯 Qu'est-ce que je peux faire pour toi ?"
                ]
            },
            "urgent_alert": {
                "warning": [
                    "🚨 URGENT - ",
                    "⚠️ ATTENTION - ",
                    "🔥 PRIORITÉ - "
                ],
                "action": [
                    "Action requise immédiatement",
                    "Besoin de ta décision",
                    "Intervention nécessaire"
                ]
            },
            "business_update": {
                "positive": [
                    "✅ Excellente nouvelle !",
                    "🎉 Super résultat !",
                    "💪 Parfait travail !"
                ],
                "neutral": [
                    "📊 Mise à jour business :",
                    "💼 État des affaires :",
                    "📈 Situation actuelle :"
                ]
            }
        }
    
    def get_template(self, template_name: str, context: Dict[str, Any] = None) -> str:
        """Génère un message basé sur un template"""
        if template_name not in self.templates:
            return "Message par défaut"
        
        template = self.templates[template_name]
        context = context or {}
        
        if template_name == "morning_briefing":
            return self._generate_morning_briefing(template, context)
        elif template_name == "urgent_alert":
            return self._generate_urgent_alert(template, context)
        elif template_name == "business_update":
            return self._generate_business_update(template, context)
        
        return "Template non reconnu"
    
    def _generate_morning_briefing(self, template: Dict, context: Dict) -> str:
        """Génère le briefing matinal"""
        greeting = random.choice(template["greeting"])
        structure = random.choice(template["structure"])
        closing = random.choice(template["closing"])
        
        # Construire le contenu
        content_parts = []
        
        if context.get("emails"):
            content_parts.append(f"📩 {context['emails']} mails prioritaires")
        
        if context.get("orders"):
            content_parts.append(f"🛒 {context['orders']} commandes Shopify")
        
        if context.get("whatsapp"):
            content_parts.append(f"🔔 {context['whatsapp']} client(s) WhatsApp en attente")
        
        if context.get("insight"):
            content_parts.append(f"💡 Conseil : {context['insight']}")
        
        content = "\n".join(content_parts) if content_parts else "Aucune activité majeure"
        
        return f"{greeting}\n{structure}\n{content}\n{closing}"
    
    def _generate_urgent_alert(self, template: Dict, context: Dict) -> str:
        """Génère une alerte urgente"""
        warning = random.choice(template["warning"])
        action = random.choice(template["action"])
        
        message = context.get("message", "Alerte sans message")
        return f"{warning}{message}\n{action}"
    
    def _generate_business_update(self, template: Dict, context: Dict) -> str:
        """Génère une mise à jour business"""
        if context.get("positive", False):
            intro = random.choice(template["positive"])
        else:
            intro = random.choice(template["neutral"])
        
        message = context.get("message", "Mise à jour business")
        return f"{intro}\n{message}"


class NaturalTemplates:
    """Système de templates naturels multilingues pour LUMA"""
    
    def __init__(self):
        self.templates = {
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
            },
            'es': {
                'greeting_new': ["¡Hola! ¿En qué te puedo ayudar?", "¡Hey! ¿Qué necesitas?"],
                'greeting_return': ["¿Qué tal?", "¿Te ayudo en algo?", "¿Necesitas algo?"],
                'products': ["¿Qué buscas?", "¿Qué producto te interesa?"],
                'hours': ["Abierto de 12 a 21h todos los días. ¿Vienes?", "Hasta las 21h. ¿Qué necesitas?"],
                'prices': ["Depende de qué quieras. ¿Qué te interesa?"],
                'general': ["¿Qué necesitas?", "¿Te ayudo?", "¿Qué pasa?"]
            },
            'it': {
                'greeting_new': ["Ciao! Come posso aiutarti?", "Hey! Di cosa hai bisogno?"],
                'greeting_return': ["Ciao!", "Ti serve qualcosa?", "Come va?"],
                'products': ["Cosa cerchi?", "Quale prodotto ti interessa?"],
                'hours': ["Aperto 12-21 tutti i giorni. Passi?", "Fino alle 21. Cosa ti serve?"],
                'prices': ["Dipende da cosa vuoi. Dimmi cosa ti interessa?"],
                'general': ["Cosa ti serve?", "Come ti aiuto?", "Dimmi!"]
            },
            'pt': {
                'greeting_new': ["Oi! Como posso ajudar?", "E aí! O que você precisa?"],
                'greeting_return': ["E aí!", "Precisa de algo?", "Como vai?"],
                'products': ["O que você está procurando?", "Qual produto te interessa?"],
                'hours': ["Aberto 12h-21h todo dia. Vai passar aqui?", "Até às 21h. O que precisa?"],
                'prices': ["Depende do que você quer. Me diz o que te interessa?"],
                'general': ["O que você precisa?", "Como te ajudo?", "Fala aí!"]
            }
        }
        
        self.client_memory = {}  # Mémoire par client
    
    def detect_language(self, message: str) -> str:
        """Détecte la langue du message"""
        message_lower = message.lower()
        
        # Détection hébreu (caractères hébreux)
        hebrew_chars = re.search(r'[\u0590-\u05FF]', message)
        if hebrew_chars:
            return 'he'
        
        patterns = {
            'en': r'\b(hello|hi|hey|what|how|can|you|help|thanks|price|cost|open|hours)\b',
            'es': r'\b(hola|qué|cómo|puedes|ayuda|gracias|precio|cuánto|abierto|horas)\b',
            'fr': r'\b(bonjour|salut|quoi|comment|peux|aide|merci|prix|combien|ouvert|horaires)\b',
            'it': r'\b(ciao|cosa|come|puoi|aiuto|grazie|prezzo|quanto|aperto|ore)\b',
            'pt': r'\b(olá|oi|que|como|pode|ajuda|obrigado|preço|quanto|aberto|horas)\b'
        }
        
        for lang, pattern in patterns.items():
            if re.search(pattern, message_lower):
                return lang
        
        return 'fr'  # défaut français
    
    def analyze_context(self, message: str) -> str:
        """Analyse le contexte du message"""
        msg = message.lower()
        
        if any(word in msg for word in ['price', 'cost', 'precio', 'prix', 'preço', 'cuánto', 'combien', 'quanto']):
            return 'prices'
        elif any(word in msg for word in ['open', 'hours', 'horaire', 'abierto', 'aberto', 'fermé', 'closed', 'horas', 'ore']):
            return 'hours'
        elif any(word in msg for word in ['product', 'vape', 'disponible', 'available', 'producto', 'produit', 'geekbar']):
            return 'products'
        elif any(word in msg for word in ['hi', 'hello', 'hola', 'salut', 'ciao', 'oi', 'hey']):
            return 'greeting'
        else:
            return 'general'
    
    def generate_natural_response(self, client_id: str, message: str) -> str:
        """Génère une réponse naturelle basée sur les templates"""
        lang = self.detect_language(message)
        is_new_client = client_id not in self.client_memory
        context = self.analyze_context(message)
        
        # Déterminer la catégorie de template
        if context == 'greeting':
            template_category = 'greeting_new' if is_new_client else 'greeting_return'
        else:
            template_category = context
        
        # Sélectionner réponse aléatoire
        templates = self.templates[lang][template_category]
        response = random.choice(templates)
        
        # Sauvegarder en mémoire
        self.client_memory[client_id] = {
            'last_message': message,
            'language': lang,
            'context': context,
            'timestamp': asyncio.get_event_loop().time()
        }
        
        return response


class LumaPersonality:
    """Personnalité LUMA pour Anne-Sophie"""
    
    def __init__(self):
        self.name = "LUMA"
        self.owner = "Anne-Sophie"
        self.business = "Harley Vape"
        self.templates = ConversationTemplate()
        # Clients déjà vus pour détecter premier contact
        self.known_clients = set()
        
        # Configuration OpenRouter
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY', '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')
        self.openrouter_model = os.getenv('OPENROUTER_MODEL', 'openai/gpt-4-turbo')
        
        # Configuration OpenAI pour OpenRouter
        try:
            self.openai_client = OpenAI(
                api_key=self.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        except Exception as e:
            print(f"⚠️ Erreur OpenRouter: {e}")
            self.openai_client = None
        
        self.personality_traits = {
            "professional": True,
            "warm": True,
            "proactive": True,
            "efficient": True,
            "supportive": True,
            "chill": True,
            "friendly": True
        }
        
        # Personnalité authentique Harley Vape
        self.introduction = {
            "en": "Hey there! 👋 I'm Luma — the AI of the Harley Vape Team 🌬️🌈🐾\nWe're a chill crew, always happy to help you find your perfect puff 💨",
            "fr": "Salut ! 👋 Je suis Luma — l'IA de l'équipe Harley Vape 🌬️🌈🐾\nOn est une équipe cool, toujours ravis de vous aider à trouver votre puff parfait 💨"
        }
        
        self.hours = {
            "en": "🕛 Opening hours: 12:00 PM – 9:00 PM (Paris time)",
            "fr": "🕛 Horaires d'ouverture : 12h00 – 21h00 (heure de Paris)"
        }
        
        self.availability = {
            "en": "💬 Available here on WhatsApp 24/7",
            "fr": "💬 Disponible ici sur WhatsApp 24h/24"
        }
        
        self.website = {
            "en": "🌐 Website coming soon → www.harleyvape.love",
            "fr": "🌐 Site web bientôt disponible → www.harleyvape.love"
        }
        
        self.signature = {
            "en": "Talk soon!\n– Team Harley Vape 🧡",
            "fr": "À bientôt !\n– L'équipe Harley Vape 🧡"
        }
    
    def generate_response(self, template_name: str, context: Dict[str, Any] = None) -> str:
        """Génère une réponse personnalisée"""
        return self.templates.get_template(template_name, context)
    
    def get_personality_context(self) -> Dict[str, Any]:
        """Retourne le contexte de personnalité"""
        return {
            "name": self.name,
            "owner": self.owner,
            "business": self.business,
            "traits": self.personality_traits,
            "timestamp": datetime.now().isoformat()
        }
    
    def is_first_contact(self, client_number: str) -> bool:
        """Détecte si c'est le premier contact avec ce client"""
        if client_number not in self.known_clients:
            self.known_clients.add(client_number)
            return True
        return False
    
    def should_transfer_to_human(self, message: str, conversation_history: list = None) -> bool:
        """Détecte si la conversation doit être transférée à une vraie personne"""
        message_lower = message.lower()
        
        # 🚨 MOTS CLÉS URGENTS = Transfert immédiat
        urgent_keywords = [
            'plainte', 'réclamation', 'problème', 'défaut', 'cassé', 'marché pas',
            'remboursement', 'argent', 'facture', 'commande', 'livraison',
            'urgent', 'important', 'grave', 'sérieux'
        ]
        
        for keyword in urgent_keywords:
            if keyword in message_lower:
                return True
        
        # 🤝 QUESTIONS COMPLEXES = Transfert
        complex_questions = [
            'comment ça marche', 'explique-moi', 'détaillé', 'spécifique',
            'technique', 'mécanisme', 'fonctionnement', 'différence entre'
        ]
        
        for question in complex_questions:
            if question in message_lower:
                return True
        
        # 💰 NÉGOCIATION = Transfert
        negotiation_words = [
            'prix', 'coût', 'tarif', 'réduction', 'promotion', 'offre',
            'moins cher', 'bon plan', 'deal', 'marchandage'
        ]
        
        for word in negotiation_words:
            if word in message_lower:
                return True
        
        # 📞 DEMANDE DE CONTACT = Transfert
        contact_requests = [
            'parler à', 'vraie personne', 'humain', 'responsable',
            'manager', 'patron', 'propriétaire', 'directeur'
        ]
        
        for request in contact_requests:
            if request in message_lower:
                return True
        
        # 🔄 CONVERSATION TROP LONGUE = Transfert après 5 échanges
        if conversation_history and len(conversation_history) >= 5:
            return True
        
        return False
    
    def generate_transfer_message(self, client_name: str, reason: str = None) -> str:
        """Génère un message de transfert vers une vraie personne"""
        transfer_messages = [
            f"OK {client_name}, je vais te mettre en contact avec Anne-Sophie directement. Elle va te rappeler dans 2 minutes !",
            f"Parfait, je transfère à Anne-Sophie qui va t'appeler tout de suite.",
            f"Je passe la main à Anne-Sophie qui va te contacter dans 2 minutes.",
            f"Anne-Sophie va te rappeler immédiatement pour s'occuper de ça !"
        ]
        
        return transfer_messages[0]  # Version simple pour l'instant
    
    def validate_human_response(self, response: str) -> str:
        """Valide et corrige les réponses pour qu'elles soient naturelles"""
        response_lower = response.lower()
        
        # ❌ INTERDIRE ces mots robots SEULEMENT si c'est le début de la réponse
        robot_words = ['bonjour', '😊', 'comment puis-je', 'équipe harley vape', 'n\'hésitez pas', 'merci pour votre']
        
        # Vérifier si la réponse commence par un mot robot
        for word in robot_words:
            if response_lower.startswith(word.lower()):
                # Remplacer par version naturelle
                return "Salut ! Comment je peux t'aider ?"
        
        # ❌ INTERDIRE les réponses trop longues (plus de 150 caractères)
        if len(response) > 150:
            return "Dis-moi ce qui t'intéresse ?"
        
        # ✅ Si la réponse est bonne, la garder
        return response
    
    def adapt_tone(self, message: str, urgency: str = "normal") -> str:
        """Adapte le ton selon l'urgence"""
        if urgency == "urgent":
            return f"🚨 {message}"
        elif urgency == "positive":
            return f"✅ {message}"
        elif urgency == "warning":
            return f"⚠️ {message}"
        else:
            return message
    
    async def generate_whatsapp_response(self, message: str, context: Dict[str, Any]) -> str:
        """
        🧠 Génère une réponse WhatsApp conversationnelle et personnalisée
        Utilise les templates naturels pour des réponses intelligentes
        """
        
        # 🎯 UTILISER LES TEMPLATES NATURELS DIRECTEMENT
        client_name = context.get("client_name", "Client")
        client_number = context.get("from", "unknown")
        message_lower = message.lower()
        
        # Détection de langue
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
        
        # Déterminer la catégorie de template
        is_first_contact = client_number not in self.client_memory
        if context_type == 'greeting':
            template_category = 'greeting_new' if is_first_contact else 'greeting_return'
        else:
            template_category = context_type
        
        # Sélectionner réponse aléatoire
        templates = self.templates[lang][template_category]
        response = random.choice(templates)
        
        # Sauvegarder en mémoire
        self.client_memory[client_number] = {
            'last_message': message,
            'language': lang,
            'context': context_type,
            'timestamp': asyncio.get_event_loop().time()
        }
        
        # Ajouter la signature
        signature = "\n\n– L'équipe Harley Vape 🧡" if lang == 'fr' else "\n\n– Team Harley Vape 🧡"
        
        return response + signature

    async def generate_whatsapp_response_with_openrouter(self, message: str, context: Dict[str, Any]) -> str:
        """
        🧠 Génère une réponse conversationnelle avec GPT-4 via OpenRouter
        Utilise une vraie IA pour des réponses naturelles et contextuelles
        """
        
        client_name = context.get("client_name", "Client")
        client_number = context.get("from", "unknown")
        message_lower = message.lower()
        conversation_history = context.get("conversation_history", [])
        
        # Détecter si c'est le premier contact
        is_first_contact = self.is_first_contact(client_number)
        
        # 🚨 VÉRIFIER SI TRANSFERT VERS HUMAIN
        if self.should_transfer_to_human(message, conversation_history):
            transfer_message = self.generate_transfer_message(client_name)
            # Ajouter un flag pour notifier Anne-Sophie
            context["transfer_to_human"] = True
            context["transfer_reason"] = "Conversation complexe détectée"
            return transfer_message
        
        try:
            # Détecter la langue du message
            detected_lang = self.detect_language(message)
            
            # 🎯 PROMPT POUR OPENROUTER (MULTILINGUE)
            if detected_lang == 'he':  # Hébreu
                system_prompt = f"""You are Luma, Anne-Sophie's WhatsApp assistant for her Harley Vape shop.

PERSONALITY:
- Experienced vape shop seller
- Relaxed but professional tone
- Natural Hebrew speaker
- Maximum 10-15 words per response
- Direct and efficient
- NO "Hello" if not first message
- NO systematic smile emoji

IMPORTANT INFO:
- Shop: Harley Vape
- Hours: 12:00-21:00 daily (Paris time)
- WhatsApp available 24/7
- Website: www.harleyvape.love

CONTEXT:
- Client: {client_name}
- First contact: {"Yes" if is_first_contact else "No"}
- Message: "{message}"
- History: {len(conversation_history)} previous messages

STRICT RULES:
- Answer ONLY in 1-2 short sentences
- Natural Hebrew seller tone
- No excessive formalities
- No systematic emojis
- Direct and useful response

EXAMPLES:
Client: "שלום" (Hello)
→ "שלום! איך אני יכול לעזור לך?" (Hello! How can I help you?)

Client: "יש לכם גיקבר?" (Do you have geekbar?)
→ "כן, יש לנו כמה מודלים. איזה אתה מחפש?" (Yes, we have several models. Which one are you looking for?)

Answer like a natural Hebrew vape shop seller:"""
            
            elif detected_lang == 'en':  # Anglais
                system_prompt = f"""You are Luma, Anne-Sophie's WhatsApp assistant for her Harley Vape shop.

PERSONALITY:
- Experienced vape shop seller
- Relaxed but professional tone
- Natural English speaker
- Maximum 10-15 words per response
- Direct and efficient
- NO "Hello" if not first message
- NO systematic smile emoji

IMPORTANT INFO:
- Shop: Harley Vape
- Hours: 12:00-21:00 daily (Paris time)
- WhatsApp available 24/7
- Website: www.harleyvape.love

CONTEXT:
- Client: {client_name}
- First contact: {"Yes" if is_first_contact else "No"}
- Message: "{message}"
- History: {len(conversation_history)} previous messages

STRICT RULES:
- Answer ONLY in 1-2 short sentences
- Natural English seller tone
- No excessive formalities
- No systematic emojis
- Direct and useful response

EXAMPLES:
Client: "Do you have geekbar?"
→ "Yeah, several models. Which one are you looking for?"

Client: "Are you open?"
→ "Yes, until 9pm. Coming by?"

Answer like a natural English vape shop seller:"""
            
            else:  # Français (défaut)
                system_prompt = f"""Tu es Luma, assistante WhatsApp personnelle d'Anne-Sophie pour sa boutique Harley Vape.

PERSONNALITÉ:
- Vendeur expérimenté de vape shop en France
- Ton décontracté mais professionnel
- Français naturel de vendeur
- Maximum 10-15 mots par réponse
- Direct et efficace
- JAMAIS de "Bonjour" si pas le premier message
- JAMAIS d'émoji sourire systématique

INFORMATIONS IMPORTANTES:
- Boutique: Harley Vape
- Horaires: 12h00-21h00 tous les jours (heure de Paris)
- WhatsApp disponible 24h/24
- Site web: www.harleyvape.love

CONTEXTE:
- Client: {client_name}
- Premier contact: {"Oui" if is_first_contact else "Non"}
- Message: "{message}"
- Historique: {len(conversation_history)} messages précédents

RÈGLES STRICTES:
- Réponds UNIQUEMENT en 1-2 phrases courtes
- Ton naturel de vendeur français
- Pas de formalités excessives
- Pas d'émojis systématiques
- Réponse directe et utile

EXEMPLES:
Client: "Tu as des geekbar ?"
→ "Ouais, plusieurs modèles. Lequel tu cherches ?"

Client: "C'est ouvert ?"
→ "Oui, jusqu'à 21h. Tu passes ?"

Réponds comme un vrai vendeur français décontracté:"""

            # 🚀 APPEL OPENROUTER
            response = self.openai_client.chat.completions.create(
                model=self.openrouter_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=120
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # 🧹 NETTOYAGE DE LA RÉPONSE
            # Supprimer les guillemets si présents
            if ai_response.startswith('"') and ai_response.endswith('"'):
                ai_response = ai_response[1:-1]
            
            # Ajouter la signature
            signature = "\n\n– L'équipe Harley Vape 🧡"
            
            return ai_response + signature
        
        except Exception as e:
            logging.error(f"❌ Erreur OpenRouter: {e}")
            # Fallback vers templates naturels
            return await self.generate_whatsapp_response(message, context)
    
    def detect_language(self, message: str) -> str:
        """Détecte la langue du message"""
        message_lower = message.lower()
        
        # Détection hébreu (caractères hébreux)
        hebrew_chars = re.search(r'[\u0590-\u05FF]', message)
        if hebrew_chars:
            return 'he'
        
        patterns = {
            'en': r'\b(hello|hi|hey|what|how|can|you|help|thanks|price|cost|open|hours)\b',
            'es': r'\b(hola|qué|cómo|puedes|ayuda|gracias|precio|cuánto|abierto|horas)\b',
            'fr': r'\b(bonjour|salut|quoi|comment|peux|aide|merci|prix|combien|ouvert|horaires)\b',
            'it': r'\b(ciao|cosa|come|puoi|aiuto|grazie|prezzo|quanto|aperto|ore)\b',
            'pt': r'\b(olá|oi|que|como|pode|ajuda|obrigado|preço|quanto|aberto|horas)\b'
        }
        
        for lang, pattern in patterns.items():
            if re.search(pattern, message_lower):
                return lang
        
        return 'fr'  # défaut français


if __name__ == "__main__":
    # Test de la personnalité LUMA
    personality = LumaPersonality()
    
    # Test morning briefing
    morning_context = {
        "emails": "3",
        "orders": "1",
        "whatsapp": "2",
        "insight": "Journée productive en vue !"
    }
    
    morning_msg = personality.generate_response("morning_briefing", morning_context)
    print("🌞 Test Template Lulu:")
    print(morning_msg)
    
    # Test urgent alert
    urgent_context = {
        "message": "Client mécontent sur Instagram"
    }
    
    urgent_msg = personality.generate_response("urgent_alert", urgent_context)
    print("\n🚨 Test Alerte Urgente:")
    print(urgent_msg) 