#!/bin/bash

# 🚀 LUMA SUPREME - Gestionnaire de services
# Script pour démarrer/arrêter les services LUMA en arrière-plan

LUMA_DIR="/Users/harleyvapestaff/Desktop/LUMA-SUPREME"
cd "$LUMA_DIR"

case "$1" in
    "start")
        echo "🚀 Démarrage LUMA en arrière-plan..."
        
        # Démarrer Baileys WhatsApp
        echo "📱 Démarrage Baileys WhatsApp..."
        nohup node baileys_whatsapp_luma.js > luma_baileys.log 2>&1 &
        echo "✅ Baileys démarré (PID: $!)"
        
        # Démarrer Webhook LUMA
        echo "🧠 Démarrage Webhook LUMA..."
        source venv/bin/activate && nohup python modules/whatsapp_n8n_service.py > luma_webhook.log 2>&1 &
        echo "✅ Webhook LUMA démarré (PID: $!)"
        
        echo "🎉 LUMA est maintenant opérationnel en arrière-plan !"
        echo "📊 Logs: luma_baileys.log et luma_webhook.log"
        echo "🔍 Status: curl http://localhost:5001/health"
        ;;
        
    "stop")
        echo "🛑 Arrêt des services LUMA..."
        
        # Arrêter tous les processus LUMA
        pkill -f "baileys_whatsapp_luma.js"
        pkill -f "modules/whatsapp_n8n_service.py"
        pkill -f "luma_start.py"
        
        echo "✅ Services LUMA arrêtés"
        ;;
        
    "status")
        echo "📊 Status des services LUMA:"
        echo ""
        
        # Vérifier Baileys
        if pgrep -f "baileys_whatsapp_luma.js" > /dev/null; then
            echo "✅ Baileys WhatsApp: ACTIF"
        else
            echo "❌ Baileys WhatsApp: INACTIF"
        fi
        
        # Vérifier Webhook
        if pgrep -f "modules/whatsapp_n8n_service.py" > /dev/null; then
            echo "✅ Webhook LUMA: ACTIF"
        else
            echo "❌ Webhook LUMA: INACTIF"
        fi
        
        # Test de santé
        echo ""
        echo "🏥 Test de santé:"
        curl -s http://localhost:5001/health 2>/dev/null || echo "❌ Webhook non accessible"
        ;;
        
    "logs")
        echo "📋 Logs LUMA:"
        echo ""
        echo "=== BAILEYS LOG ==="
        tail -10 luma_baileys.log 2>/dev/null || echo "Aucun log Baileys"
        echo ""
        echo "=== WEBHOOK LOG ==="
        tail -10 luma_webhook.log 2>/dev/null || echo "Aucun log Webhook"
        ;;
        
    "restart")
        echo "🔄 Redémarrage LUMA..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    *)
        echo "🚀 LUMA SUPREME - Gestionnaire de services"
        echo ""
        echo "Usage: $0 {start|stop|status|logs|restart}"
        echo ""
        echo "  start   - Démarrer LUMA en arrière-plan"
        echo "  stop    - Arrêter tous les services LUMA"
        echo "  status  - Vérifier le statut des services"
        echo "  logs    - Afficher les logs récents"
        echo "  restart - Redémarrer tous les services"
        echo ""
        echo "📱 WhatsApp: +13072251057"
        echo "🌐 Webhook: http://localhost:5001"
        ;;
esac 