===============================
Implementing Frictionless Login
===============================

Many modern games and applications want their users to be able to start with as little resistance as possible. Often called
*frictionless login*, the idea is to provide users a method for immediately jumping in before requiring them to create an
account and enter personal details such as their name or e-mail.

Using AcceleratXR it is possible to implement frictionless login with a few easy steps.

#. Use device login
#. Set a valid e-mail address
#. Create a password

Device Login
============

Device login allows your application to use the unique device identifier (e.g. *IMEI* on mobile) to perform automatic account registration and login.
The first time a device attempts device login a new account is automatically created with the username being the device id and the e-mail
address generated as ``<device_id>@device.goaxr.cloud``. A special user secret is also created of type ``device`` using a determistic
hash of the device information. This is what allows the device to login each time safely and securely. Subsequent logins use the device id
and secret hash to lookup and authorize the user.

The following example shows how to perform a device login.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            CoreSDK->LoginDevice().then([](pplx::task<void> task)
            {
                try
                {
                    // Force the exception to be re-thrown if an error occurred.
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
                await CoreSDK.LoginDevice();
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            try
            {
                await CoreSDK.LoginDevice();
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
                await SDK.Instance.LoginDevice();
            }
            catch (Exception error)
            {
                Debug.LogError("Failed device login. Error=" + error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);
            const IOnlineIdentityPtr IdentityInterface = OnlineSub->GetIdentityInterface();
            check(IdentityInterface.IsValid());

            FDelegateHandle LoginDelegateHandler;
            auto LoginDelegate = FOnLoginCompleteDelegate::CreateLambda([=](int32 InLocalUserNum, bool bWasSuccessful, const FUniqueNetId& UserId, const FString& Error)
            {
                if (Error.Len() > 0)
                {
                    // Handle error here
                }

                IdentityInterface->ClearOnLoginCompleteDelegate_Handle(InLocalUserNum, LoginDelegateHandler);
            });
            LoginDelegateHandler = IdentityInterface->AddOnLoginCompleteDelegate_Handle(0, LoginDelegate);

            IdentityInterface->AutoLogin(0);

Set a Valid E-mail Address
==========================

After some time, you will offer the user the ability to customize their account. This is typically performed after a duration of
time such as the end of the play session. You may also prefer to not prompt the user at all but instead provide a user interface
to their account and allow them to set their personal information on-demand.

In either case you will request some information from the user to customize their account. The minimum recommended information to
request from the user is their personal e-mail address. You can optionally request any additional information you like such as:

* E-mail (**required**)
* First Name
* Last Name
* Phone Number
* Username

In the below example we assume that we have prompted for all of the above information. Note that before you can perform this action
the user must already be logged in.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            auto user = CoreSDK->GetLoggedInUser();
            user->SetFirstName(_XPLATSTR("John"));
            user->SetLastName(_XPLATSTR("Smith"));
            user->SetEmail(_XPLATSTR("john.smith@gmail.com"));
            user->SetName(_XPLATSTR("john.smith"));
            user->SetPhone(_XPLATSTR("+1 213-555-1234"));

            auto service = CoreSDK->GetServiceFactory<axr::sdk::services::UserService>();
            service->Update(user->GetUid(), user).then([=](pplx::task<std::shared_ptr<axr::sdk::models::User>> task)
            {
                try
                {
                    user = task.get();
                }
                catch (const axr::sdk::Exception& e)
                {
                    // Handle error here
                }
            });

    .. tab:: C#

        .. code-block:: csharp

            User user = CoreSDK.LoggedInUser;
            user.FirstName = "John";
            user.LastName = "Smith";
            user.Email = "john.smith@gmail.com";
            user.Name = "john.smith";
            user.Phone = "+1 213-555-1234";

            UserService userService = CoreSDK.ServiceFactory.GetService<UserService>();
            try
            {
                await userService.Update(user.Uid, user);
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            const user: User = CoreSDK.LoggedInUser;
            user.FirstName = "John";
            user.LastName = "Smith";
            user.Email = "john.smith@gmail.com";
            user.Name = "john.smith";
            user.Phone = "+1 213-555-1234";

            const userService: UserService = CoreSDK.ServiceFactory.GetService(UserService);
            try
            {
                await userService.Update(user.uid, user);
            }
            catch (error: any)
            {
                // Handle error here
            }

    .. tab:: Unity

        .. code-block:: csharp

            AXRCoreSDK SDK = AXRCoreSDK.GetInstance();
            User user = SDK.Instance.LoggedInUser;
            user.FirstName = "John";
            user.LastName = "Smith";
            user.Email = "john.smith@gmail.com";
            user.Name = "john.smith";
            user.Phone = "+1 213-555-1234";

            UserService userService = SDK.Instance.ServiceFactory.GetService<UserService>();
            try
            {
                await userService.Update(user.Uid, user);
            }
            catch (Exception error)
            {
                Debug.LogError("Failed to update account. Error=" + error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            const FOnlineSubsystemAXR* OnlineSub = (FOnlineSubsystemAXR*)Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);
            
            auto user = OnlineSub->CoreSDK->GetLoggedInUser();
            user->SetFirstName(_XPLATSTR("John"));
            user->SetLastName(_XPLATSTR("Smith"));
            user->SetEmail(_XPLATSTR("john.smith@gmail.com"));
            user->SetName(_XPLATSTR("john.smith"));
            user->SetPhone(_XPLATSTR("+1 213-555-1234"));

            auto service = OnlineSub->CoreSDK->GetServiceFactory<axr::sdk::services::UserService>();
            service->Update(user->GetUid(), user).then([=](pplx::task<std::shared_ptr<axr::sdk::models::User>> task)
            {
                try
                {
                    user = task.get();
                }
                catch (const axr::sdk::Exception& e)
                {
                    // Handle error here
                }
            });

Once this operation is complete the user will be sent an e-mail asking them to verify their e-mail address.

Create a Password
=================

In order for the user to be able to login to their account from another device it is necessary to create a password. This is done by
creating a user secret of type ``password``. The ``password`` secret can be either created at the time of updating the account information
as performed in step two, or it can be done implicitly later as a result of the e-mail verification step. In the latter case the user will
be prompted to enter a new password upon clicking the e-mail verification link and will be either sent to the AcceleratXR Admin Console or
your custom website that is able to fulfill the request.

We will cover the former case here and assume that following the customization of the user account information your game either prompts
the user to enter a password or you provide a UI for the user to set a password on their account. In either situation the following code
is used to create the new password secret.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            auto secret = std::make_shared<axr::sdk::models::UserSecret>();
            secret->SetType(axr::sdk::models::UserSecret::Type::TYPE_PASSWORD);
            secret->SetSecret(_XPLATSTR("<PASSWORD>"));
            secret->SetUserId(CoreSDK->GetLoggedInUser()->GetUid());

            auto service = CoreSDK->GetServiceFactory<axr::sdk::services::UserSecretService>();
            service->Create(secret).then([=](pplx::task<std::shared_ptr<axr::sdk::models::UserSecret>> task)
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

            UserSecret secret = new UserSecret();
            secret.Type = UserSecret.TYPE_MFA;
            secret.Secret = "<PASSWORD>";

            UserSecretService service = CoreSDK.ServiceFactory.GetService<UserSecretService>();
            try
            {
                await service.Create(secret);
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            const secret: UserSecret = new UserSecret();
            secret.Type = UserSecret.TYPE_MFA;
            secret.Secret = "<PASSWORD>";

            const service: UserSecretService = CoreSDK.ServiceFactory.GetService(UserSecretService);
            try
            {
                await service.Create(secret);
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: Unity

        .. code-block:: csharp

            AXRCoreSDK SDK = AXRCoreSDK.GetInstance();
            UserSecret secret = new UserSecret();
            secret.Type = UserSecret.TYPE_MFA;
            secret.Secret = "<PASSWORD>";

            UserSecretService service = SDK.Instance.ServiceFactory.GetService<UserSecretService>();
            try
            {
                await service.Create(secret);
            }
            catch (Exception error)
            {
                Debug.LogError("Failed to update account. Error=" + error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            const FOnlineSubsystemAXR* OnlineSub = (FOnlineSubsystemAXR*)Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);
            
            auto secret = std::make_shared<axr::sdk::models::UserSecret>();
            secret->SetType(axr::sdk::models::UserSecret::Type::TYPE_PASSWORD);
            secret->SetSecret(_XPLATSTR(password));
            secret->SetUserId(CoreSDK->GetLoggedInUser()->GetUid());

            auto service = OnlineSub->CoreSDK->GetServiceFactory<axr::sdk::services::UserSecretService>();
            service->Create(secret).then([=](pplx::task<std::shared_ptr<axr::sdk::models::UserSecret>> task)
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

Now that a password is set on the account the user can use this for all future logins on new devices. Note that the automatic login used for the
original device will still work and does not require re-authentication.