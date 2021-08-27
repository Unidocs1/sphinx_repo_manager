==============
Social Profile
==============

The user ``Profile`` is for storing social profile data about a user. The ``Profile`` object contains information such as the user's current online ``presence``\ , an alternate name or ``alias`` by which the user wants to identify to others as, as well as an arbitrary set of ``data`` that can contain any application-specific metadata.

Alias
-----

Often times a user wishes to be identifiable by another name from their real name. The ``alias`` is a way for a user to provide this alternate name that can be displayed to others. The alias is not gauranteed to be unique within the system.

Avatar
------

The ``avatar`` property stores a UUID, URI or other identifier that the application uses to render or display an custom avatar for the user.

Presence
--------

Online presence is application-specific data that allows other users to know what their friends are actively doing. The ``presence`` property takes an arbitrary data object that can contain any useful information that the application needs to identify and display the current state of the user. The value of this property does not have an expiration time associated with it. Therefore, it is the responsibility of the client application to update this property when the state changes, including during a logout event as the user logs offline.

Data
----

The ``data`` property allows an application to store any arbitrary social profile information that the user and/or application may care about. The value is stored as a key-value pair object whose keys are the names of the data properties desired.

For example let's assume an application that stores links to various third-party social networking profiles for a given user. This may look like the following.

.. code-block:: javascript

   data: {
       facebook: "https://www.facebook.com/acceleratxr",
       linkedin: "https://www.linkedin.com/company/acceleratxr/",
       twitter: "https://twitter.com/acceleratxr",
   },
