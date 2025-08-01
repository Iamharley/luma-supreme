#!/bin/bash
# 🔥 LUMA BUSINESS PRO - SCRIPT DE DÉMARRAGE AUTOMATIQUE

cd "$(dirname "$0")"
source venv/bin/activate

echo "🚀 Démarrage LUMA Business Pro en mode autonome..."
python luma_start.py
