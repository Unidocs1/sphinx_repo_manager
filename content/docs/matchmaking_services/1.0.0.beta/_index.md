---
title: "1.0.0.alpha"
date: 2019-03-15T20:09:14-07:00
---

This service provides a set of APIs for managing matchmaking tickets. A matchmaking ticket is a request from a client to be matched with other clients whom have also submitted a ticket. Matchmaking tickets can have a set of criteria that the client wishes to be matched from.

Note that this service does not perform the actual ticket processing and matching. See the [Ticket Processing](ticket_processor.md) document for detailed information on how tickets are processed.

## Introduction

Matchmaking is the process of searching a collection of users and finding a sub-collection of those users whom are all equally suited to participate in some user experience together. In a video game, this often means finding a group of players whom all have the same level of skill and want to participate in a real-time multi-player game together. However, games aren't the only use case that matchmaking is useful or. Other types of products such as social networks, virtual worlds, or even organizing a team of workers in a business setting could also make use of matchmaking technology.

The process of matchmaking includes two distinct features. The first is the matchmaking Ticket. A ticket is a representation of a single user or group that wish to be matched with other like users or groups. The ticket often carries information detailing a set of criteria the user or group cares about such as the type of game mode to be played, the rules of a particular game or information such as the network or geo-physical location of the user or group. Tickets are then placed into a specialized database that can efficiently store and sort these tickets based upon the given criteria. Then, a [Ticket Processor](ticket_processor.md) is created with the responsibility to process each ticket to find the desired sub-collections to match together. The processor will return a sub-list of tickets at a time and evaluate whether or not the given subset are alike. When a suitable subset of tickets are found the processor updates each ticket to notify the user or group that a match has been found.

## Getting Started

To get started using this service first clone the source. It is highly recommended that you fork the project first.

```bash
git clone https://gitlab.com/AcceleratXR/Core/matchmaking_services.git
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
