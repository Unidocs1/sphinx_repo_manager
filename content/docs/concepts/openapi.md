---
title: "Open API"
date: 2019-03-18T17:01:42-07:00
weight: 1
---

_AcceleratXR_ makes extensive use of the [OpenAPI Specification](https://www.openapis.org/) standard. All services start with an OpenAPI specification file that is processed by our custom [code generator](/docs/axr-generator). The output that the generator produces is a nearly complete micro-service implementation based on the specification provided. In order to make this possible we have added several custom extensions.

| Field Name   | Parent                                                                                                         | Type                                                                                                          | Description                                                                                                                                                                                          |
| ------------ | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| x-baseClass  | [Schema Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#schemaObject)       | string                                                                                                        | The name of the base class to use when defining the schema's class file. Possible values are: `None`, `BaseEntity`, `BaseMongoEntity`, `SimpleEntity`, `SimpleMongoEntity`. Default value is `None`. |
| x-datastores | [Components](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#componentsObject)      | Map[string, Datastore Object]                                                                                 | A map containing all datastore definition objects.                                                                                                                                                   |
| x-datastore  | [Schema Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#schemaObject)       | Object                                                                                                        | Describes a single datastore connection the service uses.                                                                                                                                            |
| x-identifier | [Schema Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#schemaObject)       | boolean                                                                                                       | Set to `true` to indicate the Schema property is an indentifier.                                                                                                                                     |
| x-index      | [Schema Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#schemaObject)       | boolean                                                                                                       | Set to `true` to indicate the Schema property is an index.                                                                                                                                           |
| x-name       | [Operation Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject) | [Path Item Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#pathItemObject) | string                                                                                                                                                                                               | The unique name of the operation that is used for the route handler or SDK service function name. |
| x-schema     | [Path Item Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#pathItemObject)  | The name of a Schema Object that the path handles operations for.                                             |
| x-unique     | [Schema Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#schemaObject)       | boolean                                                                                                       | Set to `true` to indicate the Schema property must be unique.                                                                                                                                        |

## Datastore Object

The Datastore Object is used to identify what database types and connection information is required by the service.

| Field Name | Type   | Description                                           |
| ---------- | ------ | ----------------------------------------------------- |
| type       | string | **REQUIRED**. The type of database engine to be used. |
| url        | string | The connection URL to the database.                   |
