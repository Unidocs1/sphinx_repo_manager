===================
Restaring a Cluster
===================

Pre-requisites
==============

The following tools are required to follow this guide.

* `kubectl <https://kubernetes.io/docs/reference/kubectl/overview/>`_

Restarting the Platform
=======================

Sometimes it's necessary to restart all of the platform services in an AcceleratXR cluster. This can be easily done using the `kubectl delete pod`
command. AcceleratXR tags each service pod with a special label so that you can perform such operations against only the platform itself.


.. code-block:: bash

    kubectl delete pods -ltype=platform

The output of this operation will look like the following.

.. image:: /images/admin/restart_delete_pods.png

From the admin console you can then watch the progress as each platform service is restarted.

.. image:: /images/admin/restart_service_health.png

Restarting Everything
=====================

In extreme circumstances it may be desirable to restart everything within a given cluster's namespace. To do this run the command.

.. code-block:: bash

    kubectl delete pods --all

To monitor the progress of this operation it is best to run the `get pods` command with the `-w` flag as shown below.

.. code-block:: bash

    kubectl get pods -w
    
.. image:: /images/admin/restart_get_pods_watch.png