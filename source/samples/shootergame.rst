==================
Unreal ShooterGame
==================

The **ShooterGame** project provides an example implementation of integrating the
`AcceleratXR SDK for Unreal <../sdks/unreal>`_ in Unreal Engine. It is based upon Epic's standard
`ShooterGame <https://docs.unrealengine.com/4.26/en-US/Resources/SampleGames/ShooterGame/>`_ sample project. The project
is compatible with Unreal Engine 4.25 and can be downloaded using git.

.. code-block:: bash

    git clone https://gitlab.acceleratxr.com/Core/samples/unrealshootergame.git

Differences
===========

A number of changes have been made to the original project to support the AcceleratXR platform.

ShooterOnlineSearchSettings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **FShooterOnlineSearchSettings** class has been modified to remove all default query parameters. This is needed to
avoid unnecessary filtering of game sessions from the backend.

ShooterLocalPlayer
~~~~~~~~~~~~~~~~~~

The **UShooterLocalPlayer** class has been modified to not use a **FPlatformUserId** for loading of persistent user
data. This is due to the fact that the *FPlatformUserId* data type is a 32-bit value and all AcceleratXR platfrom id's
must be 128-bit values and thus cannot be represented correctly.

ShooterGameInstance
~~~~~~~~~~~~~~~~~~~

The **ShooterGameInstance** class has been modified to load a custom login menu on game startup that players use to
authenticate with the AcceleratXR platform.

ShooterMainMenu
~~~~~~~~~~~~~~~

The **FShooterMainMenu** class has been changed to alter certain main menu items and behavior for better compatibility
with the platform. This includes enabling Quickmatch for all builds, removing query search parameters that are specific
to non-AXR platforms and adding required query settings that the platform needs when searching for matches.

ShooterGameSession
~~~~~~~~~~~~~~~~~~

The **AShooterGameSession** class has been changed to extend **AGameSessionAXR** instead of the engine's base
**AGameSession** class. *AGameSessionAXR* is provided by the *GameFrameworkAXR* plug-in and provides automatic server
registration and session management with the platform.