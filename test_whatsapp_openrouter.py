#!/usr/bin/env python3
"""
🧪 TEST WHATSAPP + OPENROUTER
Script de test pour vérifier l'intégration OpenRouter avec WhatsApp
"""

import asyncio
import json
import logging
from datetime import datetime
from modules.whatsapp_n8n_service import LumaWhatsAppProcessor, N8NWebhookReceiver
from core.luma_personality import LumaPersonality

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_openrouter_responses():
    """🧠 Test des réponses OpenRouter"""
    print("🧠 TEST OPENROUTER RESPONSES")
    print("=" * 50)
    
    personality = LumaPersonality()
    
    test_messages = [
        "Salut ! Tu as des geekbar ?",
        "C'est ouvert ?",
        "Ça coûte combien ?",
        "Tu as des liquides ?",
        "Bonjour, je cherche des pods"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📱 Test {i}: '{message}'")
        
        context = {
            'client_name': 'Test Client',
            'from': f'test{i}',
            'conversation_history': []
        }
        
        try:
            response = await personality.generate_whatsapp_response_with_openrouter(message, context)
            print(f"✅ Réponse: {response}")
        except Exception as e:
            print(f"❌ Erreur: {e}")

async def test_whatsapp_processor():
    """📱 Test du processeur WhatsApp complet"""
    print("\n📱 TEST WHATSAPP PROCESSOR")
    print("=" * 50)
    
    config = {
        'n8n_send_webhook': '',
        'openrouter_api_key': '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',
        'openrouter_model': 'openai/gptIb-4-turbo'
    }
    
    processor = LumaWhatsAppProcessor(config)
    
    test_message = {
        'phone': '+33123456789',
        'message': 'Salut ! Tu as des geekbar ?',
        'contact_name': 'Thomas',
        'timestamp': datetime.now().isoformat(),
        'id': 'test123'
    }
    
    try:
        response = await processor.process_whatsapp_message(test_message)
        print(f"✅ Réponse WhatsApp: {response}")
    except Exception as e:
        print(f"❌ Erreur processeur: {e}")

def start_webhook_server():
    """🔗 Démarrage serveur webhook pour tests"""
    print("\n🔗 DÉMARRAGE SERVEUR WEBHOOK")
    print("=" * 50)
    
    config = {
        'n8n_send_webhook': '',
        'openrouter_api_key': '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',
        'openrouter_model': 'openai/gpt-4-turbo'
    }
    
    processor = LumaWhatsAppProcessor(config)
    receiver = N8NWebhookReceiver(processor)
    
    print("🚀 Serveur webhook démarré sur http://localhost:5000")
    print("📱 Test avec: curl -X POST http://localhost:5000/webhook/whatsapp")
    print("📋 Body: {\"from\": \"+33123456789\", \"message\": \"Salut !\", \"contact_name\": \"Test\"}")
    print("\n⏹️  Ctrl+C pour arrêter")
    
    try:
        receiver.start_server(host='localhost', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Serveur arrêté")

async def main():
    """🧪 Tests principaux"""
    print("🔥 TEST INTÉGRATION OPENROUTER + WHATSAPP")
    print("=" * 60)
    
    # Test 1: Réponses OpenRouter directes
    await test_openrouter_responses()
    
    # Test 2: Processeur WhatsApp complet
    await test_whatsapp_processor()
    
    # Test 3: Serveur webhook (optionnel)
    print("\n🔗 Voulez-vous démarrer le serveur webhook ? (y/n)")
    # start_webhook_server()

if __name__ == "__main__":
    asyncio.run(main()) 