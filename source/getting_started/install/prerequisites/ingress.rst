=======
Ingress
=======

AcceleratXR requires an ingress controller in order to expose its REST API, administration console, databases and other
tools to the outside world. Most Kubernetes distrobutions do not include an ingress controller out of the box and there
are many options to choose from.

Supported Ingress Controllers
=============================

* `ingress-nginx <https://github.com/kubernetes/ingress-nginx>_` version v1.0.0 and higher

Configuration
~~~~~~~~~~~~~

The AcceleratXR platform takes advantage of several important web technologies including the following:

* HTTP2
* Proxy Protocol
* Source IP Forwarding
* TLS 1.2 or newer
* WebSockets

It is therefore recommended to enable these features be present in the deployed ingress controller.

Depending on where you are hosting your kubernetes cluster the settings may be different per provider.

Installation for AWS
~~~~~~~~~~~~~~~~~~~~

When installing *ingress-nginx* on an AWS EC2 or EKS based Kubernetes cluster use the following installation command.

.. code-block:: bash

    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm install nginx ingress-nginx/ingress-nginx \
        --namespace nginx \
        --create-namespace \
        --set rbac.create=true \
        --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-cross-zone-load-balancing-enabled"="true" \
        --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-backend-protocol"="tcp"\
        --set controller.service.annotations."service\.\beta\.kubernetes\.io/aws-load-balancer-connection-idle-timeout"="60" \
        --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"="nlb" \
        --set controller.replicaCount=3 \
        --set-string controller.config.use-forward-headers=true,controller.config.compute-full-forward-for=true,controller.config.ssl-protocols="TLSv1.2 TLSv1.3",controller.config.ssl-cipers="ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384"

Installation for Proxy Protocol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following installation command is for providers that support proxy protocol such as bare metal providers and some public clouds.

.. code-block:: bash

    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm install nginx ingress-nginx/ingress-nginx \
        --namespace nginx \
        --create-namespace \
        --set rbac.create=true \
        --set controller.service.externalTrafficPolicy=Local \
        --set controller.service.annotations."service\.beta\.kubernetes\.io/do-loadbalancer-enable-proxy-protocol=true" \
        --set controller.replicaCount=3 \
        --set-string controller.config.use-proxy-protocol=true,controller.config.use-forward-headers=true,controller.config.compute-full-forward-for=true,controller.config.ssl-protocols="TLSv1.2 TLSv1.3",controller.config.ssl-cipers="ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384"

Installation for Other
~~~~~~~~~~~~~~~~~~~~~~

When installing the  *ingress-nginx* controller on other providers with whom proxy protocol is not available use the following command.

.. code-bloock:: bash

    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm install nginx ingress-nginx/ingress-nginx \
        --namespace nginx \
        --create-namespace \
        --set rbac.create=true \
        --set controller.service.externalTrafficPolicy=Local \
        --set controller.replicaCount=3 \
        --set-string controller.config.use-forward-headers=true,controller.config.compute-full-forward-for=true,controller.config.ssl-protocols="TLSv1.2 TLSv1.3",controller.config.ssl-cipers="ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384"