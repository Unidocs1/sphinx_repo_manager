=====
Tools
=====

AcceleratXR Admin Console
=========================

The AcceleratXR Admin Console is our custom cluster administration tool.

https://console.goaxr.cloud/

Fiddler
=======

Often times it is necessary to inspect the traffic going between your game and the backend servers. This helps in debugging
what is being sent and received directly. For this task we recommend `Telerik Fiddler <https://www.telerik.com/fiddler>`_.

Postman
=======

`Postman <https://www.postman.com/>`_ is a free tool for working directly with AcceleratXR's REST API.

Install the AcceleratXR Workspace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To install the AcceleratXR workspace perform the following.

1. `Install <https://www.postman.com/downloads>`_ or `sign-in<https://identity.getpostman.com/login?continue=https%3A%2F%2Fgo.postman.co%2Fbuild>`_ to Postman
2. Click the **Import** button near the top left corner.
3. In the pop-up window, select **Link**.
4. Paste the following URL into the text field and click **Continue**.
   https://www.getpostman.com/collections/afec68df8e1d205a1524
5. Verify the name of the workspace as *AcceleratXR* and click **Import**.

Setting up the workspace
~~~~~~~~~~~~~~~~~~~~~~~~

Once the AcceleratXR workspace has been installed you need to configure an environment to talk to your cluster.

1. Near the top right corner click the little eye icon next to *No Environment*.
2. Click the **Add** button under *Environment*.
3. Enter a name at the top.
4. Add a new variable named *base_url* and enter your cluster address for the initial value.
   e.g. *base_url* = *https://api.demo.goaxr.cloud/v1*
5. Now click the Save button.

You are now ready to access your cluster with Postman.

In order to begin making REST API calls to the cluster you need to authenticate.

1. Under the AcceleratXR collection, expand **Account Services**.
2. Click on **Auth Password**.
3. Click the *Authorization* tab.
4. Enter your desired username and password.
   e.g. Username: `admin`, Password: `@xrD3m0!` for the demo environment.
5. Click the **Send** button.

If all is successful you will see a JSON response similar to the following.

.. code-block:: bash

    {
        "refresh": "<refresh>",
        "token": "<token>",
        "type": "ACCESS",
        "userUid": "<user_uid>"
    }

You are now ready to start using the AcceleratXR postman API.

Visual Studio Code
==================

AcceleratXR develops all of our products and services using the very popular and
powerful `Microsoft Visual Studio Code <https://code.visualstudio.com/>`_.

We recommend installing the following extensions.

* `AcceleratXR Script Manager <https://marketplace.visualstudio.com/items?itemName=acceleratxr.vscode-scripts-scm>`_
* `Docker <https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker>`_
* `ESLint <https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint>`_
* `Jest <https://marketplace.visualstudio.com/items?itemName=Orta.vscode-jest>`_
* `Jest Runner <https://marketplace.visualstudio.com/items?itemName=firsttris.vscode-jest-runner>`_
* `TSLint <https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-typescript-tslint-plugin>`_