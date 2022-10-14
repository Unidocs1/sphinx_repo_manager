======
C# SDK
======

The `AcceleratXR C# SDK <https://gitlab.acceleratxr.com/Core/sdk/sdk_csharp/>`__ is written
for compatibility with the .NET 4.x and .NET Standard 2.0 runtimes.

Looking for a Unity SDK, instead?
===============================
Ignore this guide -> Instead, jump to the README in `unity_sdk <https://gitlab.acceleratxr.com/Core/sdk/sdk_unity>`__.

Installation via NuGet
======================

The simplest way to install the C# SDK is `through NuGet <https://www.nuget.org/packages/acceleratxr.sdk/>`__:

To install using the NuGet Package Manager CLI, run the following command:

.. code-block::

   Install-Package acceleratxr.sdk

Building from Source
====================

Clone the repository containing the C# SDK using the following command.

.. code-block:: bash

    git clone https://gitlab.com/AcceleratXR/Core/sdk/sdk_csharp

Building on Windows
~~~~~~~~~~~~~~~~~~~

You will need `.NET Standard 2.0` and `.NET Framework 4.6.1` components installed (that is generally included with Visual Studio).

This project is tested for use with Visual Studio 2019, for full compatibility:

1. Open the `sdk_csharp.sln` solution file.
2. [For updating `unity_sdk <https://gitlab.acceleratxr.com/Core/sdk/sdk_unity>`__] At the top-right, be sure to target `Unity`.
3. Select `Build Solution`.
