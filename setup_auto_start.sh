#!/bin/bash

# 🚀 LUMA SUPREME - Configuration démarrage automatique
# Configure LUMA pour démarrer automatiquement au démarrage du Mac

LUMA_DIR="/Users/harleyvapestaff/Desktop/LUMA-SUPREME"

echo "🚀 Configuration démarrage automatique LUMA..."
echo ""

# Créer le fichier de lancement
cat > ~/Library/LaunchAgents/com.luma.supreme.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.luma.supreme</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$LUMA_DIR/manage_luma.sh</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LUMA_DIR/luma_autostart.log</string>
    <key>StandardErrorPath</key>
    <string>$LUMA_DIR/luma_autostart_error.log</string>
    <key>WorkingDirectory</key>
    <string>$LUMA_DIR</string>
</dict>
</plist>
EOF

# Charger le service
launchctl load ~/Library/LaunchAgents/com.luma.supreme.plist

echo "✅ LUMA configuré pour démarrer automatiquement !"
echo ""
echo "📋 Commandes utiles :"
echo "  Désactiver auto-démarrage : launchctl unload ~/Library/LaunchAgents/com.luma.supreme.plist"
echo "  Réactiver auto-démarrage : launchctl load ~/Library/LaunchAgents/com.luma.supreme.plist"
echo "  Vérifier le statut : launchctl list | grep luma"
echo ""
echo "🔄 Redémarrez votre Mac pour tester l'auto-démarrage !" 