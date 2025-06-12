#!/bin/sh
# Inicia el agent (ajusta si tu entrypoint es distinto a main.py)
python3 /app/agent/main.py &

# Inicia nginx en primer plano
nginx -g 'daemon off;'