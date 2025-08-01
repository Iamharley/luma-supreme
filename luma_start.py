#!/usr/bin/env python3
"""
🔥 LUMA BUSINESS PRO - SCRIPT DE LANCEMENT
Démarre l'employée digitale autonome
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Ajouter le répertoire à Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.main_engine import LumaBusinessEngine


async def main():
    """Point d'entrée principal pour LUMA"""
    # Charger configuration
    load_dotenv('luma_config.env')
    
    config = {
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "claude_key": os.getenv("CLAUDE_API_KEY"),
        "shopify_key": os.getenv("SHOPIFY_ACCESS_TOKEN"),
        "gmail_address": os.getenv("GMAIL_ADDRESS"),
        "notion_token": os.getenv("NOTION_TOKEN")
    }
    
    # Initialiser LUMA
    luma = LumaBusinessEngine(config)
    
    print("🔥 LUMA BUSINESS PRO - DÉMARRAGE")
    print("=" * 50)
    print("💙 Employée digitale d'Anne-Sophie activée")
    print("📧 Surveillance: hello@iamharley.com")
    print("🛒 Business: Harley Vape")
    print("⚡ Mode: Proactif 24/7")
    print("=" * 50)
    
    try:
        # Démarrer opérations autonomes
        await luma.start_autonomous_operations()
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
    except asyncio.CancelledError:
        print("\n⏰ Opérations annulées")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1
    finally:
        # Arrêt propre
        try:
            await luma.stop_autonomous_operations()
            print("✅ LUMA arrêté proprement")
        except Exception as e:
            print(f"⚠️ Erreur lors de l'arrêt: {e}")
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 