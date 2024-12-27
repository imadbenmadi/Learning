
### **What is Docker?**
Docker is a containerization platform. It packages your app and its dependencies into containers to ensure consistent environments across development, testing, and production.

---

### **Key Concepts**
1. **Image**: A blueprint of your application (OS + dependencies + your app).
2. **Container**: A running instance of an image.
3. **Dockerfile**: A script to build Docker images.
4. **Docker Compose**: A tool to manage multi-container applications.

---

### **Install Docker**
1. Download Docker Desktop from [docker.com](https://www.docker.com/).
2. Install and verify:
   ```bash
   docker --version
   ```

---

### **Dockerize Your Node.js App**
#### **1. Create a `Dockerfile`:**
```dockerfile
# Use a base Node.js image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app files
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Define the command to run the app
CMD ["npm", "start"]
```

#### **2. Build and Run:**
```bash
docker build -t my-node-app .
docker run -p 3000:3000 my-node-app
```
Visit: `http://localhost:3000`

---

### **Dockerize Your React App**
#### **1. Create a `Dockerfile`:**
```dockerfile
# Use a base Node.js image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app files
COPY . .

# Build the app for production
RUN npm run build

# Use an Nginx image to serve the app
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

# Expose the port
EXPOSE 80
```

#### **2. Build and Run:**
```bash
docker build -t my-react-app .
docker run -p 8080:80 my-react-app
```
Visit: `http://localhost:8080`

---

### **Using Docker Compose**
For running both React and Node.js together:
#### **Create a `docker-compose.yml` file:**
```yaml
version: '3.8'
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - ./backend:/app
    command: npm start

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    volumes:
      - ./frontend:/app
    stdin_open: true
```

#### **Run the services:**
```bash
docker-compose up
```

---

### **Useful Commands**
1. **Check running containers**: 
   ```bash
   docker ps
   ```
2. **Stop a container**: 
   ```bash
   docker stop <container-id>
   ```
3. **Remove all stopped containers**: 
   ```bash
   docker system prune
   ```
4. **Logs from a container**: 
   ```bash
   docker logs <container-id>
   ```

---

### **Tips for Your Projects**
1. **Use `.dockerignore`:** To prevent copying unnecessary files (e.g., `node_modules`).
   ```plaintext
   node_modules
   .env
   ```
2. **Environment Variables:** Use Docker Compose or pass them during `docker run`.
   ```yaml
   environment:
     - NODE_ENV=production
   ```
3. **Volumes:** Sync files between your local machine and the container for development.

