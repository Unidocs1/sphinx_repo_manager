================================
Platform Installation using Helm
================================

This article details the steps to install the AcceleratXR platform to Kubernetes using Helm. Before you begin make sure
that all `pre-requisites <prerequisites>` have been installed and configured correctly.

Clone the Helm Chart
====================

A Helm chart capable of deploying the platform including all supported micro-services, databases and stats servers is
available in GitLab. Select the URL of the repository for the subscription plan you have below.

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Subscription
     - URL
   * - Core
     - https://gitlab.com/AcceleratXR/Core/tools/k8s_deploy
   * - Professional
     - https://gitlab.com/AcceleratXR/professional/tools/k8s_deploy
   * - Studio
     - https://gitlab.com/AcceleratXR/studio/tools/k8s_deploy
   * - Enterprise
     - https://gitlab.com/AcceleratXR/enterprise/tools/k8s_deploy

Next clone the repository to your local machine.

.. code-block:: bash
   :linenos:

   git clone git@gitlab.acceleratxr.com:Core/tools/k8s_deploy.git

Dependencies
============

Before the helm chart can be used the dependencies must be locally downloaded and initialized. This is done with the
following command.

.. code-block:: bash
   :linenos:

   helm dep up

Create a Namespace
==================

It is recommended that AcceleratXR be installed within a dedicated namespace within Kubernetes.

.. code-block:: bash
   :linenos:

   kubectl create axr-demo-v1

In the above example we create a namespace called `axr-demo-v1`.  This namespace will contain all of the platform's
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
   * - `title`
     - The title of the product being deployed.
     - AXR Demo
   * - `domain`
     - The primary domain that the platform will be deployed to.
     - `demo.goaxr.cloud`
   * - `ingress.hosts[0].host`
     - The exact hostname that the platform's REST API will be served from.
     - `api.demo.goaxr.cloud`
   * - `mongodb.auth.password`
     - The password to the MongoDB database server that each service will use to connect.
     - 
   * - `postgresql.postgresqlPassword`
     - The password to the MongoDB database server that each service will use to connect.
     - 
   * - `admin.password`
     - The password to the adminstrator account that will have superuser access to the platform.

For details on all available configuration options please consult the repository's
`README <https://gitlab.com/AcceleratXR/Core/tools/k8s_deploy/-/blob/master/README.md>`.

Utilizing In-Cluster Database Servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following command will install the AcceleratXR platform and set up all necessary database
servers within the running cluster. This is the **RECOMMENDED** install method.

.. code-block:: bash
   :linenos:

   helm install axr-demo-v1 . \
   --namespace axr-demo-v1 \
   --set title=AXR-Demo \
   --set domain=demo.goaxr.cloud \
   --set ingress.hosts[0].host=api.demo.goaxr.cloud \
   --set mongodb.create=true \
   --set mongodb.architecture=standalone \
   --set mongodb.auth.enabled=false \
   --set mongodb.auth.username="admin" \
   --set mongodb.auth.password="<PASSWORD>" \
   --set mongodb.auth.rootPassword="<PASSWORD>" \
   --set postgresql.create=true \
   --set postgresql.postgresqlPassword="<PASSWORD>" \
   --set admin.password="<PASSWORD>"

Utilizing External Database Servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If external database providers are desired, such as using DocumentDB/RDS/Elasticache when running in AWS,
the following command should be used.

.. code-block:: bash
   :linenos:

   helm install axr-demo-v1 . \
   --namespace axr-demo-v1 \
   --set title=AXR-Demo \
   --set domain=demo.goaxr.cloud \
   --set ingress.hosts[0].host=api.demo.goaxr.cloud \
   --set mongodb.create=false \
   --set mongodb.url=mongodb://admin:<PASSWORD>@ext.hosted.mongodb \
   --set mongodb.auth.username="admin" \
   --set mongodb.auth.password="<PASSWORD>" \
   --set mongodb.auth.rootPassword="<PASSWORD>" \
   --set postgresql.create=false \
   --set postgresql.url=postgres://admin:<PASSWORD>@ext.hosted.postgresql \
   --set postgresql.postgresqlPassword="<PASSWORD>" \
   --set admin.password="<PASSWORD>"

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

      https://api.demo.goaxr.cloud/v1

   Admin Account:
   Username: admin
   Password: <PASSWORD>

   Authentication Configuration:
   Audience: demo.goaxr.cloud
   Issuer: api.demo.goaxr.cloud
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

Validating the Installation
===========================

To validate that the platform was successfuly installed and running correctly you can run `kubectl get all` on your
cluster. The output should look similar to the following.

.. code-block:: bash

   $ kubectl -n axr-demo-v1 get all
   NAME                                                  READY   STATUS    RESTARTS   AGE
   pod/account-services-84d5497c6c-lm55l                 1/1     Running   0          18d
   pod/achievement-services-dc5cddfbb-bd8rh              1/1     Running   0          18d
   pod/axr-demo-v1-kube-state-metrics-7bb547d5bf-p4gps   1/1     Running   0          18d
   pod/axr-demo-v1-prometheus-server-6dd5bb84bf-b2hgl    0/2     Running   0          18d
   pod/cache-db-master-0                                 1/1     Running   0          18d
   pod/cache-db-slave-0                                  1/1     Running   0          18d
   pod/cache-db-slave-1                                  1/1     Running   0          18d
   pod/events-db-master-0                                1/1     Running   0          18d
   pod/events-db-slave-0                                 1/1     Running   0          18d
   pod/events-db-slave-1                                 1/1     Running   0          18d
   pod/leaderboard-services-b6f47b9d-fsqg5               1/1     Running   0          18d
   pod/mongodb-7bf99647dd-wlfmm                          1/1     Running   0          18d
   pod/notification-services-58f58cf469-846fd            1/1     Running   0          18d
   pod/persona-services-5b56d644ff-vmlbl                 1/1     Running   0          10d
   pod/progression-services-cb5d57b74-vzsgk              1/1     Running   0          18d
   pod/quest-services-7f8c8fdf74-q98pz                   1/1     Running   0          18d
   pod/redis-master-0                                    1/1     Running   0          18d
   pod/redis-slave-0                                     1/1     Running   0          18d
   pod/redis-slave-1                                     1/1     Running   0          18d
   pod/scripting-services-664d6c58c-kmw5p                1/1     Running   0          18d
   pod/server-instance-services-ddfbf87f-6bb4p           1/1     Running   0          18d
   pod/session-services-7776455cc5-t547j                 1/1     Running   0          18d
   pod/social-services-59b49d6759-f9n86                  1/1     Running   0          18d
   pod/telemetry-services-c964b9f68-vvc5c                1/1     Running   0          18d
   pod/world-services-7966478747-7cvkr                   1/1     Running   0          18d

   NAME                                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
   service/account-services                 NodePort    172.23.24.95     <none>        80:31973/TCP   18d
   service/achievement-services             NodePort    172.23.83.121    <none>        80:32680/TCP   18d
   service/asset-services                   NodePort    172.23.99.69     <none>        80:31164/TCP   18d
   service/axr-demo-v1-kube-state-metrics   ClusterIP   172.23.44.249    <none>        8080/TCP       18d
   service/axr-demo-v1-prometheus-server    ClusterIP   172.23.113.23    <none>        80/TCP         18d
   service/cache-db-headless                ClusterIP   None             <none>        6379/TCP       18d
   service/cache-db-master                  ClusterIP   172.23.26.101    <none>        6379/TCP       18d
   service/cache-db-slave                   ClusterIP   172.23.47.30     <none>        6379/TCP       18d
   service/events-db-headless               ClusterIP   None             <none>        6379/TCP       18d
   service/events-db-master                 ClusterIP   172.23.137.208   <none>        6379/TCP       18d
   service/events-db-slave                  ClusterIP   172.23.124.235   <none>        6379/TCP       18d
   service/leaderboard-services             NodePort    172.23.195.9     <none>        80:32514/TCP   18d
   service/matchmaking-services             NodePort    172.23.203.156   <none>        80:31485/TCP   18d
   service/mongodb                          ClusterIP   172.23.128.149   <none>        27017/TCP      18d
   service/notification-services            NodePort    172.23.17.68     <none>        80:31633/TCP   18d
   service/persona-services                 NodePort    172.23.182.245   <none>        80:30153/TCP   18d
   service/progression-services             NodePort    172.23.154.102   <none>        80:30574/TCP   18d
   service/purchasing-services              NodePort    172.23.3.25      <none>        80:31819/TCP   18d
   service/quest-services                   NodePort    172.23.95.212    <none>        80:32669/TCP   18d
   service/redis-headless                   ClusterIP   None             <none>        6379/TCP       18d
   service/redis-master                     ClusterIP   172.23.83.112    <none>        6379/TCP       18d
   service/redis-slave                      ClusterIP   172.23.236.230   <none>        6379/TCP       18d
   service/scripting-services               NodePort    172.23.212.20    <none>        80:32317/TCP   18d
   service/server-instance-services         NodePort    172.23.221.3     <none>        80:31630/TCP   18d
   service/server-manager-services          NodePort    172.23.126.73    <none>        80:30269/TCP   18d
   service/session-services                 NodePort    172.23.116.217   <none>        80:31285/TCP   18d
   service/social-services                  NodePort    172.23.119.29    <none>        80:31150/TCP   18d
   service/telemetry-services               NodePort    172.23.202.100   <none>        80:30828/TCP   18d
   service/validation-services              NodePort    172.23.199.234   <none>        80:31972/TCP   18d
   service/world-services                   NodePort    172.23.93.253    <none>        80:31589/TCP   18d

   NAME                                             READY   UP-TO-DATE   AVAILABLE   AGE
   deployment.apps/account-services                 1/1     1            1           18d
   deployment.apps/achievement-services             1/1     1            1           18d
   deployment.apps/axr-demo-v1-kube-state-metrics   1/1     1            1           18d
   deployment.apps/axr-demo-v1-prometheus-server    0/1     1            1           18d
   deployment.apps/leaderboard-services             1/1     1            1           18d
   deployment.apps/mongodb                          1/1     1            1           18d
   deployment.apps/notification-services            1/1     1            1           18d
   deployment.apps/persona-services                 1/1     1            1           18d
   deployment.apps/progression-services             1/1     1            1           18d
   deployment.apps/quest-services                   1/1     1            1           18d
   deployment.apps/scripting-services               1/1     1            1           18d
   deployment.apps/server-instance-services         1/1     1            1           18d
   deployment.apps/session-services                 1/1     1            1           18d
   deployment.apps/social-services                  1/1     1            1           18d
   deployment.apps/telemetry-services               1/1     1            1           18d
   deployment.apps/world-services                   1/1     1            1           18d

   NAME                                                        DESIRED   CURRENT   READY   AGE
   replicaset.apps/account-services-84d5497c6c                 1         1         1       18d
   replicaset.apps/achievement-services-dc5cddfbb              1         1         1       18d
   replicaset.apps/axr-demo-v1-kube-state-metrics-7bb547d5bf   1         1         1       18d
   replicaset.apps/axr-demo-v1-prometheus-server-6dd5bb84bf    1         1         1       18d
   replicaset.apps/leaderboard-services-b6f47b9d               1         1         1       18d
   replicaset.apps/mongodb-7bf99647dd                          1         1         1       18d
   replicaset.apps/notification-services-58f58cf469            1         1         1       18d
   replicaset.apps/persona-services-5b56d644ff                 1         1         1       18d
   replicaset.apps/progression-services-cb5d57b74              1         1         1       18d
   replicaset.apps/quest-services-7f8c8fdf74                   1         1         1       18d
   replicaset.apps/scripting-services-664d6c58c                1         1         1       18d
   replicaset.apps/server-instance-services-ddfbf87f           1         1         1       18d
   replicaset.apps/session-services-7776455cc5                 1         1         1       18d
   replicaset.apps/social-services-59b49d6759                  1         1         1       18d
   replicaset.apps/telemetry-services-c964b9f68                1         1         1       18d
   replicaset.apps/world-services-7966478747                   1         1         1       18d

   NAME                                READY   AGE
   statefulset.apps/cache-db-master    1/1     18d
   statefulset.apps/cache-db-slave     2/2     18d
   statefulset.apps/events-db-master   1/1     18d
   statefulset.apps/events-db-slave    2/2     18d
   statefulset.apps/redis-master       1/1     18d
   statefulset.apps/redis-slave        2/2     18d

Lastly you can check that the platform is correctly responding to API requests using the following test.
The URL is obtained using the Cluster Address reported from the installation command and adding
`/status/accounts` to the end.

.. code-block:: bash

$ curl https://api.demo.goaxr.cloud/v1/status/accounts
{"name":"account_services","time":"2021-06-08T00:50:25.786Z","version":"1.0.0"}