# Kubernetes

Notes on anything k8s related

## Introduction to Kubernetes

Kubernetes (K8s) is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. It groups containers that make up an application into logical units for easy management and discovery. Kubernetes provides a framework to run distributed systems resiliently, handling failover, scaling, and deployment patterns.

## Architecture and Components

A Kubernetes cluster consists of a set of worker machines, called Nodes, that run containerized applications. Every cluster has at least one worker node. The worker node(s) host the Pods that are the components of the application workload.

The Control Plane manages the worker nodes and the Pods in the cluster. In production environments, the control plane usually runs across multiple computers and a cluster usually runs multiple nodes, providing fault-tolerance and high availability.

### Control Plane Components

*   **kube-apiserver**: The API server is a component of the Kubernetes control plane that exposes the Kubernetes API. It is the front end for the Kubernetes control plane.
*   **etcd**: Consistent and highly-available key value store used as Kubernetes' backing store for all cluster data.
*   **kube-scheduler**: Watches for newly created Pods with no assigned node, and selects a node for them to run on.
*   **kube-controller-manager**: Runs controller processes. These controllers include:
    *   Node Controller: Responsible for noticing and responding when nodes go down.
    *   Replication Controller: Responsible for maintaining the correct number of pods for every replication controller object.
    *   Endpoints Controller: Populates the Endpoints object (i.e., joins Services & Pods).
    *   Service Account & Token Controllers: Create default Service Accounts and API access tokens for new Namespaces.
*   **cloud-controller-manager**: Runs controllers that interact with the underlying cloud providers. This component is only present in clusters deployed on cloud infrastructure.

### Node Components

*   **kubelet**: An agent that runs on each node in the cluster. It ensures that containers are running in a Pod.
*   **kube-proxy**: A network proxy that runs on each node in the cluster, implementing part of the Kubernetes Service concept. It maintains network rules on nodes, allowing network communication to your Pods from network sessions inside or outside of the cluster.
*   **Container Runtime**: The software that is responsible for running containers. Kubernetes supports container runtimes such as Docker, containerd, and CRI-O.

## Scaling Considerations

Scaling in Kubernetes can be approached in several ways:

*   **Horizontal Pod Autoscaler (HPA)**: Automatically scales the number of pods in a replication controller, deployment, replica set, or stateful set based on observed CPU utilization or other select metrics.
*   **Vertical Pod Autoscaler (VPA)**: Automatically adjusts the CPU and memory requests and limits for containers in a Pod based on their historical usage.
*   **Cluster Autoscaler**: Automatically adjusts the size of the Kubernetes cluster when there are insufficient resources to run all pending pods, or when nodes are underutilized and can be safely terminated.
*   **Manual Scaling**: Directly changing the number of replicas for a deployment or replica set using `kubectl scale`.

Considerations for scaling:

*   **Resource Limits and Requests**: Properly define CPU and memory requests and limits for your containers to ensure efficient resource allocation and prevent resource starvation.
*   **Pod Disruption Budgets (PDBs)**: Specify the minimum number or percentage of replicas that must be available during a voluntary disruption (e.g., node maintenance) to ensure application availability.
*   **Node Affinity and Anti-affinity**: Control which nodes your pods are scheduled on based on labels, allowing for better resource utilization and high availability.
*   **Taints and Tolerations**: Prevent pods from being scheduled on specific nodes (taints) and allow pods to be scheduled on those nodes (tolerations), useful for dedicated nodes or handling node failures.
*   **Storage**: Ensure your storage solution can scale with your application and handle increased I/O demands.
*   **Networking**: Design your network to handle increased traffic and ensure proper communication between services and pods.

## Index

*   [Installation](installation.md)
*   [kubectl CLI](kubectl.md)
*   [Application Deployment Concepts](Application-Deployment.md)
*   [Authentication and Authorization](Authentication-Authorization.md)
*   [Helm](Helm.md)
*   [Autoscaling](Autoscaling.md)
*   [Custom Metrics](Custom-Metrics.md)
*   [Storage](Storage.md)
