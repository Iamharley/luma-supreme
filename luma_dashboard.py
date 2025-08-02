#!/usr/bin/env python3
"""
🔥 LUMA BUSINESS PRO - DASHBOARD VISUEL
Interface pour voir LUMA en action
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import asyncio
import sys
import os
from datetime import datetime

# Ajouter le répertoire à Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.main_engine import LumaBusinessEngine
from core.luma_personality import LumaPersonality
from dotenv import load_dotenv


class LumaDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 LUMA BUSINESS PRO - DASHBOARD")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a1a')
        
        # Variables
        self.luma_running = False
        self.luma_engine = None
        self.personality = LumaPersonality()
        
        # Charger configuration
        load_dotenv('config/.env')
        self.config = {
            "openai_key": os.getenv("OPENAI_API_KEY"),
            "claude_key": os.getenv("CLAUDE_API_KEY"),
            "shopify_key": os.getenv("SHOPIFY_ACCESS_TOKEN"),
            "gmail_address": os.getenv("GMAIL_ADDRESS"),
            "notion_token": os.getenv("NOTION_TOKEN")
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titre
        title_label = tk.Label(
            main_frame, 
            text="🔥 LUMA BUSINESS PRO", 
            font=("Arial", 24, "bold"),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        title_label.pack(pady=10)
        
        # Sous-titre
        subtitle_label = tk.Label(
            main_frame,
            text="💙 Employée digitale d'Anne-Sophie - Harley Vape",
            font=("Arial", 12),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        subtitle_label.pack(pady=5)
        
        # Frame de contrôle
        control_frame = tk.Frame(main_frame, bg='#1a1a1a')
        control_frame.pack(fill=tk.X, pady=10)
        
        # Boutons de contrôle
        self.start_button = tk.Button(
            control_frame,
            text="🚀 DÉMARRER LUMA",
            font=("Arial", 12, "bold"),
            bg='#00ff88',
            fg='#000000',
            command=self.start_luma,
            width=15,
            height=2
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            control_frame,
            text="🛑 ARRÊTER LUMA",
            font=("Arial", 12, "bold"),
            bg='#ff4444',
            fg='#ffffff',
            command=self.stop_luma,
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.test_button = tk.Button(
            control_frame,
            text="🧪 TEST TEMPLATE",
            font=("Arial", 12, "bold"),
            bg='#4444ff',
            fg='#ffffff',
            command=self.test_template,
            width=15,
            height=2
        )
        self.test_button.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = tk.Label(
            control_frame,
            text="⏸️ LUMA ARRÊTÉ",
            font=("Arial", 14, "bold"),
            fg='#ff4444',
            bg='#1a1a1a'
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Frame des logs
        logs_frame = tk.Frame(main_frame, bg='#1a1a1a')
        logs_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Label logs
        logs_label = tk.Label(
            logs_frame,
            text="📋 LOGS EN TEMPS RÉEL",
            font=("Arial", 14, "bold"),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        logs_label.pack(anchor=tk.W, pady=5)
        
        # Zone de logs
        self.logs_text = scrolledtext.ScrolledText(
            logs_frame,
            height=20,
            bg='#000000',
            fg='#00ff88',
            font=("Courier", 10),
            insertbackground='#00ff88'
        )
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame des actions
        actions_frame = tk.Frame(main_frame, bg='#1a1a1a')
        actions_frame.pack(fill=tk.X, pady=10)
        
        # Actions rapides
        actions_label = tk.Label(
            actions_frame,
            text="⚡ ACTIONS RAPIDES",
            font=("Arial", 14, "bold"),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        actions_label.pack(anchor=tk.W, pady=5)
        
        # Boutons d'actions
        actions_buttons_frame = tk.Frame(actions_frame, bg='#1a1a1a')
        actions_buttons_frame.pack(fill=tk.X)
        
        tk.Button(
            actions_buttons_frame,
            text="🌞 Briefing Matinal",
            font=("Arial", 10),
            bg='#4444ff',
            fg='#ffffff',
            command=lambda: self.generate_message('morning_briefing'),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            actions_buttons_frame,
            text="🚨 Alerte Urgente",
            font=("Arial", 10),
            bg='#ff4444',
            fg='#ffffff',
            command=lambda: self.generate_message('urgent_alert'),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            actions_buttons_frame,
            text="📊 Rapport Business",
            font=("Arial", 10),
            bg='#44ff44',
            fg='#000000',
            command=lambda: self.generate_message('business_report'),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            actions_buttons_frame,
            text="💬 Message Personnalisé",
            font=("Arial", 10),
            bg='#ff8844',
            fg='#ffffff',
            command=self.custom_message,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
    def log_message(self, message):
        """Ajoute un message aux logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
        self.root.update()
        
    def start_luma(self):
        """Démarre LUMA"""
        if not self.luma_running:
            self.log_message("🚀 Démarrage de LUMA Business Pro...")
            self.luma_running = True
            self.status_label.config(text="🟢 LUMA ACTIF", fg='#00ff88')
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Démarrer LUMA dans un thread séparé
            self.luma_thread = threading.Thread(target=self.run_luma_async)
            self.luma_thread.daemon = True
            self.luma_thread.start()
            
            self.log_message("✅ LUMA Business Engine initialisé")
            self.log_message("💙 Propriétaire: Anne-Sophie")
            self.log_message("🏢 Business: Harley Vape")
            self.log_message("⚡ Mode: Proactif 24/7")
            self.log_message("📧 Surveillance: hello@iamharley.com")
            
    def stop_luma(self):
        """Arrête LUMA"""
        if self.luma_running:
            self.log_message("🛑 Arrêt de LUMA...")
            self.luma_running = False
            self.status_label.config(text="⏸️ LUMA ARRÊTÉ", fg='#ff4444')
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            if self.luma_engine:
                # Arrêter le moteur
                pass
                
            self.log_message("✅ LUMA arrêté proprement")
            
    def run_luma_async(self):
        """Exécute LUMA de manière asynchrone"""
        try:
            self.luma_engine = LumaBusinessEngine(self.config)
            
            # Simuler des opérations en cours
            while self.luma_running:
                time.sleep(5)
                self.log_message("⏰ Vérification des tâches programmées...")
                time.sleep(5)
                self.log_message("📧 Surveillance des emails...")
                time.sleep(5)
                self.log_message("🛒 Monitoring business Harley Vape...")
                
        except Exception as e:
            self.log_message(f"❌ Erreur: {e}")
            
    def test_template(self):
        """Teste un template de message"""
        self.log_message("🧪 Test du template Lulu...")
        
        morning_context = {
            'emails': '3',
            'orders': '1', 
            'whatsapp': '2',
            'insight': 'Journée productive en vue !'
        }
        
        try:
            message = self.personality.generate_response('morning_briefing', morning_context)
            self.log_message("🌞 Template généré:")
            self.log_message(message)
        except Exception as e:
            self.log_message(f"❌ Erreur template: {e}")
            
    def generate_message(self, message_type):
        """Génère un message spécifique"""
        self.log_message(f"💬 Génération message: {message_type}")
        
        try:
            if message_type == 'morning_briefing':
                context = {'emails': '5', 'orders': '2', 'whatsapp': '1', 'insight': 'Belle journée en perspective !'}
                message = self.personality.generate_response('morning_briefing', context)
            elif message_type == 'urgent_alert':
                context = {'alert_type': 'client_urgent', 'priority': 'high', 'action': 'décision_requise'}
                message = self.personality.generate_response('urgent_alert', context)
            elif message_type == 'business_report':
                context = {'sales': '1500€', 'orders': '8', 'customers': '12', 'trend': 'positif'}
                message = self.personality.generate_response('business_report', context)
            else:
                message = "Message personnalisé généré !"
                
            self.log_message("📝 Message généré:")
            self.log_message(message)
            
        except Exception as e:
            self.log_message(f"❌ Erreur génération: {e}")
            
    def custom_message(self):
        """Interface pour message personnalisé"""
        self.log_message("💬 Interface message personnalisé...")
        # Ici on pourrait ouvrir une fenêtre de dialogue
        self.log_message("✨ Fonctionnalité à développer")


def main():
    """Point d'entrée principal"""
    root = tk.Tk()
    app = LumaDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main() 