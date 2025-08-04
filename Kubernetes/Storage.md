# Kubernetes: Storage

Kubernetes provides a robust and flexible storage system that abstracts away the complexities of underlying storage infrastructure. This allows applications to consume storage resources without knowing the specifics of how that storage is provisioned. The key concepts are PersistentVolumes (PVs), PersistentVolumeClaims (PVCs), and StorageClasses.

## 1. PersistentVolumes (PVs)

*   **Definition**: A piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using StorageClasses. It is a resource in the cluster, much like a node is a cluster resource. PVs are independent of the lifecycle of any individual Pod that uses the PV.
*   **Characteristics**:
    *   **Capacity**: The size of the volume (e.g., 10Gi, 100Gi).
    *   **Access Modes**: How the volume can be mounted on a host:
        *   `ReadWriteOnce`: The volume can be mounted as read-write by a single node.
        *   `ReadOnlyMany`: The volume can be mounted read-only by many nodes.
        *   `ReadWriteMany`: The volume can be mounted as read-write by many nodes.
        *   `ReadWriteOncePod`: The volume can be mounted as read-write by a single Pod.
    *   **Reclaim Policy**: What happens to the volume when its PVC is deleted:
        *   `Retain`: Manual reclamation. The PV still exists and the data is retained.
        *   `Delete`: The PV and the underlying storage asset are deleted.
        *   `Recycle` (deprecated): The volume is wiped and made available for a new claim.
*   **Supported Volume Types**: Kubernetes supports various types of PVs, including:
    *   `awsElasticBlockStore` (EBS)
    *   `azureDisk`
    *   `azureFile`
    *   `gcePersistentDisk` (GPD)
    *   `nfs`
    *   `iscsi`
    *   `hostPath` (for single-node testing, not production)
    *   `local`
    *   `cephfs`
    *   `cinder`
    *   `flexVolume`
    *   `flocker`
    *   `portworxVolume`
    *   `vsphereVolume`
    *   `csi` (Container Storage Interface - the modern standard)

### PV Example (NFS)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  nfs:
    path: /data/nfs-share
    server: 192.168.1.100
  persistentVolumeReclaimPolicy: Retain
```

## 2. PersistentVolumeClaims (PVCs)

*   **Definition**: A request for storage by a user. It is similar to a Pod requesting CPU and memory. PVCs consume PV resources.
*   **Use Case**: Pods request storage by specifying a PVC in their volume configuration. This decouples the application from the underlying storage details.
*   **Characteristics**:
    *   **Access Modes**: Must match the PV's access modes.
    *   **Storage Request**: The amount of storage requested.
    *   **StorageClassName**: (Optional) Specifies the StorageClass to use for dynamic provisioning.

### PVC Example

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-app-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 2Gi
  storageClassName: nfs-storage # Binds to a PV provisioned by this StorageClass
```

## 3. StorageClasses

*   **Definition**: Provides a way for administrators to describe the "classes" of storage they offer. Different classes might map to quality-of-service levels, backup policies, or arbitrary policies determined by the cluster administrators.
*   **Use Case**: Enables dynamic provisioning of PersistentVolumes. Instead of pre-provisioning PVs, a StorageClass can automatically create a PV when a PVC requests it.
*   **Key Parameters**:
    *   **Provisioner**: Specifies what volume plugin is used for provisioning PVs (e.g., `kubernetes.io/aws-ebs`, `kubernetes.io/gce-pd`, `nfs.csi.k8s.io`).
    *   **Parameters**: Specific to the provisioner (e.g., `type`, `zone` for cloud providers).
    *   **ReclaimPolicy**: Overrides the PV's reclaim policy.
    *   **VolumeBindingMode**: `Immediate` or `WaitForFirstConsumer`. `WaitForFirstConsumer` delays PV binding until a Pod using the PVC is scheduled, improving topology awareness.

### StorageClass Example (AWS EBS)

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp2-storage
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  fsType: ext4
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

## How Applications Use Storage

1.  **Define a PVC**: An application developer creates a PVC, requesting a certain amount of storage and access modes, optionally specifying a `StorageClassName`.
2.  **Provisioning**:
    *   **Static**: If a matching PV already exists, the PVC binds to it.
    *   **Dynamic**: If a `StorageClassName` is specified and a corresponding StorageClass exists, the StorageClass's provisioner creates a new PV for the PVC.
3.  **Mount in Pod**: The Pod then mounts the PVC as a volume.

### Pod Mounting PVC Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-with-storage
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-container
        image: my-image:latest
        volumeMounts:
        - name: my-persistent-storage
          mountPath: /data
      volumes:
      - name: my-persistent-storage
        persistentVolumeClaim:
          claimName: my-app-pvc # Refers to the PVC created earlier
```

## Other Volume Types (Ephemeral)

Besides PVs/PVCs for persistent storage, Kubernetes also supports ephemeral volumes that are tied to the Pod's lifecycle.

*   **`emptyDir`**: A simple empty directory created when a Pod is assigned to a node. It is initially empty and exists as long as the Pod is running on that node. Data is lost when the Pod is removed from the node.
    *   **Use Case**: Temporary storage, caching, sharing files between containers in the same Pod.
*   **`configMap` / `secret`**: Mounts data from a ConfigMap or Secret as files inside a Pod.
    *   **Use Case**: Injecting configuration or sensitive data into applications.
*   **`hostPath`**: Mounts a file or directory from the host node's filesystem into a Pod.
    *   **Use Case**: Advanced use cases for cluster administration or when a Pod needs access to host-specific resources. **Generally discouraged for application Pods due to security and portability concerns.**

Understanding these storage concepts is crucial for deploying stateful applications effectively and reliably in Kubernetes.
