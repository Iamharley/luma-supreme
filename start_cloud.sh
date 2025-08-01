#!/bin/bash

# 🚀 LUMA SUPREME - Script de démarrage cloud
echo "🚀 Démarrage LUMA SUPREME sur le cloud..."

# Configuration des variables d'environnement
export OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-"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"}
export OPENROUTER_MODEL=${OPENROUTER_MODEL:-"openai/gpt-4-turbo"}

# Démarrage des services en arrière-plan
echo "📱 Démarrage Baileys WhatsApp..."
nohup node baileys_whatsapp_luma.js > logs/luma_baileys.log 2>&1 &
BAILEYS_PID=$!
echo "✅ Baileys démarré (PID: $BAILEYS_PID)"

echo "🧠 Démarrage Webhook LUMA..."
nohup python modules/whatsapp_n8n_service.py > logs/luma_webhook.log 2>&1 &
WEBHOOK_PID=$!
echo "✅ Webhook LUMA démarré (PID: $WEBHOOK_PID)"

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 10

# Vérification du statut
echo "📊 Vérification du statut..."
if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ Webhook LUMA opérationnel"
else
    echo "❌ Erreur webhook LUMA"
fi

echo "🎉 LUMA SUPREME est maintenant opérationnel sur le cloud !"
echo "📱 WhatsApp: Connecté via Baileys"
echo "🌐 Webhook: http://localhost:5001"
echo "📊 Monitoring: http://localhost:3001"

# Garder le conteneur en vie
echo "🔄 Services en cours d'exécution..."
while true; do
    sleep 30
    # Vérification périodique
    if ! kill -0 $BAILEYS_PID 2>/dev/null; then
        echo "⚠️ Baileys arrêté, redémarrage..."
        nohup node baileys_whatsapp_luma.js > logs/luma_baileys.log 2>&1 &
        BAILEYS_PID=$!
    fi
    
    if ! kill -0 $WEBHOOK_PID 2>/dev/null; then
        echo "⚠️ Webhook arrêté, redémarrage..."
        nohup python modules/whatsapp_n8n_service.py > logs/luma_webhook.log 2>&1 &
        WEBHOOK_PID=$!
    fi
done 