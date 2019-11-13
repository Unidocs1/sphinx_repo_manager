---
title: "About"
date: 2019-03-15T20:09:14-07:00
weight: 1
---

_AcceleratXR_ is a modern and robust framework and set of services for building massively scalable back-end services for real-time interactive products and services. Also featuring great client SDK support (provided in several languages) for building online capabilities into products.

## Why AcceleratXR?

_AcceleratXR_ technology is designed to enable ground-breaking solutions for the upcoming wave of Extended Reality products and services while also being able to meet and exceed the needs of developers of more traditional games and entertainment products. Our technology is the only production-ready open source solution on the market today and provides a robust set of out-of-the-box features developers need and want.

Bolstered further by our micro-services based architecture AcceleratXR is a perfect fit for any organization, whether small or large, to integrate only the features needed to ship a product. Complete customization is our top priority and every effort has been made to create and expose a simple API to extend and customize every aspect of each system and feature.

As veteran game developers we understand the requirement to be able to handle millions of active simultaneous users. Our team has vast experience building online technology for some of the biggest titles in the gaming industry. We are bringing this knowledge and experience into every part of AcceleratXR so that developers can focus on what matters most; building a high quality experience for their customers. This is why we've chosen proven standards and technologies to ensure that our code will perform at massive scale with grace and speed.

We also understand that consumers and enterprise users demand high availability for their products. That's why a part of our approach is to provide zero down-time for patches and maintenance. We utilize enterprise industry proven best practices and standards in order to give AcceleratXR technology the ability to maintain near perfect up-time while supporting capabilities such as in-place updates, blue-green deployments and concurrent API versioning for backwards compatibility.

Whether you need only a single feature like our revolutionary matchmaking system or you are starting from scratch and need a complete back-end solution AcceleratXR can provide the tools you need to ship product. Take a look at our growing list of features below.

## Architecture & Design

_AcceleratXR_ is a micro-services architecture. That means each system exists as a standalone unit containing all the information it needs to perform its work. This structure makes it possible to scale to millions of concurrent users simply and efficiently. It also allows developers to easily integrate individual systems and features into new or existing back-end infrastructure without wasting time and resources. The combination of one or more of these micro-services used together is referred to as an AcceleratXR cluster.

All systems and features provide a complete API for a single purpose such as user management, matchmaking, character and inventory management, etc. All data transmitted to and from each micro-service is encoded as _JavaScript Object Notation (JSON)_ with transmission occurring via either the HTTP or WebSocket protocol.

Authentication is implemented using the _[JSON Web Token (JWT)](http://jwt.io)_ standard where the payload includes all relevant user information for a service to be able to perform operations on that user's behalf. Due to the decentralized nature of JWT tokens it is therefore not required for any micro-service to negotiate or validate a token against a central authoritative server. This eliminates an important bottleneck with the cluster's architecture and design over other methodologies.

As _AcceleratXR_ is a feature first technology solution each micro-service is focused on providing a complete feature or system implementation that can be custom tailored to meet any desired scenario. This means that each micro-service should provide complete out-of-the-box functionality for the average use case, while also providing the necessary hooks and customization paths in order to easily extend and customize that system for any desired use case.

Cluster deployment, auto-scaling and management is handled using the Kubernetes orchestration system. In addition, each micro-service implements the OpenAPI Specification standard allowing the cluster to perform automatic service discovery and routing via the Envoy Proxy load balancer. This powerful combination of cloud infrastructure technologies gives _AcceleratXR_ it's ability to seamlessly scale while providing a single consistent API to connected clients.

![Architecture Overview](/images/overview_architecture_diagram.png)

## Systems & Features

The following is a list of systems and features that are available as individual micro-services to be incorporated into any given cluster.

- [**User Account Management Services**](/docs/account_services)

  This service provides user account access and authentication as well as support for Single Sign-On authentication via popular OAuth2 compatible providers (Facebook, Google, Twitter et al).

- [**Achievements Services**](/docs/achievements_services)

  The achievements service provides a way for titles to give users targets and goals to strive for. The system allows for the definition of any arbitrary goal as an achievement and provides a mechanism for tracking a user's progress.

- [**Asset Services**](/docs/asset_services)

  Provides localized text and binary asset management making it possible for projects to have simple patch-less updates and localization built-in.

- [**Leaderboards**](/docs/leaderboard_services)

  This service provides a system for creating and managing user ranking tables and goal tracking.

- [**Matchmaking Services**](/docs/matchmaking_services)

  The matchmaking services allows projects to bring users together quickly and efficiently. Our revolutionary approach to matchmaking uses a region-less, bucket-less, search algorithm that provides incredible performance and scale capable of matching millions of users in mere seconds instead of minutes.

- [**Notification Services**](/docs/notification_services)

  This service provides push notification support allowing micro-services within a cluster to send messages to connected clients in real-time. Great for providing real-time updates to modified data and events without requiring clients to constantly poll services.

- [**Persona Services**](/docs/persona_services)

  This service provides storage and management for player data information such as avatars, characters, skills, and abilities.

- [**Quest Services**](/docs/quest_services)

  The quest service provides a robust system for defining and tracking progress of player goals.

- [**Real-Time Communication Server**](/docs/rtc_server)

  The real-time communication server is our custom server technology for implementing session based real-time games and applications. The server has features such as state replication, remote-procedure calls and event based messaging. The server provides a great alternative to game engines that don't have native server networking capability or when a simple lightweight solution is desired.

- [**Session Services**](/docs/session_services)

  Session services provides management of real-time game and lobby sessions.

- [**Server Management Services**](/docs/server_manager_services)

  This service provides a system for the management and automatic scaling of session based real-time game servers and applications. Our solution can efficiently run and scale session servers across any cloud provider and coordinate them all from a single cluster.

- [**Social Services**](/docs/social_services)

  The social services allows for the implementation of social constructs such as friends, player messaging and online presence.

- [**Analytics & Telemetry**](/docs/telemetry_services)

  Telemetry services offers a mechanism for tracking events within any system for data collection purposes that can be used in real-time or deferred post-processing.

* **Party Services** [coming soon]

  This service provides the ability for users to group together using a dedicated real-time chat and communication system.

* **Guild Services** [coming soon]

  This service provides a way for users to come together into a permanent social group with social ranks and positions and special communication channels.

* **Economy Services** [coming soon]

  The economy services provides a virtual economy system enabling products to build rich experiences where users can buy and trade items amongst eachother and/or Non-Player Characters (NPCs).
