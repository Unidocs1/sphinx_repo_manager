[persona_services](../README.md) > [PersonaRoute](../classes/personaroute.md)

# Class: PersonaRoute

Handles all REST API requests for the endpoint `/personas`.

*__author__*: Jean-Philippe Steinmetz [info@acceleratxr.com](mailto:info@acceleratxr.com)

## Hierarchy

 `ModelRoute`<[Persona](persona.md)>

**↳ PersonaRoute**

## Index

### Constructors

* [constructor](personaroute.md#constructor)

### Properties

* [config](personaroute.md#config)
* [logger](personaroute.md#logger)
* [repo](personaroute.md#repo)

### Methods

* [canEdit](personaroute.md#canedit)
* [count](personaroute.md#count)
* [create](personaroute.md#create)
* [delete](personaroute.md#delete)
* [doCount](personaroute.md#docount)
* [doCreate](personaroute.md#docreate)
* [doDelete](personaroute.md#dodelete)
* [doFindAll](personaroute.md#dofindall)
* [doFindById](personaroute.md#dofindbyid)
* [doTruncate](personaroute.md#dotruncate)
* [doUpdate](personaroute.md#doupdate)
* [findAll](personaroute.md#findall)
* [findById](personaroute.md#findbyid)
* [initialize](personaroute.md#initialize)
* [update](personaroute.md#update)

---

## Constructors

<a id="constructor"></a>

###  constructor

⊕ **new PersonaRoute**(): [PersonaRoute](personaroute.md)

*Overrides ModelRoute.__constructor*

*Defined in routes/PersonaRoute.ts:42*

Initializes a new instance with the specified defaults.

**Returns:** [PersonaRoute](personaroute.md)

___

## Properties

<a id="config"></a>

### `<Protected>` config

**● config**: *`any`*

*Defined in routes/PersonaRoute.ts:36*

___
<a id="logger"></a>

### `<Protected>` logger

**● logger**: *`any`*

*Defined in routes/PersonaRoute.ts:39*

___
<a id="repo"></a>

### `<Protected>``<Optional>` repo

**● repo**: *`Repo`<[Persona](persona.md)>*

*Overrides ModelRoute.repo*

*Defined in routes/PersonaRoute.ts:42*

___

## Methods

<a id="canedit"></a>

### `<Private>` canEdit

▸ **canEdit**(obj: *[Persona](persona.md)*, user: *`JWTUser`*): `boolean`

*Defined in routes/PersonaRoute.ts:57*

Returns `true` if the user is allowed to create or modify the given `Persona` object.

**Parameters:**

| Name | Type | Description |
| ------ | ------ | ------ |
| obj | [Persona](persona.md) |  The \`Persona\` object to validate. |
| user | `JWTUser` |  The user to check has permission to perform the create or modify operation. |

**Returns:** `boolean`

___
<a id="count"></a>

### `<Private>` count

▸ **count**(params: *`any`*, query: *`any`*, user?: *`JWTUser`*): `Promise`<[Count](count.md)>

*Defined in routes/PersonaRoute.ts:104*

Returns the count of personas

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

▸ **create**(obj: *[Persona](persona.md)*, user?: *`JWTUser`*): `Promise`<[Persona](persona.md)>

*Defined in routes/PersonaRoute.ts:87*

Create a new persona.

**Parameters:**

| Name | Type |
| ------ | ------ |
| obj | [Persona](persona.md) |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[Persona](persona.md)>

___
<a id="delete"></a>

### `<Private>` delete

▸ **delete**(id: *`string`*, user?: *`JWTUser`*): `Promise`<`void`>

*Defined in routes/PersonaRoute.ts:141*

Deletes the persona

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

▸ **doCreate**(obj: *[Persona](persona.md)*, user?: *`any`*): `Promise`<[Persona](persona.md)>

*Inherited from ModelRoute.doCreate*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:37*

Attempts to store the object provided in `req.body` into the datastore. Upon success, sets the newly persisted object to the `result` property of the `res` argument, otherwise sends a `400 BAD REQUEST` response to the client.

**Parameters:**

| Name | Type |
| ------ | ------ |
| obj | [Persona](persona.md) |
| `Optional` user | `any` |

**Returns:** `Promise`<[Persona](persona.md)>

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

▸ **doFindAll**(params: *`any`*, query: *`any`*, user?: *`any`*): `Promise`<[Persona](persona.md)[]>

*Inherited from ModelRoute.doFindAll*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:52*

Attempts to retrieve all data model objects matching the given set of criteria as specified in the request `query`. Any results that have been found are set to the `result` property of the `res` argument. `result` is never null.

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `any` |

**Returns:** `Promise`<[Persona](persona.md)[]>

___
<a id="dofindbyid"></a>

### `<Protected>` doFindById

▸ **doFindById**(id: *`string`*, user?: *`any`*): `Promise`<[Persona](persona.md) \| `undefined`>

*Inherited from ModelRoute.doFindById*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:60*

Attempts to retrieve a single data model object as identified by the `id` parameter in the URI.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `any` |

**Returns:** `Promise`<[Persona](persona.md) \| `undefined`>

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

▸ **doUpdate**(id: *`string`*, obj: *[Persona](persona.md)*, user?: *`any`*): `Promise`<[Persona](persona.md)>

*Inherited from ModelRoute.doUpdate*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:74*

Attempts to modify an existing data model object as identified by the `id` parameter in the URI.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| obj | [Persona](persona.md) |
| `Optional` user | `any` |

**Returns:** `Promise`<[Persona](persona.md)>

___
<a id="findall"></a>

### `<Private>` findAll

▸ **findAll**(params: *`any`*, query: *`any`*, user?: *`JWTUser`*): `Promise`<`Array`<[Persona](persona.md)>>

*Defined in routes/PersonaRoute.ts:74*

Returns all personas from the system that the user has access to

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<`Array`<[Persona](persona.md)>>

___
<a id="findbyid"></a>

### `<Private>` findById

▸ **findById**(id: *`string`*, user?: *`JWTUser`*): `Promise`<[Persona](persona.md)>

*Defined in routes/PersonaRoute.ts:113*

Returns a single persona from the system that the user has access to

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[Persona](persona.md)>

___
<a id="initialize"></a>

### `<Private>` initialize

▸ **initialize**(): `Promise`<`void`>

*Defined in routes/PersonaRoute.ts:65*

Called on server startup to initialize the route with any defaults.

**Returns:** `Promise`<`void`>

___
<a id="update"></a>

### `<Private>` update

▸ **update**(id: *`string`*, obj: *[Persona](persona.md)*, user?: *`JWTUser`*): `Promise`<[Persona](persona.md)>

*Defined in routes/PersonaRoute.ts:122*

Updates a single persona

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| obj | [Persona](persona.md) |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[Persona](persona.md)>

___

