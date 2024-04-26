=====================
Live Scripting System
=====================

The Live Scripting System is one of the most exciting features of the Xsolla Backend engine and service framework. The
system allows for any code published within a given service to be modifiable in real-time using the REST API. This
gives developers tremendous power and flexibility to alter the behavior of an existing Xsolla Backend backend without
needing to fork, build, publish and deploy services.

The system works by implementing Source Code Management (SCM) principles. On service startup, all of the code that is
pre-packaged with the service is loaded into memory and stored in a special database, before the server performs any
initialization. The system then compiles the code stored in the database back to disk in order to continue with
server initialization and setup.

The stored files from the database are then exposed via REST API. When you make a modification to a given file using
this REST API the changes are compiled for verification and stored in the database as a new unique version. If the file
is then set to publish the service restarts and loads the modified file.

At some point the service will likely need to be upgraded to a new version as provided by Xsolla Backend. During the upgrade process
any modified files stored in the database are merged with the latest official release. If there are no merge conflicts or
compilation errors after the upgrade the script is automatically marked as published and is loaded along with the rest
of the changes during server startup.

You can interface with the Live Scripting System in one of the following two ways:

Xsolla Backend Admin Console
=========================

.. image:: /images/admin/console_live_scripting_editor.png

The Xsolla Backend Admin Console features a complete integrated code editor and interface for working with the Live Scripting System.
Simply select *Live Scripting* from the menu bar on the left and select the backend service you want to modify from the drop-down
menu. Once connected, you can browse all of the pre-bundled code that ships with the service by default as well as add new files
and folders as desired.

Xsolla Backend Script Manager
==========================

.. image:: /images/tutorials/scripting/part1_diagram1.png

The Xsolla Backend Script Manager is a plug-in for `Visual Studio Code <https://code.visualstudio.com/>`. The plug-in implements the
REST API as a SCM provider that makes working with the system feel native like any other SCM such as Git.

For a complete guide on how to work with the Live Scripting System using Script Manager read the :doc:`Live Scripting Tutorial </tutorials/scripting/part1>`.