# Kubernetes: kubectl CLI

`kubectl` is the command-line tool for running commands against Kubernetes clusters. It allows you to run commands against Kubernetes clusters. You can use `kubectl` to deploy applications, inspect and manage cluster resources, and view logs.

## Basic Syntax

The basic syntax for `kubectl` commands is:

```bash
kubectl [command] [TYPE] [NAME] [flags]
```

*   `command`: Specifies the operation you want to perform (e.g., `get`, `describe`, `apply`, `delete`).
*   `TYPE`: Specifies the resource type (e.g., `pods`, `deployments`, `services`). You can use singular, plural, or abbreviated forms (e.g., `pod`, `pods`, `po`).
*   `NAME`: Specifies the name of the resource. If omitted, the command applies to all resources of that type.
*   `flags`: Optional flags to modify the command's behavior (e.g., `--namespace`, `-o yaml`).

## Important Subcommands

### 1. `get` - Display Resources

Used to list resources.

*   **List all pods in the current namespace:**
    ```bash
    kubectl get pods
    ```
*   **List all deployments in all namespaces:**
    ```bash
    kubectl get deployments --all-namespaces
    ```
*   **Get a specific service by name:**
    ```bash
    kubectl get service my-service
    ```
*   **Get a pod in YAML format:**
    ```bash
    kubectl get pod my-pod -o yaml
    ```
*   **Get wide output (more details):**
    ```bash
    kubectl get pods -o wide
    ```

### 2. `describe` - Show Detailed Information

Used to show detailed information about a specific resource or group of resources.

*   **Describe a specific pod:**
    ```bash
    kubectl describe pod my-pod
    ```
*   **Describe a deployment:**
    ```bash
    kubectl describe deployment my-deployment
    ```

### 3. `apply` - Apply a Configuration

Used to apply a configuration to a resource by filename or stdin. This is the primary way to create or update resources from manifest files.

*   **Apply a configuration from a file:**
    ```bash
    kubectl apply -f my-deployment.yaml
    ```
*   **Apply multiple configurations from a directory:**
    ```bash
    kubectl apply -f configs/
    ```

### 4. `delete` - Delete Resources

Used to delete resources by filename, stdin, resource type and name, or by labels.

*   **Delete a pod by name:**
    ```bash
    kubectl delete pod my-pod
    ```
*   **Delete a deployment defined in a file:**
    ```bash
    kubectl delete -f my-deployment.yaml
    ```
*   **Delete all pods with a specific label:**
    ```bash
    kubectl delete pods -l app=my-app
    ```

### 5. `logs` - Print Container Logs

Used to print the logs for a container in a pod.

*   **View logs of a pod:**
    ```bash
    kubectl logs my-pod
    ```
*   **View logs of a specific container in a multi-container pod:**
    ```bash
    kubectl logs my-pod -c my-container
    ```
*   **Follow logs in real-time:**
    ```bash
    kubectl logs -f my-pod
    ```
*   **View logs from the last 5 minutes:**
    ```bash
    kubectl logs my-pod --since=5m
    ```

### 6. `exec` - Execute a Command in a Container

Used to execute a command in a container.

*   **Execute a shell inside a pod:**
    ```bash
    kubectl exec -it my-pod -- /bin/bash
    ```
*   **Run a command in a specific container:**
    ```bash
    kubectl exec my-pod -c my-container -- ls -l /app
    ```

### 7. `port-forward` - Forward One or More Local Ports to a Pod

Used to forward one or more local ports to a pod. Useful for accessing services running inside a cluster from your local machine.

*   **Forward local port 8080 to pod's port 80:**
    ```bash
    kubectl port-forward my-pod 8080:80
    ```

### 8. `top` - Display Resource (CPU/Memory) Usage

Used to display resource (CPU/memory) usage for nodes or pods. Requires Metrics Server to be installed in the cluster.

*   **Show node resource usage:**
    ```bash
    kubectl top nodes
    ```
*   **Show pod resource usage:**
    ```bash
    kubectl top pods
    ```

### 9. `config` - Manage kubeconfig File

Used to manage the `kubeconfig` file, which stores cluster connection information.

*   **View current context:**
    ```bash
    kubectl config current-context
    ```
*   **List all contexts:**
    ```bash
    kubectl config get-contexts
    ```
*   **Switch context:**
    ```bash
    kubectl config use-context my-cluster-context
    ```

### 10. `edit` - Edit a Resource

Used to edit a resource in your default editor.

*   **Edit a deployment:**
    ```bash
    kubectl edit deployment my-deployment
    ```

### 11. `rollout` - Manage Rollouts

Used to manage the rollout of a resource (e.g., deployment).

*   **Check rollout status:**
    ```bash
    kubectl rollout status deployment/my-deployment
    ```
*   **Undo a rollout:**
    ```bash
    kubectl rollout undo deployment/my-deployment
    ```

### 12. `cp` - Copy Files to/from Containers

Used to copy files and directories to and from containers.

*   **Copy a file from local to pod:**
    ```bash
    kubectl cp my-local-file.txt my-pod:/path/in/container/
    ```
*   **Copy a file from pod to local:**
    ```bash
    kubectl cp my-pod:/path/in/container/my-file.txt my-local-directory/
    ```

## Common Flags

*   `-n`, `--namespace`: Specify the namespace.
*   `-o`, `--output`: Output format (e.g., `yaml`, `json`, `wide`).
*   `-l`, `--selector`: Select resources by label.
*   `-f`, `--filename`: Filename, directory, or URL to files to use to create or update the resource.
*   `--all-namespaces`: If present, list the requested object(s) across all namespaces.

This covers the most commonly used `kubectl` commands. For a comprehensive list and more details, refer to the official Kubernetes documentation.
