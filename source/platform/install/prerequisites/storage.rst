==================
Persistent Storage
==================

AcceleratXR utilizes multiple database servers to function. Each micro-service manages its own database, leveraging the
database technology best suited for its intended purpose. The databases used by the platform are:

* `MongoDB <https://www.mongodb.com/>_`
* `Redis <https://redis.com/>_`

As Kubernetes is inherently a stateless container platform it is necessary to setup an Container Attached Storage (CAS)
system in order for the required databases to function correctly and be able to scale to tens of millions of users.

Many Kubernetes distrobutions provide support for persistent storage out of the box and do not require additional
third-party software to be installed. Public cloud providers such as AWS, Azure and GCP all provide scalable and
performant storage support.

Many on-premises Kubernetes and DIY distrobutions such as k3s, microk8s and so on also feature persistent storage
support out of the box, often called hostpath or local storage. Hostpath and local storage however is not scalable
and will only work for single-node Kubernetes clusters. For multi-node and production clusters one of the following
container attached storage providers must be installed.

Mayastor
========

Ondat
=====



Portworx
========

Before you can install Portworx you will need additional hard disks installed to your on-premises server that are
**unformatted** and **unmounted**. These disks will serve as the storage devices Portworx will use.

In order to install Portworx you must first create a new spec with the
`Portworx Central Dashboard <https://central.portworx.com/>`_. For production deployments it is recommended to use
Portworx Enterprise, for all others Portworx Essentials is sufficient.

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
