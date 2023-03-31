============
Installation
============

.. toctree::
   :maxdepth: 1

   prerequisites
   onprem_helm
   onprem_operator
   aws_helm
   aws_operator

The AcceleratXR backend platform can be easily installed anywhere that Kubernetes operates.

Two methods of installation are provided.

* Helm Chart
* Operator for Kubernetes

AcceleratXR Helm Chart
======================

A `Helm chart <https://helm.sh/>`_ is a package for deploying a set of Kubernetes resources. The AcceleratXR Helm Chart makes it easy to deploy
a production ready platform in a matter of minutes and provides complete configuration over every part of the system.

* :doc:`Installation On-Premises with Helm <onprem_helm>`
* :doc:`Installation for Amazon Web Services using Helm <aws_helm>`

AcceleratXR Operator for Kubernetes
===================================

A `Kubernetes Operator <https://kubernetes.io/docs/concepts/extend-kubernetes/operator/>`_ is a special container that runs in the Kubernetes
cluster that is capable of managing custom resource definitions (CRDs). The AcceleratXR Operator for Kubernetes is used to manage `acceleratxr.com/Cluster`
resources. A `Cluster` resource defines a fully functional AcceleratXR platform including all databases, service pods, metrics servers and more.

* :doc:`Installation On-Premises with Operator <onprem_operator>`
* :doc:`Installation for Amazon Web Services using Operator <aws_operator>`