#!/bin/bash

echo "🧹 Nettoyage des images Docker existantes..."
docker system prune -f

echo "🏗️  Reconstruction de l'image LUMA-SUPREME..."
docker build -t luma-supreme .

echo "✅ Build terminé !"
echo "🚀 Pour lancer le conteneur :"
echo "docker run -p 5001:5001 -p 3001:3001 luma-supreme" 