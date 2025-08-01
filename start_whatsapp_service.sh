#!/bin/bash
cd ~/Desktop/LUMA-SUPREME
source venv/bin/activate

echo "🚀 Démarrage LUMA WhatsApp Service..."
python modules/whatsapp_n8n_service.py &

echo $! > luma_whatsapp.pid
echo "✅ Service LUMA WhatsApp démarré (PID: $(cat luma_whatsapp.pid))"
echo "🔗 Webhook disponible sur: http://localhost:5000/webhook/whatsapp"
echo "📱 Pour arrêter: kill $(cat luma_whatsapp.pid)" 