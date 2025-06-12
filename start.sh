#!/bin/bash

# Iniciar el agente Python en segundo plano
python3 /app/agent/playground.py &

# Iniciar el servidor Next.js en producción
cd /app/agent-ui
npm run start
