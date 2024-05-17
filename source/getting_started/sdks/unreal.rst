=================
Unreal Engine SDK
=================

The Xsolla Backend SDK for Unreal is compatible with Unreal Engine 4.25 and above. The SDK is broken up
into three plug-ins; **AXRCoreSDK**, **OnlineSubsystemAXR** and **GameFrameworkAXR**.

AXRCoreSDK
==========

The **AXRCoreSDK** plug-in is a wrapper for the C++ SDK. It does not provide any direct functionality other than
enabling a means of compiling and exposing the C++ SDK to Unreal.

OnlineSubsystemAXR
==================

The **OnlineSubsystemAXR** plug-in provides an implementation of the
`OnlineSubsystem <https://docs.unrealengine.com/4.26/en-US/ProgrammingAndScripting/Online/>`_ interfaces designed to
work with the Xsolla Backend engine. The plug-in supports a variety of platform features including:

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

1. Navigate to the root directory of your Unreal Project, open a command prompt (Cmd Terminal or PowerShell window) and use the cd command followed by the path to your project directory. For example:
    .. code-block:: bash

        cd Path/To/Project

2. You can use the mkdir command to create the Plugins folder if it doesn't already exist. Additionally, you can set read, write, and execute permissions for everyone using the -m 777 flag. Here's the command:

    .. code-block:: bash

        mkdir -m 777 -p Plugins

This command will create the Plugins folder with the specified permissions if it doesn't already exist. If the folder already exists, it will simply set the permissions accordingly.

3. Once the Plugins directory is created (or if it already exists), navigate into it using the cd command:

    .. code-block:: bash

        cd Plugins

4. Now, clone the repository containing the Unreal plugins into your project's Plugins folder. Use the git clone command followed by the repository URL. For example:

    .. code-block:: bash
    
        git clone https://unreal:_9EZ7XzLBuzBb_ctT1yS@gitlab.acceleratxr.com/Core/sdk/sdk_unreal.git Xsolla Backend

This command will clone the repository into a directory named AcceleratXR within your Plugins folder.

Setup
============
1. Navigate into the AcceleratXR directory and run the appropriate setup script for your platform. For Linux, execute setup.sh, and for Windows, execute setup.ps1. For example:

For Linux...

    .. code-block:: bash
        
        cd Xsolla Backend
        ./setup.sh

For Windows...

    .. code-block:: powershell

        Set-ExecutionPolicy Bypass -Scope Process -Force
        cd Xsolla Backend
        .\setup.ps1

These scripts will perform necessary setup tasks for the Unreal plugins on your platform.

2. Add the desired plug-ins to your project's ``.uproject`` file at the root directory. Open the .uproject file with your IDE or text editor of your choice, and add the following:

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

3. Next, you will need to Set ``AXR`` as the default OnlineSubsytem in ``DefaultEngine.ini``, located at ``Path/To/Project/Config/..``

Open the file ``DefaultEngine.ini`` with your IDE or text editor of your choice, and add the following anywhere in the file.

    .. code-block:: ini

        [OnlineSubsystem]
        DefaultPlatformService=AXR

4. You will need to Launch the project (UE Editor) by double clicking the ``.uproject`` file, right clicking and selecting ``Open`` or by launching it from the Epic Games Launcher.

    *Note: If prompted to rebuild missing modules, click 'Yes' and wait for the project to load.*

That's it! If your project supports the ``OnlineSubsystem`` interface, you should now be using Xsolla Backend user login and session management on the AXR demo environment.

Admin Console Demo
================
Take a sneak peak at the web admin console for the demo environment at `https://console.demo.xsolla.cloud <https://console.demo.xsolla.cloud>`__ with the followng credentials:

- Username: **admin**
 
- Password: **@xrD3m0!**


Learn More
================
To learn more about how to work with these plug-ins check out the `Unreal ShooterGame <../examples/shootergame.html>`_ project.
