=======================
Platform Pre-requisites
=======================

The AcceleratXR platform is designed to run on top of the Kubernetes orchestration system. This article will guide you
through setting up your Kubernetes cluster to be ready to install the AcceleratXR software.

Installing Kubernetes
=====================

The first thing to do is install `Kubernetes <https://kubernetes.io/>`_. The simplest way to accomplish this is to
install `Docker for Windows <https://docs.docker.com/docker-for-windows/install/>`_ or
`Docker for Mac <https://docs.docker.com/docker-for-mac/install/>`_.

For Linux based installations we recommend consulting the official `documentation <https://kubernetes.io/docs/setup/production-environment/>`_.

Docker for Windows/Mac
~~~~~~~~~~~~~~~~~~~~~~

Once Docker is installed you can enable Kubernetes by following this `guide <https://docs.docker.com/desktop/kubernetes/>`_.

Command Line Tools
==================

There are two commadn line tools that are required for installation. They are:

* `kubectl <https://kubernetes.io/docs/reference/kubectl/overview/>`_
* `helm <https://helm.sh/>`_

The ``kubectl`` will automatically be installed to your local machine if you are using Docker for Windows/Mac. If you've set up
Kubernetes on a dedicated Linux server you likely already installed this tool during that installation process.

Helm Repositories
=================

AcceleratXR makes use of several third-party applications and services that must be installed and/or discoverable during
the installation process. Each of these is available via different publicaly available helm repositories that must be
added to your local helm installation.

.. code-block:: bash

   helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo add bokysan https://bokysan.github.io/docker-postfix/
   helm repo add jetstack https://charts.jetstack.io
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update

nginx
=====

The platform requires an ingress load balancer capable of coordinating HTTP/HTTPS traffic and routing to the necessary
microservice pods. For this `nginx <https://www.nginx.com/>`_ is recommended. There are two versions of the nginx load
balancer for Kubernetes; a community supported module named ingress-nginx and an official supported module named
nginx-ingress. We recommend the use of the community support module `ingress-nginx <https://kubernetes.github.io/ingress-nginx/>`_.

To install ingress-nginx run the following set of commands.

.. code-block:: bash

    kubectl create ns nginx
    helm install nginx ingress-nginx/ingress-nginx \
    --namespace nginx \
    --set rbac.create=true \
    --set controller.service.externalTrafficPolicy=Local \
    --set controller.service.annotations."service\.beta\.kubernetes\.io/do-loadbalancer-enable-proxy-protocol=true" \
    --set controller.replicaCount=3 \
    --set-string controller.config.use-proxy-protocol=true,controller.config.use-forward-headers=true,controller.config.compute-full-forward-for=true,controller.config.ssl-protocols="TLSv1.2 TLSv1.3",controller.config.ssl-cipers="ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384"

Note the modified configuration above. The above configuration enables proxy-protocol which is needed by the platform to enable source IP discovery used in tracking client requests as well as certain geolocation-sensitive services such as Matchmaking.
For additional security, a specific set of cyphers and TLS support is enabled to ensure maximum protection against known exploits. This is based on industry standard recommendations.

Cert Manager
============

The next module that needs to be installed is cert manager. Cert manager is used to automatically generate and manage
TLS certificates for HTTPS termination using Let’s Encrypt. Unfortunately there is a bug when using proxy protocol so
the stock cert-manager can’t be used. Instead a modified version of cert-manager is leveraged instead. We can enable
this by overriding the image.repository setting.

.. code-block:: bash

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
       solvers:
       - http01:
           ingress:
             class: nginx

Now apply the file to the kubernetes cluster with the command.

.. code-block:: bash

   kubectl apply -f letsencrypt.yaml

Portworx
========

.. attention:: If you are using ephemeral storage or installing to a cloud provider such as AWS or GCP you can skip this section.

If you are running an on-premises cluster you will need to install a data storage provider. Portworx is one such provider and is the recommended solution
for AcceleratXR deployments based on it's best-in-class performance and scalability. Before you can install Portworx you will need additional hard disks
installed to your on-premises server that are **unformatted** and **unmounted**. These disks will serve as the storage devices Portworx will use.

In order to install Portworx you must first create a new spec with the `Portworx Central Dashboard <https://central.portworx.com/>`_. For production deployments it is recommended to use Portworx Enterprise, for all others Portworx Essentials is more than sufficient.

.. image:: /images/install/prereqs_diagram1.png

In the spec generator wizard you'll check the box for ``Use the Portworx Operator`` and select the latest available version from the drop down.

.. image:: /images/install/prereqs_diagram2.png

On the next page you will select ``On Premises`` and ``Automatically scan disks``. You'll also want to check the three remaining boxes as shown above.

.. image:: /images/install/prereqs_diagram3.png

You can skip this next page and just click Next.

.. image:: /images/install/prereqs_diagram4.png

For the last page of the wizard make sure to select ``None`` from the options. It is not necessary to configure anything else. You can now click **Finish**.

.. image:: /images/install/prereqs_diagram5.png

Once you've finalized the spec creation you'll be presented with this page. Copy and run the two provided commands in order to install Portworx into your cluster. Make sure to click **Save Spec** once you are finished.

.. code-block:: bash

   kubectl apply -f 'https://install.portworx.com/2.8?comp=pxoperator'
   kubectl apply -f 'https://install.portworx.com/2.8?operator=true&mc=false&kbver=&oem=esse&user=152f6083-a52f-11ea-97e6-f6e09c7a4e5e&b=true&f=true&j=auto&c=px-cluster-5580daf5-57f3-4aeb-90ca-85559026e817&stork=true&csi=true&lh=true&mon=true&st=k8s&promop=true'

If Portworx was installed correctly you should be able to run the following command and see similar results.

.. code-block:: bash

   kubectl -n kube-system get pods

.. code-block:: bash

   NAME                                                    READY   STATUS    RESTARTS   AGE
   autopilot-f76f468d4-ccv9c                               1/1     Running   0          5d2h
   portworx-api-2gvds                                      1/1     Running   0          5d2h
   portworx-api-4qtrz                                      1/1     Running   0          5d2h
   portworx-api-jcz87                                      1/1     Running   0          5d2h
   portworx-operator-fdcbd8688-nxn8f                       1/1     Running   0          5d2h
   prometheus-px-prometheus-0                              3/3     Running   1          5d2h
   px-cluster-ed66a2d6-14ee-43f2-86a8-9998fca0cc62-66cpl   3/3     Running   0          5d2h
   px-cluster-ed66a2d6-14ee-43f2-86a8-9998fca0cc62-sbmpv   3/3     Running   0          5d2h
   px-cluster-ed66a2d6-14ee-43f2-86a8-9998fca0cc62-sjf2x   3/3     Running   0          5d2h
   px-csi-ext-5686675c58-hqm4t                             3/3     Running   3          5d2h
   px-csi-ext-5686675c58-lfjlz                             3/3     Running   3          5d2h
   px-csi-ext-5686675c58-lr7jx                             3/3     Running   3          5d2h
   px-lighthouse-7dc48b77c8-sfqss                          3/3     Running   0          5d2h
   px-prometheus-operator-8c88487bc-rgswr                  1/1     Running   0          5d2h
   stork-687ddb787d-2q6bt                                  1/1     Running   0          5d2h
   stork-687ddb787d-8zvxd                                  1/1     Running   0          5d2h
   stork-687ddb787d-nl9d4                                  1/1     Running   0          5d2h
   stork-scheduler-7666d5c7f9-278fm                        1/1     Running   0          5d2h
   stork-scheduler-7666d5c7f9-dx4nb                        1/1     Running   0          5d2h
   stork-scheduler-7666d5c7f9-q2hzl                        1/1     Running   0          5d2h

Finishing Up
============

You are now ready to install the AcceleratXR platform.