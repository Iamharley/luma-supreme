#!/bin/bash
cd ~/Desktop/LUMA-SUPREME

echo "🚀 Démarrage LUMA Baileys WhatsApp..."
echo "📱 QR Code va s'afficher dans le terminal"
echo "👆 Scannez avec WhatsApp Business Harley Vape"
echo ""

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé"
    echo "🔧 Installez Node.js depuis https://nodejs.org/"
    exit 1
fi

# Vérifier si les dépendances sont installées
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances Node.js..."
    npm install
fi

# Démarrer Baileys
echo "🎉 Démarrage LUMA Baileys..."
node baileys_whatsapp_luma.js 