# Kubernetes: Authentication and Authorization

Kubernetes provides robust mechanisms for authenticating users and authorizing their actions within the cluster. This is primarily managed through a combination of authentication methods, Role-Based Access Control (RBAC), and Service Accounts.

## Authentication

Kubernetes does not have objects for "users" directly. Instead, it relies on external authentication mechanisms to verify the identity of a user or process trying to access the API server. Once authenticated, Kubernetes identifies users by their username (e.g., `jane.doe@example.com`) and group memberships.

Common authentication methods include:

*   **Client Certificates**: X509 client certificates signed by the cluster's Certificate Authority (CA).
*   **Bearer Tokens**:
    *   **Service Account Tokens**: Used by Pods to authenticate to the API server.
    *   **OpenID Connect (OIDC) Tokens**: Integration with external identity providers like Google, Okta, Auth0.
    *   **Webhook Token Authentication**: An external service verifies tokens.
*   **Authentication Proxy**: An external proxy that authenticates requests before forwarding them to the Kubernetes API server.

## Authorization (RBAC)

Role-Based Access Control (RBAC) is the primary mechanism for authorizing users and processes to perform actions on Kubernetes resources. RBAC uses `Roles` and `RoleBindings` (or `ClusterRoles` and `ClusterRoleBindings`) to define permissions.

### 1. Roles and ClusterRoles

*   **Role**: Defines permissions within a specific `namespace`.
    *   **Use Case**: Granting permissions to manage resources within a single project or team's namespace.
    *   **Example**:
        ```yaml
        apiVersion: rbac.authorization.k8s.io/v1
        kind: Role
        metadata:
          namespace: default
          name: pod-reader
        rules:
        - apiGroups: [""] # "" indicates the core API group
          resources: ["pods"]
          verbs: ["get", "watch", "list"]
        ```

*   **ClusterRole**: Defines permissions across the entire cluster (non-namespaced) or for namespaced resources across all namespaces.
    *   **Use Case**: Granting permissions for cluster-wide resources (e.g., nodes, persistent volumes) or for operations that span multiple namespaces (e.g., listing all pods in the cluster).
    *   **Example**:
        ```yaml
        apiVersion: rbac.authorization.k8s.io/v1
        kind: ClusterRole
        metadata:
          name: node-reader
        rules:
        - apiGroups: [""]
          resources: ["nodes"]
          verbs: ["get", "watch", "list"]
        ```

### 2. RoleBindings and ClusterRoleBindings

*   **RoleBinding**: Grants the permissions defined in a `Role` (or `ClusterRole`) to a user, group, or Service Account within a specific `namespace`.
    *   **Use Case**: Connecting a `Role` to a subject (user/group/service account) in a particular namespace.
    *   **Example**:
        ```yaml
        apiVersion: rbac.authorization.k8s.io/v1
        kind: RoleBinding
        metadata:
          name: read-pods-in-default
          namespace: default
        subjects:
        - kind: User
          name: jane.doe@example.com # Name is case sensitive
          apiGroup: rbac.authorization.k8s.io
        roleRef:
          kind: Role # This must be Role or ClusterRole
          name: pod-reader # This must match the name of the Role or ClusterRole you wish to bind to
          apiGroup: rbac.authorization.k8s.io
        ```

*   **ClusterRoleBinding**: Grants the permissions defined in a `ClusterRole` to a user, group, or Service Account across the entire cluster.
    *   **Use Case**: Connecting a `ClusterRole` to a subject for cluster-wide permissions.
    *   **Example**:
        ```yaml
        apiVersion: rbac.authorization.k8s.io/v1
        kind: ClusterRoleBinding
        metadata:
          name: read-nodes-cluster-wide
        subjects:
        - kind: Group
          name: ops-team # Name is case sensitive
          apiGroup: rbac.authorization.k8s.io
        roleRef:
          kind: ClusterRole # This must be ClusterRole
          name: node-reader
          apiGroup: rbac.authorization.k8s.io
        ```

## Service Accounts

While users and groups are for human users, **Service Accounts** are for processes that run in Pods.

*   **Definition**: A Kubernetes object that provides an identity for processes that run in a Pod. Each Service Account has an associated Secret that contains a token, which Pods can use to authenticate to the Kubernetes API server.
*   **Use Case**:
    *   Granting specific permissions to applications running inside Pods.
    *   Allowing applications to interact with the Kubernetes API (e.g., a controller that lists Pods).
*   **Default Service Account**: Every namespace has a default Service Account named `default`. Pods that do not explicitly specify a Service Account will use this one. It's generally recommended to create specific Service Accounts for applications with the least necessary privileges.
*   **Example**:
    1.  **Create a Service Account**:
        ```yaml
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          namespace: default
          name: my-app-sa
        ```
    2.  **Create a RoleBinding to grant permissions to the Service Account**:
        ```yaml
        apiVersion: rbac.authorization.k8s.io/v1
        kind: RoleBinding
        metadata:
          name: my-app-sa-reader
          namespace: default
        subjects:
        - kind: ServiceAccount
          name: my-app-sa
          namespace: default
        roleRef:
          kind: Role
          name: pod-reader # Assuming 'pod-reader' Role exists
          apiGroup: rbac.authorization.k8s.io
        ```
    3.  **Assign the Service Account to a Pod/Deployment**:
        ```yaml
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: my-app-deployment
          namespace: default
        spec:
          template:
            spec:
              serviceAccountName: my-app-sa # Link the Service Account here
              containers:
              - name: my-app-container
                image: my-app-image:latest
        ```

By effectively using RBAC with Roles, ClusterRoles, RoleBindings, ClusterRoleBindings, and Service Accounts, you can implement a fine-grained and secure authorization model for your Kubernetes cluster.
