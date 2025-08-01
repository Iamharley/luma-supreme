# 🚀 LUMA SUPREME - Dockerfile pour déploiement cloud
FROM node:20-alpine

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=20

# Installation de Python et des dépendances système
RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    wget \
    gnupg

# Vérification et mise à jour de Node.js vers la version 20
RUN node --version && npm --version

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt package*.json ./

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installation des dépendances Node.js avec vérification de version
RUN node --version && npm install

# Copie du code source
COPY . .

# Création des répertoires nécessaires
RUN mkdir -p baileys_auth logs

# Script de démarrage
COPY start_cloud.sh /start_cloud.sh
RUN chmod +x /start_cloud.sh

# Exposition des ports
EXPOSE 5001 3001

# Point d'entrée
ENTRYPOINT ["/start_cloud.sh"] 