==========================================
Installation for Amazon EKS using Operator
==========================================

**Time to Complete: 10 minutes**

This article details the steps to install the Xsolla Backend engine to an Kubernetes cluster hosted on `Amazon Elastic Kubernetes Service <https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html>`_ using the official Xsolla Backend Operator for Kubernetes.

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
4. Select the *Kubernetes Operator* fulfillment option, then click *Continue to Launch*

Install the Operator
====================

To install the Xsolla Backend operator for Kubernetes run the following command.

.. code-block:: bash

   kubectl apply -f https://nexus.acceleratxr.com/repository/public/Core/tools/operator/latest/deploy/aws.yaml

Verify that the operator was successfully deployed and is running with the following command.

.. code-block:: bash

   kubectl -n acceleratxr-operator-system get pods

If the operator was installed succcessfully you should see similar output to the following.

.. code-block:: bash
   
   NAME                                                       READY   STATUS    RESTARTS   AGE
   acceleratxr-operator-controller-manager-59647d8589-rxcfw   2/2     Running   0          17s

Defining a Cluster
==================

More than likely you want to deploy Xsolla Backend in an environment that others can access it from. To do this requires some
basic configuration by defining a Cluster resource.

To get started download the file: https://nexus.acceleratxr.com/repository/public/Core/tools/operator/latest/deploy/cluster_sample.yaml

Save a copy of the downloaded file and open the copy in your favorite text editor.

The following table details key configuration options you will need to customize your cluster for external deployment.

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

Example
~~~~~~~

The following shows a simplified example configuration for the AXR Demo environment.

.. code-block:: yaml

   # The root domain name to use
   domain: demo.xsolla.cloud
   
   # The url to the cluster's account administration website.
   website: https://console.xsolla.cloud/
   
   # The name of the application or product
   title: Demo
   
   ingress:
     hosts:
       - host: "api.demo.xsolla.cloud"

Configuring DNS
===============

Before finally creating the Xsolla Backend cluster it is necessary to configure DNS to properly route requests to the configured domain(s) above.

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

Once the DNS has been set for each of the configured ingress domains it is time to create the Xsolla Backend cluster.

Create the Cluster
==================

Run the following command to create the Xsolla Backend cluster.

.. code-block:: bash
   
   kubectl apply -f cluster_sample.yaml

Validating the Installation
===========================

To validate that the platform was successfuly installed and running correctly you can run ``kubectl get all`` on your
cluster. The output should look similar to the following.

.. code-block:: bash

   kubectl get all

.. code-block:: bash

   NAME                                                  READY   STATUS    RESTARTS   AGE
   pod/account-services-84d5497c6c-lm55l                 1/1     Running   0          18d
   pod/achievement-services-dc5cddfbb-bd8rh              1/1     Running   0          18d
   pod/axr-demo-v1-kube-state-metrics-7bb547d5bf-p4gps   1/1     Running   0          18d
   pod/axr-demo-v1-prometheus-server-6dd5bb84bf-b2hgl    0/2     Running   0          18d
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
   statefulset.apps/redis-master       1/1     18d
   statefulset.apps/redis-slave        2/2     18d

Lastly you can check that the platform is correctly responding to API requests using the following test.
The URL is obtained using the Cluster Address reported from the installation command and adding
``/status`` to the end.

.. code-block:: bash

   curl https://api.demo.xsolla.cloud/v1/status

.. code-block:: json

   {"services":{"account-services":{"lastHeartbeat":"2022-02-03T01:25:41.159Z","name":"account_services","online":true,"time":"2022-02-03T01:25:41.159Z","version":"1.19.0","lastUpdate":"2022-02-03T01:25:41.160Z"},"achievement-services":{"lastHeartbeat":"2022-02-03T01:25:41.161Z","name":"achievement_services","online":true,"time":"2022-02-03T01:25:41.161Z","version":"1.6.0","lastUpdate":"2022-02-03T01:25:41.162Z"},"backup-services":{"lastHeartbeat":"2022-02-03T01:25:41.163Z","name":"backup_services","online":true,"lastUpdate":"2022-02-03T01:25:41.163Z","time":"2022-02-03T01:25:41.163Z","version":"1.0.0-beta8"},"leaderboard-services":{"lastHeartbeat":"2022-02-03T01:25:41.165Z","name":"leaderboard_services","online":true,"time":"2022-02-03T01:25:41.165Z","version":"1.8.0","lastUpdate":"2022-02-03T01:25:41.165Z"},"notification-services":{"lastHeartbeat":"2022-02-03T01:25:41.167Z","name":"notification_services","online":true,"time":"2022-02-03T01:25:41.167Z","version":"1.7.0","lastUpdate":"2022-02-03T01:25:41.167Z"},"persona-services":{"lastHeartbeat":"2022-02-03T01:25:41.170Z","name":"persona_services","online":true,"time":"2022-02-03T01:25:41.170Z","version":"1.9.0","lastUpdate":"2022-02-03T01:25:41.171Z"},"progression-services":{"lastHeartbeat":"2022-02-03T01:25:41.173Z","name":"progression_services","online":true,"lastUpdate":"2022-02-03T01:25:41.173Z","time":"2022-02-03T01:25:41.173Z","version":"1.5.0"},"quest-services":{"lastHeartbeat":"2022-02-03T01:25:41.176Z","name":"quest_services","online":true,"lastUpdate":"2022-02-03T01:25:41.176Z","time":"2022-02-03T01:25:41.176Z","version":"1.5.0"},"scripting-services":{"lastHeartbeat":"2022-02-03T01:25:41.179Z","name":"scripting_services","online":true,"time":"2022-02-03T01:25:41.179Z","version":"1.7.0","lastUpdate":"2022-02-03T01:25:41.179Z"},"server-instance-services":{"lastHeartbeat":"2022-02-03T01:25:41.193Z","name":"server_instance_services","online":true,"time":"2022-02-03T01:25:41.193Z","version":"1.7.0","lastUpdate":"2022-02-03T01:25:41.193Z"},"session-services":{"lastHeartbeat":"2022-02-03T01:25:41.196Z","name":"session_services","online":true,"lastUpdate":"2022-02-03T01:25:41.196Z","time":"2022-02-03T01:25:41.196Z","version":"1.7.0"},"social-services":{"lastHeartbeat":"2022-02-03T01:25:41.198Z","name":"social_services","online":true,"lastUpdate":"2022-02-03T01:25:41.198Z","time":"2022-02-03T01:25:41.198Z","version":"1.5.0"},"telemetry-services":{"lastHeartbeat":"2022-02-03T01:25:41.200Z","name":"telemetry_services","online":true,"lastUpdate":"2022-02-03T01:25:41.200Z","time":"2022-02-03T01:25:41.200Z","version":"1.8.0"},"world-services":{"lastHeartbeat":"2022-02-03T01:25:41.202Z","name":"world_services","online":true,"time":"2022-02-03T01:25:41.202Z","version":"1.12.0","lastUpdate":"2022-02-03T01:25:41.202Z"}},"healthy":14,"offline":0,"total":14}

Additional Support
==================

Xsolla Backend offers commercial support at https://www.acceleratxr.com/pricing/ under Self-Hosted plans.