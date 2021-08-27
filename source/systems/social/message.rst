
==========================
Player-to-Player Messaging
==========================

The social services system supports the sending and receiving of player-to-player messages. Each message has a ``senderUid`` of the user sending the message, a ``receiverUid`` of the user that the message is destined for as well as ``subject``\ , ``body`` and ``attachments``.

Inbox
-----

Each user has their own inbox of messages that they have been sent by other users accessible via the ``/{userUid}/messages/inbox`` endpoint. Messages are considered permanent and will not be deleted or removed unless the application specifically removes them. To improve the user interface usability of your application a ``hasRead`` property is provided for each message that indicates whether or not a message has been read. It is the responsibility of the application to mark a message has having been read by either performing an update or calling ``GET`` on the ``/messages/{messageUid}/read`` endpoint.

Sent Messages
-------------

Each user can access the list of all sent messages using the ``/{userUid}/messages/sent`` endpoint. Like received messages the system will not automatically delete sent messages. It is the responsibility of the application to delete sent messages. Note however that messages are not duplicated therefore the sent message and the received message are the same. Therefore, if the receiving user deletes their message it will also be removed from the sender's sent box.

Attachments
-----------

Messages can have an optional list of ``attachments`` appended to them. The actual storage is handled as a key-value pair mapping where the key is the name of the attachment. Values are always stored as strings. To encode binary data in the attachment it is recommended to use Base64 encoding for the value.

Example
^^^^^^^

.. code-block:: javascript

   attachments: {
       file: "lkfj098fu3oajf9083ufj2oij9p0a8ffujloiua9o8ubvf9p2ulijhqrlvfb98l26yqo9283yrh2r2=",
       invite: "{ appID: \"fa72de2c-77a4-494a-b6c3-b47f51d63a9a\", type: \"game\", sessionUid: \"49b58da1-61a1-4c8e-9f45-61b8007cb765\" }"
   }

Privacy & Security Considerations
---------------------------------

Only messages that have been specifically sent to or from a given user may be accessible through the REST API. The system will automatically filter out any messages belonging to another user. Similarly, any attempt to perform an action on a message that does not belong to a given user will be denied.
