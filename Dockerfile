# Etapa 1: Build de la UI (Next.js)
FROM node:20-alpine AS build

WORKDIR /app

# Copiar solo archivos necesarios para instalar dependencias
COPY agent-ui/package*.json ./

# Instalar dependencias (incluyendo dev para el build)
RUN npm install

# Copiar el resto de la app
COPY agent-ui/ .

# Build de producción
RUN npm run build

# Eliminar devDependencies para producción
RUN npm prune --omit=dev

# Etapa 2: Imagen final mínima
FROM node:20-alpine AS production

WORKDIR /app

# Copiar solo lo necesario desde el build
COPY --from=build /app ./

# Copiar script de arranque si es necesario
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8080

# Comando de inicio
CMD ["/start.sh"]
