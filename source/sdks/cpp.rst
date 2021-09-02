=======
C++ SDK
=======

The AcceleratXR C++ SDK is written using the modern C++17 standard and leverages
`vcpkg <https://github.com/microsoft/vcpkg>`_ as a package manager for third-party dependencies.

Building from Source
====================

Downloading the Source
~~~~~~~~~~~~~~~~~~~~~~

You will first want to clone the repository containing the C++ SDK using the following command.

.. code-block:: bash

    git clone https://gitlab.com/AcceleratXR/Core/sdk/sdk_cpp

Building on Windows
~~~~~~~~~~~~~~~~~~~

The SDK requires Visual Studio 2019 with the `cmake` component to be installed.

1. Open a `Developer Powershell for 2019` window.
2. Run the `build_vc2019.ps1` script.

.. code-block::

 .\build_vc2019.ps1

The process may take some time to build depending on your machine. When the build is complete you will have two new
folders; `.vcpkg` and `lib`.

You can copy the `include`, `lib` and `.vcpkg/installed` folders to your project for compilation and linking.

Building on Linux
~~~~~~~~~~~~~~~~~

When compiling on Linux it is recommended to use clang-9 instead of gcc. However, gcc should work without issue.

1. Open a terminal or ssh to your Linux machine.
2. Run the `build_linux.sh` script.

.. code-block:: bash

   ./build.sh

The included build scripts will assume clang-9 is installed and available at `/usr/bin/clang-9` and `/usr/bin/clang++-9`.

The process may take some time to build depending on your machine. When the build is complete you will have two new
folders; `.vcpkg` and `lib`.

You can copy the `include`, `lib` and `.vcpkg/installed` folders to your project for compilation and linking.