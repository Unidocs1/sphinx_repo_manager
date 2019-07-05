---
title: "Social Services"
date: 2019-07-05T22:50:13.161Z
---

A service that provides social features to users including a social profile, online presence, friends list, blocked players list and player-to-player messaging.

## Getting Started

To get started using this service first clone the source. It is highly recommended that you fork the project first.

```bash
git clone https://gitlab.com/AcceleratXR/Core/social_services.git
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

## Concepts

-   [User Profiles](concepts/profile)
-   [Player-to-Player Messaging](concepts/message)
-   [User Links](concepts/userlinks)
