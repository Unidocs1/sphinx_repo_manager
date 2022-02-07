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

Installation of the Unreal SDK is simple.

1. Clone the repository to your project's Plugins folder.
   
   .. code-block:: bash
    
    git clone git@gitlab.acceleratxr.com:Core/sdk/sdk_unreal.git AcceleratXR

2. Run the corresponding ``start`` script for your supported platform.

   For Linux...

   .. code-block:: bash

    ./setup.sh

   For Windows...

   .. code-block:: powershell

    .\setup.ps1

3. Add the desired plug-ins to project's ``uproject`` file.

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

4. Set ``AXR`` as the default OnlineSubsytem in ``DefaultEngine.ini``.

   .. code-block:: ini

    [OnlineSubsystem]
    DefaultPlatformService=AXR

That's it!

To learn more about how to work with these plug-ins check out the `Unreal ShooterGame <../examples/shootergame.html>`_ project.