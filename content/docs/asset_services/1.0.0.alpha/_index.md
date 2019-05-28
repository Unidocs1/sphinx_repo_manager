---
title: "Asset Services"
date: 2019-05-28T17:01:42-07:00
---

The `asset services` system provides for the management of versioned file, binary data and text assets as well as the localization of those assets. Individual assets are identified with a unique name (or key) and a particular version that maps to a set of localized files or text based upon IETF BCP 47 region codes. The system primarily manages metadata as is not directly intended as a storage system. The system is designed to work with both local and remote file storage systems in order to provide a simple solution for the total management of assets. As a result, as a developer you can deploy this service into a cluster and upload any number of asset files desired and it will be stored on the configured storage device. You can also use the system as purely a metadata manager and only create asset resources that link to another storage medium (e.g. physical disc).

## Getting Started

To get started using this service first clone the source. It is highly recommended that you fork the project first.

```bash
git clone https://gitlab.com/AcceleratXR/Core/asset_services
```

## Running the Service

Open up a new shell to the cloned folder and build the Docker image using `docker-compose`.

```bash
docker-compose build
```

You can now run the server with the following command.

```bash
docker-compose up
```

## Debugging

[Visual Studio Code](https://code.visualstudio.com/) is the recommended IDE to develop with. The project includes workspace and launch configuration files out of the box.

To debug while running via Docker Compose select the `Docker: Attach Debugger` configuration and hit the `F5` key. If you want to run the server directly and debug choose the `Launch Server` configuration.
