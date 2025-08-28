# Multi-stage build for Flutter Web
FROM ghcr.io/cirruslabs/flutter:3.24.3 AS build

# Set working directory
WORKDIR /app

# Copy the entire Flutter project
COPY . .

# Get dependencies
RUN flutter pub get

# Build web app
RUN flutter build web --release

# Production stage - nginx
FROM nginx:alpine

# Copy built web app
COPY --from=build /app/build/web /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]