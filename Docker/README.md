# Docker

Docker is a platform that enables developers to build, share, and run applications using containers. Containers are lightweight, portable, self-sufficient units that encapsulate an application and its dependencies, ensuring it runs consistently across different environments.

## Common Docker Commands

### 1. `docker run` - Run a container

Used to run a command in a new container.

*   **Run a simple Nginx container, mapping port 8080 on host to 80 in container:**
    ```bash
    docker run -p 8080:80 nginx
    ```
*   **Run a container in detached mode (background):**
    ```bash
    docker run -d -p 8080:80 nginx
    ```
*   **Run a container and remove it when it exits:**
    ```bash
    docker run --rm -it ubuntu bash
    ```
*   **Run a container with a specific name:**
    ```bash
    docker run --name my-nginx -p 8080:80 nginx
    ```

### 2. `docker ps` - List containers

Used to list running containers.

*   **List all running containers:**
    ```bash
    docker ps
    ```
*   **List all containers (including stopped ones):**
    ```bash
    docker ps -a
    ```
*   **List only container IDs:**
    ```bash
    docker ps -aq
    ```

### 3. `docker stop` / `docker start` / `docker restart` - Control containers

Used to stop, start, or restart one or more running containers.

*   **Stop a container by name or ID:**
    ```bash
    docker stop my-nginx
    ```
*   **Start a stopped container:**
    ```bash
    docker start my-nginx
    ```
*   **Restart a container:**
    ```bash
    docker restart my-nginx
    ```

### 4. `docker rm` - Remove containers

Used to remove one or more containers.

*   **Remove a container:**
    ```bash
    docker rm my-nginx
    ```
*   **Force remove a running container:**
    ```bash
    docker rm -f my-nginx
    ```

### 5. `docker images` - List images

Used to list Docker images.

*   **List all images:**
    ```bash
    docker images
    ```
*   **List dangling images (untagged images that are no longer used by any container):**
    ```bash
    docker images -f "dangling=true"
    ```

### 6. `docker rmi` - Remove images

Used to remove one or more images.

*   **Remove an image:**
    ```bash
    docker rmi nginx:latest
    ```
*   **Force remove an image:**
    ```bash
    docker rmi -f my-image:latest
    ```

### 7. `docker exec` - Execute a command in a running container

Used to run a command in a running container.

*   **Execute a bash shell inside a running container:**
    ```bash
    docker exec -it my-nginx bash
    ```
*   **Run a command and exit:**
    ```bash
    docker exec my-nginx ls -l /usr/share/nginx/html
    ```

### 8. `docker logs` - Fetch the logs of a container

Used to fetch the logs of a container.

*   **View logs of a container:**
    ```bash
    docker logs my-nginx
    ```
*   **Follow logs in real-time:**
    ```bash
    docker logs -f my-nginx
    ```

### 9. `docker build` - Build an image from a Dockerfile

Used to build an image from a Dockerfile.

*   **Build an image from the current directory:**
    ```bash
    docker build -t my-app:1.0 .
    ```
*   **Build an image from a specific Dockerfile:**
    ```bash
    docker build -f Dockerfile.dev -t my-app:dev .
    ```

### 10. `docker push` - Push an image to a registry

Used to push an image or a repository to a registry.

*   **Push an image to Docker Hub (after logging in):**
    ```bash
    docker push my-username/my-app:1.0
    ```

### 11. `docker pull` - Pull an image or a repository from a registry

Used to pull an image or a repository from a registry.

*   **Pull an image:**
    ```bash
    docker pull ubuntu:latest
    ```

## Building Docker Images

Docker images are built from a `Dockerfile`, which is a text file that contains all the commands a user could call on the command line to assemble an image.

### Simple Example: Nginx Static Site

This example demonstrates building a Docker image for a simple static website served by Nginx.

**`Dockerfile` for a simple static site:**
```dockerfile
# Use an official Nginx image as a base
FROM nginx:alpine

# Copy the static content into the Nginx web directory
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80 (Nginx default)
EXPOSE 80

# Nginx will run as the default command
CMD ["nginx", "-g", "daemon off;"]
```

**`index.html` content:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Simple Web App</title>
</head>
<body>
    <h1>Hello from Docker!</h1>
    <p>This is a simple static website.</p>
</body>
</html>
```

**Build and Run (assuming `Dockerfile` and `index.html` are in the current directory):**
```bash
docker build -t my-static-site:1.0 .
docker run -p 8080:80 my-static-site:1.0
```
Now, open your browser to `http://localhost:8080` to see the page.

### Complex Example: Multi-Stage Build (Go Application)

Multi-stage builds are useful for creating smaller, more secure images by separating the build environment from the runtime environment. This example builds a simple Go application.

**`Dockerfile` for a multi-stage Go application:**
```dockerfile
# Stage 1: Builder
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copy go.mod and go.sum to download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the application source code
COPY . .

# Build the Go application
RUN CGO_ENABLED=0 GOOS=linux go build -o /go-app

# Stage 2: Runner
FROM alpine:latest

# Install ca-certificates for HTTPS connections (if needed)
RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Copy the compiled binary from the builder stage
COPY --from=builder /go-app .

# Expose the port the application listens on
EXPOSE 8080

# Run the application
CMD ["./go-app"]
```

**`main.go` content:**
```go
package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello from Go application in Docker!")
	})

	log.Println("Server starting on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

**Build and Run (assuming `Dockerfile` and `main.go` are in the current directory):**
```bash
docker build -t my-go-app:1.0 .
docker run -p 8080:8080 my-go-app:1.0
```
Now, open your browser to `http://localhost:8080` to see the Go application's output.

## Publishing Docker Images

Once you've built an image, you can publish it to a Docker registry (like Docker Hub, Google Container Registry, AWS ECR, etc.) to share it with others or deploy it to production environments.

### 1. Tag the Image

Before pushing, you need to tag your image with the registry's address and your repository name.

```bash
docker tag my-go-app:1.0 your-dockerhub-username/my-go-app:1.0
# Or for a private registry:
# docker tag my-go-app:1.0 my-private-registry.com/my-go-app:1.0
```

### 2. Log in to the Registry

You need to authenticate with the Docker registry.

```bash
docker login # For Docker Hub
# docker login my-private-registry.com # For a private registry
```

### 3. Push the Image

After tagging and logging in, you can push the image.

```bash
docker push your-dockerhub-username/my-go-app:1.0
# docker push my-private-registry.com/my-go-app:1.0
```

This will upload your image to the specified registry, making it available for others to pull and use.