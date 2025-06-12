# Etapa 1: Build de la UI (Next.js)
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

# Etapa 3: Imagen final combinada basada en Ubuntu
FROM ubuntu:22.04

# Instalar Node, Python y pip
RUN apt-get update && \
    apt-get install -y curl python3 python3-pip && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

# Copiar frontend y backend al contenedor final
COPY --from=ui-build /app/agent-ui /app/agent-ui
COPY --from=agent /app/agent /app/agent

# Instalar dependencias Python
RUN pip3 install --no-cache-dir -r /app/agent/requirements.txt

# Instalar dependencias Node (solo producción)
WORKDIR /app/agent-ui
RUN npm install --omit=dev

# Copiar script de arranque
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 3000

CMD ["/start.sh"]
