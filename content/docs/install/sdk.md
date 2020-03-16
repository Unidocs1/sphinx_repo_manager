---
title: "AXR Core SDK"
date: 2019-05-28T17:50:05-07:00
---

The 'AcceleratXR Core Software Development Kit (AXRCoreSDK)' is intended to be used by game clients and applications that wish to access AcceleratXR powered services. The SDK comes in five flavors.

- C++ Library
- C# Library
- JavaScript/TypeScript Library
- Unity Plug-in
- Unreal Plug-in

## Concepts

All of the SDK libraries have a similar structure and set of features. Each uses heavy asynchronous programming models to simplify development and reduce boilerplate code. In C++, this is accomplished using the powerful Microsoft Parallel Patterns Library. In C#, this is handled using the built-in `Task` patterns API. In JavaScript/TypeScript this is handled using the `Promises` API.

### Models

Every AcceleratXR service exposes a series of endpoints that all map to a particular data model. Each represented data model contains information related to the task or job that the service manages. In the case of account management, the data models `User` and `Role` objects. In the case of `matchmaking_services` the system deals with `Ticket` objects. For each data model of each system there is a corresponding class in the SDK library of the same name.

When working with the SDK it is important to note that you will primarily be working with these data model structures. Data contained in these structures will automatically be serialized and deserialized when communicating between an AcceleratXR powered services cluster and the client SDK. It is therefore not neceessary to decode or unpack messages on your own.

### Services

In order to interact with the backend services you will need to send HTTP requests to the appropriate endpoints for each data model resource. All of the complexity of this communication has been wrapped up and abstracted for you into `Service` classes. These classes are utilities that provide all of the supported operations through a simple interface. Access to the interface is provided through a `ServiceFactory` which handles any configuration and set up that is necessary for the service class to function.

### EntityWatchdog

It is often necessary at times to monitor a particular data object as it changes over time. Traditionally this meant that you needed to write logic to poll the backend for changes. Within the SDK resides a utility class called the `EntityWatchdog`. This class can be used to automatically monitor a specific object for data changes. Internally it will establish a websocket connection to the backend and await for any data changes pushed from the backend. If a websocket connection cannot be reliably established then the utility will fall back to traditional polling techniques.

## C++ Library

The C++ library is a C++13 compatible library that is largely built upon [cpprestsdk](https://github.com/Microsoft/cpprestsdk).

## C# Library

The C# library is a .NET Standard 2.0 compatible library.

## Unreal Engine Plug-in

The Unreal Engine Plug-in builds on top of the C++ library to provide a simplified wrapper for compiling the SDK within Unreal engine as a static library dependency. In addition, an implementation of the OnlineSubsystem is also provided which utilizes the SDK so games and applications can reuse existing platform agnostic code to work with an AcceleratXR backend.

## Unity Engine Plug-in

The Unity Engine Plug-in builds upon the C# library and adds a simplified wrapper for compiling the SDK within Unity engine. The plug-in also contains editor extensions and components that make it easier to initialize and work with the SDK.
