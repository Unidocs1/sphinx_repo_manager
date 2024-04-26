================
Unity Engine SDK
================

The `Xsolla Backend SDK for Unity <https://gitlab.acceleratxr.com/Core/sdk/sdk_unity/>`__ provides
a simple wrapper around the :doc:`C# SDK <csharp>` in addition to prefabs and basic scripts
included to make the process of working with the platform easier.

Looking for a Unity Demo?
========================= 

Want something that works out of the box? Check out the `example_unity repo <https://gitlab.acceleratxr.com/Core/samples/example_unity>`__.

Prerequisites
=============

This plug-in requires the following:

1. **Unity 2021.3+ LTS** or newer.

Installation
============

There are two ways to import the SDK into your project...

* Option 1: Install From Git URL *[Recommended]*
* Option 2: Clone The Repo and Install From Local Disk

Option 1: Install From Git URL *[Recommended]*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open your project in Unity and navigate to the Package Manager window (`Windows > Package Manager`).
2. In the `Package Manager` window click the `+` button in the top left corner and select `Add package from git URL...`
3. Enter the following URL into the text box and click `Add`.

  .. code-block:: text
   
    https://unity:4sWpuQS6dnuSqa-Ki_nV@gitlab.acceleratxr.com/Core/sdk/sdk_unity.git

4. *Xsolla Backend SDK* should now be listed in the package manager.
5. Next follow the section on Configuration.

Option 2: Clone The Repo and Install From Local Disk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the `sdk_unity` repo to your local machine.

  .. code-block:: text
  
    git clone https://gitlab.acceleratxr.com/Core/sdk/sdk_unity.git

2. Open your project in Unity and navigate to the Package Manager window (`Windows > Package Manager`).
3. In the `Package Manager` window click the `+` button in the top left corner and select `Add package from disk...`
4. Browse to the root folder of your local `sdk_unity` checkout, select the `package.json` file, and click `Open`.
5. *Xsolla Backend SDK* should now be listed in the package manager.
6. Next follow the section on Configuration.

WebGL - Additional Steps
~~~~~~~~~~~~~~~~~~~~~~~~

The Xsolla Backend SDK for Unity supports WebGL, however there are a few additional steps required to enable the SDK to work properly in a WebGL build.

1. Install the `WebGL Threading Patcher` package to enable async tasks to function properly in WebGL builds. Go to the `Package Manager`, select `Add package from git URL...`, and enter the follwing URL:
  
  .. code-block:: text

    https://github.com/VolodymyrBS/WebGLThreadingPatcher.git

2. Go to `Project Settings > Player Settings` and make the following changes under the `WebGL` tab:

   -  In `Other Settings`, set `Managed Stripping Level` to `Minimal` to prevent code stripping from making Newtonsoft unable to deserialize JWT.Builder models.
   -  In `Publishing Settings` set `Enable Exceptions` to `Full Without Stacktrace` and also uncheck the `Data Caching` checkbox.

Configuration
=============

In order for your game or application to communicate with an Xsolla Backend cluster you must first create a configuration asset to configure the SDK. This can be accomplished by creating a new Asset of type `AXRCoreSDK` by selecting `Assets > Create > Xsolla Backend > Core SDK`. Once created, you will see the new object selected in the `Project` window and the configuration options shown in the `Inspector` window.

The most important setting is *BaseUrl*. This is the URL to your Xsolla Backend cluster that your app will communicate with.

The *JWT* settings are optional and only needed if you will be using the `ClientSDK.LocalLogin()` function. The *JWT Settings* section and `LocalLogin` function is provided for debugging purposes and is not recommended for production use. For production builds make sure that the *JWTPassword* field is blank.

The default values in the `AXRCoreSDK` asset correspond to the Xsolla Backend demo environment.

Using the Xsolla Backend Demo Environment
======================================

You can use the following settings to access Xsolla Backend's demo environment. This environment is a shared environment that is reset daily and is intended for testing purposes only. You can use the demo environment to test your integration with the Xsolla Backend API before deploying your own cluster.

  .. code-block:: text

    Global Settings
    URL: https://api.demo.goaxr.cloud/v1

    JWT Settings
    Audience: demo.goaxr.cloud
    Issuer: api.demo.goaxr.cloud
    Password:

You can access the web admin console for the demo environment at `https://console.demo.goaxr.cloud <https://console.demo.goaxr.cloud>`__ with the followng credentials:

- Username: **admin**
 
- Password: **@xrD3m0!**


*Note that the demo environment has a limited feature set that will result in
run-time failures when using certain SDK services.*

Using an AXRCoreSDK Configuration To Access The API
===================================================

Assign your desired AXRCoreSDK configuration asset to a field on a behavior or scriptable object that's referenced in your scene, and use the Instance property to access the CoreSDK features. The Instance property on AXRCoreSDK will always return the same reference for a given AXRCoreSDK asset.

  .. code-block:: csharp

    using axr.sdk; // Required for AXRCoreSDK, base Object, and other SDK types
    using axr.sdk.Models; // Required models such as User below
    using axr.sdk.Services; // Required for Services such as SessionService below
    using System.Linq; // Not required, but used below for Linq where clause as an example
    using UnityEngine; // Required for MonoBehaviour

    public class AXRExample : MonoBehaviour
    {
        // Assign in the inspector
        public AXRCoreSDK config;

        async void Start()
        {
            // Validate config is set
            if (config == null)
            {
                // Warn if no configuration is set
                Debug.LogWarning($"WARNING: AXRCoreSDK config not set!");
                return;
            }

            // Get core SDK instance from configuration
            CoreSDK sdk = config.Instance;

            // Print DeviceId (set) and logged in user UID (null)
            Debug.Log($"Device: {sdk.DeviceId} | User: {sdk.LoggedInUser?.Uid}");

            // Login using Device method
            await sdk.LoginDevice();

            // Print DeviceId (set) and logged in user UID (now set!)
            Debug.Log($"Device: {sdk.DeviceId} | User: {sdk.LoggedInUser?.Uid}");

            // Logged in user now non-null, let's inspect..
            User localUser = sdk.LoggedInUser;

            // Walk each property on the logged in user's object and print the value
            foreach (var prop in localUser.Properties.Keys)
                Debug.Log($"\t{prop}: {localUser.GetProperty(prop)}");

            // Get the session service
            var sessionService = sdk.GetService<SessionService>();

            // Find all sessions
            var sessions = await sessionService.FindAll();

            // Filter results locally to non-empty sessions with Linq
            var sessionsNonEmpty = sessions.Where(s => s.Users.Count() > 0).ToList();

            // Print sessions found
            Debug.Log($"Sessions found: {sessions.Count} ({sessionsNonEmpty.Count} non-empty)");

            // Print info from each session
            sessionsNonEmpty.ForEach(s =>
                Debug.Log($"\t{s.Type}\t{s.Status}\t({s.Users.Count})\th:{s.HostUid}\ts:{s.ServerUrl ?? "NONE"}"));
        }
    }

Enabling and Running Tests
==========================

The SDK includes a suite of unit tests that can be run from within Unity. To enable the tests you must first add the `com.unity.test-framework` package at version `1.4.1` or greater to your project. To add or upgrade the package from the package manager:

#. Open the `Package Manager` window (`Windows > Package Manager`) and clicking the `+` button in the top left corner.
#. Select *Add package by name...*
#. Set the `Name` field to *com.unity.test-framework*.
#. Set the `Version` field to *1.4.1* or greater.
#. Click `Add`.

Open your project's `Packages/manifest.json`, verify that the `com.unity.test-framework` package is listed in the `dependencies` section with an appropriate version, and add the `com.acceleratxr.sdk` package name to the `testables` array as shown below. Save the file and return to Unity.

  .. code-block:: json

    {
        "dependencies": {
            "com.acceleratxr.sdk": "...",
            // ...
            "com.unity.test-framework": "1.4.1",
            // ...
        },
        "testables": [
            "com.acceleratxr.sdk"
        ]
    }


*Note that the `com.unity.test-framework` package may be installed by default at a lower version, please make sure you verify the version number and upgrade if necessary or the tests will not run properly.*

Once the `com.acceleratxr.sdk` package has been added to the `testables` list, you can open the `Test Runner` window (`Windows > General > Test Runner`) and run the tests from the package by clicking the `Run All` button at the bottom right of the window, or by double-clicking on a particular test or group.

You can right click any test and select `Open Source Code` to load the test code in your IDE, where you can sample from various use cases or debug any integration issues you might be experiencing.
