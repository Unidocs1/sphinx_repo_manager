---
title: "1.0.0.alpha"
date: 2019-05-22T10:58:00-08:00
---

Provides services for the management of user personas. A `Persona` is a digital representation of a user (aka avatar) within a game or application. Users can have more than one `Persona` associated with their account. Each `Persona` has data associated with it including statistics which can describe arbitrary attributes about the user's persona.

## Getting Started

To get started using this service first clone the source. It is highly recommended that you fork the project first.

```bash
git clone https://gitlab.com/AcceleratXR/Core/persona_services
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
