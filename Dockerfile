# 🚀 LUMA SUPREME - Dockerfile optimisé pour Railway
FROM node:20-alpine

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION=20
ENV PYTHON_VERSION=3.11

# Installation de Python et des dépendances système
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    build-base \
    curl \
    wget \
    gnupg

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt package*.json ./

# Installation des dépendances Python avec gestion d'erreur
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt || echo "⚠️ Erreur pip, continuation..."

# Installation des dépendances Node.js
RUN npm install --production

# Copie du code source
COPY . .

# Création des répertoires nécessaires
RUN mkdir -p baileys_auth config logs

# Exposition des ports
EXPOSE 5001 3001

# Script de démarrage
CMD ["npm", "start"] 