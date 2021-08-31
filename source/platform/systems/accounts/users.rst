=====
Users
=====

Users can create accounts with the system by creating a ``User`` object with this system. Users contain a minimal
amount of personally identifiable information (PII). For instance, passwords are stored separately from the primary
user object. This is both for simplicity of the system as well as additional protection of sensitive data.

Roles
=====

The ``roles`` property of the User document contains the list of Role names that the user is a member or owner of.
This makes it more practical to quickly discover the user's permissions within the larger security system. This
list is automatically updated by the system upon any change to a Role document itself.

External IDs
============

In order to support single-sign on with external authentication providers it is important to link a user's
third-party account id with their AcceleratXR id. These IDs are stored in the ``externalIds` property as an array
of ``<type>:<uid>`` mappings that indicate which third-party provider is represented along with the universally
unique identifier for that provider.

At present there are three supported external authentication providers.

* Facebook
* Google
* Twitter

Existing external ID links may be re-associated with another account if a user performs a single-sign on attempt in
collaboration with an existing AcceleratXR authentication token.

Verifying Accounts
==================

When a new user is created, the account is considered to be ``unverified`` until that user responds to a verification
e-mail sent to the address provided at the time of creation. The verification e-mail contains a short lifespan JWT
authentication token that must be provided to the ``/users/:id/verify`` endpoint in order to prove the user received
the e-mail at the given address. Once verified the ``verified`` property is set to ``true``.

If a user changes their e-mail address at any future point, they will be required to verify the address again, even if
a previous e-mail is specified again.

Admin Account
=============

On system startup, a single user account is automatically created called the ``admin`` user. This user is given
superuser power within the system to perform any action. The login credentials of this account are logged to the stdout
of the service exactly once. It is important to save this information for future reference. Since this is an account
with root level access it is **highly recommended** that this account not be used in daily practice, even when
superuser privileges are desired.

.. attention::
    To prevent risk of unauthorized access to the system the default ``admin`` account should never be used from an
    external device. Create another user and add them as a member to one of the default **Trusted Roles** roles
    instead.