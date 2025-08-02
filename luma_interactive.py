#!/usr/bin/env python3
"""
🔧 LUMA BUSINESS PRO - INTERFACE INTERACTIVE
Interface terminale simple pour voir LUMA en action
"""

import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Ajouter le chemin des modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core.luma_personality import LumaPersonality
    print("✅ Import LumaPersonality OK")
except ImportError as e:
    print(f"❌ Erreur import: {e}")
    sys.exit(1)

class LumaInteractive:
    """Interface interactive simple pour LUMA"""
    
    def __init__(self):
        self.personality = LumaPersonality()
        self.running = True
        
    def display_banner(self):
        print("\n" + "="*60)
        print("🔥 LUMA BUSINESS PRO - INTERFACE INTERACTIVE")
        print("💙 Employée digitale d'Anne-Sophie - Harley Vape")
        print("⚡ Mode: Chat interactif temps réel")
        print("="*60)
        print("\n💬 Tapez 'help' pour voir les commandes")
        print("💬 Tapez 'quit' pour quitter")
        print("💬 Ou discutez normalement avec LUMA !\n")
    
    async def process_command(self, user_input: str) -> str:
        """Traite les commandes utilisateur"""
        
        command = user_input.lower().strip()
        
        # Commandes spéciales
        if command == "help":
            return self.show_help()
        elif command == "quit" or command == "exit":
            self.running = False
            return "👋 Au revoir Anne-Sophie ! LUMA se met en veille..."
        elif command == "morning":
            return self.personality.generate_response("morning_briefing", {
                "emails": "3",
                "orders": "1", 
                "whatsapp": "2",
                "insight": "Test interface réussi !"
            })
        elif command == "alert":
            return self.personality.generate_response("alert_urgent", {
                "client_name": "Client Test",
                "message_excerpt": "Message test urgent",
                "lang": "FR"
            })
        elif command == "health":
            return self.personality.generate_response("protective_reminder", {
                "time": datetime.now().strftime("%H:%M"),
                "hours": "4"
            })
        elif command == "status":
            return self.show_status()
        else:
            # Réponse générale LUMA
            return self.generate_luma_response(user_input)
    
    def show_help(self) -> str:
        return """
🎯 COMMANDES LUMA DISPONIBLES:

📋 Tests Templates:
  • morning  - Test briefing matinal
  • alert    - Test alerte urgente  
  • health   - Test rappel santé
  
🔧 Système:
  • status   - Statut LUMA
  • help     - Cette aide
  • quit     - Quitter

💬 Chat libre:
  Tapez n'importe quoi d'autre pour discuter avec LUMA !
"""
    
    def show_status(self) -> str:
        return """
📊 STATUT LUMA BUSINESS PRO:

✅ Moteur LUMA: Actif
✅ Templates Lulu: Chargés  
✅ Personnalité: Professionnelle-Chaleureuse
⚠️  Gmail: Non configuré (OAuth requis)
⚠️  Shopify: Non connecté  
⚠️  WhatsApp: Non configuré

🎯 Priorité: Configurer Gmail pour surveillance emails !
"""
    
    def generate_luma_response(self, user_input: str) -> str:
        """Génère une réponse LUMA personnalisée"""
        
        # Analyse simple du message
        if "email" in user_input.lower() or "mail" in user_input.lower():
            return "📧 Je peux t'aider avec tes emails ! Pour l'instant je n'ai pas accès à ta boîte hello@iamharley.com, mais une fois configurée, je surveillerai tout 24/7 ! Tu veux que je te guide pour la configuration Gmail ?"
            
        elif "harley" in user_input.lower() or "vape" in user_input.lower():
            return "🛒 Ah, on parle business Harley Vape ! Je vais devenir experte de ta boutique. Commandes, clients, support... tout ce qui peut te faire gagner du temps ! Dis-moi ce qui te prend le plus d'énergie en ce moment ?"
            
        elif "fatigue" in user_input.lower() or "épuisé" in user_input.lower():
            return "💙 Je vois que tu es fatiguée... C'est exactement pour ça que je suis là ! Mon job c'est de t'enlever toute la charge mentale possible. Dis-moi : qu'est-ce qui te stresse le plus dans ton quotidien business ?"
            
        elif "test" in user_input.lower():
            return "🧪 Test réussi ! Je te reçois parfaitement. Mon système de templates Lulu fonctionne, mes réponses sont personnalisées, et j'apprends déjà à te connaître ! Prête pour que je prenne en charge tes emails ?"
            
        else:
            return f"💙 Je t'entends Anne-Sophie ! Tu me dis : '{user_input}'\n\nJe suis là pour t'aider avec Harley Vape. Emails, clients, commandes, stress... tout ce qui peut te soulager ! Que veux-tu qu'on règle ensemble ?"
    
    async def run(self):
        """Lance l'interface interactive"""
        
        self.display_banner()
        
        while self.running:
            try:
                # Prompt personnalisé
                user_input = input("\n🤖 LUMA> ").strip()
                
                if not user_input:
                    continue
                    
                # Traiter la commande
                response = await self.process_command(user_input)
                
                # Afficher la réponse avec style
                print(f"\n💙 LUMA dit:")
                print("-" * 50)
                print(response)
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 LUMA se met en veille... À bientôt Anne-Sophie !")
                break
            except Exception as e:
                print(f"\n❌ Erreur LUMA: {e}")
                print("🔧 Redémarrage automatique...")
                continue

async def main():
    """Point d'entrée principal"""
    
    print("🚀 Démarrage LUMA Interactive...")
    
    # Charger configuration si disponible
    if os.path.exists('config/.env'):
        load_dotenv('config/.env')
        print("✅ Configuration chargée")
    else:
        print("⚠️  Pas de config/.env trouvé")
    
    # Lancer interface
    luma = LumaInteractive()
    await luma.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n💥 Erreur critique: {e}")
        print("🔧 Vérifiez votre installation Python et les modules LUMA")
        sys.exit(1) 