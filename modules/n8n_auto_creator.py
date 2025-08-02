#!/usr/bin/env python3
"""
🤖 N8N WORKFLOW AUTO-CREATOR - LUMA CRÉE TOUT AUTOMATIQUEMENT !
================================================================
Anne-Sophie n'a RIEN à faire manuellement dans N8N !
LUMA crée, configure et active tous les workflows automatiquement !
================================================================
FICHIER POUR CURSOR - modules/n8n_auto_creator.py
"""

import asyncio
import json
import logging
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
import time
import os
from dotenv import load_dotenv

# Charger configuration
load_dotenv('config/.env')

# ==================================================================
# 🔧 N8N API CLIENT - CONTRÔLE TOTAL AUTOMATIQUE
# ==================================================================

class N8NAutomaticManager:
    """
    🚀 Gestionnaire automatique N8N via API
    LUMA crée et gère tous les workflows sans intervention humaine !
    """
    
    def __init__(self, n8n_host: str = None, api_key: str = None):
        self.n8n_host = (n8n_host or os.getenv('N8N_HOST', 'http://localhost:5678')).rstrip('/')
        self.api_key = api_key or os.getenv('N8N_API_KEY')
        self.session = requests.Session()
        
        # Headers pour API N8N
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        
        if self.api_key:
            self.session.headers.update({'X-N8N-API-KEY': self.api_key})
        
        logging.info(f"🔗 N8N Manager connecté à: {self.n8n_host}")
    
    def test_connection(self) -> bool:
        """🧪 Test connexion N8N"""
        try:
            response = self.session.get(f"{self.n8n_host}/api/v1/workflows")
            if response.status_code in [200, 401]:  # 401 = pas d'auth mais N8N répond
                logging.info("✅ Connexion N8N OK")
                return True
            else:
                logging.error(f"❌ N8N non accessible: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"❌ Erreur connexion N8N: {e}")
            return False
    
    async def create_whatsapp_workflow(self, config: Dict) -> Dict:
        """
        🎯 Création automatique workflow WhatsApp complet
        Anne-Sophie n'a RIEN à faire !
        """
        
        if not self.test_connection():
            return {'success': False, 'error': 'N8N non accessible'}
        
        workflow_definition = self._generate_whatsapp_workflow_json(config)
        
        try:
            # 1. Créer le workflow
            response = self.session.post(
                f"{self.n8n_host}/api/v1/workflows",
                json=workflow_definition
            )
            
            if response.status_code == 201:
                workflow_data = response.json()
                workflow_id = workflow_data['id']
                
                logging.info(f"✅ Workflow WhatsApp créé: ID {workflow_id}")
                
                # 2. Activer le workflow automatiquement
                activated = await self._activate_workflow(workflow_id)
                
                # 3. Récupérer URL webhook
                webhook_url = await self._get_webhook_url(workflow_id)
                
                return {
                    'success': True,
                    'workflow_id': workflow_id,
                    'webhook_url': webhook_url,
                    'status': 'active' if activated else 'created',
                    'message': '🎉 Workflow WhatsApp créé automatiquement !'
                }
            else:
                logging.error(f"❌ Erreur création workflow: {response.status_code} - {response.text}")
                return {'success': False, 'error': f"Erreur N8N: {response.status_code}"}
                
        except Exception as e:
            logging.error(f"💥 Erreur N8N: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_whatsapp_workflow_json(self, config: Dict) -> Dict:
        """
        📋 Génération automatique du JSON workflow N8N
        Aucune configuration manuelle requise !
        """
        
        luma_webhook_url = config.get('luma_webhook_url', 'http://localhost:5000/webhook/whatsapp')
        business_name = config.get('business_name', 'Harley Vape')
        
        workflow = {
            "name": f"LUMA {business_name} - WhatsApp Auto-Response",
            "nodes": [
                {
                    "parameters": {
                        "path": "whatsapp-luma-receive",
                        "httpMethod": "POST",
                        "responseMode": "responseNode",
                        "options": {}
                    },
                    "id": "webhook-receive",
                    "name": "WhatsApp Webhook Receive",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [240, 300],
                    "webhookId": "whatsapp-luma-receive"
                },
                {
                    "parameters": {
                        "url": luma_webhook_url,
                        "sendHeaders": True,
                        "headerParameters": {
                            "parameters": [
                                {
                                    "name": "Content-Type",
                                    "value": "application/json"
                                },
                                {
                                    "name": "X-LUMA-Source", 
                                    "value": "N8N-WhatsApp"
                                }
                            ]
                        },
                        "sendBody": True,
                        "contentType": "json",
                        "jsonParameters": True,
                        "bodyParametersJson": "={{ {\n  \"from\": $json.from,\n  \"message\": $json.message || $json.text?.body,\n  \"timestamp\": $json.timestamp || $now,\n  \"id\": $json.id,\n  \"contact_name\": $json.contact?.profile?.name || $json.from,\n  \"media_type\": $json.type || \"text\",\n  \"n8n_source\": true\n} }}",
                        "options": {
                            "timeout": 30000
                        }
                    },
                    "id": "luma-processor",
                    "name": "LUMA AI Processor",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 4,
                    "position": [480, 300]
                },
                {
                    "parameters": {
                        "respondWith": "json",
                        "responseBody": "={{ {\n  \"status\": \"success\",\n  \"message\": \"Message traité par LUMA\",\n  \"luma_response\": $node[\"LUMA AI Processor\"].json.luma_response,\n  \"timestamp\": $now\n} }}"
                    },
                    "id": "webhook-response",
                    "name": "Webhook Response",
                    "type": "n8n-nodes-base.respondToWebhook",
                    "typeVersion": 1,
                    "position": [720, 300]
                }
            ],
            "connections": {
                "WhatsApp Webhook Receive": {
                    "main": [
                        [
                            {
                                "node": "LUMA AI Processor",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                },
                "LUMA AI Processor": {
                    "main": [
                        [
                            {
                                "node": "Webhook Response",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            },
            "active": False,
            "settings": {
                "executionOrder": "v1"
            }
        }
        
        return workflow
    
    async def _activate_workflow(self, workflow_id: str) -> bool:
        """🔛 Activation automatique du workflow"""
        
        try:
            # Note: L'endpoint d'activation peut varier selon version N8N
            response = self.session.patch(
                f"{self.n8n_host}/api/v1/workflows/{workflow_id}",
                json={"active": True}
            )
            
            if response.status_code == 200:
                logging.info(f"✅ Workflow {workflow_id} activé automatiquement")
                return True
            else:
                logging.warning(f"⚠️ Activation workflow: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"💥 Erreur activation: {e}")
            return False
    
    async def _get_webhook_url(self, workflow_id: str) -> str:
        """🔗 Récupération URL webhook automatique"""
        
        try:
            response = self.session.get(
                f"{self.n8n_host}/api/v1/workflows/{workflow_id}"
            )
            
            if response.status_code == 200:
                webhook_url = f"{self.n8n_host}/webhook/whatsapp-luma-receive"
                logging.info(f"🔗 Webhook URL: {webhook_url}")
                return webhook_url
            
            return f"{self.n8n_host}/webhook/whatsapp-luma-receive"
            
        except Exception as e:
            logging.error(f"💥 Erreur récupération webhook: {e}")
            return f"{self.n8n_host}/webhook/whatsapp-luma-receive"
    
    def list_workflows(self) -> List[Dict]:
        """📋 Liste tous les workflows existants"""
        
        try:
            response = self.session.get(f"{self.n8n_host}/api/v1/workflows")
            
            if response.status_code == 200:
                workflows = response.json()
                logging.info(f"📋 {len(workflows)} workflows trouvés")
                return workflows
            else:
                logging.error(f"❌ Erreur liste workflows: {response.status_code}")
                return []
                
        except Exception as e:
            logging.error(f"💥 Erreur liste workflows: {e}")
            return []
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """🗑️ Suppression workflow"""
        
        try:
            response = self.session.delete(f"{self.n8n_host}/api/v1/workflows/{workflow_id}")
            
            if response.status_code == 200:
                logging.info(f"✅ Workflow {workflow_id} supprimé")
                return True
            else:
                logging.error(f"❌ Erreur suppression: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"💥 Erreur suppression: {e}")
            return False

# ==================================================================
# 🤖 LUMA N8N AUTOMATION ORCHESTRATOR
# ==================================================================

class LumaN8NOrchestrator:
    """
    🎯 Orchestrateur automatique complet N8N pour LUMA
    Anne-Sophie n'a QU'À CLIQUER SUR UN BOUTON !
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.n8n_manager = N8NAutomaticManager(
            n8n_host=config.get('n8n_host'),
            api_key=config.get('n8n_api_key')
        )
        
    async def setup_complete_automation(self) -> Dict:
        """
        🚀 SETUP COMPLET AUTOMATIQUE - TOUT EN UN CLIC !
        Anne-Sophie n'a RIEN à faire dans N8N !
        """
        
        results = {
            'whatsapp': None,
            'status': 'starting'
        }
        
        try:
            print("🔥 LUMA - CRÉATION AUTOMATIQUE WORKFLOWS N8N")
            print("=" * 50)
            
            # Test connexion N8N
            if not self.n8n_manager.test_connection():
                results['status'] = 'error'
                results['error'] = 'N8N non accessible - Vérifiez que N8N tourne sur http://localhost:5678'
                return results
            
            # 1. WhatsApp workflow
            print("📱 Création workflow WhatsApp...")
            results['whatsapp'] = await self.n8n_manager.create_whatsapp_workflow(self.config)
            
            if results['whatsapp']['success']:
                print(f"✅ WhatsApp: {results['whatsapp']['message']}")
                print(f"🔗 Webhook: {results['whatsapp']['webhook_url']}")
                results['status'] = 'success'
            else:
                print(f"❌ WhatsApp: {results['whatsapp']['error']}")
                results['status'] = 'error'
            
            return results
            
        except Exception as e:
            logging.error(f"💥 Erreur orchestration: {e}")
            results['status'] = 'error'
            results['error'] = str(e)
            return results
    
    def cleanup_old_workflows(self):
        """🧹 Nettoyage anciens workflows LUMA"""
        
        print("🧹 Nettoyage anciens workflows LUMA...")
        
        workflows = self.n8n_manager.list_workflows()
        luma_workflows = [w for w in workflows if 'LUMA' in w.get('name', '')]
        
        if luma_workflows:
            print(f"📋 {len(luma_workflows)} workflows LUMA trouvés:")
            for workflow in luma_workflows:
                print(f"  - {workflow['name']} (ID: {workflow['id']})")
            
            cleanup_input = input("🗑️ Supprimer les anciens workflows LUMA ? (o/n): ")
            if cleanup_input.lower() == 'o':
                for workflow in luma_workflows:
                    if self.n8n_manager.delete_workflow(workflow['id']):
                        print(f"✅ Supprimé: {workflow['name']}")
                    else:
                        print(f"❌ Erreur suppression: {workflow['name']}")
        else:
            print("✅ Aucun ancien workflow LUMA trouvé")

# ==================================================================
# 🔧 CONFIGURATION & LANCEMENT AUTOMATIQUE
# ==================================================================

def create_automation_config() -> Dict:
    """⚙️ Configuration complète pour automation N8N"""
    
    return {
        # N8N Configuration
        'n8n_host': os.getenv('N8N_HOST', 'http://localhost:5678'),
        'n8n_api_key': os.getenv('N8N_API_KEY'),
        
        # LUMA Service
        'luma_webhook_url': 'http://localhost:5000/webhook/whatsapp',
        'luma_service_host': 'localhost',
        'luma_service_port': 5000,
        
        # WhatsApp Business (à configurer plus tard)
        'whatsapp_access_token': os.getenv('WHATSAPP_ACCESS_TOKEN', ''),
        'whatsapp_phone_number_id': os.getenv('WHATSAPP_PHONE_NUMBER_ID', ''),
        'whatsapp_verify_token': os.getenv('WHATSAPP_VERIFY_TOKEN', 'luma_secure_token'),
        
        # Business
        'business_name': 'Harley Vape',
        'business_phone': '+33123456789',
    }

async def main():
    """🎯 LANCEMENT AUTOMATION COMPLÈTE N8N"""
    
    # Configuration logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    config = create_automation_config()
    
    print("🤖 LUMA N8N AUTOMATION - CRÉATION AUTOMATIQUE WORKFLOWS")
    print("💙 Anne-Sophie n'a RIEN à faire manuellement dans N8N !")
    print("=" * 60)
    
    # Initialisation orchestrateur
    orchestrator = LumaN8NOrchestrator(config)
    
    # Option nettoyage
    cleanup_input = input("🧹 Nettoyer les anciens workflows LUMA ? (o/n): ")
    if cleanup_input.lower() == 'o':
        orchestrator.cleanup_old_workflows()
    
    # Setup complet automatique
    print("\n🚀 Création des nouveaux workflows...")
    results = await orchestrator.setup_complete_automation()
    
    if results['status'] == 'success':
        print("\n🎉 WORKFLOW N8N CRÉÉ AUTOMATIQUEMENT !")
        print("🚀 LUMA peut maintenant recevoir les messages WhatsApp !")
        print(f"🔗 URL Webhook: {results['whatsapp']['webhook_url']}")
        print("\n📱 Pour tester: Configurez WhatsApp Business API avec cette URL webhook")
        
    elif results['status'] == 'error':
        print(f"\n❌ Erreur création: {results.get('error', 'Erreur inconnue')}")
        print("🔧 Vérifications suggérées:")
        print("  - N8N est-il démarré sur http://localhost:5678 ?")
        print("  - Y a-t-il des erreurs dans les logs N8N ?")
        print("  - La configuration .env est-elle correcte ?")
    
    else:
        print(f"\n⚠️ Création partielle: {results}")

def test_n8n_connection():
    """🧪 Test simple connexion N8N"""
    
    config = create_automation_config()
    manager = N8NAutomaticManager(config['n8n_host'], config['n8n_api_key'])
    
    print("🧪 Test connexion N8N...")
    
    if manager.test_connection():
        workflows = manager.list_workflows()
        print(f"✅ N8N accessible - {len(workflows)} workflows trouvés")
        
        for workflow in workflows[:5]:  # Afficher 5 premiers
            print(f"  - {workflow.get('name', 'Sans nom')} ({'Actif' if workflow.get('active') else 'Inactif'})")
            
        if len(workflows) > 5:
            print(f"  ... et {len(workflows) - 5} autres")
            
    else:
        print("❌ N8N non accessible")
        print("🔧 Vérifiez que N8N est démarré sur http://localhost:5678")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_n8n_connection()
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n👋 Automation arrêtée")
        except Exception as e:
            print(f"💥 Erreur: {e}")
            logging.error(f"Erreur automation: {e}") 