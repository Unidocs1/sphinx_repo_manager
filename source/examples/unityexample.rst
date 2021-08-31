=============
Unity Example
=============

.. image:: /images/samples/unity_example.png

The Unity Sample project integrates the AcceleratXR Unity SDK and provides an example implementation of the following features.

* Account registration
* User login
* Device login
* Personas
* Matchmaking
* Sessions
* Social Profiles
* Friends List
* Player Messaging
* Achievements
* Leaderboards

Getting Started
===============

To get started with the Unity Example project you must clone the Git repository from our GitLab server. The project is compatible with **Unity 2019.4**.

.. code-block:: bash
   :linenos:

   git clone git@gitlab.acceleratxr.com:Core/samples/example_unity.git

Project Structure
=================

Upon opening the project you'll notice a very simple project structure.

.. image:: /images/samples/unity_example_diagram1.png

All of the project's relevant files are located in the ``Scenes`` and ``UI`` folder. The ``Scenes`` folder contains the primary scene and the ``UI`` folder contains all of the code.

Default Scene
=============

The default scene for the project is called ``SampleScene``. Upon opening the scene you will see the following in the editor viewport.

.. image:: /images/samples/unity_example_diagram3.png

The scene is composed of a single camera and ``Canvas`` object containing all relevant UI objects.

.. image:: /images/samples/unity_example_diagram2.png

``MainScene.cs``
================

The ``MainScene.cs`` file located in the ``UI/Controllers`` folder contains the entry point for the project. This class implements a `MonoBehavior <https://docs.unity3d.com/2019.4/Documentation/ScriptReference/MonoBehaviour.html>`_
and initializes the AcceleratXR SDK. It also registers necessary push notification handlers so that the application can respond to SDK push messages coming from the backend.

Login & User Registration
=========================

The following source code files contain example implementations for common tasks such as user login, account registration and device login.

``LoginUser.cs``
~~~~~~~~~~~~~~~~

The `LoginUser.cs`` file contains relevant code for performing user login. The login menu is the first UI screen shown when the application is started.

``RegisterUser.cs``
~~~~~~~~~~~~~~~~~~~

The ``RegisterUser.cs`` file contains example code for how to properly register a new user with the backend. In AcceleratXR, account creation is typically a two-step
process. The first step is to create the actual user account record. Once the user account has been created then a second step is performed to create a password for
the new user that will allow that person to login with their username and password in the future. Note that it is possible to create a user account without creating
a password.

Social
======

The example project includes implementations of various social features including player-to-player messaging, social profiles, and friends list. These features are implemented in the following files.

* ``EditProfileScreen.cs``
* ``ViewProfileScreen.cs``
* ``ListFriendsScreen.cs``
* ``ListMessagesScreen.cs``
* ``ViewMessageScreen.cs``

Matchmaking & Sessions
======================

Reference implementations are also provided for the matchmaking and session systems. These features are implemented in the following files.

* ``ListSessionsScreen.cs``
* ``NewSessionScreen.cs``
* ``NewTicketScreen.cs``
* ``ViewSessionScreen.cs``
* ``ViewTicketScreen.cs``