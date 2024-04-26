====================
SSL/TLS Certificates
====================

By default, the Xsolla Backend engine enables SSL/TLS for all HTTP traffic and utilizes HTTP Strict Transport Security
(HSTS). While support for SSL and HSTS can be disabled it is **strongly** recommended not to.

SSL certificates can be  installed from any certificate authority, including self-signed, for use by the platform.
However, for simplicity and security Xsolla Backend comes with native support for Let's Encrypt certificates.

To utilize a Let's Encrypt certificate *cert-manager* is recommended to be installed on the Kubernetes cluster.

Cert Manager
============

Cert manager is a great tool for generating SSL/TLS certificates from a variety of certificate authorities, including
Let's Encrypt.

The following commands can be used to install cert-manager with a default configuration for Let's Encrypt.

Installation
~~~~~~~~~~~~

.. code-block:: bash

    helm repo add jetstack https://charts.jetstack.io
    helm repo update
    helm install cert-manager jetstack/cert-manager \
        --namespace cert-manager \
        --create-namespace \
        --set installCRDs=true \
        --set ingressShim.defaultIssuerName=letsencrypt-prod \
        --set ingressShim.defaultIssuerKind=ClusterIssuer \
        --set ingressShim.defaultIssuerGroup=<DOMAIN>
    cat << EOF | kubectl apply -f -
    apiVersion: cert-manager.io/v1
    kind: ClusterIssuer
    metadata:
        name: letsencrypt-prod
    spec:
        acme:
            server: https://acme-v02.api.letsencrypt.org/directory
            email: <EMAIL>
            privateKeySecretRef:
                name: letsencrypt-prod
            solvers:
            - http01:
                ingress:
                    class: nginx
    EOF

The above command will install **cert-manager** to the Kubernetes cluster and define a default cluster wide certificate
issuer that uses the default HTTP domain validation method. Make sure to replace the `<DOMAIN>` and `<EMAIL>` with
appropriate values for your situation.