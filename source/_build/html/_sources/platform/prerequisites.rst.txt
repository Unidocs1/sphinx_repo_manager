=======================
Platform Pre-requisites
=======================

The AcceleratXR platform is designed to run on top of the Kubernetes orchestration system. This article will guide you
through setting up your Kubernetes cluster to be ready to install the AcceleratXR software.

Installing Kubernetes
=====================

The first thing to do is install `Kubernetes <https://kubernetes.io/>`. The simplest way to accomplish this is to
install `Docker for Windows <https://docs.docker.com/docker-for-windows/install/>` or
`Docker for Mac <https://docs.docker.com/docker-for-mac/install/>`.

For Linux based installations we recommend consulting the official `documentation <https://kubernetes.io/docs/setup/production-environment/>`.

Docker for Windows/Mac
~~~~~~~~~~~~~~~~~~~~~~

Once Docker is installed you can enable Kubernetes by following this `guide <https://docs.docker.com/desktop/kubernetes/>`.

Command Line Tools
==================

There are two commadn line tools that are required for installation. They are:

* `kubectl <https://kubernetes.io/docs/reference/kubectl/overview/>`
* `helm <https://helm.sh/>`

The `kubectl` will automatically be installed to your local machine if you are using Docker for Windows/Mac. If you've set up
Kubernetes on a dedicated Linux server you likely already installed this tool during that installation process.

Helm Repositories
=================

AcceleratXR makes use of several third-party applications and services that must be installed and/or discoverable during
the installation process. Each of these is available via different publicaly available helm repositories that must be
added to your local helm installation.

.. code-block:: bash
   :linenos:

   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo add jetstack https://charts.jetstack.io
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update

nginx
=====

The platform requires an ingress load balancer capable of coordinating HTTP/HTTPS traffic and routing to the necessary
microservice pods. For this `nginx <https://www.nginx.com/>` is recommended. There are two versions of the nginx load
balancer for Kubernetes; a community supported module named ingress-nginx and an official supported module named
nginx-ingress. We recommend the use of the community support module `ingress-nginx <https://kubernetes.github.io/ingress-nginx/>`.

To install ingress-nginx run the following set of commands.

.. code-block:: bash
   :linenos:

    kubectl create ns nginx
    helm install nginx ingress-nginx/ingress-nginx \
    --namespace nginx \
    --set rbac.create=true \
    --set controller.service.externalTrafficPolicy=Local \
    --set controller.service.annotations."service\.beta\.kubernetes\.io/do-loadbalancer-enable-proxy-protocol=true" \
    --set controller.replicaCount=3 \
    --set-string controller.config.use-proxy-protocol=true,controller.config.use-forward-headers=true,controller.config.compute-full-forward-for=true,controller.config.ssl-protocols="TLSv1.2 TLSv1.3",controller.config.ssl-cipers="ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384"

Cert Manager
============

The next module that needs to be installed is cert manager. Cert manager is used to automatically generate and manage
TLS certificates for HTTPS termination using Let’s Encrypt. Unfortunately there is a bug when using proxy protocol so
the stock cert-manager can’t be used. Instead a modified version of cert-manager is leveraged instead. We can enable
this by overriding the image.repository setting.

.. code-block:: bash
   :linenos:

    kubectl create ns cert-manager
    helm install cert-manager --namespace cert-manager jetstack/cert-manager \
    --set image.repository=jyrno42/cert-manager-controller \
    --set installCRDs=true \
    --set ingressShim.defaultIssuerName=letsencrypt-prod \
    --set ingressShim.defaultIssuerKind=ClusterIssuer \
    --set ingressShim.defaultIssuerGroup=<DOMAIN>

Next we need to register the ClusterIssuer with cert-manager. The Issuer is the CA service that will be used to generate
certificates. Let’s Encrypt is simple and free and works with cert-manager out of the box. Create a file named
`letsencrypt.yaml` with the following contents.

.. code-block:: yaml
   :linenos:

   apiVersion: cert-manager.io/v1alpha2
   kind: ClusterIssuer
   metadata:
   name: letsencrypt-prod
   spec:
   acme:
       # The ACME server URL
       server: https://acme-v02.api.letsencrypt.org/directory
       # Email address used for ACME registration
       email: admin@acceleratxr.com
       # Name of a secret used to store the ACME account private key
       privateKeySecretRef:
       name: letsencrypt-prod
       # AXR owned domains like goaxr.cloud will be handled by DNS, all others by http
       solvers:
       - http01:
           ingress:
             class: nginx

Now apply the file to the kubernetes cluster with the command.

.. code-block:: bash
   :linenos:

   kubectl apply -f letsencrypt.yaml

You are now ready to install the AcceleratXR platform.