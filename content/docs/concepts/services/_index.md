---
title: "Services"
date: 2019-03-18T17:53:28-07:00
weight: 3
---

All backend services and features are written in [TypeScript](https://www.typescriptlang.org/) and run on the [NodeJS](https://nodejs.org) platform. This combination of tools was chosen specifically for the speed and ease of development in addition to the constantly improving runtime performance.

Each service is intended to provide only one feature or system with all necessary data storage and processing wholly contained in the service. User authentication is handled via [JWT token](security) passing which obviates the need for a constant connection to a user authentication system in order to verify requests. With this decentralized micro-service architecture systems and features can easily be developed that integrate into a variety of situations.

## Project Structure

```
/-
    /- docs                 // API, REST API and white paper documentation

    /- src
        /- models           // Data model classes
        /- routes           // REST API route handlers
        - behaviors.ts      // Utility functions aiding in route handling
        - config.ts         // Service global configuration
        - server.ts         // Server entry point
    /- test                 // Source code for automated tests

    - CONTRIBUTORS
    - docker-compose.yaml   // Docker compose configuration for local development
    - Dockerfile            // Docker image specification
    - LICENSE.pdf           // End User License Agreement
    - openapi.yaml          // OpenAPI Specification
    - package.json          // NodeJS package configuration
    - README.md             // Entry point documentation
    - tsconfig.json         // TypeScript compiler configuration
    - tslint.json           // TSLint configuration
```

### Models

Each service uses [TypeORM](https://typeorm.io) to abstract access to the datastores. This makes it easier to support connections to many of the most popular databases. TypeORM uses a decorator based API for identifying entity classes and their associated columns and configuration.

### Routes

All HTTP request processing is handled by a Route class. Each route class corresponds to a single base endpoint path such as `/users` and is responsible for processing every request sent to the service at the designated path (including sub-paths).
When the generator produces the initial code it names the route class after the model schema associated to each endpoint (via the [`x-schema`](/docs/openapi) extension). Each operation specified in the OpenAPI Specification file is then added to the route class as a separate function.
