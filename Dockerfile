# ----------- Frontend Build Stage ------------
FROM node:20 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/ ./
RUN npm install && npm run build

# ----------- Final Stage ------------
FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y nginx supervisor && apt-get clean

# Copy backend
COPY backend/ /app/backend
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Nginx config
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080
EXPOSE 8000

CMD ["/usr/bin/supervisord"]

