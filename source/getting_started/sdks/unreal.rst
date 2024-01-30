=================
Unreal Engine SDK
=================

The AcceleratXR SDK for Unreal is compatible with Unreal Engine 4.25 and above. The SDK is broken up
into three plug-ins; **AXRCoreSDK**, **OnlineSubsystemAXR** and **GameFrameworkAXR**.

AXRCoreSDK
==========

The **AXRCoreSDK** plug-in is a wrapper for the C++ SDK. It does not provide any direct functionality other than
enabling a means of compiling and exposing the C++ SDK to Unreal.

OnlineSubsystemAXR
==================

The **OnlineSubsystemAXR** plug-in provides an implementation of the
`OnlineSubsystem <https://docs.unrealengine.com/4.26/en-US/ProgrammingAndScripting/Online/>`_ interfaces designed to
work with the AcceleratXR platform. The plug-in supports a variety of platform features including:

* Authentication
* Achievements
* Economy
* Leaderboards
* Matchmaking
* Missions / Quests
* Personas
* Progression
* Sessions
* Social

GameFrameworkAXR
================

The **GameFrameworkAXR** plug-in offers higher level gameplay implementation of common online and multi-player
functionality.

Some important features include:

* Dedicated server registration
* Automatic session management
* Automatic shard management (Virtual World System)

Installation
============

Installation of the Unreal plugins is simple...

1. Clone the repository to your project's Plugins folder.

From your project root directory:

    .. code-block:: bash

        cd Plugins
        git clone https://unreal:_9EZ7XzLBuzBb_ctT1yS@gitlab.acceleratxr.com/Core/sdk/sdk_unreal.git AcceleratXR

2. Run the corresponding ``start`` script for your supported platform.

For Linux...

    .. code-block:: bash
        
        cd AcceleratXR
        ./setup.sh

For Windows...

    .. code-block:: powershell

        cd AcceleratXR
        .\setup.ps1

1. Add the desired plug-ins to your project's ``.uproject`` file at the root directory.

    .. code-block:: json

        {
            "Name": "AXRCoreSDK",
            "Enabled": true
        },
        {
            "Name": "OnlineSubsystemAXR",
            "Enabled": true
        },
        {
            "Name": "GameFrameworkAXR",
            "Enabled": true
        }

2. Set ``AXR`` as the default OnlineSubsytem in ``Config/DefaultEngine.ini``.

    .. code-block:: ini

        [OnlineSubsystem]
        DefaultPlatformService=AXR

3. Launch the project by double clicking the ``.uproject`` file or by launching it from the Epic Games Launcher.

    *Note: If prompted to rebuild missing modules, click 'Yes' and wait for the project to load.*

That's it! If your project supports the ``OnlineSubsystem`` interface, you should now be using AcceleratXR user login and session management on the AXR demo environment.

You can access the web admin console for the demo environment at `https://console.demo.goaxr.cloud <https://console.demo.goaxr.cloud>`__ with the followng credentials:

- Username: **admin**
 
- Password: **@xrD3m0!**

To learn more about how to work with these plug-ins check out the `Unreal ShooterGame <../examples/shootergame.html>`_ project.

