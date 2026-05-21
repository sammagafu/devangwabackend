# Build from monorepo root:
#   docker build -f devangwabackend/Dockerfile -t devangwa-app .
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Build frontend
COPY devangwacoaching/package*.json ./devangwacoaching/
WORKDIR /app/devangwacoaching
RUN npm ci --omit=dev 2>/dev/null || npm install
COPY devangwacoaching/ ./
RUN npm run build

# Install backend
WORKDIR /app
COPY devangwabackend/requirements.txt ./devangwabackend/
RUN pip install --no-cache-dir -r devangwabackend/requirements.txt

COPY devangwabackend/ ./devangwabackend/

# Bundle SPA assets into Django
RUN mkdir -p /app/devangwabackend/templates /app/devangwabackend/static/assets
RUN cp /app/devangwacoaching/dist/index.html /app/devangwabackend/templates/
RUN cp -r /app/devangwacoaching/dist/assets/* /app/devangwabackend/static/assets/

COPY devangwabackend/nginx.conf /etc/nginx/sites-available/default
COPY devangwabackend/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=devangwa.settings

WORKDIR /app/devangwabackend

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD nginx -g "daemon off;" & exec gunicorn devangwa.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile -
