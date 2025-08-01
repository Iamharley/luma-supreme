"""
⏰ Proactive Scheduler
Planification proactive 24/7 pour LUMA
"""

import asyncio
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Callable
import logging


class ProactiveScheduler:
    """Planificateur proactive pour LUMA Business"""
    
    def __init__(self):
        self.scheduled_tasks = {}
        self.running = False
        self.logger = logging.getLogger('ProactiveScheduler')
        
        # Tâches programmées par défaut
        self.default_schedule = {
            "morning_briefing": {
                "time": "08:00",
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                "description": "Briefing matinal pour Anne-Sophie"
            },
            "business_health_check": {
                "time": "10:00",
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                "description": "Vérification santé business"
            },
            "lunch_reminder": {
                "time": "12:30",
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                "description": "Rappel pause déjeuner"
            },
            "afternoon_check": {
                "time": "15:00",
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                "description": "Point de l'après-midi"
            },
            "end_of_day": {
                "time": "18:00",
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                "description": "Résumé de fin de journée"
            },
            "weekend_prep": {
                "time": "16:00",
                "days": ["friday"],
                "description": "Préparation weekend"
            }
        }
    
    async def start_scheduler(self):
        """Démarre le planificateur"""
        self.running = True
        self.logger.info("⏰ Planificateur proactive démarré")
        
        # Programmer les tâches par défaut
        await self._schedule_default_tasks()
        
        # Boucle principale
        while self.running:
            schedule.run_pending()
            try:
                await asyncio.sleep(60)  # Vérifier toutes les minutes
            except asyncio.CancelledError:
                self.logger.info("⏰ Planificateur interrompu")
                break
    
    async def stop_scheduler(self):
        """Arrête le planificateur"""
        self.running = False
        self.logger.info("⏰ Planificateur proactive arrêté")
    
    async def _schedule_default_tasks(self):
        """Programme les tâches par défaut"""
        for task_name, task_config in self.default_schedule.items():
            await self.schedule_task(
                task_name=task_name,
                time=task_config["time"],
                days=task_config["days"],
                callback=self._get_default_callback(task_name),
                description=task_config["description"]
            )
    
    def _get_default_callback(self, task_name: str) -> Callable:
        """Retourne le callback par défaut pour une tâche"""
        callbacks = {
            "morning_briefing": self._morning_briefing_callback,
            "business_health_check": self._business_health_callback,
            "lunch_reminder": self._lunch_reminder_callback,
            "afternoon_check": self._afternoon_check_callback,
            "end_of_day": self._end_of_day_callback,
            "weekend_prep": self._weekend_prep_callback
        }
        return callbacks.get(task_name, self._default_callback)
    
    async def schedule_task(self, task_name: str, time: str, days: List[str], 
                          callback: Callable, description: str = ""):
        """Programme une nouvelle tâche"""
        try:
            # Programmer pour chaque jour spécifié
            for day in days:
                if day == "monday":
                    schedule.every().monday.at(time).do(callback)
                elif day == "tuesday":
                    schedule.every().tuesday.at(time).do(callback)
                elif day == "wednesday":
                    schedule.every().wednesday.at(time).do(callback)
                elif day == "thursday":
                    schedule.every().thursday.at(time).do(callback)
                elif day == "friday":
                    schedule.every().friday.at(time).do(callback)
                elif day == "saturday":
                    schedule.every().saturday.at(time).do(callback)
                elif day == "sunday":
                    schedule.every().sunday.at(time).do(callback)
            
            self.scheduled_tasks[task_name] = {
                "time": time,
                "days": days,
                "description": description,
                "callback": callback.__name__
            }
            
            self.logger.info(f"✅ Tâche programmée: {task_name} à {time}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur programmation tâche {task_name}: {e}")
    
    async def schedule_urgent_task(self, task_name: str, delay_minutes: int, 
                                 callback: Callable, description: str = ""):
        """Programme une tâche urgente avec délai"""
        try:
            schedule.every(delay_minutes).minutes.do(callback)
            
            self.scheduled_tasks[f"urgent_{task_name}"] = {
                "time": f"+{delay_minutes}min",
                "days": ["urgent"],
                "description": description,
                "callback": callback.__name__
            }
            
            self.logger.info(f"🚨 Tâche urgente programmée: {task_name} dans {delay_minutes}min")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur programmation tâche urgente {task_name}: {e}")
    
    # Callbacks par défaut
    async def _morning_briefing_callback(self):
        """Callback briefing matinal"""
        self.logger.info("🌞 Exécution briefing matinal")
        # Ici on appellerait le système de personnalité LUMA
        return "Briefing matinal généré"
    
    async def _business_health_callback(self):
        """Callback vérification santé business"""
        self.logger.info("🏥 Vérification santé business")
        return "Santé business vérifiée"
    
    async def _lunch_reminder_callback(self):
        """Callback rappel déjeuner"""
        self.logger.info("🍽️ Rappel pause déjeuner")
        return "Rappel déjeuner envoyé"
    
    async def _afternoon_check_callback(self):
        """Callback point après-midi"""
        self.logger.info("☕ Point de l'après-midi")
        return "Point après-midi généré"
    
    async def _end_of_day_callback(self):
        """Callback fin de journée"""
        self.logger.info("🌙 Résumé fin de journée")
        return "Résumé fin de journée généré"
    
    async def _weekend_prep_callback(self):
        """Callback préparation weekend"""
        self.logger.info("🎉 Préparation weekend")
        return "Préparation weekend générée"
    
    async def _default_callback(self):
        """Callback par défaut"""
        self.logger.info("⚡ Tâche par défaut exécutée")
        return "Tâche exécutée"
    
    def get_scheduled_tasks(self) -> Dict[str, Any]:
        """Retourne la liste des tâches programmées"""
        return {
            "tasks": self.scheduled_tasks,
            "running": self.running,
            "next_run": schedule.next_run(),
            "timestamp": datetime.now().isoformat()
        }
    
    async def clear_all_tasks(self):
        """Efface toutes les tâches programmées"""
        schedule.clear()
        self.scheduled_tasks = {}
        self.logger.info("🗑️ Toutes les tâches effacées")
    
    async def remove_task(self, task_name: str):
        """Supprime une tâche spécifique"""
        if task_name in self.scheduled_tasks:
            # Note: schedule ne permet pas de supprimer une tâche spécifique facilement
            # On recrée le planificateur sans cette tâche
            await self.clear_all_tasks()
            await self._schedule_default_tasks()
            self.logger.info(f"🗑️ Tâche supprimée: {task_name}")


if __name__ == "__main__":
    # Test du planificateur
    async def test_scheduler():
        scheduler = ProactiveScheduler()
        
        print("⏰ Test Planificateur Proactive")
        print("=" * 40)
        
        # Afficher les tâches programmées
        tasks = scheduler.get_scheduled_tasks()
        print(f"Tâches programmées: {len(tasks['tasks'])}")
        
        for task_name, task_info in tasks['tasks'].items():
            print(f"  - {task_name}: {task_info['time']} ({', '.join(task_info['days'])})")
        
        # Démarrer le planificateur (test court)
        print("\n🚀 Démarrage planificateur (test 10 secondes)...")
        try:
            await asyncio.wait_for(scheduler.start_scheduler(), timeout=10)
        except asyncio.TimeoutError:
            await scheduler.stop_scheduler()
            print("✅ Test terminé")
    
    asyncio.run(test_scheduler()) 