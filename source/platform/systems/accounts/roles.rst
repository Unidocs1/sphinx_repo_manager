=====
Roles
=====

Roles are a method of organizing a collection of users for the purposes of enabling group based permissions within the system.
Within the larger security system, user id's and roles are used to identify permissions via Access Control Lists. The Access
Control List is a construct for defining the permissable operations for a given user and/or role on a given system resource.

Users can be a member and/or owner of any number of roles with no restrictions on membership. Once added to a role, the
system will add the user's id to the appropriate property of the Role document as well as the User document's ``roles``
property. This allows easy retrievable of any user's roles without requiring additional searches.

Members
=======
Users can be assigned as members to a given Role object. A member inherits all permissions of the role to perform actions
permissible to that group within the system. Members however only have permission to view Role data and have no permission
to modify or delete the role itself.

Owners
======

A Role owners is a user with full privileges to add, modify and delete a Role, including any and all members, metadata and
additional owners. While it is possible to define a user as only an owner of a Role, it is functionally equivalent to being
both a member and an owner as the system does not make any distinction between the two. An owner is always a member of the
role regardless of whether they are explicitly listed as a member or not.

Trusted Roles
=============

On startup the system will automatically create a set of roles which are considered to be for those users with
superuser permissions. These roles are called **Trusted Roles** and are explicitly declared in the cluster's configuration
setting upon deployment.