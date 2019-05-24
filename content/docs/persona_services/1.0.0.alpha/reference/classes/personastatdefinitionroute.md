[persona_services](../README.md) > [PersonaStatDefinitionRoute](../classes/personastatdefinitionroute.md)

# Class: PersonaStatDefinitionRoute

Handles all REST API requests for the endpoint `/personas/stats/definitions`.

*__author__*: Jean-Philippe Steinmetz [info@acceleratxr.com](mailto:info@acceleratxr.com)

## Hierarchy

 `ModelRoute`<[PersonaStatDefinition](personastatdefinition.md)>

**↳ PersonaStatDefinitionRoute**

## Index

### Constructors

* [constructor](personastatdefinitionroute.md#constructor)

### Properties

* [config](personastatdefinitionroute.md#config)
* [logger](personastatdefinitionroute.md#logger)
* [repo](personastatdefinitionroute.md#repo)

### Methods

* [canEdit](personastatdefinitionroute.md#canedit)
* [count](personastatdefinitionroute.md#count)
* [create](personastatdefinitionroute.md#create)
* [delete](personastatdefinitionroute.md#delete)
* [doCount](personastatdefinitionroute.md#docount)
* [doCreate](personastatdefinitionroute.md#docreate)
* [doDelete](personastatdefinitionroute.md#dodelete)
* [doFindAll](personastatdefinitionroute.md#dofindall)
* [doFindById](personastatdefinitionroute.md#dofindbyid)
* [doTruncate](personastatdefinitionroute.md#dotruncate)
* [doUpdate](personastatdefinitionroute.md#doupdate)
* [findAll](personastatdefinitionroute.md#findall)
* [findById](personastatdefinitionroute.md#findbyid)
* [initialize](personastatdefinitionroute.md#initialize)
* [update](personastatdefinitionroute.md#update)
* [validate](personastatdefinitionroute.md#validate)

---

## Constructors

<a id="constructor"></a>

###  constructor

⊕ **new PersonaStatDefinitionRoute**(): [PersonaStatDefinitionRoute](personastatdefinitionroute.md)

*Overrides ModelRoute.__constructor*

*Defined in routes/PersonaStatDefinitionRoute.ts:42*

Initializes a new instance with the specified defaults.

**Returns:** [PersonaStatDefinitionRoute](personastatdefinitionroute.md)

___

## Properties

<a id="config"></a>

### `<Protected>` config

**● config**: *`any`*

*Defined in routes/PersonaStatDefinitionRoute.ts:36*

___
<a id="logger"></a>

### `<Protected>` logger

**● logger**: *`any`*

*Defined in routes/PersonaStatDefinitionRoute.ts:39*

___
<a id="repo"></a>

### `<Protected>``<Optional>` repo

**● repo**: *`Repo`<[PersonaStatDefinition](personastatdefinition.md)>*

*Overrides ModelRoute.repo*

*Defined in routes/PersonaStatDefinitionRoute.ts:42*

___

## Methods

<a id="canedit"></a>

### `<Private>` canEdit

▸ **canEdit**(obj: *[PersonaStatDefinition](personastatdefinition.md)*, user: *`JWTUser`*): `boolean`

*Defined in routes/PersonaStatDefinitionRoute.ts:57*

Returns `true` if the user is allowed to create or modify the given `PersonaStatDefinition` object.

**Parameters:**

| Name | Type | Description |
| ------ | ------ | ------ |
| obj | [PersonaStatDefinition](personastatdefinition.md) |  The \`PersonaStatDefinition\` object to validate. |
| user | `JWTUser` |  The user to check has permission to perform the create or modify operation. |

**Returns:** `boolean`

___
<a id="count"></a>

### `<Private>` count

▸ **count**(params: *`any`*, query: *`any`*, user?: *`JWTUser`*): `Promise`<[Count](count.md)>

*Defined in routes/PersonaStatDefinitionRoute.ts:141*

Returns the count of persona stat definitions

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[Count](count.md)>

___
<a id="create"></a>

### `<Private>` create

▸ **create**(obj: *[PersonaStatDefinition](personastatdefinition.md)*, user?: *`JWTUser`*): `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

*Defined in routes/PersonaStatDefinitionRoute.ts:117*

Create a persona stat definitions

**Parameters:**

| Name | Type |
| ------ | ------ |
| obj | [PersonaStatDefinition](personastatdefinition.md) |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

___
<a id="delete"></a>

### `<Private>` delete

▸ **delete**(id: *`string`*, user?: *`JWTUser`*): `Promise`<`void`>

*Defined in routes/PersonaStatDefinitionRoute.ts:189*

Deletes the persona stat definition

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<`void`>

___
<a id="docount"></a>

### `<Protected>` doCount

▸ **doCount**(params: *`any`*, query: *`any`*, user?: *`any`*): `Promise`<`any`>

*Inherited from ModelRoute.doCount*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:31*

Attempts to retrieve the number of data model objects matching the given set of criteria as specified in the request `query`. Any results that have been found are set to the `result` property of the `res` argument. `result` is never null.

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `any` |

**Returns:** `Promise`<`any`>

___
<a id="docreate"></a>

### `<Protected>` doCreate

▸ **doCreate**(obj: *[PersonaStatDefinition](personastatdefinition.md)*, user?: *`any`*): `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

*Inherited from ModelRoute.doCreate*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:37*

Attempts to store the object provided in `req.body` into the datastore. Upon success, sets the newly persisted object to the `result` property of the `res` argument, otherwise sends a `400 BAD REQUEST` response to the client.

**Parameters:**

| Name | Type |
| ------ | ------ |
| obj | [PersonaStatDefinition](personastatdefinition.md) |
| `Optional` user | `any` |

**Returns:** `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

___
<a id="dodelete"></a>

### `<Protected>` doDelete

▸ **doDelete**(id: *`string`*, user?: *`any`*): `Promise`<`void`>

*Inherited from ModelRoute.doDelete*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:42*

Attempts to delete an existing data model object with a given unique identifier encoded by the URI parameter `id`.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `any` |

**Returns:** `Promise`<`void`>

___
<a id="dofindall"></a>

### `<Protected>` doFindAll

▸ **doFindAll**(params: *`any`*, query: *`any`*, user?: *`any`*): `Promise`<[PersonaStatDefinition](personastatdefinition.md)[]>

*Inherited from ModelRoute.doFindAll*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:52*

Attempts to retrieve all data model objects matching the given set of criteria as specified in the request `query`. Any results that have been found are set to the `result` property of the `res` argument. `result` is never null.

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `any` |

**Returns:** `Promise`<[PersonaStatDefinition](personastatdefinition.md)[]>

___
<a id="dofindbyid"></a>

### `<Protected>` doFindById

▸ **doFindById**(id: *`string`*, user?: *`any`*): `Promise`<[PersonaStatDefinition](personastatdefinition.md) \| `undefined`>

*Inherited from ModelRoute.doFindById*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:60*

Attempts to retrieve a single data model object as identified by the `id` parameter in the URI.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `any` |

**Returns:** `Promise`<[PersonaStatDefinition](personastatdefinition.md) \| `undefined`>

___
<a id="dotruncate"></a>

### `<Protected>` doTruncate

▸ **doTruncate**(user?: *`any`*): `Promise`<`void`>

*Inherited from ModelRoute.doTruncate*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:66*

Attempts to remove all entries of the data model type from the datastore.

**Parameters:**

| Name | Type | Description |
| ------ | ------ | ------ |
| `Optional` user | `any` |  The authenticated user performing the action, otherwise undefined. |

**Returns:** `Promise`<`void`>

___
<a id="doupdate"></a>

### `<Protected>` doUpdate

▸ **doUpdate**(id: *`string`*, obj: *[PersonaStatDefinition](personastatdefinition.md)*, user?: *`any`*): `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

*Inherited from ModelRoute.doUpdate*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:74*

Attempts to modify an existing data model object as identified by the `id` parameter in the URI.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| obj | [PersonaStatDefinition](personastatdefinition.md) |
| `Optional` user | `any` |

**Returns:** `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

___
<a id="findall"></a>

### `<Private>` findAll

▸ **findAll**(params: *`any`*, query: *`any`*, user?: *`JWTUser`*): `Promise`<`Array`<[PersonaStatDefinition](personastatdefinition.md)>>

*Defined in routes/PersonaStatDefinitionRoute.ts:104*

Returns all persona stat definitions from the system that the user has access to

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<`Array`<[PersonaStatDefinition](personastatdefinition.md)>>

___
<a id="findbyid"></a>

### `<Private>` findById

▸ **findById**(id: *`string`*, user?: *`JWTUser`*): `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

*Defined in routes/PersonaStatDefinitionRoute.ts:150*

Returns a single persona stat definition from the system that the user has access to

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

___
<a id="initialize"></a>

### `<Private>` initialize

▸ **initialize**(): `Promise`<`void`>

*Defined in routes/PersonaStatDefinitionRoute.ts:65*

Called on server startup to initialize the route with any defaults.

**Returns:** `Promise`<`void`>

___
<a id="update"></a>

### `<Private>` update

▸ **update**(id: *`string`*, obj: *[PersonaStatDefinition](personastatdefinition.md)*, user?: *`JWTUser`*): `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

*Defined in routes/PersonaStatDefinitionRoute.ts:159*

Updates a single persona stat definition

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| obj | [PersonaStatDefinition](personastatdefinition.md) |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[PersonaStatDefinition](personastatdefinition.md)>

___
<a id="validate"></a>

### `<Private>` validate

▸ **validate**(def: *[PersonaStatDefinition](personastatdefinition.md)*): `void`

*Defined in routes/PersonaStatDefinitionRoute.ts:73*

Validates the given `PersonaStatDefinition` is valid.

**Parameters:**

| Name | Type | Description |
| ------ | ------ | ------ |
| def | [PersonaStatDefinition](personastatdefinition.md) |  The \`PersonaStatDefinition\` object to validate. |

**Returns:** `void`

___

