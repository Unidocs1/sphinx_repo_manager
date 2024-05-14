======================================
Installation for Amazon EKS using Helm
======================================

**Time to Complete: 10 minutes**

This article details the steps to install the Xsolla Backend engine to an Kubernetes cluster hosted on `Amazon Elastic Kubernetes Service <https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html>`_ using Helm.

Amazon EKS
==========

Amazon EKS is the preferred way to run Xsolla Backend on AWS.

* `Getting Started <https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html>`_
* `Service endpoints and quotas <https://docs.aws.amazon.com/general/latest/gr/eks.html>`_
* `IAM for Amazon EKS <https://docs.aws.amazon.com/eks/latest/userguide/security-iam.html>`_
* `EKS Pricing <https://aws.amazon.com/eks/pricing/>`_
* `EKS Troubleshooting <https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html>`_

Pre-requisites
==============

Before you begin make sure that all :doc:`pre-requisites <prerequisites>` have been installed and configured correctly on the EKS cluster.

Recommendations
===============

We recommend the following configurations when setting up a Amazon EKS cluster for Xsolla Backend.

* At least one EKS cluster node
* Minimum EC2 `t3.medium` instance size for Amazon EKS nodes
* Elastic IP for public load balancer
* Private S3 bucket for database backup storage

Subscribe to Xsolla Backend
========================

Before you can deploy Xsolla Backend to Amazon EKS you need to Subscribe to the Xsolla Backend engine on the AWS Marketplace.

1. Navigate to https://aws.amazon.com/marketplace/pp/prodview-anpdwpjanxl4s
2. Click the *Continue to Subscribe* button
3. Click the *Continue to Configuration* button
4. Select the *Helm Chart* fulfillment option, then click *Continue to Launch*

Chart Repository
================

Xsolla Backend maintains its own Helm repository containing all the official Helm charts. Add the repository with the following command.

.. code-block:: bash

   helm repo add axr https://nexus.acceleratxr.com/repository/axr-helm/
   helm repo update

Namespaces
==========

It is recommended that Xsolla Backend be installed within a dedicated namespace within Kubernetes. A namespace can be created
explicitly as shown below or automatically during helm installation using the `--create-namespace` option.

.. code-block:: bash

   kubectl create axr-demo-v1

The above example creates a namespace called ``axr-demo-v1``.  This namespace will contain all of the platform's
resources.

Install Command
===============

The helm chart has a number of required properties that must be set in order to install correctly. These are:

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Setting
     - Description
     - Example
   * - ``title``
     - The title of the product being deployed.
     - AXR Demo
   * - ``domain``
     - The primary domain that the platform will be deployed to.
     - ``demo.xsolla.cloud``
   * - ``ingress.hosts[0].host``
     - The exact hostname that the platform's REST API will be served from.
     - ``api.demo.xsolla.cloud``

For details on all available configuration options please consult the repository's
`README <https://gitlab.com/Xsolla Backend/Core/tools/k8s_deploy/-/blob/master/README.md>`_.

Utilizing In-Cluster Database Servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following command will install the Xsolla Backend engine and set up all necessary database
servers within the running cluster. This is the **RECOMMENDED** install method.

.. code-block:: bash

   helm upgrade --install axr-demo-v1 axr/acceleratxr \
   --create-namespace \
   --namespace axr-demo-v1 \
   --set title=AXR-Demo \
   --set domain=demo.xsolla.cloud \
   --set ingress.hosts[0].host=api.demo.xsolla.cloud

Utilizing External Database Servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If external database providers are desired, such as using DocumentDB/RDS/Elasticache when running in AWS,
the following command should be used.

.. code-block:: bash

   helm upgrade --install axr-demo-v1 axr/acceleratxr \
   --create-namespace \
   --namespace axr-demo-v1 \
   --set title=AXR-Demo \
   --set domain=demo.xsolla.cloud \
   --set ingress.hosts[0].host=api.demo.xsolla.cloud \
   --set mongodb.create=false \
   --set mongodb.url=mongodb://admin:<PASSWORD>@ext.hosted.mongodb \
   --set mongodb.auth.username="admin" \
   --set mongodb.auth.password="<PASSWORD>" \
   --set mongodb.auth.rootPassword="<PASSWORD>"

Utilizing Custom ``values.yaml``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes our default configuration is not the most desirable option. In such scenarios you can freely edit the ``values.yaml`` file
included in the helm chart repository and deploy using that method instead. Be sure to fill in any of values marked as **Required**.
Then you can install your cluster with the following simple command.

.. code-block:: bash

   helm upgrade --install axr-demo-v1 axr/acceleratxr \
   --create-namespace \
   --namespace axr-demo-v1 \
   -f values.yaml

Output
======

Once you've successfully installed the platform with Helm you will see output from the command like the following.

.. code-block:: bash

   NAME: axr-demo-v1
   LAST DEPLOYED: Thu May 13 12:11:31 2021
   NAMESPACE: axr-demo-v1
   STATUS: deployed
   REVISION: 1
   NOTES:
   ###############################################################################
   # !!!IMPORTANT!!! WRITE DOWN THE FOLLOWING INFORMATION                        #
   ###############################################################################
   Cluster Addresses:

      https://api.demo.xsolla.cloud/v1

   Admin Account:
   Username: admin
   Password: <PASSWORD>

   Authentication Configuration:
   Audience: demo.xsolla.cloud
   Issuer: api.demo.xsolla.cloud
   ExpiresIn: 1 hour
   Secret: "<SECRET>"

   Databases:
   MongoDB:
      Root Password: <PASSWORD>
      Username: admin
      Password: <PASSWORD>
      URL: mongodb://mongodb
   PostgreSQL:
      Username: postgres
      Password: <PASSWORD>

Configuring DNS
===============

Once Xsolla Backend cluster is created you must configure your DNS server to point to the ingress domain(s) set.

When nginx is setup it creates a Load Balancer resource. This LoadBalancer is what traffic will come in to the cluster to and will be routed to the Xsolla Backend ingress. Therefore, the external IP address of the load balancer is required. You can discover this IP address with the following command.

.. code-block:: bash

   kubectl -n nginx get svc

This will result in an output like the following.

.. code-block:: bash

   NAME                                       TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)                      AGE
   nginx-ingress-nginx-controller             LoadBalancer   172.23.207.63   96.46.186.213   80:31246/TCP,443:32541/TCP   204d
   nginx-ingress-nginx-controller-admission   ClusterIP      172.23.254.84   <none>          443/TCP                      204d

In the above example, the public IP of the LoadBalancer is `96.46.186.213`. Now update your DNS for the configured **ingress** domains by creating an *A* record
for the domains with this address.

As an example, using the above cluster configuration we must create an **A Record** DNS entry for the domain `api.demo.xsolla.cloud` to point to IP `96.46.186.213`.

Validating the Installation
===========================

To validate that the platform was successfuly installed and running correctly you can run ``kubectl get all`` on your
cluster. The output should look similar to the following.

.. code-block:: bash

   kubectl -n axr-demo-v1 get all

.. code-block:: bash

   NAME                                                READY   STATUS    RESTARTS   AGE
   pod/account-services-75f7757b9-j5znc                1/1     Running   0          13h
   pod/achievement-services-ddd975bd7-2zvmk            1/1     Running   0          13h
   pod/axr-demo-v1-kube-state-metrics-7bb8f78d-24pnp   1/1     Running   0          13h
   pod/axr-demo-v1-prometheus-server-8bdcb4f8b-tqnqt   2/2     Running   0          13h
   pod/backup-services-855fd94ff8-rfdv8                1/1     Running   0          13h
   pod/db-mongodb-ff99b45b6-624jf                      1/1     Running   0          13h
   pod/db-redis-master-0                               1/1     Running   0          13h
   pod/db-redis-replicas-0                             0/1     Pending   0          13h
   pod/leaderboard-services-7787bf777f-4zkww           1/1     Running   0          13h
   pod/matchmaking-services-dfc5577f9-mv4q4            1/1     Running   0          13h
   pod/notification-services-6f85948cbc-n2wfs          1/1     Running   0          13h
   pod/persona-services-7864cdf6c6-mfmll               1/1     Running   0          13h
   pod/progression-services-dcc848898-z8rqp            1/1     Running   0          13h
   pod/quest-services-6bc67b86bd-xs2f4                 1/1     Running   0          13h
   pod/scripting-services-5d8677cf7c-tclds             1/1     Running   0          13h
   pod/server-instance-services-6857f6dbf5-ppl88       1/1     Running   0          13h
   pod/service-monitor-df8d54d9d-rh9qk                 1/1     Running   0          13h
   pod/session-services-5b7fbc5b66-6hqc8               1/1     Running   0          13h
   pod/social-services-7ccbcff887-7sdxt                1/1     Running   0          13h
   pod/telemetry-services-5c646dbb96-szz72             1/1     Running   0          13h
   pod/world-services-5666c4dd56-hzq4b                 1/1     Running   0          13h
   
   NAME                                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)     AGE
   service/account-services                 ClusterIP   172.23.51.107    <none>        80/TCP      13h
   service/achievement-services             ClusterIP   172.23.17.89     <none>        80/TCP      13h
   service/axr-demo-v1-kube-state-metrics   ClusterIP   172.23.252.168   <none>        8080/TCP    13h
   service/axr-demo-v1-prometheus-server    ClusterIP   172.23.221.250   <none>        80/TCP      13h
   service/backup-services                  ClusterIP   172.23.58.201    <none>        80/TCP      13h
   service/db-mongodb                       ClusterIP   172.23.241.71    <none>        27017/TCP   13h
   service/db-redis-headless                ClusterIP   None             <none>        6379/TCP    13h
   service/db-redis-master                  ClusterIP   172.23.19.37     <none>        6379/TCP    13h
   service/db-redis-replicas                ClusterIP   172.23.198.89    <none>        6379/TCP    13h
   service/leaderboard-services             ClusterIP   172.23.69.25     <none>        80/TCP      13h
   service/matchmaking-services             ClusterIP   172.23.245.237   <none>        80/TCP      13h
   service/notification-services            ClusterIP   172.23.109.120   <none>        80/TCP      13h
   service/persona-services                 ClusterIP   172.23.103.87    <none>        80/TCP      13h
   service/progression-services             ClusterIP   172.23.227.87    <none>        80/TCP      13h
   service/quest-services                   ClusterIP   172.23.110.215   <none>        80/TCP      13h
   service/scripting-services               ClusterIP   172.23.12.103    <none>        80/TCP      13h
   service/server-instance-services         ClusterIP   172.23.69.222    <none>        80/TCP      13h
   service/service-monitor                  ClusterIP   172.23.165.42    <none>        80/TCP      13h
   service/session-services                 ClusterIP   172.23.151.33    <none>        80/TCP      13h
   service/social-services                  ClusterIP   172.23.190.34    <none>        80/TCP      13h
   service/telemetry-services               ClusterIP   172.23.62.122    <none>        80/TCP      13h
   service/world-services                   ClusterIP   172.23.115.135   <none>        80/TCP      13h
   
   NAME                                             READY   UP-TO-DATE   AVAILABLE   AGE
   deployment.apps/account-services                 1/1     1            1           13h
   deployment.apps/achievement-services             1/1     1            1           13h
   deployment.apps/axr-demo-v1-kube-state-metrics   1/1     1            1           13h
   deployment.apps/axr-demo-v1-prometheus-server    1/1     1            1           13h
   deployment.apps/backup-services                  1/1     1            1           13h
   deployment.apps/db-mongodb                       1/1     1            1           13h
   deployment.apps/leaderboard-services             1/1     1            1           13h
   deployment.apps/matchmaking-services             1/1     1            1           13h
   deployment.apps/notification-services            1/1     1            1           13h
   deployment.apps/persona-services                 1/1     1            1           13h
   deployment.apps/progression-services             1/1     1            1           13h
   deployment.apps/quest-services                   1/1     1            1           13h
   deployment.apps/scripting-services               1/1     1            1           13h
   deployment.apps/server-instance-services         1/1     1            1           13h
   deployment.apps/service-monitor                  1/1     1            1           13h
   deployment.apps/session-services                 1/1     1            1           13h
   deployment.apps/social-services                  1/1     1            1           13h
   deployment.apps/telemetry-services               1/1     1            1           13h
   deployment.apps/world-services                   1/1     1            1           13h
   
   NAME                                                      DESIRED   CURRENT   READY   AGE
   replicaset.apps/account-services-75f7757b9                1         1         1       13h
   replicaset.apps/achievement-services-ddd975bd7            1         1         1       13h
   replicaset.apps/axr-demo-v1-kube-state-metrics-7bb8f78d   1         1         1       13h
   replicaset.apps/axr-demo-v1-prometheus-server-8bdcb4f8b   1         1         1       13h
   replicaset.apps/backup-services-855fd94ff8                1         1         1       13h
   replicaset.apps/db-mongodb-ff99b45b6                      1         1         1       13h
   replicaset.apps/leaderboard-services-7787bf777f           1         1         1       13h
   replicaset.apps/matchmaking-services-dfc5577f9            1         1         1       13h
   replicaset.apps/notification-services-6f85948cbc          1         1         1       13h
   replicaset.apps/persona-services-7864cdf6c6               1         1         1       13h
   replicaset.apps/progression-services-dcc848898            1         1         1       13h
   replicaset.apps/quest-services-6bc67b86bd                 1         1         1       13h
   replicaset.apps/scripting-services-5d8677cf7c             1         1         1       13h
   replicaset.apps/server-instance-services-6857f6dbf5       1         1         1       13h
   replicaset.apps/service-monitor-57bfcdcbc6                0         0         0       13h
   replicaset.apps/service-monitor-6d4598b578                0         0         0       13h
   replicaset.apps/service-monitor-df8d54d9d                 1         1         1       13h
   replicaset.apps/session-services-5b7fbc5b66               1         1         1       13h
   replicaset.apps/social-services-7ccbcff887                1         1         1       13h
   replicaset.apps/telemetry-services-5c646dbb96             1         1         1       13h
   replicaset.apps/world-services-5666c4dd56                 1         1         1       13h
   
   NAME                                 READY   AGE
   statefulset.apps/db-redis-master     1/1     13h
   statefulset.apps/db-redis-replicas   0/3     13h
   
Lastly you can check that the platform is correctly responding to API requests using the following test.
The URL is obtained using the Cluster Address reported from the installation command and adding
``/status`` to the end.

.. code-block:: bash

   curl https://api.demo.xsolla.cloud/v1/status

.. code-block:: json

   {
   	"services": {
   		"account-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.153Z",
   			"name": "account_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.152Z",
   			"version": "1.26.0",
   			"lastUpdate": "2022-03-11T21:02:35.153Z"
   		},
   		"achievement-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.158Z",
   			"name": "achievement_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.157Z",
   			"version": "1.7.0",
   			"lastUpdate": "2022-03-11T21:02:35.160Z"
   		},
   		"backup-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.166Z",
   			"name": "backup_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.166Z",
   			"version": "1.0.0",
   			"lastUpdate": "2022-03-11T21:02:35.166Z"
   		},
   		"leaderboard-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.171Z",
   			"name": "leaderboard_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.171Z",
   			"version": "1.9.0",
   			"lastUpdate": "2022-03-11T21:02:35.171Z"
   		},
   		"matchmaking-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.176Z",
   			"name": "matchmaking_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.175Z",
   			"version": "1.0.0-rc10",
   			"lastUpdate": "2022-03-11T21:02:35.176Z"
   		},
   		"notification-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.182Z",
   			"name": "notification_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.181Z",
   			"version": "1.8.0",
   			"lastUpdate": "2022-03-11T21:02:35.182Z"
   		},
   		"persona-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.186Z",
   			"name": "persona_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.186Z",
   			"version": "1.10.0",
   			"lastUpdate": "2022-03-11T21:02:35.186Z"
   		},
   		"progression-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.191Z",
   			"name": "progression_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.190Z",
   			"version": "1.6.0",
   			"lastUpdate": "2022-03-11T21:02:35.191Z"
   		},
   		"quest-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.195Z",
   			"name": "quest_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.195Z",
   			"version": "1.6.0",
   			"lastUpdate": "2022-03-11T21:02:35.195Z"
   		},
   		"scripting-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.200Z",
   			"name": "scripting_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.200Z",
   			"version": "1.8.0",
   			"lastUpdate": "2022-03-11T21:02:35.200Z"
   		},
   		"server-instance-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.208Z",
   			"name": "server_instance_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.207Z",
   			"version": "1.8.0",
   			"lastUpdate": "2022-03-11T21:02:35.208Z"
   		},
   		"session-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.214Z",
   			"name": "session_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.214Z",
   			"version": "1.9.0",
   			"lastUpdate": "2022-03-11T21:02:35.214Z"
   		},
   		"social-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.220Z",
   			"name": "social_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.219Z",
   			"version": "1.6.0",
   			"lastUpdate": "2022-03-11T21:02:35.220Z"
   		},
   		"telemetry-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.229Z",
   			"name": "telemetry_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.228Z",
   			"version": "1.8.0",
   			"lastUpdate": "2022-03-11T21:02:35.229Z"
   		},
   		"world-services": {
   			"lastHeartbeat": "2022-03-11T21:02:35.235Z",
   			"name": "world_services",
   			"online": true,
   			"time": "2022-03-11T21:02:35.234Z",
   			"version": "1.14.0",
   			"lastUpdate": "2022-03-11T21:02:35.235Z"
   		}
   	},
   	"healthy": 15,
   	"offline": 0,
   	"total": 15
   }

Additional Support
==================

Xsolla Backend offers commercial support at https://www.acceleratxr.com/pricing/ under Self-Hosted plans.