================
Unity Engine SDK
================

The `AcceleratXR SDK for Unity <https://gitlab.acceleratxr.com/Core/sdk/sdk_unity/>`__ provides
a simple wrapper around the :doc:`C# SDK <csharp>` in addition to prefabs and basic scripts
included to make the process of working with the platform easier.

Looking for a Unity Demo?
========================= 

Want something that works out of the box? Check out the `example_unity repo <https://gitlab.acceleratxr.com/Core/samples/example_unity>`__.

Pre-Requisites
==============

This plug-in requires that you have the following settings for your project.

1. **Api Compatibility Level:** ``.NET 4.x``
2. Unity 2019+ LTS (2021.3 LTS == currently recommended)

Installation
============

There are two options to import the SDK into your Unity project: 

#. Link the repository directly via the ``manifest.json`` file. [RECOMMENDED]
#. Clone the repo and link from a local path.

Linking Directly via Manifest [RECOMMENDED]
~~~~~~~~~~~~~~~~

#. Close the project or Unity editor, if currently open.
#. Open your project root ``Packages/manifest.json`` file.
#. Add the following ``scopedRegistries`` and ``dependencies``:

  // The example below specifies ``2021-lts`` branch. Browse `other supported versions <https://gitlab.acceleratxr.com/Core/samples/example_unity/-/branches>`__.
   
   .. code-block:: json

    {
        "dependencies": {
            "com.acceleratxr.sdk": "https://unity:4sWpuQS6dnuSqa-Ki_nV@gitlab.acceleratxr.com/Core/sdk/sdk_unity.git#2021-lts"
        }
    }
    
#. Open your project in the Unity editor.

Linking from a Local Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Clone the repo to your local machine.
   
   .. code-block::

       git clone https://gitlab.acceleratxr.com/Core/sdk/sdk_unity.git

#. Open your project in the Unity editor.
#. Open the Package Manager: ``[Top Menu] Windows -> Package Manager``.
#. Click the ``[ + ]`` button in the top-left corner -> ``Add package from disk..``
#. Browse to the cloned dir containing the SDK -> ``Open``.

Configuration
=============

#. Create ``AXRCoreSDK`` <ScriptableObject> via right-click context menu in Project tab:
  .. image:: /images/samples/unity_create_coresdk.png

#. This is your settings file -> Edit to match your server info: Most notably, your `BaseUrl`:
  .. image:: /images/samples/unity_example_coresdk_inspector.png

  \* Leave ``JWT`` empty, unless debugging with ``ClientSDK.LocalLogin()``.

#. To init AXR:
    #. Make a `AxrManager` prefab and place it in your 1st scene.
    #. Add a new `AxrMgr.cs` script to the prefab.
    #. Serialize the AXRCoreSDK settings ScriptableObject created earlier.

#. Start your scene -> check logs for success.

Using the AcceleratXR Demo Environment
======================================

Creating a new AXRCoreSDK ScriptableObject creates the following default settings,
pointing to the `demo env (web dashboard) <https://console.demo.goaxr.cloud/>`__:

.. code-block::

    Global Settings
    URL: https://api.demo.goaxr.cloud/v1

    JWT Settings
    Audience: demo.goaxr.cloud
    Issuer: api.demo.goaxr.cloud
    Password:

(Note that the demo environment has a limited feature set that will result in
run-time failures when using certain SDK services.)

Updating the SDK
================

Remote Git Link
~~~~~~~~~~~~~~~

If you linked the SDK directly in the ``manifest.json`` file, simply update it within the ``Unity Package Manager (UPM)``:

  .. image:: /images/samples/unity_pkg_mgr.png

Once updated, restart the Unity editor (to refresh the DLL bindings) to finalize the update.

Local Path
~~~~~~~~~~

If you cloned the repo locally you can update the SDK by performing a ``git pull`` on the folder
that you have cloned this repository to.
Once updated, restart the Unity editor (to refresh the DLL bindings) to finalize the update.

Accessing the SDK from Code
===========================

The instance of the ``AXRCoreSDK`` asset can be easily accessed from anywhere in your code:

.. code-block::

    using axr.sdk;
    using UnityEngine;

    public class MyBehavior : MonoBehaviour
        void Start()
        {
            AXRCoreSDK SDK = AXRCoreSDK.GetInstance();
            if (SDK != null)
            {
                CoreSDK = SDK.Instance;
                EntityWatchdog = SDK.EntityWatchdog;
                ServiceFactory = SDK.ServiceFactory;
            }
        // ...
        }
    }

💡For convenience, an `AxrMgr.cs <https://gitlab.acceleratxr.com/Core/samples/example_unity/-/blob/master/Assets/%23Setup/Scripts/AxrMgr.cs>`__
template is already made for you from our `example_unity <https://gitlab.acceleratxr.com/Core/samples/example_unity>`__ project!
Drop this in any GameObject in your 1st scene and serialize your selected AxrManager's AXRCoreSDK.

Multi-User Support
=====================

The SDK supports multiple users through the creation of multiple AXRCoreSDK assets.
This can be useful when developing a game that supports split-screen multiplayer.

For example, if you want to support two-player split-screen - where each player has their own login to AcceleratXR -
this can easily be accomplished by creating two asset instances of AXRCoreSDK.

To access these instances, use the name of the asset when calling ``AXRCoreSDK.GetInstance()``:

.. code-block::

    using axr.sdk;
    using UnityEngine;

    public class PlayerOneBehavior : MonoBehaviour
        void Start()
        {
            AXRCoreSDK SDK = AXRCoreSDK.GetInstance("PlayerOne"); // << Here
            if (SDK != null)
            {
                CoreSDK = SDK.Instance;
                EntityWatchdog = SDK.EntityWatchdog;
                ServiceFactory = SDK.ServiceFactory;
            }
        // ...
        }
    }
