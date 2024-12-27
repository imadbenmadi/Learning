# Stage 1: Build the React app
FROM node:18-alpine AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the app for production
RUN npm run build

# Stage 2: Serve the built React app
FROM nginx:stable-alpine

# Copy the build output from the previous stage to the nginx directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose the port that nginx runs on
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
