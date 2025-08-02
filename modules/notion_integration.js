/**
 * 🔗 LUMA NOTION INTEGRATION
 * =========================
 * Intégration automatique WhatsApp → Notion
 * Centralisation de toutes les conversations
 * =========================
 */

const axios = require('axios')

// Configuration Notion avec variables d'environnement
const NOTION_CONFIG = {
    TOKEN: process.env.NOTION_API_KEY,
    DATABASES: {
        WHATSAPP_HUB: "2428658dde348043ae51dec1a73fc612",
        COMMAND_CENTER: "2428658dde3480899f00e4d4fc7dddcb", 
        DASHBOARD: "2428658dde348081a8b8ce99ae6fc7e8",
        INTEGRATIONS: "2428658dde34806f9cb3ed3fa2f8244d",
        HARLEY_PRODUCTS: "22d8658dde348012a4aaf7731823668f",
        EMAIL_SUIVI: "1fc8658dde348021bf6dd567a38527c6"
    }
}

class NotionIntegration {
    constructor() {
        this.baseUrl = 'https://api.notion.com/v1'
        this.headers = {
            'Authorization': `Bearer ${NOTION_CONFIG.TOKEN}`,
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
    }

    // 🔍 Détection automatique de langue
    detectLanguage(text) {
        const french = /\b(bonjour|salut|merci|oui|non|comment|quoi|pourquoi|quand|où|qui)\b/i
        const english = /\b(hello|hi|thanks|yes|no|how|what|why|when|where|who)\b/i
        const spanish = /\b(hola|gracias|si|no|como|que|porque|cuando|donde|quien)\b/i
        
        if (french.test(text)) return 'Français'
        if (spanish.test(text)) return 'Espagnol'  
        if (english.test(text)) return 'Anglais'
        return 'Français' // Par défaut
    }

    // 🎯 Classification automatique des demandes
    classifyRequest(text) {
        const lower = text.toLowerCase()
        
        if (lower.includes('geekbar') || lower.includes('produit') || lower.includes('vape')) 
            return 'Info produit'
        if (lower.includes('ouvert') || lower.includes('horaire') || lower.includes('fermé')) 
            return 'Horaires'
        if (lower.includes('problème') || lower.includes('bug') || lower.includes('sav')) 
            return 'SAV'
        if (lower.includes('commande') || lower.includes('livraison') || lower.includes('suivi')) 
            return 'Commande'
        if (lower.includes('prix') || lower.includes('tarif') || lower.includes('coût')) 
            return 'Tarification'
        
        return 'Info générale'
    }

    // ⚡ Détection de priorité
    getPriority(text) {
        const urgent = /urgent|emergency|problème|help|sos|immédiat/i
        const high = /important|rapide|vite|dépêche/i
        
        if (urgent.test(text)) return 'Urgent'
        if (high.test(text)) return 'Élevée'
        return 'Normal'
    }

    // 📝 Créer entrée dans WhatsApp Business Hub
    async createWhatsAppEntry(messageData) {
        const startTime = Date.now()
        
        const notionData = {
            nom: messageData.contactName || messageData.phone.split('@')[0],
            contact: messageData.phone,
            dernier_message: messageData.text,
            statut: "Nouveau",
            langue: this.detectLanguage(messageData.text),
            type_demande: this.classifyRequest(messageData.text),
            priorite: this.getPriority(messageData.text),
            numero: messageData.phone,
            nombre_echanges: 1,
            date_creation: new Date().toISOString()
        }

        try {
            const response = await axios.post(`${this.baseUrl}/pages`, {
                parent: { database_id: NOTION_CONFIG.DATABASES.WHATSAPP_HUB },
                properties: {
                    'Nom': { title: [{ text: { content: notionData.nom } }] },
                    'Contact': { rich_text: [{ text: { content: notionData.contact } }] },
                    'Dernier message': { rich_text: [{ text: { content: notionData.dernier_message } }] },
                    'Statut': { select: { name: notionData.statut } },
                    'Langue': { select: { name: notionData.langue } },
                    'Type demande': { select: { name: notionData.type_demande } },
                    'Priorité': { select: { name: notionData.priorite } },
                    'Numéro': { phone_number: notionData.numero },
                    'Nombre d\'échanges': { number: notionData.nombre_echanges }
                }
            }, { headers: this.headers })

            console.log(`✅ Contact créé dans Notion WhatsApp Hub: ${notionData.nom}`)
            return { success: true, data: response.data, processingTime: Date.now() - startTime }
            
        } catch (error) {
            console.error('❌ Erreur création entrée WhatsApp Hub:', error.response?.data || error.message)
            return { success: false, error: error.message }
        }
    }

    // 🎮 Logger dans Command Center
    async logCommandCenter(actionData) {
        try {
            const response = await axios.post(`${this.baseUrl}/pages`, {
                parent: { database_id: NOTION_CONFIG.DATABASES.COMMAND_CENTER },
                properties: {
                    'Action': { title: [{ text: { content: actionData.action } }] },
                    'Canal': { select: { name: actionData.canal } },
                    'Statut': { select: { name: actionData.statut } },
                    'Client': { rich_text: [{ text: { content: actionData.client } }] },
                    'IA impliquée': { rich_text: [{ text: { content: actionData.ia_impliquee } }] },
                    'Temps traitement': { number: actionData.temps_traitement },
                    'Date': { date: { start: new Date().toISOString() } }
                }
            }, { headers: this.headers })

            console.log(`✅ Action loggée dans Command Center: ${actionData.action}`)
            return { success: true, data: response.data }
            
        } catch (error) {
            console.error('❌ Erreur log Command Center:', error.response?.data || error.message)
            return { success: false, error: error.message }
        }
    }

    // 📊 Mettre à jour Dashboard Central
    async updateDashboard(metricsData) {
        try {
            const response = await axios.post(`${this.baseUrl}/pages`, {
                parent: { database_id: NOTION_CONFIG.DATABASES.DASHBOARD },
                properties: {
                    'Type': { select: { name: metricsData.type } },
                    'Client': { rich_text: [{ text: { content: metricsData.client } }] },
                    'Langue': { select: { name: metricsData.language } },
                    'Priorité': { select: { name: metricsData.priority } },
                    'Date': { date: { start: new Date().toISOString() } }
                }
            }, { headers: this.headers })

            console.log(`✅ Métriques mises à jour dans Dashboard: ${metricsData.type}`)
            return { success: true, data: response.data }
            
        } catch (error) {
            console.error('❌ Erreur mise à jour Dashboard:', error.response?.data || error.message)
            return { success: false, error: error.message }
        }
    }

    // 🔗 Logger dans Intégrations auto
    async logIntegration(integrationData) {
        try {
            const response = await axios.post(`${this.baseUrl}/pages`, {
                parent: { database_id: NOTION_CONFIG.DATABASES.INTEGRATIONS },
                properties: {
                    'Nom': { title: [{ text: { content: integrationData.nom } }] },
                    'Statut': { select: { name: integrationData.statut } },
                    'Source': { select: { name: integrationData.source } },
                    'Cible': { select: { name: integrationData.cible } },
                    'Connecteur': { select: { name: integrationData.connecteur } },
                    'Type': { select: { name: integrationData.type } },
                    'Dernière exécution': { date: { start: integrationData.derniere_execution } },
                    'IA impliquée': { rich_text: [{ text: { content: integrationData.ia_impliquee } }] }
                }
            }, { headers: this.headers })

            console.log(`✅ Intégration loggée: ${integrationData.nom}`)
            return { success: true, data: response.data }
            
        } catch (error) {
            console.error('❌ Erreur log intégration:', error.response?.data || error.message)
            return { success: false, error: error.message }
        }
    }

    // 🚀 Fonction principale d'intégration complète
    async logToNotion(messageData, responseData, processingTime) {
        const startTime = Date.now()
        
        try {
            // 1. Créer entrée dans WhatsApp Business Hub
            const whatsappResult = await this.createWhatsAppEntry(messageData)
            
            // 2. Logger dans Command Center  
            const commandResult = await this.logCommandCenter({
                action: "Réponse automatique WhatsApp",
                canal: "WhatsApp", 
                statut: "Succès",
                client: messageData.phone,
                ia_impliquee: "Luma Pro (Railway)",
                temps_traitement: processingTime || (Date.now() - startTime)
            })
            
            // 3. Mettre à jour Dashboard Central
            const dashboardResult = await this.updateDashboard({
                type: "whatsapp_message",
                client: messageData.phone,
                language: this.detectLanguage(messageData.text),
                priority: this.getPriority(messageData.text)
            })
            
            // 4. Logger dans Intégrations auto
            const integrationResult = await this.logIntegration({
                nom: "WhatsApp → Luma → Notion (support)",
                statut: "Actif",
                source: "WhatsApp",
                cible: "Notion", 
                connecteur: "Twilio",
                type: "Unidirectionnelle",
                derniere_execution: new Date().toISOString(),
                ia_impliquee: "Luma Pro"
            })

            console.log(`🎉 Intégration Notion complète réussie pour ${messageData.contactName}`)
            return {
                success: true,
                results: {
                    whatsapp: whatsappResult,
                    command: commandResult,
                    dashboard: dashboardResult,
                    integration: integrationResult
                },
                totalTime: Date.now() - startTime
            }
            
        } catch (error) {
            console.error('❌ Erreur intégration Notion complète:', error)
            return { success: false, error: error.message }
        }
    }
}

module.exports = NotionIntegration 