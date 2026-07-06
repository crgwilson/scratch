# Kubernetes: Helm

Helm is the package manager for Kubernetes. It allows you to define, install, and upgrade even the most complex Kubernetes applications. Helm Charts are packages of pre-configured Kubernetes resources.

## What is Helm?

Helm streamlines installing and managing Kubernetes applications. Think of it like `apt`, `yum`, or `brew` for Kubernetes.

*   **Helm Charts**: A Helm Chart is a collection of files that describe a related set of Kubernetes resources. A single chart might be used to deploy something simple, like a Memcached pod, or something complex, like a full web app stack with a database, frontend, and backend.
*   **Helm Releases**: When a chart is installed, Helm creates a "release." A release is a running instance of a chart in a Kubernetes cluster. You can have multiple releases of the same chart.
*   **Helm Repositories**: Charts are stored in Helm chart repositories, which are HTTP servers that house one or more packaged charts.

## Why Use Helm?

*   **Simplifies Deployment**: Packages complex applications into a single, easy-to-manage unit.
*   **Version Control**: Manages different versions of your application deployments.
*   **Rollbacks**: Easily revert to a previous application version in case of issues.
*   **Customization**: Allows you to customize deployments using `values.yaml` files.
*   **Dependency Management**: Handles dependencies between different Kubernetes components.

## Getting Started with Helm

### 1. Install Helm

You can install Helm using various methods. For Linux, a common way is via `snap` or by downloading the binary.

**Using Snap (Linux):**
```bash
sudo snap install helm --classic
```

**Using Homebrew (macOS/Linux):**
```bash
brew install helm
```

**Direct Download (Linux):**
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

Verify installation:
```bash
helm version
```

### 2. Add a Chart Repository

To install charts, you first need to add a repository. The `stable` repository (now deprecated) was a common one, but many projects now host their own. Let's add the Bitnami repository, which hosts many popular applications.

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update # Always update your repositories after adding a new one
```

### 3. Search for Charts

You can search for available charts in your added repositories:

```bash
helm search repo wordpress
```

### 4. Install a Chart

To install a chart, use the `helm install` command. You need to give your release a name.

```bash
helm install my-wordpress bitnami/wordpress
```

This will install WordPress into your Kubernetes cluster, creating all the necessary Deployments, Services, PersistentVolumeClaims, etc.

### 5. List Releases

To see all installed releases:

```bash
helm list
```

### 6. Get Release Status

To check the status of a specific release:

```bash
helm status my-wordpress
```

### 7. Upgrade a Release

If there's a new version of the chart or you want to change configuration values, you can upgrade a release.

First, update your local chart repositories:
```bash
helm repo update
```

Then, upgrade the release, optionally providing new values:
```bash
helm upgrade my-wordpress bitnami/wordpress --set service.type=LoadBalancer
```

### 8. Rollback a Release

If an upgrade goes wrong, you can easily rollback to a previous version:

```bash
helm history my-wordpress # Get the revision numbers
helm rollback my-wordpress 1 # Rollback to revision 1
```

### 9. Uninstall a Release

To remove a release and all its associated Kubernetes resources:

```bash
helm uninstall my-wordpress
```

## Common Helm Features

### 1. Chart Structure

A typical Helm chart directory structure looks like this:

```
mychart/
  Chart.yaml          # A YAML file containing information about the chart
  values.yaml         # The default configuration values for this chart
  charts/             # A directory containing any dependent charts
  templates/          # A directory of templates that will be rendered into Kubernetes manifest files
  templates/NOTES.txt # A plain text file containing short usage notes
```

### 2. `values.yaml`

This file defines the default configuration values for a chart. You can override these values during installation or upgrade using the `--set` flag or by providing your own `values.yaml` file with `-f`.

**Example `values.yaml`:**
```yaml
replicaCount: 1
image:
  repository: nginx
  tag: stable
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
```

**Overriding values:**
```bash
helm install my-nginx ./mychart --set replicaCount=3 --set service.type=LoadBalancer
helm install my-nginx ./mychart -f my-custom-values.yaml
```

### 3. Templates

The `templates/` directory contains Kubernetes manifest files written in Go template syntax. Helm's templating engine allows for dynamic generation of Kubernetes YAML based on the values provided.

**Example `templates/deployment.yaml` snippet:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "mychart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
```

### 4. Hooks

Helm provides a hook mechanism to allow chart developers to intervene at certain points in a release's life cycle. For example, you can use a `pre-install` hook to run a database migration job before the new application pods start.

### 5. Dependencies

Charts can declare dependencies on other charts. These dependencies are managed in the `Chart.yaml` file under the `dependencies` section. Helm will fetch and manage these dependent charts automatically.

```yaml
# Chart.yaml
apiVersion: v2
name: my-app
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.16.0"

dependencies:
- name: postgresql
  version: 12.x.x
  repository: https://charts.bitnami.com/bitnami
- name: redis
  version: 15.x.x
  repository: https://charts.bitnami.com/bitnami
```

Helm is a powerful tool that significantly simplifies the management of applications on Kubernetes. By understanding its core concepts and features, you can effectively deploy and operate complex systems.
