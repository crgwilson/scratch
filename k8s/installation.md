# Kubernetes: Installation

## Installation: Pre-reqs

Kernel requirements...

* Enabled `cgroups`

Required modules...

* `br_netfilter`
* `overlay`

Sysctl settings...

```text
net.bridge.bridge-nf-call-iptables=1
net.bridge.bridge-nf-call-ip6tables=1
net.ipv4.ip_forward=1  # If you're using CRI-O or Containerd
```

Other requirements...

* Each node must have a unique MAC address

## Installation: Container runtimes

Choose a container runtime between...

* [Docker][docker]
* [CRI-O][crio]
* [Containerd][containerd]

## Installation: Kubernetes packages

Install...

* `kubelet`
* `kubeadm`
* `kubectl`

Snippet from docs:

<!-- markdownlint-disable line-length -->
```console
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```
<!-- markdownlint-enable line-length -->

## Installation: Bootstrapping the control-plane node

Bootstrap your master node with `kubeadm init`. Running `kubeadm config images pull`
is also a good idea to make sure you can reach the container registry.

```console
kubeadm config images pull
kubeadm init
```

Useful flags for `kubeadm` include...

* `--config`
* `--pod-network-cidr`
* `--apiserver-advertise-address`
* `--apiserver-bind-port`
* `--image-repository`
* `--control-plane-endpoint`

[Kubeadm docs][kubeadm-ref]

`kubeadm` performs the tasks described in the below installation "phases"
<!-- markdownlint-disable line-length -->
```text
preflight                    Run pre-flight checks
certs                        Certificate generation
  /ca                          Generate the self-signed Kubernetes CA to provision identities for other Kubernetes components
  /apiserver                   Generate the certificate for serving the Kubernetes API
  /apiserver-kubelet-client    Generate the certificate for the API server to connect to kubelet
  /front-proxy-ca              Generate the self-signed CA to provision identities for front proxy
  /front-proxy-client          Generate the certificate for the front proxy client
  /etcd-ca                     Generate the self-signed CA to provision identities for etcd
  /etcd-server                 Generate the certificate for serving etcd
  /etcd-peer                   Generate the certificate for etcd nodes to communicate with each other
  /etcd-healthcheck-client     Generate the certificate for liveness probes to healthcheck etcd
  /apiserver-etcd-client       Generate the certificate the apiserver uses to access etcd
  /sa                          Generate a private key for signing service account tokens along with its public key
kubeconfig                   Generate all kubeconfig files necessary to establish the control plane and the admin kubeconfig file
  /admin                       Generate a kubeconfig file for the admin to use and for kubeadm itself
  /kubelet                     Generate a kubeconfig file for the kubelet to use *only* for cluster bootstrapping purposes
  /controller-manager          Generate a kubeconfig file for the controller manager to use
  /scheduler                   Generate a kubeconfig file for the scheduler to use
kubelet-start                Write kubelet settings and (re)start the kubelet
control-plane                Generate all static Pod manifest files necessary to establish the control plane
  /apiserver                   Generates the kube-apiserver static Pod manifest
  /controller-manager          Generates the kube-controller-manager static Pod manifest
  /scheduler                   Generates the kube-scheduler static Pod manifest
etcd                         Generate static Pod manifest file for local etcd
  /local                       Generate the static Pod manifest file for a local, single-node local etcd instance
upload-config                Upload the kubeadm and kubelet configuration to a ConfigMap
  /kubeadm                     Upload the kubeadm ClusterConfiguration to a ConfigMap
  /kubelet                     Upload the kubelet component config to a ConfigMap
upload-certs                 Upload certificates to kubeadm-certs
mark-control-plane           Mark a node as a control-plane
bootstrap-token              Generates bootstrap tokens used to join a node to a cluster
kubelet-finalize             Updates settings relevant to the kubelet after TLS bootstrap
  /experimental-cert-rotation  Enable kubelet client certificate rotation
addon                        Install required addons for passing Conformance tests
  /coredns                     Install the CoreDNS addon to a Kubernetes cluster
  /kube-proxy                  Install the kube-proxy addon to a Kubernetes cluster
```
<!-- markdownlint-enable line-length -->

## Installation: Pod network add-on

Kubernetes has a number of networking plugins to handle inter-pod communication

* [Calico][calico]
* [Flannel][flannel]
* [Weave][weave]

Each of these will come with a `yaml` file describing their setup so they're
trivial to install...

```console
kubectl apply -f add-on.yaml
```

## Installation: Joining a kubelet to an existing cluster

Once your control-plane node has been setup you can join other nodes to it via...

<!-- markdownlint-disable line-length -->
```console
kubeadm join control-plane-host:control-plane-port --token mytoken --disvoery-token-ca-cert-hash sha256:myhash
```
<!-- markdownlint-enable line-length -->

## Further reading

[Container runtimes][containers]
[Installing kubeadm][kubeadm]
[Creating a cluster with kubeadm][create]

[docker]:https://www.docker.com/ "https://www.docker.com/"
[crio]:https://github.com/cri-o/cri-o "https://github.com/cri-o/cri-o"
[containerd]:https://containerd.io/ "https://containerd.io/"
[containers]:https://kubernetes.io/docs/setup/production-environment/container-runtimes/ "https://kubernetes.io/docs/setup/production-environment/container-runtimes/"
[kubeadm]:https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/ "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/"
[kubeadm-ref]:https://kubernetes.io/docs/reference/setup-tools/kubeadm/ "https://kubernetes.io/docs/reference/setup-tools/kubeadm/"
[create]:https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/ "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/"
[calico]:https://www.projectcalico.org/ "https://www.projectcalico.org/"
[flannel]:https://github.com/coreos/flannel "https://github.com/coreos/flannel"
[weave]:https://www.weave.works/oss/net/ "https://www.weave.works/oss/net/"
