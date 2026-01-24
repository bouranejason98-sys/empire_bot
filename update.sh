#!/bin/bash
echo "Updating Empire OS..."
docker-compose down
git pull origin main
docker-compose build --no-cache
docker-compose up -d
echo "Update complete."
