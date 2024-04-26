===================
Upgrading a Cluster
===================

When an update is available to one of the Xsolla Backend engine services you can apply the update with one of two methods. The first
method is to edit the deployment directly and set the desired version. The second method is to use `helm upgrade` to modify the
installation.

Quickstart
----------
1. Setup via `this powershell script <https://gitlab.acceleratxr.com/Core/tools/scripts/-/blob/main/kube-helm/%23helm-setup.ps1>`__.
2. Your service's git repo should have version++.
3. Your helm_charts repo should version++ within `values.yaml`.
4. Upgrade via

Pre-requisites
==============

via script:
-----------
Have everything installed for you via `this powershell script <https://gitlab.acceleratxr.com/Core/tools/scripts/-/blob/main/kube-helm/%23helm-setup.ps1>`__.

via manual setup:
-----------------
The following tools are required to follow this guide.

* `kubectl <https://kubernetes.io/docs/reference/kubectl/overview/>`_
* `helm <https://helm.sh/>`_
* helm repos:
    * ingress-nginx
    * bitnami
    * bokysan
    * jetstack
    * prometheus-community
    * cortex-helm

Editing the Deployment
======================

The simplest way to upgrade an Xsolla Backend engine service is to edit the deployment directly. This is often useful when only
upgrading a single service at a time.

In a terminal run the following `kubectl` command.

.. code-block:: bash

    kubectl -n <namespace> edit deploy <service-name>

For our example we'll upgrade the `server-instance-services` system.

.. code-block:: bash

    kubectl -n axr-demo-v1 edit deploy server-instance-services

In the editor look for the line that starts with `image:`. At the end will be a version number like `v1.0.0`. Change it to the desired new version you want to deploy and save.

.. image:: /images/admin/upgrade_service_edit_deploy.png

Once you have edited the deployment you can monitor the pods as the upgrade happens. The system will first create a new pod with new version, leaving the original running. Once
the new pod is running.

.. image:: /images/admin/upgrade_service_pod_deploy.png

Once the new pod is verified as working the system will shut down the old pod. This ensures no gap in service during the upgrade process.

.. image:: /images/admin/upgrade_service_pod_deploy2.png

Using Helm Upgrade
==================

The recommended method to update any Xsolla Backend engine service is to use `helm upgrade`.
The primary benefit of this approach is that it allows you to better track which versions of
the system have been deployed. This helps if the cluster ever needs to be rebuilt.

First open the `values.yaml` file that was used to install the Xsolla Backend cluster in the first place.
Look for the section for the service in question and change the version value to the one desired.
Then save the file.

.. code-block:: yaml

    server_instance_services:
      enabled: true
      version: v1.3.0
      config:
        # Override any environment variables here (e.g. admin_user__name)

Upgrade via Script
------------------

Have everything upgraded for you via `this powershell script <https://gitlab.acceleratxr.com/Core/tools/scripts/-/blob/main/kube-helm/%23helm-upgrade.ps1>`__.

Upgrade via Manually Setup
--------------------------

Now run the `helm upgrade` command as in the following example -- or use our `helm upgrade script <>`__.

.. code-block:: bash

    helm upgrade axr-demo-v1 -f values.yaml . \
        --namespace axr-demo-v1

When the upgrade is complete you'll get a similar output as you did when you first installed the cluster.

The system will first create a new pod with new version, leaving the original running. Once the new pod is running.

.. image:: /images/admin/upgrade_service_pod_deploy.png

Once the new pod is verified as working the system will shut down the old pod. This ensures no gap in service during the upgrade process.

.. image:: /images/admin/upgrade_service_pod_deploy2.png