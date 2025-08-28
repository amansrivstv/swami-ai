# Multi-stage build for Flutter Web
FROM ghcr.io/cirruslabs/flutter:3.24.3 AS build

# Set working directory
WORKDIR /app

# Copy the entire Flutter project
COPY . .

# Get dependencies
RUN flutter pub get

# Build web app with environment variables
ARG BACKEND_URL=http://localhost:8000
ARG BACKEND_WS_URL=ws://localhost:8000
RUN flutter build web --release \
    --dart-define=BACKEND_URL=$BACKEND_URL \
    --dart-define=BACKEND_WS_URL=$BACKEND_WS_URL

# Production stage - nginx
FROM nginx:alpine

# Copy built web app
COPY --from=build /app/build/web /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create a proper entrypoint script for runtime configuration
RUN echo '#!/bin/sh' > /docker-entrypoint.sh && \
    echo 'set -e' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '# Function to update URLs in the HTML file' >> /docker-entrypoint.sh && \
    echo 'update_urls() {' >> /docker-entrypoint.sh && \
    echo '  local backend_url="$1"' >> /docker-entrypoint.sh && \
    echo '  local backend_ws_url="$2"' >> /docker-entrypoint.sh && \
    echo '  local html_file="/usr/share/nginx/html/index.html"' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '  if [ -n "$backend_url" ] && [ "$backend_url" != "http://localhost:8000" ]; then' >> /docker-entrypoint.sh && \
    echo '    echo "Updating backend URL to: $backend_url"' >> /docker-entrypoint.sh && \
    echo '    # Add script tag with backend URL if not exists' >> /docker-entrypoint.sh && \
    echo '    if ! grep -q "data-backend-url" "$html_file"; then' >> /docker-entrypoint.sh && \
    echo '      sed -i "s|<head>|<head>\\n    <script data-backend-url=\"$backend_url\"></script>|" "$html_file"' >> /docker-entrypoint.sh && \
    echo '    else' >> /docker-entrypoint.sh && \
    echo '      sed -i "s|data-backend-url=\"[^\"]*\"|data-backend-url=\"$backend_url\"|" "$html_file"' >> /docker-entrypoint.sh && \
    echo '    fi' >> /docker-entrypoint.sh && \
    echo '  fi' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '  if [ -n "$backend_ws_url" ] && [ "$backend_ws_url" != "ws://localhost:8000" ]; then' >> /docker-entrypoint.sh && \
    echo '    echo "Updating backend WebSocket URL to: $backend_ws_url"' >> /docker-entrypoint.sh && \
    echo '    # Add script tag with backend WebSocket URL if not exists' >> /docker-entrypoint.sh && \
    echo '    if ! grep -q "data-backend-ws-url" "$html_file"; then' >> /docker-entrypoint.sh && \
    echo '      sed -i "s|<head>|<head>\\n    <script data-backend-ws-url=\"$backend_ws_url\"></script>|" "$html_file"' >> /docker-entrypoint.sh && \
    echo '    else' >> /docker-entrypoint.sh && \
    echo '      sed -i "s|data-backend-ws-url=\"[^\"]*\"|data-backend-ws-url=\"$backend_ws_url\"|" "$html_file"' >> /docker-entrypoint.sh && \
    echo '    fi' >> /docker-entrypoint.sh && \
    echo '  fi' >> /docker-entrypoint.sh && \
    echo '}' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '# Update URLs if environment variables are set' >> /docker-entrypoint.sh && \
    echo 'update_urls "$BACKEND_URL" "$BACKEND_WS_URL"' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '# Start nginx' >> /docker-entrypoint.sh && \
    echo 'exec nginx -g "daemon off;"' >> /docker-entrypoint.sh && \
    chmod +x /docker-entrypoint.sh

# Expose port
EXPOSE 80

# Start with custom entrypoint
CMD ["/docker-entrypoint.sh"]