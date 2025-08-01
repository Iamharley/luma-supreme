"""
💼 Harley Vape Business Intelligence
Logique business spécifique pour Anne-Sophie
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json


class HarleyVapeIntelligence:
    """Intelligence business spécifique à Harley Vape"""
    
    def __init__(self):
        self.business_name = "Harley Vape"
        self.owner = "Anne-Sophie"
        self.business_metrics = {
            "daily_orders": 0,
            "pending_emails": 0,
            "urgent_alerts": [],
            "customer_satisfaction": 0.0,
            "revenue_today": 0.0
        }
        self.business_rules = {
            "urgent_response_time": 30,  # minutes
            "normal_response_time": 120,  # minutes
            "customer_priority": ["vip", "regular", "new"],
            "order_thresholds": {
                "low": 5,
                "medium": 15,
                "high": 30
            }
        }
    
    async def analyze_business_health(self) -> Dict[str, Any]:
        """Analyse la santé du business"""
        health_score = 0
        issues = []
        recommendations = []
        
        # Analyser les métriques
        if self.business_metrics["daily_orders"] < self.business_rules["order_thresholds"]["low"]:
            issues.append("Commandes en baisse")
            health_score -= 20
        elif self.business_metrics["daily_orders"] > self.business_rules["order_thresholds"]["high"]:
            recommendations.append("Excellent volume de commandes !")
            health_score += 20
        
        if self.business_metrics["pending_emails"] > 10:
            issues.append("Beaucoup d'emails en attente")
            health_score -= 15
            recommendations.append("Prioriser les emails urgents")
        
        if self.business_metrics["customer_satisfaction"] < 0.7:
            issues.append("Satisfaction client en baisse")
            health_score -= 25
            recommendations.append("Vérifier les retours clients")
        
        if len(self.business_metrics["urgent_alerts"]) > 0:
            issues.append(f"{len(self.business_metrics['urgent_alerts'])} alertes urgentes")
            health_score -= 30
        
        # Normaliser le score
        health_score = max(0, min(100, health_score + 50))
        
        return {
            "health_score": health_score,
            "status": self._get_health_status(health_score),
            "issues": issues,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_health_status(self, score: float) -> str:
        """Détermine le statut de santé"""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "bon"
        elif score >= 40:
            return "attention"
        else:
            return "critique"
    
    async def prioritize_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Priorise les tâches selon l'urgence business"""
        for task in tasks:
            priority_score = 0
            
            # Facteurs de priorité
            if task.get("customer_type") == "vip":
                priority_score += 30
            
            if task.get("urgency") == "urgent":
                priority_score += 25
            
            if task.get("revenue_impact", 0) > 100:
                priority_score += 20
            
            if task.get("time_sensitive"):
                priority_score += 15
            
            task["priority_score"] = priority_score
        
        # Trier par score de priorité décroissant
        return sorted(tasks, key=lambda x: x.get("priority_score", 0), reverse=True)
    
    async def generate_business_insights(self) -> Dict[str, Any]:
        """Génère des insights business"""
        insights = {
            "revenue_trend": self._analyze_revenue_trend(),
            "customer_behavior": self._analyze_customer_behavior(),
            "operational_efficiency": self._analyze_operational_efficiency(),
            "market_opportunities": self._identify_market_opportunities()
        }
        
        return insights
    
    def _analyze_revenue_trend(self) -> Dict[str, Any]:
        """Analyse la tendance des revenus"""
        current_revenue = self.business_metrics["revenue_today"]
        
        # Simulation d'analyse (dans un vrai système, on aurait des données historiques)
        if current_revenue > 500:
            trend = "positive"
            message = "Revenus excellents aujourd'hui !"
        elif current_revenue > 200:
            trend = "stable"
            message = "Revenus dans la moyenne"
        else:
            trend = "attention"
            message = "Revenus en baisse, action requise"
        
        return {
            "trend": trend,
            "message": message,
            "current": current_revenue
        }
    
    def _analyze_customer_behavior(self) -> Dict[str, Any]:
        """Analyse le comportement client"""
        return {
            "satisfaction": self.business_metrics["customer_satisfaction"],
            "recommendation": "Maintenir la qualité de service",
            "alert": "Surveiller les retours négatifs" if self.business_metrics["customer_satisfaction"] < 0.8 else None
        }
    
    def _analyze_operational_efficiency(self) -> Dict[str, Any]:
        """Analyse l'efficacité opérationnelle"""
        pending_emails = self.business_metrics["pending_emails"]
        
        if pending_emails > 20:
            efficiency = "low"
            message = "Beaucoup d'emails en attente, prioriser"
        elif pending_emails > 10:
            efficiency = "medium"
            message = "Emails en attente modérée"
        else:
            efficiency = "high"
            message = "Efficacité opérationnelle excellente"
        
        return {
            "efficiency": efficiency,
            "message": message,
            "pending_emails": pending_emails
        }
    
    def _identify_market_opportunities(self) -> List[str]:
        """Identifie les opportunités de marché"""
        opportunities = []
        
        if self.business_metrics["daily_orders"] < 10:
            opportunities.append("Promouvoir les produits vedettes")
        
        if self.business_metrics["customer_satisfaction"] > 0.9:
            opportunities.append("Demander des avis clients")
        
        if self.business_metrics["revenue_today"] > 1000:
            opportunities.append("Étendre la gamme de produits")
        
        return opportunities
    
    async def update_metrics(self, new_metrics: Dict[str, Any]):
        """Met à jour les métriques business"""
        self.business_metrics.update(new_metrics)
    
    def get_business_summary(self) -> Dict[str, Any]:
        """Retourne un résumé business"""
        return {
            "business_name": self.business_name,
            "owner": self.owner,
            "metrics": self.business_metrics,
            "last_updated": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Test de l'intelligence business
    async def test_business_intelligence():
        bi = HarleyVapeIntelligence()
        
        # Mettre à jour les métriques
        await bi.update_metrics({
            "daily_orders": 8,
            "pending_emails": 15,
            "customer_satisfaction": 0.85,
            "revenue_today": 450.0
        })
        
        # Analyser la santé
        health = await bi.analyze_business_health()
        print("🏥 Santé Business:")
        print(f"Score: {health['health_score']}/100")
        print(f"Statut: {health['status']}")
        print(f"Problèmes: {health['issues']}")
        print(f"Recommandations: {health['recommendations']}")
        
        # Générer insights
        insights = await bi.generate_business_insights()
        print("\n💡 Insights Business:")
        print(f"Revenus: {insights['revenue_trend']['message']}")
        print(f"Efficacité: {insights['operational_efficiency']['message']}")
        print(f"Opportunités: {insights['market_opportunities']}")
    
    asyncio.run(test_business_intelligence()) 