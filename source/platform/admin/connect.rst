===================
Accessing a Cluster
===================

Pre-requisites
==============

The following tools are required to follow this guide.

* `kubectl <https://kubernetes.io/docs/reference/kubectl/overview/>`_

.. note::
    AcceleratXR *Cloud* customers can request Kubernetes access by submitting a support request. Access may require a separate VPN connection.

Overview
========

Accessing an AcceleratXR platform cluster for administration purposes can either be done using the AcceleratXR Admin Console or directly
managed using Kubernetes. In order to adminster the cluster using Kubernetes the *kubeconfig* file used to install the cluster will be
needed.

Checking System Health
======================

Using Admin Console
~~~~~~~~~~~~~~~~~~~

Checking the system health with the AcceleratXR Admin Console is incredibly easy. Simply log in to your cluster and the dashboard page will show
you the health of all deployed services as well as their currently deployed versions. This is the simplest way to check the health of your cluster.

.. image:: /images/admin/system_health_admin_console.png

Using Kubernetes
~~~~~~~~~~~~~~~~

It's very easy to check the system health of an AcceleratXR cluster using Kubernetes' `kubectl` tool. This is done simply with the `kubectl get pods` command.

.. code-block:: bash

    kubectl -n axr-demo-v1 get pods

The above command will display the system health of the AcceleratXR cluster installed to the `axr-demo-v1` namespace.
In this example we are checking the official AcceleratXR demo environment. The result should look like the following.

.. image:: /images/admin/system_health.png

If everything is running correctly you should see at least one pod for each system service in the **Running** state. You will also see
additional pods such as the various databases and monitoring systems.