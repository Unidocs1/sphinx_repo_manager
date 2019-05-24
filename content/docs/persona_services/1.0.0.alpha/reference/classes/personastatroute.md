[persona_services](../README.md) > [PersonaStatRoute](../classes/personastatroute.md)

# Class: PersonaStatRoute

Handles all REST API requests for the endpoint `/personas/stats`.

*__author__*: Jean-Philippe Steinmetz [info@acceleratxr.com](mailto:info@acceleratxr.com)

## Hierarchy

 `ModelRoute`<[PersonaStat](personastat.md)>

**↳ PersonaStatRoute**

## Index

### Constructors

* [constructor](personastatroute.md#constructor)

### Properties

* [config](personastatroute.md#config)
* [logger](personastatroute.md#logger)
* [personaRepo](personastatroute.md#personarepo)
* [repo](personastatroute.md#repo)
* [statDefRepo](personastatroute.md#statdefrepo)

### Methods

* [canEdit](personastatroute.md#canedit)
* [count](personastatroute.md#count)
* [create](personastatroute.md#create)
* [delete](personastatroute.md#delete)
* [deleteByPersonaId](personastatroute.md#deletebypersonaid)
* [doCount](personastatroute.md#docount)
* [doCreate](personastatroute.md#docreate)
* [doDelete](personastatroute.md#dodelete)
* [doFindAll](personastatroute.md#dofindall)
* [doFindById](personastatroute.md#dofindbyid)
* [doTruncate](personastatroute.md#dotruncate)
* [doUpdate](personastatroute.md#doupdate)
* [findAll](personastatroute.md#findall)
* [findAllByPersonaId](personastatroute.md#findallbypersonaid)
* [findById](personastatroute.md#findbyid)
* [findByIdAndPersonaId](personastatroute.md#findbyidandpersonaid)
* [initialize](personastatroute.md#initialize)
* [update](personastatroute.md#update)
* [updateByPersonaId](personastatroute.md#updatebypersonaid)
* [validate](personastatroute.md#validate)

---

## Constructors

<a id="constructor"></a>

###  constructor

⊕ **new PersonaStatRoute**(): [PersonaStatRoute](personastatroute.md)

*Overrides ModelRoute.__constructor*

*Defined in routes/PersonaStatRoute.ts:50*

Initializes a new instance with the specified defaults.

**Returns:** [PersonaStatRoute](personastatroute.md)

___

## Properties

<a id="config"></a>

### `<Protected>` config

**● config**: *`any`*

*Defined in routes/PersonaStatRoute.ts:38*

___
<a id="logger"></a>

### `<Protected>` logger

**● logger**: *`any`*

*Defined in routes/PersonaStatRoute.ts:41*

___
<a id="personarepo"></a>

### `<Protected>``<Optional>` personaRepo

**● personaRepo**: *`Repo`<[Persona](persona.md)>*

*Defined in routes/PersonaStatRoute.ts:47*

___
<a id="repo"></a>

### `<Protected>``<Optional>` repo

**● repo**: *`Repo`<[PersonaStat](personastat.md)>*

*Overrides ModelRoute.repo*

*Defined in routes/PersonaStatRoute.ts:44*

___
<a id="statdefrepo"></a>

### `<Protected>``<Optional>` statDefRepo

**● statDefRepo**: *`Repo`<[PersonaStatDefinition](personastatdefinition.md)>*

*Defined in routes/PersonaStatRoute.ts:50*

___

## Methods

<a id="canedit"></a>

### `<Private>` canEdit

▸ **canEdit**(persona: *[Persona](persona.md)*, obj: *[PersonaStat](personastat.md)*, user: *`JWTUser`*): `boolean`

*Defined in routes/PersonaStatRoute.ts:66*

Returns `true` if the user is allowed to create or modify the given `PersonaStat` object.

**Parameters:**

| Name | Type | Description |
| ------ | ------ | ------ |
| persona | [Persona](persona.md) |  The \`Persona\` object taht owns the \`PersonaStat\`. |
| obj | [PersonaStat](personastat.md) |  The \`PersonaStat\` object to validate. |
| user | `JWTUser` |  The user to check has permission to perform the create or modify operation. |

**Returns:** `boolean`

___
<a id="count"></a>

### `<Private>` count

▸ **count**(params: *`any`*, query: *`any`*, user?: *`JWTUser`*): `Promise`<[Count](count.md)>

*Defined in routes/PersonaStatRoute.ts:158*

Returns the count of persona stats

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

▸ **create**(obj: *[PersonaStat](personastat.md)*, user?: *`JWTUser`*): `Promise`<[PersonaStat](personastat.md)>

*Defined in routes/PersonaStatRoute.ts:123*

Create a new stat for an persona

**Parameters:**

| Name | Type |
| ------ | ------ |
| obj | [PersonaStat](personastat.md) |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[PersonaStat](personastat.md)>

___
<a id="delete"></a>

### `<Private>` delete

▸ **delete**(id: *`string`*, user?: *`JWTUser`*): `Promise`<`void`>

*Defined in routes/PersonaStatRoute.ts:220*

Deletes the persona stat

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<`void`>

___
<a id="deletebypersonaid"></a>

### `<Private>` deleteByPersonaId

▸ **deleteByPersonaId**(personaUid: *`string`*, statUid: *`string`*, user?: *`JWTUser`*): `Promise`<`void`>

*Defined in routes/PersonaStatRoute.ts:323*

Deletes the persona stat

**Parameters:**

| Name | Type |
| ------ | ------ |
| personaUid | `string` |
| statUid | `string` |
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

▸ **doCreate**(obj: *[PersonaStat](personastat.md)*, user?: *`any`*): `Promise`<[PersonaStat](personastat.md)>

*Inherited from ModelRoute.doCreate*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:37*

Attempts to store the object provided in `req.body` into the datastore. Upon success, sets the newly persisted object to the `result` property of the `res` argument, otherwise sends a `400 BAD REQUEST` response to the client.

**Parameters:**

| Name | Type |
| ------ | ------ |
| obj | [PersonaStat](personastat.md) |
| `Optional` user | `any` |

**Returns:** `Promise`<[PersonaStat](personastat.md)>

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

▸ **doFindAll**(params: *`any`*, query: *`any`*, user?: *`any`*): `Promise`<[PersonaStat](personastat.md)[]>

*Inherited from ModelRoute.doFindAll*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:52*

Attempts to retrieve all data model objects matching the given set of criteria as specified in the request `query`. Any results that have been found are set to the `result` property of the `res` argument. `result` is never null.

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `any` |

**Returns:** `Promise`<[PersonaStat](personastat.md)[]>

___
<a id="dofindbyid"></a>

### `<Protected>` doFindById

▸ **doFindById**(id: *`string`*, user?: *`any`*): `Promise`<[PersonaStat](personastat.md) \| `undefined`>

*Inherited from ModelRoute.doFindById*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:60*

Attempts to retrieve a single data model object as identified by the `id` parameter in the URI.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `any` |

**Returns:** `Promise`<[PersonaStat](personastat.md) \| `undefined`>

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

▸ **doUpdate**(id: *`string`*, obj: *[PersonaStat](personastat.md)*, user?: *`any`*): `Promise`<[PersonaStat](personastat.md)>

*Inherited from ModelRoute.doUpdate*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:74*

Attempts to modify an existing data model object as identified by the `id` parameter in the URI.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| obj | [PersonaStat](personastat.md) |
| `Optional` user | `any` |

**Returns:** `Promise`<[PersonaStat](personastat.md)>

___
<a id="findall"></a>

### `<Private>` findAll

▸ **findAll**(params: *`any`*, query: *`any`*, user?: *`JWTUser`*): `Promise`<`Array`<[PersonaStat](personastat.md)>>

*Defined in routes/PersonaStatRoute.ts:110*

Returns all persona stats from the system that the user has access to

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<`Array`<[PersonaStat](personastat.md)>>

___
<a id="findallbypersonaid"></a>

### `<Private>` findAllByPersonaId

▸ **findAllByPersonaId**(params: *`any`*, query: *`any`*, user?: *`JWTUser`*): `Promise`<`Array`<[PersonaStat](personastat.md)>>

*Defined in routes/PersonaStatRoute.ts:249*

Returns all persona stats from the system that the user has access to

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<`Array`<[PersonaStat](personastat.md)>>

___
<a id="findbyid"></a>

### `<Private>` findById

▸ **findById**(id: *`string`*, user?: *`JWTUser`*): `Promise`<[PersonaStat](personastat.md)>

*Defined in routes/PersonaStatRoute.ts:167*

Returns a single persona stat from the system that the user has access to

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[PersonaStat](personastat.md)>

___
<a id="findbyidandpersonaid"></a>

### `<Private>` findByIdAndPersonaId

▸ **findByIdAndPersonaId**(statUid: *`string`*, user?: *`JWTUser`*): `Promise`<[PersonaStat](personastat.md)>

*Defined in routes/PersonaStatRoute.ts:262*

Returns a single persona stat from the system that the user has access to

**Parameters:**

| Name | Type |
| ------ | ------ |
| statUid | `string` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[PersonaStat](personastat.md)>

___
<a id="initialize"></a>

### `<Private>` initialize

▸ **initialize**(): `Promise`<`void`>

*Defined in routes/PersonaStatRoute.ts:80*

Called on server startup to initialize the route with any defaults.

**Returns:** `Promise`<`void`>

___
<a id="update"></a>

### `<Private>` update

▸ **update**(id: *`string`*, obj: *[PersonaStat](personastat.md)*, user?: *`JWTUser`*): `Promise`<[PersonaStat](personastat.md)>

*Defined in routes/PersonaStatRoute.ts:176*

Updates a single persona stat

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| obj | [PersonaStat](personastat.md) |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[PersonaStat](personastat.md)>

___
<a id="updatebypersonaid"></a>

### `<Private>` updateByPersonaId

▸ **updateByPersonaId**(personaUid: *`string`*, statUid: *`string`*, obj: *[PersonaStat](personastat.md)*, user?: *`JWTUser`*): `Promise`<[PersonaStat](personastat.md)>

*Defined in routes/PersonaStatRoute.ts:274*

Updates a single persona stat

**Parameters:**

| Name | Type |
| ------ | ------ |
| personaUid | `string` |
| statUid | `string` |
| obj | [PersonaStat](personastat.md) |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[PersonaStat](personastat.md)>

___
<a id="validate"></a>

### `<Private>` validate

▸ **validate**(def: *[PersonaStatDefinition](personastatdefinition.md)*, obj: *[PersonaStat](personastat.md)*): `void`

*Defined in routes/PersonaStatRoute.ts:90*

Validates that the provided `PersonaStat` object is valid.

*__throws__*: An error if the validation check fails

**Parameters:**

| Name | Type | Description |
| ------ | ------ | ------ |
| def | [PersonaStatDefinition](personastatdefinition.md) |  The definition of the stat to validate against. |
| obj | [PersonaStat](personastat.md) |  The stat to validate. |

**Returns:** `void`

___

