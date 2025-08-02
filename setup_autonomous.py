#!/usr/bin/env python3
"""
🚀 LUMA BUSINESS PRO - CONFIGURATION AUTONOME
Configure LUMA pour fonctionner 24/7
"""

import os
import sys
from pathlib import Path

def setup_autonomous():
    """Configure LUMA pour le mode autonome"""
    
    print("🚀 CONFIGURATION LUMA AUTONOME")
    print("=" * 50)
    
    # 1. Créer le dossier config s'il n'existe pas
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # 2. Créer le fichier .env
    env_file = config_dir / ".env"
    
    if not env_file.exists():
        print("📝 Création du fichier de configuration...")
        
        env_content = """# 🔥 LUMA BUSINESS PRO - CONFIGURATION
# Remplissez ces valeurs avec vos vraies clés API

# OpenAI (pour l'IA)
OPENAI_API_KEY=your_openai_key_here

# Claude (pour l'IA avancée)
CLAUDE_API_KEY=your_claude_key_here

# Gmail (pour les emails)
GMAIL_ADDRESS=hello@iamharley.com
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret

# Shopify (pour les commandes)
SHOPIFY_ACCESS_TOKEN=your_shopify_token
SHOPIFY_STORE_URL=your_store.myshopify.com

# WhatsApp Business (pour les clients)
WHATSAPP_ACCESS_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id

# Notion (pour la gestion)
NOTION_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_database_id

# Configuration LUMA
LUMA_OWNER=Anne-Sophie
LUMA_BUSINESS=Harley Vape
LUMA_MODE=autonomous
"""
        
        with open(env_file, "w") as f:
            f.write(env_content)
        
        print("✅ Fichier .env créé dans config/.env")
    else:
        print("✅ Fichier .env existe déjà")
    
    # 3. Créer le script de lancement automatique
    startup_script = """#!/bin/bash
# 🔥 LUMA BUSINESS PRO - SCRIPT DE DÉMARRAGE AUTOMATIQUE

cd "$(dirname "$0")"
source venv/bin/activate

echo "🚀 Démarrage LUMA Business Pro en mode autonome..."
python luma_start.py
"""
    
    with open("start_luma.sh", "w") as f:
        f.write(startup_script)
    
    # Rendre le script exécutable
    os.chmod("start_luma.sh", 0o755)
    
    print("✅ Script de démarrage créé: start_luma.sh")
    
    # 4. Créer le script de service (pour macOS)
    service_script = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.luma.businesspro</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/harleyvapestaff/Desktop/LUMA-SUPREME/start_luma.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/harleyvapestaff/Desktop/LUMA-SUPREME/luma.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/harleyvapestaff/Desktop/LUMA-SUPREME/luma_error.log</string>
</dict>
</plist>
"""
    
    with open("com.luma.businesspro.plist", "w") as f:
        f.write(service_script)
    
    print("✅ Fichier de service créé: com.luma.businesspro.plist")
    
    # 5. Instructions
    print("\n" + "=" * 50)
    print("🎯 INSTRUCTIONS POUR L'AUTONOMIE :")
    print("=" * 50)
    
    print("\n1️⃣ CONFIGURATION DES APIs :")
    print("   - Ouvrez config/.env")
    print("   - Remplacez 'your_xxx_key' par vos vraies clés API")
    print("   - Sauvegardez le fichier")
    
    print("\n2️⃣ MODE AUTONOME SIMPLE :")
    print("   ./start_luma.sh")
    print("   (Arrêt avec Ctrl+C)")
    
    print("\n3️⃣ MODE AUTONOME 24/7 :")
    print("   nohup ./start_luma.sh > luma.log 2>&1 &")
    print("   (Tourne en arrière-plan)")
    
    print("\n4️⃣ MODE SERVICE SYSTÈME :")
    print("   sudo cp com.luma.businesspro.plist ~/Library/LaunchAgents/")
    print("   launchctl load ~/Library/LaunchAgents/com.luma.businesspro.plist")
    print("   (Démarre automatiquement au boot)")
    
    print("\n5️⃣ MONITORING :")
    print("   tail -f luma.log")
    print("   (Voir les logs en temps réel)")
    
    print("\n" + "=" * 50)
    print("💙 LUMA sera autonome une fois configurée !")
    print("=" * 50)

if __name__ == "__main__":
    setup_autonomous() 