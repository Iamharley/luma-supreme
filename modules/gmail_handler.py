"""
📧 Gmail Handler pour LUMA Business
Gestion des emails hello@iamharley.com
"""

import os
import pickle
import base64
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailHandler:
    """Gestionnaire Gmail pour Anne-Sophie"""
    
    def __init__(self, gmail_address: str = "hello@iamharley.com"):
        self.gmail_address = gmail_address
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.service = None
        self.logger = logging.getLogger('GmailHandler')
        
        # Authentification
        self._authenticate()
    
    def _authenticate(self):
        """Authentification OAuth2 pour Gmail"""
        try:
            creds = None
            token_path = 'config/token.pickle'
            
            # Charger les credentials existants
            if os.path.exists(token_path):
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
            
            # Si pas de credentials valides, faire le flow OAuth
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Note: Dans un vrai système, on aurait les credentials OAuth
                    # Pour l'instant, on simule
                    self.logger.warning("⚠️ Credentials OAuth non configurés")
                    return
                
                # Sauvegarder les credentials
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info(f"✅ Gmail authentifié pour {self.gmail_address}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur authentification Gmail: {e}")
    
    async def check_urgent_emails(self) -> List[Dict[str, Any]]:
        """Vérifie les emails urgents"""
        try:
            if not self.service:
                self.logger.warning("⚠️ Service Gmail non disponible")
                return []
            
            # Rechercher emails non lus
            query = "is:unread"
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=10
            ).execute()
            
            urgent_emails = []
            
            for message in results.get('messages', []):
                msg = self.service.users().messages().get(
                    userId='me', id=message['id']
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                
                # Classifier l'urgence
                urgency = self._classify_urgency(subject, sender)
                
                if urgency in ['high', 'critical']:
                    urgent_emails.append({
                        'id': message['id'],
                        'subject': subject,
                        'sender': sender,
                        'date': date,
                        'urgency': urgency,
                        'snippet': msg.get('snippet', '')
                    })
            
            self.logger.info(f"📧 {len(urgent_emails)} emails urgents trouvés")
            return urgent_emails
            
        except HttpError as error:
            self.logger.error(f"❌ Erreur API Gmail: {error}")
            return []
        except Exception as e:
            self.logger.error(f"❌ Erreur vérification emails: {e}")
            return []
    
    def _classify_urgency(self, subject: str, sender: str) -> str:
        """Classifie l'urgence d'un email"""
        subject_lower = subject.lower()
        sender_lower = sender.lower()
        
        # Mots-clés critiques
        critical_keywords = ['urgent', 'urgente', 'critique', 'problème', 'erreur', 'bug']
        high_keywords = ['important', 'priorité', 'commande', 'client', 'livraison']
        
        # Vérifier les mots-clés critiques
        for keyword in critical_keywords:
            if keyword in subject_lower:
                return 'critical'
        
        # Vérifier les mots-clés importants
        for keyword in high_keywords:
            if keyword in subject_lower:
                return 'high'
        
        # Vérifier l'expéditeur
        if 'client' in sender_lower or 'customer' in sender_lower:
            return 'high'
        
        return 'normal'
    
    async def get_email_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des emails"""
        try:
            if not self.service:
                return {"error": "Service Gmail non disponible"}
            
            # Compter les emails non lus
            query = "is:unread"
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=100
            ).execute()
            
            unread_count = len(results.get('messages', []))
            
            # Compter par type d'urgence
            urgent_emails = await self.check_urgent_emails()
            critical_count = len([e for e in urgent_emails if e['urgency'] == 'critical'])
            high_count = len([e for e in urgent_emails if e['urgency'] == 'high'])
            
            return {
                "total_unread": unread_count,
                "critical_emails": critical_count,
                "high_priority_emails": high_count,
                "urgent_emails": urgent_emails,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur résumé emails: {e}")
            return {"error": str(e)}
    
    async def mark_as_read(self, email_id: str) -> bool:
        """Marque un email comme lu"""
        try:
            if not self.service:
                return False
            
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            self.logger.info(f"✅ Email marqué comme lu: {email_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur marquage email: {e}")
            return False
    
    async def send_notification(self, email_data: Dict[str, Any]) -> str:
        """Génère une notification pour un email urgent"""
        urgency_emoji = {
            'critical': '🚨',
            'high': '⚠️',
            'normal': '📧'
        }
        
        emoji = urgency_emoji.get(email_data['urgency'], '📧')
        
        notification = (
            f"{emoji} Email urgent de {email_data['sender']}\n"
            f"📋 Sujet: {email_data['subject']}\n"
            f"📅 Date: {email_data['date']}\n"
            f"💬 Extrait: {email_data['snippet'][:100]}..."
        )
        
        return notification


if __name__ == "__main__":
    # Test du gestionnaire Gmail
    async def test_gmail_handler():
        handler = GmailHandler()
        
        print("📧 Test Gmail Handler")
        print("=" * 30)
        
        # Test résumé emails
        summary = await handler.get_email_summary()
        print(f"📊 Résumé emails:")
        print(f"  - Non lus: {summary.get('total_unread', 0)}")
        print(f"  - Critiques: {summary.get('critical_emails', 0)}")
        print(f"  - Importants: {summary.get('high_priority_emails', 0)}")
        
        # Test emails urgents
        urgent_emails = await handler.check_urgent_emails()
        print(f"\n🚨 Emails urgents: {len(urgent_emails)}")
        
        for email in urgent_emails[:3]:  # Afficher les 3 premiers
            print(f"  - {email['subject']} ({email['urgency']})")
    
    asyncio.run(test_gmail_handler()) 