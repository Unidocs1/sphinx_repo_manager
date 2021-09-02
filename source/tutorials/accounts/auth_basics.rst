=====================
Authentication Basics
=====================

This article covers the basics of how to register user accounts as well as the available authentication methods for logging in
a user account to an AcceleratXR cluster.

Account Registration
====================

Registering a new account in AcceleratXR is very simple, requiring only the creation of a new account record. Due to the design
of the platform setting a password during the registration process is completely optional. This gaurantees flexibility in how
you choose to implement authentication with your game.

A user account requires very little data, keeping the personally identifiable information to a minimum. The configurable properties
of a user account are as follows.

+---------------+----------------------------------------+-----------+
| Property      | Description                            | Required  |
+===============+========================================+===========+
| ``name``      | The unique name of the user.           | ``true``  |
+---------------+----------------------------------------+-----------+
| ``email``     | The unique e-mail address of the user. | ``true``  |
+---------------+----------------------------------------+-----------+
| ``firstName`` | The user's real first name.            | ``false`` |
+---------------+----------------------------------------+-----------+
| ``lastName``  | The user's real last name.             | ``false`` |
+---------------+----------------------------------------+-----------+
| ``phone``     | The user's real telephone number.      | ``false`` |
+---------------+----------------------------------------+-----------+

For security reasons all the information above (except ``name``) is removed when requesting or searching for account data unless the user
requesting that data is yourself or a system ``admin``.

You can learn more about how these features are used by reading the :doc:`Account Services </platform/systems/accounts/index>` system documentation.

To implement user registration simply call the ``RegisterUser`` or ``RegisterUserAndPassword`` function on the ``CoreSDK`` object instance
from the SDK as shown below.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            using namespace axr::sdk;

            auto newUser = std::make_shared<models::User>();
            newUser->SetName(_XPLATSTR("jsmith")); // Required
            newUser->SetEmail(_XPLATSTR("john.smith@gmail.com")); // Required
            newUser->SetFirstName(_XPLATSTR("John")); // Optional
            newUser->SetLastName(_XPLATSTR("Smith")); // Optional
            newUser->SetPhone(_XPLATSTR("+1 213-555-1234")); // Optional

            CoreSDK->RegisterUser(newUser).then([](pplx::task<std::shared_ptr<models::User>> task)
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
                User newUser = new User();
                newUser.FirstName = "John";
                newUser.LastName = "Smith";
                newUser.Email = "john.smith@gmail.com";
                newUser.Name = "john.smith";
                newUser.Phone = "+1 213-555-1234";

                await CoreSDK.RegisterUser(newUser);
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            try
            {
                const newUser: User = new User();
                newUser.FirstName = "John";
                newUser.LastName = "Smith";
                newUser.Email = "john.smith@gmail.com";
                newUser.Name = "john.smith";
                newUser.Phone = "+1 213-555-1234";

                await CoreSDK.RegisterUser(newUser);
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
                User newUser = new User();
                newUser.FirstName = "John";
                newUser.LastName = "Smith";
                newUser.Email = "john.smith@gmail.com";
                newUser.Name = "john.smith";
                newUser.Phone = "+1 213-555-1234";

                await SDK.Instance.RegisterUser(newUser);
            }
            catch (Exception error)
            {
                Debug.LogError("Failed device login. Error=" + error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            using namespace axr::sdk;

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);

            auto newUser = std::make_shared<models::User>();
            newUser->SetName(_XPLATSTR("jsmith")); // Required
            newUser->SetEmail(_XPLATSTR("john.smith@gmail.com")); // Required
            newUser->SetFirstName(_XPLATSTR("John")); // Optional
            newUser->SetLastName(_XPLATSTR("Smith")); // Optional
            newUser->SetPhone(_XPLATSTR("+1 213-555-1234")); // Optional

            OnlineSub->CoreSDK->RegisterUser(newUser).then([](pplx::task<std::shared_ptr<models::User>> task)
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

The following example shows how to register a new account and immediately create a password for the newly created user.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            using namespace axr::sdk;

            auto newUser = std::make_shared<models::User>();
            newUser->SetName(_XPLATSTR("jsmith")); // Required
            newUser->SetEmail(_XPLATSTR("john.smith@gmail.com")); // Required
            newUser->SetFirstName(_XPLATSTR("John")); // Optional
            newUser->SetLastName(_XPLATSTR("Smith")); // Optional
            newUser->SetPhone(_XPLATSTR("+1 213-555-1234")); // Optional

            CoreSDK->RegisterUserAndPassword(newUser, _XPLATSTR("MyP@ssw0rdIsSecur3!")).then([](pplx::task<std::shared_ptr<models::User>> task)
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
                User newUser = new User();
                newUser.FirstName = "John";
                newUser.LastName = "Smith";
                newUser.Email = "john.smith@gmail.com";
                newUser.Name = "john.smith";
                newUser.Phone = "+1 213-555-1234";

                await CoreSDK.RegisterUserAndPassword(newUser, "MyP@ssw0rdIsSecur3!");
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            try
            {
                const newUser: User = new User();
                newUser.FirstName = "John";
                newUser.LastName = "Smith";
                newUser.Email = "john.smith@gmail.com";
                newUser.Name = "john.smith";
                newUser.Phone = "+1 213-555-1234";

                await CoreSDK.RegisterUserAndPassword(newUser, "MyP@ssw0rdIsSecur3!");
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
                User newUser = new User();
                newUser.FirstName = "John";
                newUser.LastName = "Smith";
                newUser.Email = "john.smith@gmail.com";
                newUser.Name = "john.smith";
                newUser.Phone = "+1 213-555-1234";

                await SDK.Instance.RegisterUserAndPassword(newUser, "MyP@ssw0rdIsSecur3!");
            }
            catch (Exception error)
            {
                Debug.LogError("Failed device login. Error=" + error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            using namespace axr::sdk;

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);

            auto newUser = std::make_shared<models::User>();
            newUser->SetName(_XPLATSTR("jsmith")); // Required
            newUser->SetEmail(_XPLATSTR("john.smith@gmail.com")); // Required
            newUser->SetFirstName(_XPLATSTR("John")); // Optional
            newUser->SetLastName(_XPLATSTR("Smith")); // Optional
            newUser->SetPhone(_XPLATSTR("+1 213-555-1234")); // Optional

            OnlineSub->CoreSDK->RegisterUserAndPassword(newUser, _XPLATSTR("MyP@ssw0rdIsSecur3!")).then([](pplx::task<std::shared_ptr<models::User>> task)
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

Authentication
==============

AcceleratXR supports five different methods of user authentication.

* API key
* Password
* Token
* Device
* Third-party (e.g. OAuth2, Facebook, Google, Twitter)

In addition to the above, multi-factor authentication (`TOTP <https://en.wikipedia.org/wiki/Time-based_One-Time_Password>`_)
is also supported.

API Key & Password
~~~~~~~~~~~~~~~~~~

Basic authentication is used to perform a standard login using a valid user identifier and password or API key. Any valid user identifier
can be used for the login name including the ``name``, ``email``, and ``phone`` properties of the registered User account data.

In the below example we will assume the use of the ``email`` property as the identifier for the account created in the previous
section.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            using namespace axr::sdk;

            CoreSDK->Login(_XPLATSTR("john.smith@gmail.com"), _XPLATSTR("MyP@ssw0rdIsSecur3!")).then([=](pplx::task<void> task)
            {
                try
                {
                    task.get();

                    if (CoreSDK->GetLoggedInUser() != nullptr)
                    {
                        // Success
                    }
                    else
                    {
                        // Fail
                    }
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
                await CoreSDK.Login("john.smith@gmail.com", "MyP@ssw0rdIsSecur3!");
                if (CoreSDK.LoggedInUser != null)
                {
                    // Success
                }
                else
                {
                    // Fail
                }
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            try
            {
                await CoreSDK.Login("john.smith@gmail.com", "MyP@ssw0rdIsSecur3!");
                if (CoreSDK.LoggedInUser)
                {
                    // Success
                }
                else
                {
                    // Fail
                }
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
                await SDK.Instance.Login("john.smith@gmail.com", "MyP@ssw0rdIsSecur3!");
                if (CoreSDK.LoggedInUser != null)
                {
                    // Success
                }
                else
                {
                    // Fail
                }
            }
            catch (Exception error)
            {
                Debug.LogError("Failed device login. Error=" + error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            using namespace axr::sdk;

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);

            OnlineSub->CoreSDK->Login(_XPLATSTR("john.smith@gmail.com"), _XPLATSTR("MyP@ssw0rdIsSecur3!")).then([](pplx::task<void> task)
            {
                try
                {
                    task.get();

                    if (OnlineSub->CoreSDK->GetLoggedInUser() != nullptr)
                    {
                        // Success
                    }
                    else
                    {
                        // Fail
                    }
                }
                catch (const axr::sdk::Exception& e)
                {
                    // Handle error here
                }
            });

.. attention::

    Never store a user's login credentials to local disk or memory. If retaining the authenticated session
    between application runtimes is desired it is recommended to use the ``Device`` or ``Token`` login methods
    as described below.

Token
~~~~~

It is also possible to login using an existing authentication token. The token may be obtained from a previous authenticated
session or provided to the application as a command line argument.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            using namespace axr::sdk;

            CoreSDK->LoginToken(_XPLATSTR("<TOKEN>")).then([=](pplx::task<void> task)
            {
                try
                {
                    task.get();

                    if (CoreSDK->GetLoggedInUser() != nullptr)
                    {
                        // Success
                    }
                    else
                    {
                        // Fail
                    }
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
                await CoreSDK.LoginToken("<TOKEN>");
                if (CoreSDK.LoggedInUser != null)
                {
                    // Success
                }
                else
                {
                    // Fail
                }
            }
            catch (Exception error)
            {
                // Handle error here
            }

    .. tab:: TypeScript

        .. code-block:: typescript

            try
            {
                await CoreSDK.LoginToken("<TOKEN>");
                if (CoreSDK.LoggedInUser)
                {
                    // Success
                }
                else
                {
                    // Fail
                }
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
                await SDK.Instance.LoginToken("<TOKEN>");
                if (CoreSDK.LoggedInUser != null)
                {
                    // Success
                }
                else
                {
                    // Fail
                }
            }
            catch (Exception error)
            {
                Debug.LogError("Failed device login. Error=" + error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            using namespace axr::sdk;

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);
            
            OnlineSub->CoreSDK->LoginToken(_XPLATSTR("<TOKEN>")).then([](pplx::task<void> task)
            {
                try
                {
                    task.get();

                    if (OnlineSub->CoreSDK->GetLoggedInUser() != nullptr)
                    {
                        // Success
                    }
                    else
                    {
                        // Fail
                    }
                }
                catch (const axr::sdk::Exception& e)
                {
                    // Handle error here
                }
            });

Device
~~~~~~

Device authentication allows a user to automatically identify theirself using a device's unique machine identifier
and deterministic secret hash. This is the **recommended** method for maintaining session logins between
application runtimes. This method is frequently desirable to implement :doc:`Frictionless Login <frictionless_login>`.

Device authentication will work regardless of whether or not an existing account has been created for a given user.
This works by generating a deterministic unique identifier for the device as the login name and a secret hash to
serve as a special type of password. The SDK will first attempt to login using this credential. If login fails
a new account is created automatically.

.. tabs::

    .. tab:: C++
    
        .. code-block:: cpp

            using namespace axr::sdk;

            CoreSDK->LoginDevice().then([=](pplx::task<void> task)
            {
                try
                {
                    task.get();

                    if (CoreSDK->GetLoggedInUser() != nullptr)
                    {
                        // Success
                    }
                    else
                    {
                        // Fail
                    }
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
                if (CoreSDK.LoggedInUser != null)
                {
                    // Success
                }
                else
                {
                    // Fail
                }
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
                if (CoreSDK.LoggedInUser)
                {
                    // Success
                }
                else
                {
                    // Fail
                }
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
                if (CoreSDK.LoggedInUser != null)
                {
                    // Success
                }
                else
                {
                    // Fail
                }
            }
            catch (Exception error)
            {
                Debug.LogError("Failed device login. Error=" + error.Message);
            }

    .. tab:: Unreal

        .. code-block:: cpp

            using namespace axr::sdk;

            const IOnlineSubsystem* OnlineSub = Online::GetSubsystem(GetWorld());
            check(OnlineSub != nullptr);
            
            OnlineSub->CoreSDK->LoginDevice().then([](pplx::task<void> task)
            {
                try
                {
                    task.get();

                    if (OnlineSub->CoreSDK->GetLoggedInUser() != nullptr)
                    {
                        // Success
                    }
                    else
                    {
                        // Fail
                    }
                }
                catch (const axr::sdk::Exception& e)
                {
                    // Handle error here
                }
            });

Third-party
~~~~~~~~~~~

AcceleratXR supports multiple third-party authentication methods for single-sign-on including OAuth2 compatibility.

The following third-party providers are supported out of the box.

* Facebook
* Google
* Twitter