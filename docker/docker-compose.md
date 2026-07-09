---
tags:
  - containers
  - docker
  - docker-compose
---
# Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. It uses a YAML file to configure the application's services, networks, and volumes. This allows you to manage your entire application stack with a single command.

## Common Docker Compose Commands

### 1. `docker-compose up` - Create and start containers

Builds, (re)creates, starts, and attaches to containers for a service.

* **Start containers in the background:**
  ```bash
  docker-compose up -d
  ```
* **Build images before starting containers:**
  ```bash
  docker-compose up --build
  ```
* **Force recreate containers even if their configuration and image haven't changed:**
  ```bash
  docker-compose up --force-recreate
  ```

### 2. `docker-compose down` - Stop and remove containers

Stops containers and removes containers, networks, volumes, and images created by `up`.

* **Stop and remove containers:**
  ```bash
  docker-compose down
  ```
* **Remove volumes along with containers:**
  ```bash
  docker-compose down -v
  ```

### 3. `docker-compose ps` - List containers

Lists containers for the services in the current project.

* **List all containers:**
  ```bash
  docker-compose ps
  ```

### 4. `docker-compose logs` - View output from containers

Displays log output from services.

* **View logs for all services:**
  ```bash
  docker-compose logs
  ```
* **Follow logs in real-time:**
  ```bash
  docker-compose logs -f
  ```
* **View logs for a specific service:**
  ```bash
  docker-compose logs -f my-service
  ```

### 5. `docker-compose exec` - Execute a command in a running container

Runs a one-off command in a service.

* **Execute a bash shell in the `web` service container:**
  ```bash
  docker-compose exec web bash
  ```

### 6. `docker-compose build` - Build or rebuild services

Builds or rebuilds services.

* **Build all services:**
  ```bash
  docker-compose build
  ```
* **Build a specific service:**
  ```bash
  docker-compose build my-service
  ```

## Simple Example: Single Service

This example runs a single Nginx container.

**`docker-compose.yml`:**
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

To run this, save the content in a `docker-compose.yml` file and run `docker-compose up`. You can then access the Nginx welcome page at `http://localhost:8080`.

## Complex Example: Multi-Service Application

This example demonstrates a more realistic setup with a reverse proxy (Nginx), a web application (a simple Node.js app), and a database (PostgreSQL).

### Project Structure

```
.
├── docker-compose.yml
├── nginx/
│   └── Dockerfile
└── web/
    ├── Dockerfile
    └── index.js
```

### `docker-compose.yml`

```yaml
version: '3.8'

services:
  proxy:
    build: ./nginx
    ports:
      - "80:80"
    depends_on:
      - web

  web:
    build: ./web
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/mydatabase
    depends_on:
      - db

  db:
    image: postgres:13-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydatabase
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### `nginx/Dockerfile`

```dockerfile
FROM nginx:alpine

COPY default.conf /etc/nginx/conf.d/default.conf
```

### `nginx/default.conf`

Create a file named `default.conf` inside the `nginx` directory.

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://web:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### `web/Dockerfile`

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "index.js"]
```

### `web/index.js`

```javascript
const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = 3000;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

app.get('/', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT NOW()');
    res.send(`Hello from the web application! The current time from the database is: ${rows[0].now}`);
  } catch (err) {
    console.error(err);
    res.status(500).send('Error connecting to the database');
  }
});

app.listen(port, () => {
  console.log(`Web application listening at http://localhost:${port}`);
});
```

### `web/package.json`

```json
{
  "name": "web",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.17.1",
    "pg": "^8.7.1"
  }
}
```

To run this setup, you would need to create the directory structure and files as shown above. Then, from the root directory containing the `docker-compose.yml`, run `docker-compose up`. This will build the images for the `proxy` and `web` services and start all three services. You can then access the application at `http://localhost`.
