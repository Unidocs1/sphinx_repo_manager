==========================
Player-to-Player Messaging
==========================

Xsolla Backend supports asynchronus Player-to-Player messaging as well as real-time chat. This article describes
how to implement the former.

Each player has their own inbox and outbox of messages both received and sent respectively. Access to these mailboxes is
accessible via the ``MessageService`` class in the SDK or via the `IOnlineMessage <https://docs.unrealengine.com/4.26/en-US/API/Plugins/OnlineSubsystem/Interfaces/IOnlineMessage/>`_ interface in Unreal.

Messages follow a standard e-mail structure that includes the following properties.

+------------------+-------------------------------------------------------------------------------+-----------+
| Property         | Description                                                                   | Required  |
+==================+===============================================================================+===========+
| ``receiverUid``  | The unique identifier of the user that is to receive the message.             | ``true``  |
+------------------+-------------------------------------------------------------------------------+-----------+
| ``senderUid``    | The unique identifier of the user that sent the message.                      | ``false`` |
+------------------+-------------------------------------------------------------------------------+-----------+
| ``subject``      | The summary of the message contents.                                          | ``false`` |
+------------------+-------------------------------------------------------------------------------+-----------+
| ``body``         | The message contents.                                                         | ``false`` |
+------------------+-------------------------------------------------------------------------------+-----------+
| ``attachments``  | A map of key-value pairs representing a list of attachments that have been    | ``false`` |
|                  | appended that have been appended to the message. The key of each pair is the  |           |
|                  | can represent any data including binary data using base64 encoding.           |           |
+------------------+-------------------------------------------------------------------------------+-----------+

Note that the ``attachments`` is an arbitrary map of key-value pairs. The value can be any valid JSON type
including strings, numbers, objects and even base64 encoded binary. This makes it possible to implement any manner of
game-specific features such as invites, embedded media and so on.

Unreal Considerations
=====================

Unreal's OnlineSubsystem handles player messaging a little differently than Xsolla Backend. This affects the way the
`IOnlineMessage <https://docs.unrealengine.com/4.26/en-US/API/Plugins/OnlineSubsystem/Interfaces/IOnlineMessage/>`_
is both implemented and used.

The following table details how the ``IOnlineMessage`` interface functions are intended to behave and how Xsolla Backend's
implementation differs.

+-------------------------+---------------------------------------------------------------------------+-------------------------------------------------------------------------+
| Function                | Intended Behavior                                                         | OnlineSubsystemAXR Behavior                                             |
+=========================+===========================================================================+=========================================================================+
| ``EnumerateMessages``   | Retrieves a list of message metadata for available messages.              | Retrieves the complete list of available message metadata and contents. |
+-------------------------+---------------------------------------------------------------------------+-------------------------------------------------------------------------+
| ``GetMessageHeaders``   | Get the cached list of message headers for a user.                        | Same                                                                    |
+-------------------------+---------------------------------------------------------------------------+-------------------------------------------------------------------------+
| ``ClearMessageHeaders`` | Clear the cached list of message headers.                                 | Same. Message data/contents retained.                                   |
+-------------------------+---------------------------------------------------------------------------+-------------------------------------------------------------------------+
| ``ReadMessage``         | Download a message and its payload from user's inbox.                     | Marks a given message as having been read.                              |
+-------------------------+---------------------------------------------------------------------------+-------------------------------------------------------------------------+
| ``GetMessage``          | Get the cached message and its contents for a user.                       | Same. Does not require call to ``ReadMessage``.                         |
+-------------------------+---------------------------------------------------------------------------+-------------------------------------------------------------------------+
| ``SendMessage``         | Send a message from the currently logged in user to a list of recipients. | Same                                                                    |
+-------------------------+---------------------------------------------------------------------------+-------------------------------------------------------------------------+
| ``DeleteMessage``       | Delete a message from currently logged in user's inbox.                   | Same                                                                    |
+-------------------------+---------------------------------------------------------------------------+-------------------------------------------------------------------------+

Sending a Message
=================

Messages can be sent from a player to exactly one other player. If multiple recipients are desired you must send multiple
message requests with the ``uid`` of each receiving user.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            using namespace axr::sdk;

            auto message = std::make_shared<models::Message>();
            message->SetReceiverUid(_XPLATSTR("<other_uid>"));
            message->SetSubject(_XPLATSTR("Test Message"));
            message->SetBody(_XPLATSTR("This is only a test."));

            auto service = CoreSDK->GetServiceFactory<services::MessageService>();
            service->Create(message).then([](pplx::task<std::shared_ptr<models::Message>> task)
            {
                try
                {
                    task.get();
                }
                catch (const axr::sdk::Exception& e)
                {
                    // Handle error here
                }
            });

    .. tab:: C#

        .. code-block:: csharp

            try
            {
                Message message = new Message();
                message.ReceiverUid = "<other_uid>";
                message.Subject = "Test Message";
                message.Body = "This is only a test.";

                MessageService service = CoreSDK.ServiceFactory.GetService<MessageService>();
                await service.Create(message);
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            try
            {
                const message: Message = new Message();
                message.receiverUid = "<other_uid>";
                message.subject = "Test Message";
                message.body = "This is only a test.";

                const service: MessageService = ServiceFactory.getService(MessageService);
                await service.create(message);
            }
            catch (error: any)
            {
                // Handle error here
            }

    .. tab:: Unity

        .. code-block:: csharp

            try
            {
                AXRCoreSDK SDK = AXRCoreSDK.GetInstance();
                Message message = new Message();
                message.ReceiverUid = "<other_uid>";
                message.Subject = "Test Message";
                message.Body = "This is only a test.";

                MessageService service = SDK.Instance.ServiceFactory.GetService<MessageService>();
                await service.Create(message);
            }
            catch (Exception error)
            {
                Debug.LogError(error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);
            const IOnlineMessagePtr MessageInterface = OnlineSub->GetMessageInterface();
            check(MessageInterface.IsValid());

            TArray<TSharedRef<const FUniqueNetId>> RecipientIds;
            FOnlineMessagePayload Payload;
            // Note the MessageType argument is ignored
            MessageInterface->SendMessage(LocalUserNum, RecipientIds, TEXT(""), Payload);

Note that when push notifications are enabled on the SDK instance, sent messages will automatically be forwarded
to to the receiving client if one is connected and available.

Retrieving the Inbox
====================

The following example shows how to retrieve a list of all messages that a user has received, including those already marked as read.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            using namespace axr::sdk;

            auto service = CoreSDK->GetServiceFactory<services::MessageService>();
            service->FindInbox().then([](pplx::task<std::vector<std::shared_ptr<models::Message>>> task)
            {
                try
                {
                    auto messages = task.get();
                    // TODO Process inbox messages
                }
                catch (const axr::sdk::Exception& e)
                {
                    // Handle error here
                }
            });

    .. tab:: C#

        .. code-block:: csharp

            try
            {
                MessageService service = CoreSDK.ServiceFactory.GetService<MessageService>();
                List<Message> messages = await service.FindInbox();
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            try
            {
                const service: MessageService = ServiceFactory.getService(MessageService);
                const messages: Message[] | undefined = await service.findInbox();
            }
            catch (error: any)
            {
                // Handle error here
            }

    .. tab:: Unity

        .. code-block:: csharp

            try
            {
                AXRCoreSDK SDK = AXRCoreSDK.GetInstance();
                MessageService service = SDK.Instance.ServiceFactory.GetService<MessageService>();
                List<Message> messages = await service.FindInbox();
            }
            catch (Exception error)
            {
                Debug.LogError(error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);
            const IOnlineMessagePtr MessageInterface = OnlineSub->GetMessageInterface();
            check(MessageInterface.IsValid());

            FDelegateHandle DelegateHandler;
            auto Delegate = FOnEnumerateMessagesComplete::CreateLambda([=](int32 InLocalUserNum, bool bWasSuccessful, const FString& Error)
            {
                if (bWasSuccessful)
                {
                    TArray<TSharedRef<class FOnlineMessageHeader>> headers;
                    if (MessageInterface->GetMessageHeaders(LocalUserNum, headers))
                    {
                        TArray<TSharedPtr<class FOnlineMessage>> messages;
                        for (auto header : headers)
                        {
                            messages.Add(MessageInterface->GetMessage(LocalUserNum, header->MessageId));
                        }

                        // TODO Do something with messages
                    }
                }
                else
                {
                    // Handle error here
                }

                MessageInterface->ClearOnEnumerateMessagesComplete_Handle(InLocalUserNum, DelegateHandler);
            });
            DelegateHandler = MessageInterface->AddOnEnumerateMessagesComplete_Handle(0, LoginDelegate);

            MessageInterface->EnumerateMessages(LocalUserNum);

Marking a Message as Read
=========================

It is often useful to know when a user has already read a message or opened a message (in the case of an invite).
The below example shows how to mark a message as already having been read.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            using namespace axr::sdk;

            auto service = CoreSDK->GetServiceFactory<services::MessageService>();
            service->MarkRead(message->GetUid()).then([](pplx::task<void> task)
            {
                try
                {
                    task.get();
                }
                catch (const axr::sdk::Exception& e)
                {
                    // Handle error here
                }
            });

    .. tab:: C#

        .. code-block:: csharp

            try
            {
                MessageService service = CoreSDK.ServiceFactory.GetService<MessageService>();
                await service.MarkRead(message.Uid);
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            try
            {
                const service: MessageService = ServiceFactory.getService(MessageService);
                await service.markRead(message.uid);
            }
            catch (error: any)
            {
                // Handle error here
            }

    .. tab:: Unity

        .. code-block:: csharp

            try
            {
                MessageService service = SDK.Instance.ServiceFactory.GetService<MessageService>();
                await service.MarkRead(message.Uid);
            }
            catch (Exception error)
            {
                Debug.LogError(error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);
            const IOnlineMessagePtr MessageInterface = OnlineSub->GetMessageInterface();
            check(MessageInterface.IsValid());

            MessageInterface->ReadMessage(LocalUserNum, MessageId);

Deleting a Message
==================

To delete a message simply call the ``Delete`` function on ``MessageService`` or ``DeleteMessage`` on ``IOnlineMessage`` when
using the Unreal plug-in.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            using namespace axr::sdk;

            auto service = CoreSDK->GetServiceFactory<services::MessageService>();
            service->Delete(message->GetUid()).then([](pplx::task<void> task)
            {
                try
                {
                    task.get();
                }
                catch (const axr::sdk::Exception& e)
                {
                    // Handle error here
                }
            });

    .. tab:: C#

        .. code-block:: csharp

            try
            {
                MessageService service = CoreSDK.ServiceFactory.GetService<MessageService>();
                await service.Delete(message.Uid);
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            try
            {
                const service: MessageService = ServiceFactory.getService(MessageService);
                await service.delete(message.uid);
            }
            catch (error: any)
            {
                // Handle error here
            }

    .. tab:: Unity

        .. code-block:: csharp

            try
            {
                MessageService service = SDK.Instance.ServiceFactory.GetService<MessageService>();
                await service.Delete(message.Uid);
            }
            catch (Exception error)
            {
                Debug.LogError(error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);
            const IOnlineMessagePtr MessageInterface = OnlineSub->GetMessageInterface();
            check(MessageInterface.IsValid());

            MessageInterface->DeleteMessage(LocalUserNum, MessageId);