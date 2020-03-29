---
title: "Integrations"
date: 2019-03-17T21:21:40-07:00
weight: 1
---

Integrating _AcceleratXR_ into your game client or application is easy. A client SDK is provided for all popular languages and game engines.

## Languages & Platforms

The _AcceleratXR_ client SDK is available for the following languages and engines:

-   [C++](https://gitlab.com/AcceleratXR/Core/SDK/client_sdk_cpp)
-   [C#](https://gitlab.com/AcceleratXR/Core/SDK/client_sdk_csharp)
-   [Unity Engine](https://gitlab.com/AcceleratXR/Core/SDK/client_sdk_unity)
-   [Unreal Engine](https://gitlab.com/AcceleratXR/Core/SDK/client_sdk_unreal)
-   [NodeJS / JavaScript](https://gitlab.com/AcceleratXR/Core/sdk/client_sdk_nodejs)

## Common Structure

All of the SDKs share a common structure.

```
namespace axr::sdk
{
    namespace models
    {
        User
        ...
    }
    namespace services
    {
        UserService
        ...
    }
    namespace utils
    {
        EntityWatchdog
        ...
    }
    ClientSDK
    Configuration
    ServiceFactory
}
```

### ClientSDK

The ClientSDK class is the entry point to the SDK and is where applications begin their integration. The ClientSDK takes a Configuration object as the only argument to its `init` function which initializes the SDK. Once initialized the application can make calls to any Service class desired.

This class also provides utility functions for performing user login and account registration.

### Models

All of the data models used throughout the code base are located in the `src/models` folder. There is a single file for each data model. Any time a request is sent or received from an _AcceleratXR_ cluster it will use one of these data models.

### Services

The _Service_ class is how to make a request to the _AcceleratXR_ cluster for a particular data model. Not all data models will have corresponding service classes but every service class must have a corresponding data model. The class provides function mapping for each operation allowed on a given data model to its corresponding service.

All of the service classes are located in the `src/services` folder.

### Service Factory

The _ServiceFactory_ is a special class that manages the instances of each _Service_ class. It is a singleton class that can be accessed from anywhere in your application and provides a convenvient interface for retrieving _Service_ class instances for a given data model.
