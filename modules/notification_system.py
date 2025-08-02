"""
🔔 Notification System pour LUMA Business
Notifications macOS pour Anne-Sophie
"""

import subprocess
import platform
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import logging


class NotificationSystem:
    """Système de notifications pour macOS"""
    
    def __init__(self):
        self.system = platform.system()
        self.logger = logging.getLogger('NotificationSystem')
        
        # Vérifier la compatibilité
        if self.system != "Darwin":
            self.logger.warning(f"⚠️ Système non supporté: {self.system}")
    
    async def notify_anne_sophie(self, message: str, priority: str = "normal") -> bool:
        """Envoie une notification à Anne-Sophie"""
        try:
            if self.system == "Darwin":  # macOS
                return await self._send_macos_notification(message, priority)
            else:
                self.logger.warning(f"Notifications non supportées sur {self.system}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erreur notification: {e}")
            return False
    
    async def _send_macos_notification(self, message: str, priority: str = "normal") -> bool:
        """Envoie une notification macOS"""
        try:
            # Préparer la commande osascript
            script = f'''
            display notification "{message}" with title "LUMA Business" subtitle "Anne-Sophie"
            '''
            
            # Exécuter la commande
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.logger.info(f"✅ Notification envoyée: {message[:50]}...")
                return True
            else:
                self.logger.error(f"❌ Erreur notification: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Timeout notification")
            return False
        except Exception as e:
            self.logger.error(f"❌ Erreur notification macOS: {e}")
            return False
    
    async def alert_urgent(self, message: str) -> bool:
        """Notification urgente avec son"""
        try:
            if self.system == "Darwin":
                # Notification avec son
                script = f'''
                display notification "{message}" with title "🚨 LUMA URGENT" subtitle "Action requise" sound name "Glass"
                '''
                
                result = subprocess.run(
                    ["osascript", "-e", script],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    self.logger.info(f"🚨 Alerte urgente envoyée: {message[:50]}...")
                    return True
                else:
                    self.logger.error(f"❌ Erreur alerte urgente: {result.stderr}")
                    return False
            else:
                return await self.notify_anne_sophie(f"🚨 URGENT: {message}", "critical")
                
        except Exception as e:
            self.logger.error(f"❌ Erreur alerte urgente: {e}")
            return False
    
    async def send_business_update(self, update_data: Dict[str, Any]) -> bool:
        """Envoie une mise à jour business"""
        try:
            title = update_data.get("title", "Mise à jour Business")
            message = update_data.get("message", "Nouvelle information")
            priority = update_data.get("priority", "normal")
            
            full_message = f"{title}\n{message}"
            
            return await self.notify_anne_sophie(full_message, priority)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mise à jour business: {e}")
            return False
    
    async def send_email_alert(self, email_data: Dict[str, Any]) -> bool:
        """Alerte pour email urgent"""
        try:
            sender = email_data.get("sender", "Expéditeur inconnu")
            subject = email_data.get("subject", "Sujet inconnu")
            urgency = email_data.get("urgency", "normal")
            
            message = f"📧 Email de {sender}\n📋 {subject}"
            
            if urgency == "critical":
                return await self.alert_urgent(message)
            else:
                return await self.notify_anne_sophie(message, "high")
                
        except Exception as e:
            self.logger.error(f"❌ Erreur alerte email: {e}")
            return False
    
    async def send_daily_briefing(self, briefing_data: Dict[str, Any]) -> bool:
        """Envoie le briefing quotidien"""
        try:
            message = briefing_data.get("message", "Briefing quotidien disponible")
            
            return await self.notify_anne_sophie(
                f"🌞 Briefing Matinal\n{message}",
                "normal"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Erreur briefing quotidien: {e}")
            return False
    
    async def send_reminder(self, reminder_data: Dict[str, Any]) -> bool:
        """Envoie un rappel"""
        try:
            task = reminder_data.get("task", "Tâche")
            time = reminder_data.get("time", "maintenant")
            
            message = f"⏰ Rappel: {task} à {time}"
            
            return await self.notify_anne_sophie(message, "normal")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur rappel: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """Retourne les informations système"""
        return {
            "system": self.system,
            "supported": self.system == "Darwin",
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Test du système de notifications
    async def test_notification_system():
        notifier = NotificationSystem()
        
        print("🔔 Test Notification System")
        print("=" * 30)
        
        # Info système
        system_info = notifier.get_system_info()
        print(f"Système: {system_info['system']}")
        print(f"Supporté: {system_info['supported']}")
        
        # Test notification normale
        print("\n📧 Test notification normale...")
        success = await notifier.notify_anne_sophie(
            "Test notification LUMA Business"
        )
        print(f"Résultat: {'✅' if success else '❌'}")
        
        # Test alerte urgente
        print("\n🚨 Test alerte urgente...")
        success = await notifier.alert_urgent(
            "Test alerte urgente LUMA"
        )
        print(f"Résultat: {'✅' if success else '❌'}")
        
        # Test mise à jour business
        print("\n💼 Test mise à jour business...")
        update_data = {
            "title": "Mise à jour Harley Vape",
            "message": "3 nouvelles commandes reçues",
            "priority": "normal"
        }
        success = await notifier.send_business_update(update_data)
        print(f"Résultat: {'✅' if success else '❌'}")
    
    asyncio.run(test_notification_system()) 