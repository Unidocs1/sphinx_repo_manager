=================
Plug-ins and SDKs
=================

.. toctree::
   :caption: General Purpose SDKs

   C++ SDK <https://acceleratxr.io/projects/sdk-cpp/en/latest/>
   C# SDK <https://acceleratxr.io/projects/sdk-csharp/en/latest/>
   nodejs

.. toctree::
   :caption: Game Engine Plug-ins

   unity
   unreal

Xsolla Backend provides SDKs and plug-ins for a variety of popular programming languages and game engines including
C++, C#, JavaScript (TypeScript), Unreal and Unity.

Common SDK Features
===================

Each SDK implements the same structure and API to make it easier when switching between languages and device platforms.
The SDKs contain the following common components:

CoreSDK Class
~~~~~~~~~~~~~

The *CoreSDK* class serves as the entry point of the SDK to which all initialization and setup is performed. It is
also the primary instance and accessor for the underlying services. The class take a `Configuration` instance as a
constructor argument containing all necessary information needed to initialize the SDK for communication with a
given backend.

Data Structures
~~~~~~~~~~~~~~~

All data structures within the Xsolla Backend engine are defined as classes, typically under a sub-folder named `models`.
Each model class within the SDK is backed by one or more REST API endpoints and associated service classes for accessing
that data model.

Service Classes
~~~~~~~~~~~~~~~

Interaction with the backend REST API is done via a **Service** class instance for a given model class. For example, the
SDK has a class named `User` for the data structure describing user accounts in addition to a service class named
`UserService`. The `UserService` class exposes the backend's REST API for working with `User` data to the SDK user.

Service Factory
~~~~~~~~~~~~~~~

The `ServiceFactory` is a utility class for accessing instances of service classes (described above) for a given data
type. The `ServiceFactory` is accessible via the `CoreSDK` instance via property accessor.
