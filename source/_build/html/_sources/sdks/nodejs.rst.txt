=========================
JavaScript/TypeScript SDK
=========================

The AcceleratXR JavaScript/TypeScript SDK is written in TypeScript and includes both JavaScript and TypeScript bindings
when installed.

Installation via yarn
=====================

Yarn is the preferred package management tool when developing with NodeJS and JavaScript.
   
.. code-block:: bash
    :linenos:
   
      yarn add @acceleratxr/sdk

Installation via npm
====================

If you prefer the `npm` package manager this also works.

.. code-block:: bash
   :linenos:

   npm install @acceleratxr/sdk

Building from Source
====================

You can also build the SDK from source as well.

Downloading the Source
~~~~~~~~~~~~~~~~~~~~~~

You will first want to clone the repository containing the SDK using the following command.

.. code-block:: bash
   :linenos:

    git clone https://gitlab.com/AcceleratXR/Core/sdk/sdk_nodejs

Building the SDK
~~~~~~~~~~~~~~~~

You will need NodeJS installed and the `yarn` package manager installed and available on your path.

1. Open a terminal/shell to the source folder
2. Run the following commands.

.. code-block:: bash
   :linenos:

    yarn install
    yarn build