const twilio = require('twilio');
const express = require('express');
const axios = require('axios');

// 🔥 LUMA BUSINESS PRO - TWILIO WHATSAPP (RAILWAY)
// 💙 Employée digitale autonome pour Harley Vape

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configuration depuis variables d'environnement
const PORT = process.env.PORT || 3001;
const HOST = process.env.HOST || '0.0.0.0';

const TWILIO_CONFIG = {
    accountSid: process.env.TWILIO_ACCOUNT_SID,
    authToken: process.env.TWILIO_AUTH_TOKEN,
    apiKeySid: process.env.TWILIO_API_KEY_SID,
    twilioWhatsApp: 'whatsapp:+14155238886',
    businessWhatsApp: '+13072251057'
};

const OPENROUTER_CONFIG = {
    apiKey: process.env.OPENROUTER_API_KEY,
    model: 'openai/gpt-4o-mini',
    baseUrl: 'https://openrouter.ai/api/v1'
};

const NOTION_CONFIG = {
    token: process.env.NOTION_API_KEY,
    databases: {
        whatsappHub: '2428658dde348043ae51dec1a73fc612',
        commandCenter: '2428658dde3480899f00e4d4fc7dddcb',
        dashboard: '2428658dde348081a8b8ce99ae6fc7e8',
        integrations: '2428658dde34806f9cb3ed3fa2f8244d',
        harleyVapeProducts: '22d8658dde348012a4aaf7731823668f',
        emailTracking: '1fc8658dde348021bf6dd567a38527c6',
        crm: '1f18658dde3480309c69cb944679ebf5'
    }
};

// ===================================================
// 🛡️ SYSTÈME ANTI-SPAM
// ===================================================
const conversationMemory = new Map();
const RESPONSE_COOLDOWN = 30000; // 30 secondes entre réponses

function shouldRespond(from, messageText) {
    const now = Date.now();
    const contactKey = from.split('@')[0];
    
    // Vérifier si c'est notre propre message
    if (messageText.includes('L\'équipe Harley Vape') || 
        messageText.includes('🧡') || 
        messageText.startsWith('Salut !') ||
        messageText.includes('LUMA')) {
        console.log('🚫 Message de LUMA détecté - Pas de réponse');
        return false;
    }
    
    // Vérifier le cooldown
    const lastResponse = conversationMemory.get(contactKey);
    if (lastResponse && (now - lastResponse) < RESPONSE_COOLDOWN) {
        console.log(`⏰ Cooldown actif pour ${contactKey} - Pas de réponse`);
        return false;
    }
    
    // Messages trop courts
    if (messageText.length < 3) {
        console.log('📏 Message trop court - Pas de réponse');
        return false;
    }
    
    // Messages avec émojis seulement
    const emojiRegex = /^[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]+$/u;
    if (emojiRegex.test(messageText.trim())) {
        console.log('😀 Message émojis seulement - Pas de réponse');
        return false;
    }
    
    return true;
}

// ===================================================
// 🤖 GÉNÉRATION RÉPONSE IA
// ===================================================
async function generateOpenRouterResponse(messageInfo, context, intent) {
    try {
        const prompt = `
Tu es LUMA, l'employée digitale de Harley Vape, une boutique de vape à Paris.
Réponds de manière professionnelle, amicale et en français.

CONTEXTE: ${context}
MESSAGE: ${messageInfo.body}
INTENTION: ${intent}

Réponds comme LUMA, l'employée de Harley Vape. Sois professionnelle, amicale et utile.
`;

        const response = await axios.post(`${OPENROUTER_CONFIG.baseUrl}/chat/completions`, {
            model: OPENROUTER_CONFIG.model,
            messages: [
                { role: 'system', content: 'Tu es LUMA, employée digitale de Harley Vape à Paris.' },
                { role: 'user', content: prompt }
            ],
            max_tokens: 150,
            temperature: 0.7
        }, {
            headers: {
                'Authorization': `Bearer ${OPENROUTER_CONFIG.apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        console.log('✅ OpenRouter utilisé avec succès!');
        return response.data.choices[0].message.content.trim();
    } catch (error) {
        console.error('❌ Erreur OpenRouter:', error.message);
        return "Bonjour ! Je suis LUMA, l'employée digitale de Harley Vape. Comment puis-je vous aider ?";
    }
}

// ===================================================
// 📊 LOGGING NOTION
// ===================================================
async function logToNotion(contact, message, response) {
    try {
        const notionData = {
            parent: { database_id: NOTION_CONFIG.databases.whatsappHub },
            properties: {
                'Nom': { title: [{ text: { content: contact.split('@')[0] } }] },
                'Contact': { rich_text: [{ text: { content: contact } }] },
                'Dernier message': { rich_text: [{ text: { content: message } }] },
                'Statut': { select: { name: 'Nouveau' } },
                'Langue': { select: { name: 'Français' } },
                'Type demande': { select: { name: 'Info générale' } },
                'Priorite': { select: { name: 'Normal' } },
                'Numero': { rich_text: [{ text: { content: contact } }] },
                'Nombre echanges': { number: 1 },
                'Date creation': { date: { start: new Date().toISOString() } }
            }
        };

        await axios.post('https://api.notion.com/v1/pages', notionData, {
            headers: {
                'Authorization': `Bearer ${NOTION_CONFIG.token}`,
                'Content-Type': 'application/json',
                'Notion-Version': '2022-06-28'
            }
        });

        console.log('✅ Entrée créée dans Notion');
    } catch (error) {
        console.error('❌ Erreur Notion:', error.message);
    }
}

// ===================================================
// 📱 WEBHOOK WHATSAPP
// ===================================================
app.post('/webhook/twilio-whatsapp', async (req, res) => {
    try {
        console.log('📱 Message WhatsApp reçu:', req.body);
        
        const { From, Body, ProfileName } = req.body;
        
        if (!From || !Body) {
            return res.status(400).json({ error: 'Données manquantes' });
        }

        // Anti-spam check
        if (!shouldRespond(From, Body)) {
            console.log('🚫 Message ignoré par anti-spam');
            return res.json({ status: 'Ignored', reason: 'Anti-spam' });
        }

        // Marquer qu'on va répondre
        const contactKey = From.split('@')[0];
        conversationMemory.set(contactKey, Date.now());

        // Générer réponse IA
        const context = `Client: ${ProfileName || contactKey}`;
        const intent = 'customer_inquiry';
        const response = await generateOpenRouterResponse({ body: Body }, context, intent);

        console.log(`🤖 Réponse générée: ${response}`);

        // Logger dans Notion
        await logToNotion(From, Body, response);

        // Envoyer réponse via Twilio
        const client = twilio(TWILIO_CONFIG.accountSid, TWILIO_CONFIG.authToken);
        
        await client.messages.create({
            body: response,
            from: `whatsapp:${TWILIO_CONFIG.businessWhatsApp}`,
            to: From
        });

        console.log('✅ Réponse envoyée via Twilio');

        res.json({ 
            status: 'OK', 
            message: 'Message traité avec succès',
            response: response
        });

    } catch (error) {
        console.error('❌ Erreur webhook:', error);
        res.status(500).json({ error: error.message });
    }
});

// ===================================================
// 📊 ENDPOINTS DE MONITORING
// ===================================================
app.get('/status', (req, res) => {
    res.json({
        status: 'online',
        service: 'LUMA Twilio WhatsApp',
        timestamp: new Date().toISOString(),
        memory: conversationMemory.size,
        port: PORT,
        host: HOST
    });
});

app.get('/', (req, res) => {
    res.send(`
        <h1>🔥 LUMA BUSINESS PRO - TWILIO WHATSAPP</h1>
        <p>Employée digitale autonome pour Harley Vape</p>
        <p>Status: <a href="/status">/status</a></p>
        <p>Webhook: <code>/webhook/twilio-whatsapp</code></p>
        <p>Port: ${PORT}</p>
        <p>Host: ${HOST}</p>
    `);
});

// ===================================================
// 🚀 DÉMARRAGE SERVEUR
// ===================================================
app.listen(PORT, HOST, () => {
    console.log('🔥 LUMA BUSINESS PRO - TWILIO WHATSAPP (RAILWAY)');
    console.log('💙 Employée digitale autonome pour Harley Vape');
    console.log('===================================================');
    console.log(`📱 Webhook WhatsApp: /webhook/twilio-whatsapp`);
    console.log(`🌐 Serveur démarré sur ${HOST}:${PORT}`);
    console.log('🎉 LUMA TWILIO OPÉRATIONNEL !');
    console.log('📱 Connecté à Twilio WhatsApp Business');
    console.log('⚡ Réponses automatiques activées !');
    console.log('🛡️ Système anti-spam WhatsApp activé !');
    console.log('✅ LUMA Twilio WhatsApp prêt à recevoir des messages !');
});

// ===================================================
// 🔄 NETTOYAGE MÉMOIRE
// ===================================================
setInterval(() => {
    const now = Date.now();
    for (const [key, timestamp] of conversationMemory.entries()) {
        if (now - timestamp > RESPONSE_COOLDOWN * 2) {
            conversationMemory.delete(key);
        }
    }
}, 60000);
