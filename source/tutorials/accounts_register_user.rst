======================
How To Register a User
======================

Registering a new user with the system is quite easy. It is a two-step process in which a client must first send a
``POST`` request to the ``/users`` endpoint followed by an additional ``POST`` request to the ``/users/:id/secrets``
endpoint with a desired user secret that can be used for all future authentication.

While there are several fields that can be provided in a User document only one is actually required; ``name``.
The ``name`` field is the unique name of the user to register.

.. code-block::

    POST /users HTTP/1.1
    Host: api.demo.goaxr.cloud
    Content-Type: application/json

    {
        "name": "myusername",
    }

If the user is created successfully an object will be returned containing three fields; ``refresh``, ``token`` and
``user``. The ``refresh`` and ``token`` fields contain the JWT authentication token and refresh token used for all
future requests. The ``user`` field contains the newly created user as it was stored in the database. It is
recommended to cache this data locally for future reference.

.. code-block::

    200 OK
    Content-Type: application/json

    {
        "refresh": "f23498f72.fv4298766bfo4uvqo9.f3vlkuiq23yf3ob9q287fq9230v678br3980276qr9",
        "token": "f902e78f90827f2.f20978f23v9807039q.2vf9287vf93q879038q27f029q87vf90q2",
        "user": {
            "uid": "00000000-0000-0000-0000-000000000000",
            "name": "myusername",
            ...
        }
    }

The next step is to create a user secret. There are five types of user secrets but the most common will be the
``password`` secret. The ``password`` secret allows the user to authenticate in the future using a simple
text password. It is created like the following example.

.. code-block::

    POST /users/00000000-0000-0000-0000-000000000000/secrets HTTP/1.1
    Host: api.demo.goaxr.cloud
    Content-Type: application/json
    Authorization: jwt f902e78f90827f2.f20978f23v9807039q.2vf9287vf93q879038q27f029q87vf90q2

    {
        "type": "password",
        "secret": "MyP@ssw0rdIsS3cure!"
    }

Notice that in the above request we have specified the ``Authorization`` header. The value of this header is taken
directly from the result of the previous create request. The JWT token returned in the response of the create user
request will have a standard token lifetime, thus it does not require an aditional login step to continue using
the system. However, if no secret is created afterwards it will be impossilbe to authenticate with the account in
the future.


.. attention::
    **Always** create at least one user secret after creating an initial user account.