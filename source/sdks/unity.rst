================
Unity Engine SDK
================

The AcceleratXR SDK for Unity provides a simple wrapper around the :doc:`C# SDK <csharp>` in addition to prefabs and
basic scripts included to make the process of working with the platform easier.

Installation
============

There are two methods to import the SDK into your Unity project.

#. Link teh repository directly via the ``manifest.json`` file. **[RECOMMENDED]**
#. Clone the repo and link from a local disk path

Linking Directly
~~~~~~~~~~~~~~~~

#. Close the project or Unity editor if currently open.
#. Open the ``Packages/manifest.json`` file in your favorite text editor.
#. Add the following line to the ``dependencies`` set.
   
   .. code-block:: json

       {
           "dependencies": {
               // (!) MAINTENANCE: These credentials will be changed ASAP.
               "com.acceleratxr.sdk": "https://TODO:TODO@gitlab.acceleratxr.com/Core/sdk/sdk_unity.git"
           }
       }
#. Open your project in the Unity editor.

Linking from the Local Disk
~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Clone the repository to your local machine.
   
   .. code-block::

       git clone https://gitlab.acceleratxr.com/Core/sdk/sdk_unity.git

#. Open your project in the Unity editor.
#. Open the Package Manager (e.g. ``Windows -> Package Manager``).
#. Click the ``+`` button in the top left corner.
#. Select ``Add package from disk...``.
#. Browse to the folder that you have cloned the SDK and click **Open**.

Configuration
=============

In order for your game or application to communicate with an AcceleratXR cluster you must first configure the SDK plug-in. This can be accomplished by creating a new Asset of type ``AXRCoreSDK``. Simply go to ``Assets -> AcceleratXR -> Core SDK``. This will create a new ScriptableObject asset in your project. Once created you will see an inspector window with the settings you will need to configure.

The most important setting is *BaseUrl*. This is the URL to your AcceleratXR cluster that your app will communicate with.

The *JWT* settings are optional and only needed if you will be using the ``ClientSDK.LocalLogin()`` function. The *JWT Settings* section and ``LocalLogin`` function is provided for debugging purposes and is not recommended for production use. For production builds make sure that the *JWTPassword* field is blank.

In order to make sure that your configuration is properly loaded once you make a build you will need to add it to the ``Preloaded Assets`` list. Go to the ``Player Settings -> Other Settings -> Preloaded Assets``. Expand the list and add an entry, then link the asset you created.

### Using the AcceleratXR Demo Environment

You can use the following settings to utilize AcceleratXR's demo environment.

.. code-block::

    Global Settings
    URL: https://api.demo.goaxr.cloud/v1

    JWT Settings
    Audience: demo.goaxr.cloud
    Issuer: api.demo.goaxr.cloud
    Password:

Note that the demo environment has a limited feature set that will result in run-time failures when using certain SDK services.

Updating the SDK
================

Remote Git Link
~~~~~~~~~~~~~~~

If you linked the SDK directly in the ``manifest.json`` file then simply remove the entry for ``com.acceleratxr.sdk`` from the ``lock`` section located at the bottom of the file. An example of this section is shown below.

.. code-block::

    "lock": {
        "com.acceleratxr.sdk": {
        "hash": "408992aad7ff1a14bff5e5c5cca3a41b74a14d13",
        "revision": "HEAD"
        }
    }

Once removed, save the file and restart the Unity editor. The latest version of the plug-in will be automatically downloaded and installed.

Local Path
~~~~~~~~~~

If you cloned the repo locally you can update the SDK by performing a ``git pull`` on the folder that you have cloned this repository to. You do not need to restart the Unity Editor for changes to take effect.

Accessing the SDK from Code
===========================

The instance of the ``AXRCoreSDK`` asset can be easily accessed from anywhere in your code.

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

Multiple User Support
=====================

The SDK supports multiple users through the creation of multiple AXRCoreSDK assets. This can be useful when developing a game that supports split-screen multi-player.

For example if you want to support two-player split-screen where each player has their own login to AcceleratXR this can be easily accomplished by creating two asset instances of AXRCoreSDK.

To access these instances use the name of the asset when calling ``AXRCoreSDK.GetInstance()`` as shown in the example below.

.. code-block::

    using axr.sdk;
    using UnityEngine;

    public class PlayerOneBehavior : MonoBehaviour
        void Start()
        {
            AXRCoreSDK SDK = AXRCoreSDK.GetInstance("PlayerOne");
            if (SDK != null)
            {
                CoreSDK = SDK.Instance;
                EntityWatchdog = SDK.EntityWatchdog;
                ServiceFactory = SDK.ServiceFactory;
            }
        // ...
        }
    }
