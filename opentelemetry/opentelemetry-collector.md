---
tags:
  - observability
  - opentelemetry
  - opentelemetry-collector
---
# OpenTelemetry Collector

The OpenTelemetry Collector is a vendor-agnostic proxy that can receive, process, and export telemetry data. It is a key component of an OpenTelemetry-based observability solution, providing a flexible and scalable way to manage telemetry data between your applications and various backends.

## What is the OpenTelemetry Collector?

The Collector is a standalone application that can be deployed as an agent or a gateway. It offers several key benefits:

* **Decoupling**: It decouples your application from the specific observability backend you are using. You can change backends without re-instrumenting your code.
* **Processing**: It can process data before exporting it, for example, by batching, filtering, sampling, or adding/modifying attributes.
* **Scalability**: It can be scaled independently of your application, allowing you to handle high volumes of telemetry data.
* **Vendor Agnostic**: It can receive data in multiple formats (OTLP, Jaeger, Prometheus) and export it to dozens of backends.

There are two main distributions of the Collector:
* **Core**: Contains the essential components for OTLP and basic exporters.
* **Contrib**: Includes all core components plus a wide range of additional receivers, processors, and exporters maintained by the community. It is the recommended distribution for most use cases.

## How to Configure the Collector

The Collector is configured using a single YAML file. The configuration has four main sections: `receivers`, `processors`, `exporters`, and `service`.

### Receivers
Receivers are how data gets into the Collector. They can be push-based (listening for data on an endpoint) or pull-based (scraping an endpoint).

* **OTLP Receiver**: The standard OpenTelemetry Protocol receiver.
* **Jaeger Receiver**: For receiving traces from Jaeger clients.
* **Prometheus Receiver**: For scraping Prometheus metrics endpoints.

### Processors
Processors are run on data between being received and being exported. They are used to modify, filter, or enrich the data.

* **Batch Processor**: Batches spans, metrics, or logs before exporting to reduce the number of outgoing requests. This is highly recommended.
* **Memory Limiter Processor**: Prevents the Collector from consuming too much memory.
* **Attributes Processor**: Adds, modifies, or deletes attributes from telemetry data.

### Exporters
Exporters are how data is sent from the Collector to one or more backends.

* **Logging Exporter**: Prints telemetry data to the console. Useful for debugging.
* **OTLP Exporter**: Sends data to another OTLP-compatible endpoint (like another Collector or a backend).
* **Prometheus Exporter**: Exports metrics to a Prometheus-compatible backend.
* **AWS X-Ray Exporter**: Sends traces to AWS X-Ray.

### Service Pipelines
The `service` section defines the pipelines that connect receivers, processors, and exporters. You can have separate pipelines for traces, metrics, and logs.

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging]
```

### Example Configuration
Here is a basic `config.yaml` for a Collector that receives OTLP data, batches it, and exports it to the console.

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    # Batches data before sending to reduce network traffic.
    send_batch_size: 1024
    timeout: 10s

exporters:
  logging:
    # Logs telemetry to the console for debugging.
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging]
```

## How to Deploy the Collector

The Collector can be deployed in various ways, most commonly using Docker or Kubernetes.

### Docker
You can run the Collector as a Docker container, mounting your `config.yaml` file.

```bash
docker run -p 4317:4317 -p 4318:4318 \
  -v $(pwd)/config.yaml:/etc/otelcol-contrib/config.yaml \
  otel/opentelemetry-collector-contrib:latest
```

### Kubernetes
In Kubernetes, the Collector is typically deployed as a `Deployment` or `DaemonSet`, with the configuration managed by a `ConfigMap`.

## Recommended Deployment Architectures

### Agent Collector
In this model, a Collector instance runs on the same host as the application (e.g., as a sidecar container in Kubernetes).

* **Pros**:
  * Offloads telemetry processing from the application.
  * Can enrich telemetry with host-level metadata.
  * Reduces the need for language-specific exporters in your application.
* **Configuration**: The agent is configured to receive data from the application (e.g., over localhost) and export it to a central gateway Collector.

### Gateway Collector
A gateway is a standalone, centrally managed deployment of one or more Collector instances. It receives telemetry from many agent collectors.

* **Pros**:
  * Centralizes telemetry processing, routing, and authentication.
  * Reduces the number of egress points from your network.
  * Can be scaled independently to handle high traffic loads.
* **Configuration**: The gateway is configured to receive data from many agents and export it to one or more backends.

### Tiered Architecture for High Volume
For very high-volume environments, a tiered architecture combining agents and gateways is the recommended approach.

1. **Application**: Your application sends telemetry to a local agent collector via OTLP over localhost.
2. **Agent Collector**: Runs as a sidecar. It performs minimal processing (like batching) and forwards data to the gateway.
3. **Gateway Collector**: A horizontally-scaled fleet of Collectors running as a central service. It receives data from all agents and performs more intensive processing (e.g., filtering, sampling, routing to multiple backends).

This architecture provides maximum scalability, reliability, and manageability.

## Scaling the Collector in Azure with OpenTofu

Here is a recommended architecture for a scalable OpenTelemetry Collector gateway in Azure using Azure Kubernetes Service (AKS).

### Architecture Overview

1. **Azure Kubernetes Service (AKS)**: A managed Kubernetes cluster to host the gateway collectors.
2. **Collector Deployment**: The Collector is deployed as a `Deployment` on AKS.
3. **Horizontal Pod Autoscaler (HPA)**: Automatically scales the number of Collector pods based on CPU or memory usage.
4. **Azure Load Balancer**: An internal or public load balancer is created via a Kubernetes `Service` of type `LoadBalancer` to distribute traffic evenly across the Collector pods.
5. **ConfigMap**: The Collector's `config.yaml` is stored in a Kubernetes `ConfigMap` and mounted into the pods.

### OpenTofu Example for Azure

This example provides conceptual OpenTofu code to provision a scalable Collector gateway on AKS.

```hcl
# main.tf

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.11"
    }
  }
}

variable "resource_group_name" {
  description = "The name of the Azure Resource Group."
  type        = string
  default     = "otel-collector-rg"
}

variable "location" {
  description = "The Azure region."
  type        = string
  default     = "East US"
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

# 1. Create an AKS cluster
resource "azurerm_kubernetes_cluster" "main" {
  name                = "otel-collector-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "otelcollector"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }
}

# 2. Kubernetes provider configuration
provider "kubernetes" {
  host                   = azurerm_kubernetes_cluster.main.kube_config.0.host
  client_certificate     = base64decode(azurerm_kubernetes_cluster.main.kube_config.0.client_certificate)
  client_key             = base64decode(azurerm_kubernetes_cluster.main.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.main.kube_config.0.cluster_ca_certificate)
}

# 3. Create a ConfigMap for the Collector configuration
resource "kubernetes_config_map" "otel_collector_config" {
  metadata {
    name      = "otel-collector-conf"
    namespace = "default"
  }

  data = {
    "config.yaml" = <<-"EOT"
      receivers:
        otlp:
          protocols:
            grpc:
              endpoint: 0.0.0.0:4317
      processors:
        batch: {}
        memory_limiter:
          check_interval: 1s
          limit_percentage: 75
          spike_limit_percentage: 15
      exporters:
        # Replace with your desired backend exporter, e.g., Azure Monitor
        logging:
          loglevel: info
      service:
        pipelines:
          traces:
            receivers: [otlp]
            processors: [batch, memory_limiter]
            exporters: [logging]
    EOT
  }
}

# 4. Deploy the Collector using a Deployment
resource "kubernetes_deployment" "otel_collector" {
  metadata {
    name      = "otel-collector"
    namespace = "default"
    labels = {
      app = "otel-collector"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "otel-collector"
      }
    }

    template {
      metadata {
        labels = {
          app = "otel-collector"
        }
      }

      spec {
        container {
          name  = "otel-collector"
          image = "otel/opentelemetry-collector-contrib:latest"

          command = ["--config=/conf/config.yaml"]

          port {
            container_port = 4317
            name             = "otlp-grpc"
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "200Mi"
            }
            limits = {
              cpu    = "500m"
              memory = "1Gi"
            }
          }

          volume_mount {
            name       = "otel-collector-config-volume"
            mount_path = "/conf"
          }
        }

        volume {
          name = "otel-collector-config-volume"
          config_map {
            name = kubernetes_config_map.otel_collector_config.metadata.0.name
          }
        }
      }
    }
  }
}

# 5. Expose the deployment with a LoadBalancer service
resource "kubernetes_service" "otel_collector_service" {
  metadata {
    name      = "otel-collector-service"
    namespace = "default"
  }
  spec {
    selector = {
      app = kubernetes_deployment.otel_collector.spec.0.template.0.metadata.0.labels.app
    }
    port {
      port        = 4317
      target_port = 4317
      protocol    = "TCP"
    }
    type = "LoadBalancer"
  }
}

# 6. Configure Horizontal Pod Autoscaler
resource "kubernetes_horizontal_pod_autoscaler" "otel_collector_hpa" {
  metadata {
    name      = "otel-collector-hpa"
    namespace = "default"
  }
  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.otel_collector.metadata.0.name
    }
    min_replicas = 2
    max_replicas = 10

    target_cpu_utilization_percentage = 80
  }
}
```
