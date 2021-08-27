========================================
How to Setup Multi-Factor Authentication
========================================

Protecting your user accounts is very important to most people. Multi-Factor Authentication is a method that requires
users to provide an additional randomly generated secret during the authentication process to validate their identity
should a password secret have been compromised.

Setting up Multi-Factor Authentication for a user account is fairly straight forward. First, authenticate the user
using an existing secret such as a ``password``. Once authenticated you can now create an ``mfa`` secret for the
user account by sending a ``POST`` request to the ``/users/:id/secrets`` endpoint as shown in the example below.

.. code-block::

    POST /users/00000000-0000-0000-0000-000000000000/secrets HTTP/1.1
    Host: api.demo.goaxr.cloud
    Content-Type: application/json
    Authorization: jwt f902e78f90827f2.f20978f23v9807039q.2vf9287vf93q879038q27f029q87vf90q2

    {
        "type": "mfa",
    }

Upon success, the system will return the newly created secret containing the MFA information needed to register
a compatible MFA device. An example is shown below.

.. code-block::

    200 OK
    Content-Type: application/json
    
    {
        "type": "mfa",
        "secret": {
            "otpauth_url": "https://api.demo.goaxr.cloud/v1/auth/totp",
            "secret": "flkj32q979bv7f98327vf93q"
        }
    }

At this point while MFA has been initialized for the account it is not activated yet. Use the provided
``otpauth_url`` and ``secret`` to register the user's MFA device. Then, using an initial generated code
send a ``PUT`` request to the ``/users/:userId/secrets/:secretId`` endpoint containing the code to complete
the MFA enrollment.

For example; imagine the above response was entered into the MFA device and produced a code of ``021589``.
To finish enrollment the following request must be sent to the service.

.. code-block::

    PUT /users/00000000-0000-0000-0000-000000000000/secrets/00000000-0000-0000-0000-000000000001/enroll HTTP/1.1
    Host: api.demo.goaxr.cloud
    Content-Type: application/json
    Authorization: jwt f902e78f90827f2.f20978f23v9807039q.2vf9287vf93q879038q27f029q87vf90q2

    {
        "token": 021589,
    }

If the provided MFA code is correct the service will generate a set of backup codes that can be used to recover
the account if future authentication requests fail.

.. code-block::

    200 OK
    Content-Type: application/json
    
    {
        ...
        "codes": [
            "<code1>",
            "<code2>",
            "<code3>",
            ...
        ]
    }

Now MFA has been activated on the account! All future password authentication attempts will require MFA validation.