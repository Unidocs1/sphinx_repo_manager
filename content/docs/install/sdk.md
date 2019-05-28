---
title: "Client SDK"
date: 2019-05-28T17:50:05-07:00
---

The AcceleratXR Software Development Kit (SDK) is intended to be used by game clients and applications that wish to access AcceleratXR powered services. The SDK comes in four flavors; a general purpose C++ library, a general purpose C# library, an Unreal Engine plug-in and a Unity Engine plug-in.

## Concepts

All of the SDK libraries have a similar structure and set of features. Each uses heavy asynchronous programming models to simplify development and reduce boilerplate code common to building such code. In C++, this is accomplished using the powerful Microsoft Parallel Patterns Library. In C#, this is handled using the built-in `Task` patterns API.

### Models

Every AcceleratXR service exposes a series of endpoints that all map to a particular data model. Each represented data model contains information related to the task or job that the service manages. In the case of account management, the data models `User` and `Role` objects. In the case of `matchmaking_services` the system deals with `Ticket` and `Session` objects. For each data model of each system there is a corresponding class in the SDK library of the same name.

When working with the SDK it is important to note that you will primarily be working with these data model structures. Data contained in these structures will automatically be serialized and deserialized when communicating between an AcceleratXR powered services cluster and the client SDK. It is therefore not neceessary to decode or unpack messages on your own.

### Services

In order to interact with the backend services you will need to send HTTP requests to the appropriate endpoints for each data model resource. All of the complexity of this communication has been wrapped up and abstracted for you into `Service` classes. These classes are utilities that provide all of the supported operations through a simple interface. Access to the interface is provided through a `ServiceFactory` which handles any configuration and set up that is necessary for the service class to function.

## C++ Library

The C++ library is a C++13 compatible library that is largely built upon the [cpprestsdk](https://github.com/Microsoft/cpprestsdk) library.

## C# Library

The C# library is still in active development and has not been officially released. Please [contact us](mailto:info@acceleratxr.com?subject=C# SDK) if you would like access.

## Unreal Engine Plug-in

The Unreal Engine Plug-in builds on top of the C++ library and provides a series of special utility functions and classes in order to simplify development with that engine.

## Unity Engine Plug-in

The Unity Engine Plug-in is still in active development and has not been officially released. Please [contact us](mailto:info@acceleratxr.com?subject=Unity SDK) if you would like access.
