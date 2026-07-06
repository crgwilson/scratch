# Kubernetes: Custom Metrics for Autoscaling

While the Horizontal Pod Autoscaler (HPA) can scale based on standard resource metrics like CPU and memory utilization, many applications require scaling based on more specific, application-level metrics. This is where **Custom Metrics** come into play.

## What are Custom Metrics?

Custom metrics are application-specific metrics that are not directly provided by Kubernetes' core metrics API (like CPU or memory). These could be:

*   **Requests per second (RPS)** for a web server.
*   **Queue length** for a message processing application.
*   **Number of active connections** for a database.
*   **Latency** of an API endpoint.

Kubernetes allows HPA to consume these custom metrics through the **Custom Metrics API**.

## How Custom Metrics are Exposed

To use custom metrics with HPA, you need a component in your cluster that can:
1.  Collect these application-specific metrics (e.g., from Prometheus, application logs, or directly from the application).
2.  Expose them via the Kubernetes Custom Metrics API.

A common way to achieve this is by deploying a **Custom Metrics Adapter**.

### Common Custom Metrics Adapter: Prometheus Adapter

The Prometheus Adapter is a popular choice for exposing metrics from Prometheus to the Kubernetes Custom Metrics API.

**How it works:**
1.  Your applications expose metrics in a Prometheus-compatible format (e.g., `/metrics` endpoint).
2.  Prometheus scrapes these metrics from your applications.
3.  The Prometheus Adapter queries Prometheus for specific metrics.
4.  The Prometheus Adapter then exposes these metrics via the Kubernetes Custom Metrics API, making them available for HPA.

## Using Custom Metrics with HPA

Once a custom metrics adapter is configured and exposing metrics, you can define an HPA that targets these metrics.

### HPA Configuration Example with Custom Metrics

This HPA scales a deployment based on the `http_requests_per_second` metric.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-web-app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-web-app-deployment
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Pods # Or Object, External depending on the metric source
    pods:
      metric:
        name: http_requests_per_second # The name of the custom metric
      target:
        type: AverageValue # Or Value
        averageValue: 10k # Target average value per pod
```

**Explanation of `metrics.type`:**

*   **`Pods`**: Scales based on the average value of a metric across all pods in the target. The HPA controller calculates the sum of the metric values for all pods and divides by the number of pods to get an average.
    *   **`target.type: AverageValue`**: The HPA will try to maintain the average value of the metric across all pods at the specified `averageValue`.
*   **`Object`**: Scales based on a metric associated with a single Kubernetes object (e.g., a Service, Ingress, or the Deployment itself).
    *   **`target.type: Value`**: The HPA will try to maintain the value of the metric for the specified object at the `value`.
*   **`External`**: Scales based on metrics coming from outside the Kubernetes cluster, not directly related to any Kubernetes object (e.g., a queue length in an external message broker).
    *   **`target.type: Value`**: The HPA will try to maintain the value of the external metric at the `value`.

### Example Scenario: Scaling based on Queue Length

Imagine you have a worker application that processes messages from a Kafka queue. You want to scale the number of worker pods based on the number of messages in the queue.

1.  **Metric Collection**: A component (e.g., a custom exporter or the Prometheus JMX exporter) collects the Kafka queue length and exposes it to Prometheus.
2.  **Prometheus Adapter**: The Prometheus Adapter is configured to expose this `kafka_queue_length` metric via the Custom Metrics API.
3.  **HPA Definition**:
    ```yaml
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: kafka-worker-hpa
      namespace: default
spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: kafka-worker-deployment
      minReplicas: 1
      maxReplicas: 5
      metrics:
      - type: Object # The metric is associated with a specific object (e.g., the Kafka topic)
        object:
          metric:
            name: kafka_queue_length
          describedObject:
            apiVersion: kafka.strimzi.io/v1beta2 # Example for a Kafka topic object
            kind: KafkaTopic
            name: my-topic
          target:
            type: Value
            value: 100 # Target 100 messages in the queue
    ```

Using custom metrics provides immense flexibility in defining autoscaling policies that are precisely tailored to your application's behavior and business logic.
