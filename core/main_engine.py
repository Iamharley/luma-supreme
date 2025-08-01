"""
🔥 LUMA Business Engine
Moteur principal orchestrateur pour Anne-Sophie
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

from .luma_personality import LumaPersonality
from .business_intelligence import HarleyVapeIntelligence
from .proactive_scheduler import ProactiveScheduler


class LumaBusinessEngine:
    """Moteur principal LUMA Business"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # Initialiser les composants
        self.personality = LumaPersonality()
        self.business_intelligence = HarleyVapeIntelligence()
        self.scheduler = ProactiveScheduler()
        
        # État du système
        self.is_running = False
        self.start_time = None
        
        self.logger.info("🔥 LUMA Business Engine initialisé")
    
    def _setup_logger(self) -> logging.Logger:
        """Configure le logger"""
        logger = logging.getLogger('LumaBusinessEngine')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - LUMA Business - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    async def start_autonomous_operations(self):
        """Démarre les opérations autonomes"""
        self.is_running = True
        self.start_time = datetime.now()
        
        self.logger.info("🚀 Démarrage opérations autonomes LUMA")
        self.logger.info(f"💙 Propriétaire: {self.personality.owner}")
        self.logger.info(f"🏢 Business: {self.personality.business}")
        self.logger.info(f"⚡ Mode: Proactif 24/7")
        
        try:
            # Démarrer le planificateur
            await self.scheduler.start_scheduler()
            
        except KeyboardInterrupt:
            self.logger.info("👋 Arrêt demandé par l'utilisateur")
        except Exception as e:
            self.logger.error(f"❌ Erreur opérations autonomes: {e}")
        finally:
            await self.stop_autonomous_operations()
    
    async def stop_autonomous_operations(self):
        """Arrête les opérations autonomes"""
        self.is_running = False
        
        # Arrêter le planificateur
        await self.scheduler.stop_scheduler()
        
        runtime = datetime.now() - self.start_time if self.start_time else None
        self.logger.info(f"🛑 Opérations autonomes arrêtées (runtime: {runtime})")
    
    async def generate_morning_briefing(self) -> str:
        """Génère le briefing matinal"""
        try:
            # Récupérer les métriques business
            business_summary = self.business_intelligence.get_business_summary()
            health_analysis = await self.business_intelligence.analyze_business_health()
            
            # Préparer le contexte
            context = {
                "emails": str(business_summary["metrics"]["pending_emails"]),
                "orders": str(business_summary["metrics"]["daily_orders"]),
                "whatsapp": "0",  # À connecter avec WhatsApp API
                "insight": self._generate_insight(health_analysis)
            }
            
            # Générer le briefing
            briefing = self.personality.generate_response("morning_briefing", context)
            
            self.logger.info("🌞 Briefing matinal généré")
            return briefing
            
        except Exception as e:
            self.logger.error(f"❌ Erreur génération briefing: {e}")
            return "Erreur génération briefing matinal"
    
    def _generate_insight(self, health_analysis: Dict[str, Any]) -> str:
        """Génère un insight basé sur l'analyse de santé"""
        status = health_analysis.get("status", "unknown")
        
        if status == "excellent":
            return "Journée productive en vue !"
        elif status == "bon":
            return "Tout va bien, on continue !"
        elif status == "attention":
            return "Quelques points à surveiller"
        else:
            return "Action requise sur certains points"
    
    async def process_urgent_alert(self, alert_message: str) -> str:
        """Traite une alerte urgente"""
        try:
            context = {"message": alert_message}
            alert_response = self.personality.generate_response("urgent_alert", context)
            
            # Programmer un suivi
            await self.scheduler.schedule_urgent_task(
                task_name="follow_up_alert",
                delay_minutes=30,
                callback=self._follow_up_alert_callback,
                description=f"Suivi alerte: {alert_message[:50]}..."
            )
            
            self.logger.info(f"🚨 Alerte urgente traitée: {alert_message}")
            return alert_response
            
        except Exception as e:
            self.logger.error(f"❌ Erreur traitement alerte: {e}")
            return "Erreur traitement alerte urgente"
    
    async def _follow_up_alert_callback(self):
        """Callback suivi alerte"""
        self.logger.info("🔍 Suivi alerte urgente")
        return "Suivi alerte effectué"
    
    async def update_business_metrics(self, new_metrics: Dict[str, Any]):
        """Met à jour les métriques business"""
        try:
            await self.business_intelligence.update_metrics(new_metrics)
            self.logger.info("📊 Métriques business mises à jour")
        except Exception as e:
            self.logger.error(f"❌ Erreur mise à jour métriques: {e}")
    
    async def get_business_status(self) -> Dict[str, Any]:
        """Retourne le statut complet du business"""
        try:
            health = await self.business_intelligence.analyze_business_health()
            insights = await self.business_intelligence.generate_business_insights()
            summary = self.business_intelligence.get_business_summary()
            
            return {
                "health": health,
                "insights": insights,
                "summary": summary,
                "personality": self.personality.get_personality_context(),
                "scheduler": self.scheduler.get_scheduled_tasks(),
                "engine_status": {
                    "running": self.is_running,
                    "start_time": self.start_time.isoformat() if self.start_time else None,
                    "runtime": str(datetime.now() - self.start_time) if self.start_time else None
                }
            }
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération statut: {e}")
            return {"error": str(e)}
    
    async def handle_user_request(self, request: str) -> str:
        """Traite une requête utilisateur"""
        try:
            # Analyser le type de requête
            if "briefing" in request.lower() or "matin" in request.lower():
                return await self.generate_morning_briefing()
            elif "statut" in request.lower() or "état" in request.lower():
                status = await self.get_business_status()
                return f"Statut business: {status['health']['status']} (score: {status['health']['health_score']}/100)"
            elif "urgence" in request.lower() or "alerte" in request.lower():
                return await self.process_urgent_alert(request)
            else:
                # Réponse générique
                return self.personality.adapt_tone(f"Je traite ta demande: {request}")
                
        except Exception as e:
            self.logger.error(f"❌ Erreur traitement requête: {e}")
            return "Désolée, j'ai eu un problème avec ta demande"


if __name__ == "__main__":
    # Test du moteur principal
    async def test_main_engine():
        # Charger la configuration
        load_dotenv('config/.env')
        
        config = {
            "openai_key": os.getenv("OPENAI_API_KEY"),
            "claude_key": os.getenv("CLAUDE_API_KEY"),
            "business_name": os.getenv("BUSINESS_NAME", "Harley Vape")
        }
        
        # Créer et tester le moteur
        engine = LumaBusinessEngine(config)
        
        print("🔥 Test LUMA Business Engine")
        print("=" * 40)
        
        # Test briefing matinal
        briefing = await engine.generate_morning_briefing()
        print("🌞 Briefing matinal:")
        print(briefing)
        
        # Test statut business
        status = await engine.get_business_status()
        print(f"\n📊 Statut business: {status['health']['status']}")
        
        # Test requête utilisateur
        response = await engine.handle_user_request("Donne-moi un briefing")
        print(f"\n💬 Réponse: {response}")
    
    asyncio.run(test_main_engine()) 