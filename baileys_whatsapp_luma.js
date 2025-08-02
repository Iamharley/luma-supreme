#!/usr/bin/env node
/**
 * 🔥 LUMA BUSINESS PRO - BAILEYS WHATSAPP INTEGRATION
 * ==================================================
 * WhatsApp automatique 100% GRATUIT avec Baileys
 * Pas de Meta Business, pas d'API payante !
 * ==================================================
 * FICHIER POUR CURSOR : baileys_whatsapp_luma.js
 */

const { makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys')
const { Boom } = require('@hapi/boom')
const express = require('express')
const axios = require('axios')
const fs = require('fs')
const path = require('path')
const qrcode = require('qrcode-terminal')

// 🔗 Intégration Notion
const NotionIntegration = require('./modules/notion_integration')

// Configuration
const CONFIG = {
    // LUMA Service
    lumaWebhookUrl: 'http://localhost:5001/webhook/whatsapp',
    
    // Business Info
    businessName: 'Harley Vape',
    businessHours: { start: 9, end: 18 },
    
    // Baileys Config
    authFolder: './baileys_auth',
    logLevel: 'info',
    
    // Auto-response
    autoResponseEnabled: true,
    responseDelay: 2000 // 2 secondes pour humaniser
}

// Templates WhatsApp Lulu (intégrés directement)
const LUMA_TEMPLATES = {
    welcome_new_client: "Bonjour {name} ! 👋\nMerci de contacter Harley Vape !\n\nJe suis LUMA, l'assistante digitale d'Anne-Sophie. Comment puis-je vous aider aujourd'hui ? 😊\n\n🛒 Commandes\n📦 Suivi livraison\n❓ Questions produits\n\nRépondez simplement !",
    
    urgent_support: "🚨 URGENT - Pris en charge !\n\nBonjour {name}, je comprends l'urgence de votre situation.\n\nJe transmets immédiatement à Anne-Sophie qui vous recontacte sous 30 minutes maximum.\n\nVotre demande urgente est notre priorité absolue ! 💙",
    
    order_inquiry: "📦 Commande en cours !\n\nBonjour {name}, je vérifie votre commande immédiatement.\n\nVotre demande est prise en compte et notre équipe vous recontacte très rapidement avec toutes les infos ! 😊\n\nAutre chose pour vous aider ?",
    
    after_hours: "🌙 Harley Vape - Hors horaires\n\nBonsoir {name} !\n\nIl est {time} et notre équipe est en repos bien mérité 😴\n\nVotre message est enregistré et nous vous répondons dès demain matin (9h-18h).\n\nBonne soirée ! 🌟",
    
    general_response: "Salut {name} ! 😊\n\nMerci pour votre message ! Je suis LUMA, l'assistante d'Anne-Sophie pour Harley Vape.\n\nComment puis-je vous aider ?\n\n🛒 Commandes et produits\n📞 Contact direct\n❓ Questions diverses\n\nJe suis là pour vous ! 💙"
}

class BaileysLumaService {
    constructor() {
        this.sock = null
        this.clientContexts = new Map()
        this.isReady = false
        
        // Créer dossier auth si inexistant
        if (!fs.existsSync(CONFIG.authFolder)) {
            fs.mkdirSync(CONFIG.authFolder, { recursive: true })
        }
    }

    async start() {
        console.log('🚀 LUMA Baileys WhatsApp Service - Démarrage...')
        
        try {
            // État d'authentification multi-device
            const { state, saveCreds } = await useMultiFileAuthState(CONFIG.authFolder)
            
            // Créer socket WhatsApp
            this.sock = makeWASocket({
                auth: state,
                browser: ['LUMA Business Pro', 'Desktop', '1.0.0'],
                markOnlineOnConnect: true
            })
            
            // Gestionnaires d'événements
            this.setupEventHandlers(saveCreds)
            
            console.log('📱 En attente de connexion WhatsApp...')
            console.log('👆 Scannez le QR code avec votre WhatsApp !')
            
        } catch (error) {
            console.error('💥 Erreur démarrage Baileys:', error)
        }
    }

    setupEventHandlers(saveCreds) {
        // Gestion connexion
        this.sock.ev.on('connection.update', (update) => {
            const { connection, lastDisconnect, qr } = update
            
            if (qr) {
                console.log('📱 Nouveau QR Code généré ! Scannez avec WhatsApp')
                console.log('🔍 Affichage du QR Code dans le terminal...')
                qrcode.generate(qr, { small: true })
                console.log('👆 Scannez le QR code ci-dessus avec votre WhatsApp !')
            }
            
            if (connection === 'close') {
                const shouldReconnect = (lastDisconnect?.error instanceof Boom)?.output?.statusCode !== DisconnectReason.loggedOut
                
                console.log('🔌 Connexion fermée:', lastDisconnect?.error, ', reconnexion:', shouldReconnect)
                
                if (shouldReconnect) {
                    setTimeout(() => this.start(), 3000)
                }
            } else if (connection === 'open') {
                console.log('✅ WhatsApp connecté avec succès !')
                console.log('🎉 LUMA peut maintenant répondre automatiquement !')
                this.isReady = true
            }
        })

        // Sauvegarde credentials
        this.sock.ev.on('creds.update', saveCreds)

        // RÉCEPTION MESSAGES - CŒUR DU SYSTÈME
        this.sock.ev.on('messages.upsert', async ({ messages }) => {
            for (const message of messages) {
                await this.handleIncomingMessage(message)
            }
        })

        // Gestion présence (optionnel)
        this.sock.ev.on('presence.update', ({ id, presences }) => {
            console.log('👀 Présence update:', id, Object.keys(presences))
        })
    }

    async handleIncomingMessage(message) {
        try {
            // Ignorer messages de LUMA elle-même
            if (message.key.fromMe) return
            
            // Extraire infos message
            const messageInfo = this.extractMessageInfo(message)
            if (!messageInfo) return
            
            console.log(`📱 Message reçu de ${messageInfo.phone}: ${messageInfo.text}`)
            
            // Traitement LUMA
            await this.processWithLuma(messageInfo)
            
        } catch (error) {
            console.error('❌ Erreur traitement message:', error)
        }
    }

    extractMessageInfo(message) {
        const phone = message.key.remoteJid
        const messageType = Object.keys(message.message || {})[0]
        
        let text = ''
        let contactName = phone.split('@')[0] // Fallback
        
        // Extraction texte selon type
        if (messageType === 'conversation') {
            text = message.message.conversation
        } else if (messageType === 'extendedTextMessage') {
            text = message.message.extendedTextMessage.text
        } else if (messageType === 'imageMessage' && message.message.imageMessage.caption) {
            text = message.message.imageMessage.caption
        } else {
            console.log('📎 Type de message non supporté:', messageType)
            return null
        }
        
        // Essayer d'obtenir le nom du contact
        if (message.pushName) {
            contactName = message.pushName
        }
        
        return {
            phone: phone,
            text: text.trim(),
            contactName: contactName,
            messageId: message.key.id,
            timestamp: message.messageTimestamp || Date.now()
        }
    }

    async processWithLuma(messageInfo) {
        const startTime = Date.now()
        
        try {
            // 1. Analyser message et contexte
            const context = this.getClientContext(messageInfo.phone, messageInfo.contactName)
            const intent = this.analyzeIntent(messageInfo.text)
            
            // 2. Générer réponse LUMA
            const lumaResponse = this.generateLumaResponse(messageInfo, context, intent)
            
            // 3. Optionnel: Appeler service LUMA Python pour traitement avancé
            let enhancedResponse = lumaResponse
            if (CONFIG.lumaWebhookUrl) {
                try {
                    const webhookResponse = await axios.post(CONFIG.lumaWebhookUrl, {
                        from: messageInfo.phone,
                        message: messageInfo.text,
                        contact_name: messageInfo.contactName,
                        baileys_source: true
                    }, { timeout: 10000 })
                    
                    if (webhookResponse.data && webhookResponse.data.luma_response) {
                        enhancedResponse = webhookResponse.data.luma_response
                        console.log('🧠 Réponse LUMA Python utilisée')
                    }
                } catch (webhookError) {
                    console.log('⚠️ Service LUMA Python non disponible, utilisation templates locaux')
                }
            }
            
            // 4. Délai humanisé
            if (CONFIG.responseDelay > 0) {
                await this.sleep(CONFIG.responseDelay)
            }
            
            // 5. Envoyer réponse
            await this.sendMessage(messageInfo.phone, enhancedResponse)
            
            // 6. 🔗 Intégration Notion automatique
            const processingTime = Date.now() - startTime
            await this.integrateWithNotion(messageInfo, enhancedResponse, processingTime)
            
            // 7. Log interaction
            this.logInteraction(messageInfo, enhancedResponse, intent)
            
        } catch (error) {
            console.error('❌ Erreur processWithLuma:', error)
            
            // Réponse de fallback
            const fallbackResponse = `Bonjour ${messageInfo.contactName} ! Merci pour votre message. Notre équipe Harley Vape vous répond très rapidement ! 😊`
            await this.sendMessage(messageInfo.phone, fallbackResponse)
            
            // Intégration Notion même en cas d'erreur
            const processingTime = Date.now() - startTime
            await this.integrateWithNotion(messageInfo, fallbackResponse, processingTime)
        }
    }

    analyzeIntent(text) {
        const textLower = text.toLowerCase()
        
        const intents = {
            urgent: ['urgent', 'problème', 'help', 'aide', 'bug', 'erreur'],
            order: ['commande', 'order', 'suivi', 'tracking', 'livraison'],
            product: ['produit', 'product', 'prix', 'price', 'stock'],
            greeting: ['bonjour', 'hello', 'salut', 'hi', 'bonsoir'],
            thanks: ['merci', 'thank', 'parfait', 'super', 'génial']
        }
        
        for (const [intent, keywords] of Object.entries(intents)) {
            if (keywords.some(keyword => textLower.includes(keyword))) {
                return intent
            }
        }
        
        return 'general'
    }

    generateLumaResponse(messageInfo, context, intent) {
        const now = new Date()
        const hour = now.getHours()
        const isBusinessHours = hour >= CONFIG.businessHours.start && hour <= CONFIG.businessHours.end
        
        const variables = {
            name: messageInfo.contactName,
            time: now.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
        }
        
        let templateKey = 'general_response'
        
        // Sélection template selon contexte
        if (!isBusinessHours) {
            templateKey = 'after_hours'
        } else if (intent === 'urgent') {
            templateKey = 'urgent_support'
        } else if (intent === 'order') {
            templateKey = 'order_inquiry'
        } else if (context.interactionCount === 0) {
            templateKey = 'welcome_new_client'
        }
        
        // Génération réponse
        let response = LUMA_TEMPLATES[templateKey] || LUMA_TEMPLATES.general_response
        
        // Remplacement variables
        for (const [key, value] of Object.entries(variables)) {
            response = response.replace(new RegExp(`{${key}}`, 'g'), value)
        }
        
        return response
    }

    getClientContext(phone, name) {
        if (!this.clientContexts.has(phone)) {
            this.clientContexts.set(phone, {
                phone: phone,
                name: name,
                interactionCount: 0,
                lastInteraction: null,
                notes: ''
            })
        }
        
        const context = this.clientContexts.get(phone)
        context.interactionCount++
        context.lastInteraction = new Date()
        
        return context
    }

    async sendMessage(phone, text) {
        try {
            if (!this.isReady) {
                console.log('⚠️ WhatsApp pas encore prêt, message en attente...')
                return
            }
            
            await this.sock.sendMessage(phone, { text: text })
            console.log(`📤 Réponse envoyée à ${phone}: ${text.substring(0, 50)}...`)
            
        } catch (error) {
            console.error('❌ Erreur envoi message:', error)
        }
    }

    logInteraction(messageInfo, response, intent) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            phone: messageInfo.phone.substring(0, 8) + '****', // Privacy
            contact_name: messageInfo.contactName,
            message_in: messageInfo.text.substring(0, 100),
            message_out: response.substring(0, 100),
            intent: intent,
            source: 'baileys'
        }
        
        console.log('📊 Interaction:', JSON.stringify(logEntry))
        
        // Optionnel: Sauvegarder dans fichier
        const logFile = path.join(__dirname, 'luma_interactions.log')
        fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n')
    }

    createLogger() {
        return {
            level: CONFIG.logLevel,
            child: () => this.createLogger(),
            error: (...args) => console.log('[ERROR]', ...args),
            warn: (...args) => console.log('[WARN]', ...args),
            info: (...args) => console.log('[INFO]', ...args),
            debug: (...args) => console.log('[DEBUG]', ...args),
            trace: (...args) => console.log('[TRACE]', ...args),
            log: (level, ...args) => {
                if (level === 'error' || level === 'warn') {
                    console.log(`[${level.toUpperCase()}]`, ...args)
                }
            }
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms))
    }

    // Méthodes utilitaires
    async getProfilePicture(phone) {
        try {
            const profilePic = await this.sock.profilePictureUrl(phone, 'image')
            return profilePic
        } catch {
            return null
        }
    }

    async markAsRead(phone, messageId) {
        try {
            await this.sock.readMessages([{ remoteJid: phone, id: messageId }])
        } catch (error) {
            console.log('⚠️ Impossible de marquer comme lu:', error.message)
        }
    }

    // 🔗 Intégration automatique avec Notion
    async integrateWithNotion(messageInfo, responseText, processingTime) {
        try {
            // Initialiser l'intégration Notion
            const notionIntegration = new NotionIntegration()
            
            // Logger automatiquement dans Notion
            const notionResult = await notionIntegration.logToNotion(messageInfo, responseText, processingTime)
            
            if (notionResult.success) {
                console.log(`🎉 Intégration Notion réussie pour ${messageInfo.contactName}`)
                console.log(`⏱️ Temps total: ${notionResult.totalTime}ms`)
            } else {
                console.error('❌ Erreur intégration Notion:', notionResult.error)
            }
            
        } catch (error) {
            console.error('❌ Erreur intégration Notion:', error)
            // Ne pas bloquer le processus principal en cas d'erreur Notion
        }
    }
}

// Interface HTTP pour monitoring (optionnel)
class LumaMonitoringServer {
    constructor(baileysService) {
        this.baileys = baileysService
        this.app = express()
        this.app.use(express.json())
        
        this.setupRoutes()
    }

    setupRoutes() {
        // Status LUMA
        this.app.get('/status', (req, res) => {
            res.json({
                service: 'LUMA Baileys WhatsApp',
                status: this.baileys.isReady ? 'connected' : 'connecting',
                clients: this.baileys.clientContexts.size,
                timestamp: new Date().toISOString()
            })
        })

        // Envoyer message manuel (pour tests)
        this.app.post('/send', async (req, res) => {
            try {
                const { phone, message } = req.body
                if (!phone || !message) {
                    return res.status(400).json({ error: 'phone et message requis' })
                }
                
                await this.baileys.sendMessage(phone, message)
                res.json({ success: true, message: 'Message envoyé' })
                
            } catch (error) {
                res.status(500).json({ error: error.message })
            }
        })

        // Statistiques
        this.app.get('/stats', (req, res) => {
            const contexts = Array.from(this.baileys.clientContexts.values())
            res.json({
                total_clients: contexts.length,
                interactions_today: contexts.reduce((sum, ctx) => sum + ctx.interactionCount, 0),
                active_conversations: contexts.filter(ctx => 
                    ctx.lastInteraction && 
                    Date.now() - ctx.lastInteraction.getTime() < 24 * 60 * 60 * 1000
                ).length
            })
        })
    }

    start(port = 3001) {
        this.app.listen(port, () => {
            console.log(`📊 Monitoring LUMA disponible sur http://localhost:${port}`)
            console.log(`📊 Status: http://localhost:${port}/status`)
        })
    }
}

// DÉMARRAGE PRINCIPAL
async function main() {
    console.log('🔥 LUMA BUSINESS PRO - BAILEYS WHATSAPP (GRATUIT)')
    console.log('💙 Réponses automatiques clients sans Meta Business !')
    console.log('=' + '='.repeat(50))
    
    try {
        // Vérifier dépendances
        console.log('📦 Vérification dépendances...')
        
        // Démarrer service Baileys
        const lumaService = new BaileysLumaService()
        await lumaService.start()
        
        // Démarrer monitoring (optionnel)
        const monitoring = new LumaMonitoringServer(lumaService)
        monitoring.start(3001)
        
        console.log('\n🎉 LUMA BAILEYS OPÉRATIONNEL !')
        console.log('📱 Scannez le QR code avec WhatsApp Business Harley Vape')
        console.log('⚡ Réponses automatiques activées !')
        
        // Gestion arrêt propre
        process.on('SIGINT', () => {
            console.log('\n👋 Arrêt LUMA Baileys...')
            process.exit(0)
        })
        
    } catch (error) {
        console.error('💥 Erreur démarrage:', error)
        process.exit(1)
    }
}

// Gestion erreurs non capturées
process.on('unhandledRejection', (error) => {
    console.error('💥 Erreur non gérée:', error)
})

process.on('uncaughtException', (error) => {
    console.error('💥 Exception non capturée:', error)
    process.exit(1)
})

// Lancement si fichier principal
if (require.main === module) {
    main()
}

module.exports = { BaileysLumaService, LumaMonitoringServer } 