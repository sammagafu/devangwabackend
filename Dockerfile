# Use Python 3.11 slim as base
FROM python:3.11-slim

# Install Node.js and Nginx
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy frontend and build it
COPY devangwacoaching/ ./devangwacoaching/
WORKDIR /app/devangwacoaching
RUN npm install
RUN npm run build

# Copy backend
WORKDIR /app
COPY devangwabackend/ ./devangwabackend/

# Install Python dependencies
WORKDIR /app/devangwabackend
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend to backend
RUN mkdir -p /app/devangwabackend/templates
RUN cp /app/devangwacoaching/dist/index.html /app/devangwabackend/templates/
RUN mkdir -p /app/devangwabackend/static/assets
RUN cp -r /app/devangwacoaching/dist/assets/* /app/devangwabackend/static/assets/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=devangwa.settings

# Run migrations and collect static
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Copy Nginx config
COPY nginx.conf /etc/nginx/sites-available/default

# Expose port
EXPOSE 80

# Start Nginx and Django
CMD service nginx start && gunicorn --bind 127.0.0.1:8000 devangwa.wsgi:application