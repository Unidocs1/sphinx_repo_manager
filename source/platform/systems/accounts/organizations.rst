==============================
Organizations **[ENTERPRISE]**
==============================

.. attention::
    Requires license to AcceleratXR **Enterprise**.

A user Organization is an additional level of abstraction allowing for the grouping of multiple users together into
virtual teams.

Members
=======

Each organization has a list of member users. These users have access to any and all resources defined for the
organization. While members have permission to view organization data such as other members and owners, they
do not have permission to modify or delete an Organization or any of its members.

Owners
======

An Organization owner is a user in which has full control over the organization itself and all users that are members
as well as other owners.

Roles
=====

User roles can be associated with a given organization by prefixing the name of the role with the ``uid`` of the
organization. This makes it easily possible to define a variety of roles, all specific to different organizations.

By default, a set of roles are automatically created when each organization is created corresponding
to the *Trusted Roles* of the system. This effectively grants any owner of the organization superuser permission to
perform any action on behalf of the organization.