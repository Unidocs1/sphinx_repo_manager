==========================
AcceleratXR Script Manager
==========================

Hello everyone and welcome to the first article of a five part series discussing custom scripting with AcceleratXR. This article will focus on introducing you to the AcceleratXR Script Manager, an extension for Visual Studio Code making the management of scripts simple and powerful.

The Script Manager extension allows you to interact with an AcceleratXR cluster’s scripting system by implementing a Source Control Provider. The scm provider is able to communicate with your AXR backend cluster. With the manager you can automatically synchronize existing scripts to a local workspace, modify and commit changes, then publish those changes when you’re ready to make them live. Scripts can also be deleted and recovered so that you never lose precious work.

In AcceleratXR scripts can be created from two different places. The first script source is called disk. These are scripts that have been bundled with the service code itself. They can never be permanently deleted but they can be unpublished and/or modified. The second source of scripts are user scripts. These are scripts that you create with the Script Manager or AcceleratXR console tools. These scripts are only visible to the service that they were created with and only exist in the cluster database.

Let’s get started. Open up Visual Studio Code to the extensions panel. Type in acceleratxr into the search box. You’ll immediately see an entry for the AcceleratXR Script Manager. Click on it and hit Install.

.. image:: /images/tutorials/scripting/part1_diagram1.png

Next you’ll want to create a workspace to synchronize the scripts to. Click on File -> Save workspace As... and choose a suitable location. Now you can synchronize the scripts from your AXR cluster using the axr.checkout command using the command menu (Ctrl+Shift+P).

You will be prompted for the cluster address. This is the base url of your AXR cluster that the dashboard and clients use to connect to the service (e.g. https://api.demo.goaxr.cloud/v1). Once entered you’ll be prompted for the username of a user account to login with. The user must have the admin role in order to manage scripts. Finally enter the account password. The extension will automatically save this configuration into the settings.json file of the workspace. You can optionally have the extension remember your password so that you don’t get prompted each time you open the workspace. However note that the password is stored in plaintext.

The final prompt you’ll see is to install the script dependencies. This will install all NodeJS dependencies that the system needs in order to ensure you have the optimal scripting environment. While this is optional, it is highly recommended.

Once synchronized you’ll notice several new files have been added to your local workspace folder.

.. image:: /images/tutorials/scripting/part1_diagram2.png

Let’s modify a script. Open the DependenciesRoute.ts file from the routes folder and make some edit. You’ll notice that the Source Control icon now shows one (1) pending change.  If you click on the scm icon you can now see three (3) separate categories in the SCM panel; Changes, Unpublished, and Deleted.

The Changes category lists all locally modified script changes. If you click on a given script the editor will show you a diff from what exists on the remote server.

.. image:: /images/tutorials/scripting/part1_diagram4.png

Now that you’ve made the change you want lets save it to the remote server. Click on the  icon. You will be prompted to enter a commit note that will be stored with that version of the script. Notice that once the script is saved it moves from the Changes section to the Unpublished section.

Scripts in the unpublished section are those which are saved to the remote server but not active yet. In other words, your changes are not actually live running code. This allows you to perform any final checks before a script goes live for execution. You can click on the script in the Unpublished section and it will display a diff of the previously committed version to the version about to be made active.

.. image:: /images/tutorials/scripting/part1_diagram6.png

When you’re ready to publish click the  button. However if you realize you made a mistake, go ahead and edit the file again and re-commit your changes.

Sometimes it’s necessary to remove a script altogether. This is simple to do either using the  button or simply deleting the file from the local workspace. If you use the  button the script will immediately move to the Deleted section. If you delete the file locally it will show up as a deleted file in the Changes section and you will need to commit it first.

.. image:: /images/tutorials/scripting/part1_diagram7.png

Once deleted the script will now show up in the Deleted section.

.. image:: /images/tutorials/scripting/part1_diagram8.png

The last two features we will explore are the permanent delete and script restoration. In case you make a mistake and delete a script by accident, the restore  button let’s you immediately restore the script to it’s previous state. If the script was unpublished, it will go back to the Unpublished section. If the script was already published, it will return to the active state.

Finally to permanently remove a script simply use the  button and the script will be erased from the database.

In `part two <part2>`_ of this series we will be discussing how to define custom REST API endpoints for your cluster.