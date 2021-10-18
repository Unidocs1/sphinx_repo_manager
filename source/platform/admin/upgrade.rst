===================
Upgrading a Cluster
===================

When an update is available to one of the AcceleratXR platform services you can apply the update with one of two methods. The first
method is to edit the deployment directly and set the desired version. The second method is to use `helm upgrade` to modify the
installation.

Pre-requisites
==============

The following tools are required to follow this guide.

* `kubectl <https://kubernetes.io/docs/reference/kubectl/overview/>`_
* `helm <https://helm.sh/>`_

Editing the Deployment
======================

The simplest way to upgrade an AcceleratXR platform service is to edit the deployment directly. This is often useful when only
upgrading a single service at a time.

In a terminal run the following `kubectl` command.

.. code-block:: bash

    kubectl -n <namespace> edit deploy <service-name>

For our example we'll upgrade the `server-instance-services` system.

.. code-block:: bash

    kubectl -n axr-demo-v1 edit deploy server-instance-services

In the editor look for the line that starts with `image:`. At the end will be a version number like `v1.0.0`. Change it to the desired new version you want to deploy and save.

.. image:: /images/admin/uprade_service_edit_deploy.png

Once you have edited the deployment you can monitor the pods as the upgrade happens. The system will first create a new pod with new version, leaving the original running. Once
the new pod is running.

.. image:: /images/admin/uprade_service_pod_deploy.png

Once the new pod is verified as working the system will shut down the old pod. This ensures no gap in service during the upgrade process.

.. image:: /images/admin/uprade_service_pod_deploy2.png

Using Helm Upgrade
==================

The recommended method to update any AcceleratXR platform service is to use `helm upgrade`. The primary benefit of this approach is that it allows you to
better track which versions of the system have been deployed. This helps if the cluster ever needs to be rebuilt.

First open the `values.yaml` file that was used to install the AcceleratXR cluster in the first place. Look for the section for the service in question
and change the version value to the one desired. Then save the file.

.. code-block:: yaml

    server_instance_services:
      enabled: true
      version: v1.3.0
      config:
        # Override any environment variables here (e.g. admin_user__name)

Now run the `helm upgrade` command as in the following example.

.. code-block:: bash

    helm upgrade axr-demo-v1 -f values.yaml . \
        --namespace axr-demo-v1

When the upgrade is complete you'll get a similar output as you did when you first installed the cluster.

The system will first create a new pod with new version, leaving the original running. Once the new pod is running.

.. image:: /images/admin/uprade_service_pod_deploy.png

Once the new pod is verified as working the system will shut down the old pod. This ensures no gap in service during the upgrade process.

.. image:: /images/admin/uprade_service_pod_deploy2.png