===============
Troubleshooting
===============

This article discusses common problems that you may experience in managing an AcceleratXR platform cluster and how to solve them.

Service **X** failed to start with a compilation error.
=======================================================

On occassion you may experience script compilation errors when starting up a service. This may occur immediately after upgrading
or downgrading a particular service to a different version. The service pod log may look like the following.

.. image:: /images/admin/trouble_compile_error.png

The exact cause of the compilation error is varied but most often it is a result of the live scripting system failing to properly
merge changes between version changes. This typically occurs more often during downgrade operations.

To fix the issue it is necessary to fix the script database. This can be done one of two ways; delete the latest entry of the
named script (safest approach) or delete the entire `script_mongo` collection and let the service recreate it.

Often the second approach is the easiest and most likely method to repair the problem. However if changes have been made to the
service via the live scripting system then this option may not be feasible.

First port-forward the service's accompanying database so that you can connect to it to access it's records.

Next pull up the `script_mongo` collection or table for the service in question. For our above example that's located in the
`server_instance_static` database.

.. image:: /images/admin/database_view_script_mongo.png

If you are removing an individual record, you can search for it and delete it using the MongoDB Compass tool. However for this example
we'll assume there is nothing to preserve and so we'll delete the whole collection and let the service recreate it.

.. image:: /images/admin/database_drop_script_mongo.png

Once the collection has been dropped you can restart the service's pod by executing the `kubectl delete pod` command.

.. code-block:: bash

    kubectl -n axr-demo-v1 delete pod -lapp=server-instance-services

After the service's pod finishes the restart process everything should be repaired and working correctly.