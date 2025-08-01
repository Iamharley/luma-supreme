#!/usr/bin/env python3
"""
🔥 LUMA BUSINESS PRO - INTERFACE GRAPHIQUE
Fenêtre simple pour voir LUMA en action
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os
from datetime import datetime

# Ajouter le chemin des modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.luma_personality import LumaPersonality

class LumaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 LUMA BUSINESS PRO")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Initialiser LUMA
        self.personality = LumaPersonality()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titre
        title_label = tk.Label(
            main_frame,
            text="🔥 LUMA BUSINESS PRO",
            font=("Arial", 20, "bold"),
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
        
        # Frame des boutons
        buttons_frame = tk.Frame(main_frame, bg='#1a1a1a')
        buttons_frame.pack(pady=10)
        
        # Boutons de test
        tk.Button(
            buttons_frame,
            text="🌞 Briefing Matinal",
            font=("Arial", 12, "bold"),
            bg='#00ff88',
            fg='#000000',
            command=self.test_morning,
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            buttons_frame,
            text="🚨 Alerte Urgente",
            font=("Arial", 12, "bold"),
            bg='#ff4444',
            fg='#ffffff',
            command=self.test_alert,
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            buttons_frame,
            text="💙 Rappel Santé",
            font=("Arial", 12, "bold"),
            bg='#4444ff',
            fg='#ffffff',
            command=self.test_health,
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=5)
        
        # Zone de chat
        chat_frame = tk.Frame(main_frame, bg='#1a1a1a')
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Label chat
        chat_label = tk.Label(
            chat_frame,
            text="💬 CONVERSATION AVEC LUMA",
            font=("Arial", 14, "bold"),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        chat_label.pack(anchor=tk.W, pady=5)
        
        # Zone de chat
        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            height=15,
            bg='#000000',
            fg='#00ff88',
            font=("Courier", 10),
            insertbackground='#00ff88'
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame d'entrée
        input_frame = tk.Frame(main_frame, bg='#1a1a1a')
        input_frame.pack(fill=tk.X, pady=10)
        
        # Label entrée
        input_label = tk.Label(
            input_frame,
            text="💬 Dis quelque chose à LUMA:",
            font=("Arial", 10),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        input_label.pack(anchor=tk.W)
        
        # Zone de saisie
        self.input_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg='#333333',
            fg='#ffffff',
            insertbackground='#ffffff'
        )
        self.input_entry.pack(fill=tk.X, pady=5)
        self.input_entry.bind('<Return>', self.send_message)
        
        # Bouton envoyer
        send_button = tk.Button(
            input_frame,
            text="📤 Envoyer",
            font=("Arial", 10),
            bg='#00ff88',
            fg='#000000',
            command=self.send_message
        )
        send_button.pack(pady=5)
        
        # Message de bienvenue
        self.add_message("LUMA", "Salut Anne-Sophie ! 🌞 Je suis LUMA, ton employée digitale ! Je suis là pour t'aider avec Harley Vape. Essaie les boutons ou dis-moi quelque chose !")
        
    def add_message(self, sender, message):
        """Ajoute un message au chat"""
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "LUMA":
            self.chat_text.insert(tk.END, f"\n[{timestamp}] 💙 LUMA: {message}\n")
        else:
            self.chat_text.insert(tk.END, f"\n[{timestamp}] 👤 Anne-Sophie: {message}\n")
            
        self.chat_text.see(tk.END)
        self.root.update()
        
    def test_morning(self):
        """Test du briefing matinal"""
        self.add_message("LUMA", "🌞 Génération du briefing matinal...")
        
        morning_context = {
            'emails': '3',
            'orders': '1',
            'whatsapp': '2',
            'insight': 'Journée productive en vue !'
        }
        
        try:
            message = self.personality.generate_response('morning_briefing', morning_context)
            self.add_message("LUMA", message)
        except Exception as e:
            self.add_message("LUMA", f"❌ Erreur: {e}")
            
    def test_alert(self):
        """Test d'alerte urgente"""
        self.add_message("LUMA", "🚨 Génération d'une alerte urgente...")
        
        alert_context = {
            'alert_type': 'client_urgent',
            'priority': 'high',
            'action': 'décision_requise'
        }
        
        try:
            message = self.personality.generate_response('alert_urgent', alert_context)
            self.add_message("LUMA", message)
        except Exception as e:
            self.add_message("LUMA", f"❌ Erreur: {e}")
            
    def test_health(self):
        """Test de rappel santé"""
        self.add_message("LUMA", "💙 Génération d'un rappel santé...")
        
        health_context = {
            'time': datetime.now().strftime("%H:%M"),
            'hours': '4'
        }
        
        try:
            message = self.personality.generate_response('protective_reminder', health_context)
            self.add_message("LUMA", message)
        except Exception as e:
            self.add_message("LUMA", f"❌ Erreur: {e}")
            
    def send_message(self, event=None):
        """Envoie un message"""
        message = self.input_entry.get().strip()
        if not message:
            return
            
        self.add_message("Anne-Sophie", message)
        self.input_entry.delete(0, tk.END)
        
        # Réponse LUMA
        response = self.generate_response(message)
        self.add_message("LUMA", response)
        
    def generate_response(self, user_message):
        """Génère une réponse LUMA"""
        
        if "email" in user_message.lower() or "mail" in user_message.lower():
            return "📧 Je peux t'aider avec tes emails ! Pour l'instant je n'ai pas accès à ta boîte hello@iamharley.com, mais une fois configurée, je surveillerai tout 24/7 !"
            
        elif "harley" in user_message.lower() or "vape" in user_message.lower():
            return "🛒 Ah, on parle business Harley Vape ! Je vais devenir experte de ta boutique. Commandes, clients, support... tout ce qui peut te faire gagner du temps !"
            
        elif "fatigue" in user_message.lower() or "épuisé" in user_message.lower():
            return "💙 Je vois que tu es fatiguée... C'est exactement pour ça que je suis là ! Mon job c'est de t'enlever toute la charge mentale possible."
            
        elif "test" in user_message.lower():
            return "🧪 Test réussi ! Je te reçois parfaitement. Mon système de templates Lulu fonctionne, mes réponses sont personnalisées !"
            
        else:
            return f"💙 Je t'entends Anne-Sophie ! Je suis là pour t'aider avec Harley Vape. Emails, clients, commandes, stress... tout ce qui peut te soulager !"

def main():
    """Point d'entrée principal"""
    root = tk.Tk()
    app = LumaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 