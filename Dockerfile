# Etapa 1: Build de la UI (Node.js + TypeScript para AGNO)
FROM node:20-alpine AS ui-build

WORKDIR /app/agent-ui
COPY agent-ui/package*.json ./
RUN npm install
COPY agent-ui/ ./
RUN npm run build

# Etapa 2: Agente de IA (Python)
FROM python:3.11-slim AS agent

WORKDIR /app/agent
COPY agent/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY agent/ ./

# Etapa 3: Imagen final combinada
FROM nginx:alpine

# Copia build de la UI (AGNO) a nginx
COPY --from=ui-build /app/agent-ui/dist /usr/share/nginx/html

# Copia el agente de IA al contenedor final
COPY --from=agent /app/agent /app/agent

# Script de arranque para ambos servicios
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]