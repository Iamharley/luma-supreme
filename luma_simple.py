#!/usr/bin/env python3
"""
🔥 LUMA BUSINESS PRO - VERSION SIMPLE
Test immédiat des templates Lulu
"""

import sys
import os

# Ajouter le chemin des modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.luma_personality import LumaPersonality

def main():
    """Test simple de LUMA"""
    
    print("🔥 LUMA BUSINESS PRO - TEST SIMPLE")
    print("=" * 50)
    
    # Initialiser LUMA
    try:
        personality = LumaPersonality()
        print("✅ LUMA initialisée avec succès !")
        
        # Test 1: Briefing matinal
        print("\n🌞 TEST 1: Briefing Matinal")
        print("-" * 30)
        morning_context = {
            'emails': '3',
            'orders': '1', 
            'whatsapp': '2',
            'insight': 'Journée productive en vue !'
        }
        morning_msg = personality.generate_response('morning_briefing', morning_context)
        print(morning_msg)
        
        # Test 2: Alerte urgente
        print("\n🚨 TEST 2: Alerte Urgente")
        print("-" * 30)
        alert_context = {
            'alert_type': 'client_urgent',
            'priority': 'high',
            'action': 'décision_requise'
        }
        alert_msg = personality.generate_response('alert_urgent', alert_context)
        print(alert_msg)
        
        # Test 3: Rappel santé
        print("\n💙 TEST 3: Rappel Santé")
        print("-" * 30)
        health_context = {
            'time': '14:30',
            'hours': '4'
        }
        health_msg = personality.generate_response('protective_reminder', health_context)
        print(health_msg)
        
        print("\n" + "=" * 50)
        print("🎉 TOUS LES TESTS RÉUSSIS !")
        print("💙 LUMA est prête à sauver Harley Vape !")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 