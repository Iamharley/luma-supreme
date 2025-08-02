#!/usr/bin/env python3
"""
🚀 SERVEUR WEBHOOK WHATSAPP + OPENROUTER
Démarre le service webhook pour recevoir des messages WhatsApp
"""

import logging
from modules.whatsapp_n8n_service import LumaWhatsAppProcessor, N8NWebhookReceiver

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """🚀 Démarrage serveur webhook WhatsApp"""
    print("🔥 SERVEUR WEBHOOK WHATSAPP + OPENROUTER")
    print("=" * 60)
    
    # Configuration
    config = {
        'n8n_send_webhook': '',  # Optionnel pour tests
        'openrouter_api_key': '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',
        'openrouter_model': 'openai/gpt-4-turbo'
    }
    
    # Initialiser processeur LUMA
    processor = LumaWhatsAppProcessor(config)
    
    # Créer récepteur webhook
    receiver = N8NWebhookReceiver(processor)
    
    print("🚀 Serveur webhook WhatsApp démarré !")
    print("📍 URL: http://localhost:5000")
    print("📱 Endpoint: /webhook/whatsapp")
    print("🏥 Health: /health")
    print("\n📋 Test avec curl:")
    print('curl -X POST http://localhost:5000/webhook/whatsapp \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"from": "+33123456789", "message": "Salut ! Tu as des geekbar ?", "contact_name": "Thomas"}\'')
    print("\n⏹️  Ctrl+C pour arrêter")
    
    try:
        # Démarrer serveur
        receiver.start_server(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Serveur arrêté proprement")
    except Exception as e:
        print(f"❌ Erreur serveur: {e}")

if __name__ == "__main__":
    main() 