---
title: "1.0.0.alpha"
date: 2019-11-22T23:48:48.249Z
---

[![pipeline status](https://gitlab.com/AcceleratXR/Core/progression_services/badges/master/pipeline.svg)](https://gitlab.com/AcceleratXR/Core/progression_services/commits/master)
[![coverage report](https://gitlab.com/AcceleratXR/Core/progression_services/badges/master/coverage.svg)](https://gitlab.com/AcceleratXR/Core/progression_services/commits/master)

Provides a system for tracking of persona progress with support for levels, skill trees and classes.

## Getting Started

To get started using this service first clone the source. It is highly recommended that you fork the project first.

```bash
git clone https://gitlab.com/AcceleratXR/Core/progression_services.git
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
