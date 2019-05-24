[telemetry_services](../README.md) > [EventRoute](../classes/eventroute.md)

# Class: EventRoute

Handles all REST API requests for the endpoint `/events`.

*__author__*: Jean-Philippe Steinmetz [info@acceleratxr.com](mailto:info@acceleratxr.com)

## Hierarchy

 `ModelRoute`<[Event](event.md)>

**↳ EventRoute**

## Index

### Constructors

* [constructor](eventroute.md#constructor)

### Properties

* [repo](eventroute.md#repo)

### Methods

* [count](eventroute.md#count)
* [create](eventroute.md#create)
* [doCount](eventroute.md#docount)
* [doCreate](eventroute.md#docreate)
* [doDelete](eventroute.md#dodelete)
* [doFindAll](eventroute.md#dofindall)
* [doFindById](eventroute.md#dofindbyid)
* [doTruncate](eventroute.md#dotruncate)
* [doUpdate](eventroute.md#doupdate)
* [findAll](eventroute.md#findall)
* [findById](eventroute.md#findbyid)
* [initialize](eventroute.md#initialize)
* [validate](eventroute.md#validate)

---

## Constructors

<a id="constructor"></a>

###  constructor

⊕ **new EventRoute**(): [EventRoute](eventroute.md)

*Overrides ModelRoute.__constructor*

*Defined in routes/EventRoute.ts:34*

Initializes a new instance with the specified defaults.

**Returns:** [EventRoute](eventroute.md)

___

## Properties

<a id="repo"></a>

### `<Protected>``<Optional>` repo

**● repo**: *`Repo`<[Event](event.md)>*

*Overrides ModelRoute.repo*

*Defined in routes/EventRoute.ts:34*

___

## Methods

<a id="count"></a>

### `<Private>` count

▸ **count**(params: *`any`*, query: *`any`*, user?: *`JWTUser`*): `Promise`<[Count](count.md)>

*Defined in routes/EventRoute.ts:121*

Returns the count of events based on the given criteria.

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

▸ **create**(obj: *[Event](event.md)*, user?: *`JWTUser`*): `Promise`<[Event](event.md)>

*Defined in routes/EventRoute.ts:101*

Creates a new event record in the database.

**Parameters:**

| Name | Type |
| ------ | ------ |
| obj | [Event](event.md) |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[Event](event.md)>

___
<a id="docount"></a>

### `<Protected>` doCount

▸ **doCount**(params: *`any`*, query: *`any`*, user?: *`any`*): `Promise`<`any`>

*Inherited from ModelRoute.doCount*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:31*

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

▸ **doCreate**(obj: *[Event](event.md)*, user?: *`any`*): `Promise`<[Event](event.md)>

*Inherited from ModelRoute.doCreate*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:37*

Attempts to store the object provided in `req.body` into the datastore. Upon success, sets the newly persisted object to the `result` property of the `res` argument, otherwise sends a `400 BAD REQUEST` response to the client.

**Parameters:**

| Name | Type |
| ------ | ------ |
| obj | [Event](event.md) |
| `Optional` user | `any` |

**Returns:** `Promise`<[Event](event.md)>

___
<a id="dodelete"></a>

### `<Protected>` doDelete

▸ **doDelete**(id: *`string`*, user?: *`any`*): `Promise`<`void`>

*Inherited from ModelRoute.doDelete*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:42*

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

▸ **doFindAll**(params: *`any`*, query: *`any`*, user?: *`any`*): `Promise`<[Event](event.md)[]>

*Inherited from ModelRoute.doFindAll*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:52*

Attempts to retrieve all data model objects matching the given set of criteria as specified in the request `query`. Any results that have been found are set to the `result` property of the `res` argument. `result` is never null.

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `any` |

**Returns:** `Promise`<[Event](event.md)[]>

___
<a id="dofindbyid"></a>

### `<Protected>` doFindById

▸ **doFindById**(id: *`string`*, user?: *`any`*): `Promise`<[Event](event.md) \| `undefined`>

*Inherited from ModelRoute.doFindById*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:60*

Attempts to retrieve a single data model object as identified by the `id` parameter in the URI.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `any` |

**Returns:** `Promise`<[Event](event.md) \| `undefined`>

___
<a id="dotruncate"></a>

### `<Protected>` doTruncate

▸ **doTruncate**(user?: *`any`*): `Promise`<`void`>

*Inherited from ModelRoute.doTruncate*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:66*

Attempts to remove all entries of the data model type from the datastore.

**Parameters:**

| Name | Type | Description |
| ------ | ------ | ------ |
| `Optional` user | `any` |  The authenticated user performing the action, otherwise undefined. |

**Returns:** `Promise`<`void`>

___
<a id="doupdate"></a>

### `<Protected>` doUpdate

▸ **doUpdate**(id: *`string`*, obj: *[Event](event.md)*, user?: *`any`*): `Promise`<[Event](event.md)>

*Inherited from ModelRoute.doUpdate*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/services_common/dist/types/routes/ModelRoute.d.ts:74*

Attempts to modify an existing data model object as identified by the `id` parameter in the URI.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| obj | [Event](event.md) |
| `Optional` user | `any` |

**Returns:** `Promise`<[Event](event.md)>

___
<a id="findall"></a>

### `<Private>` findAll

▸ **findAll**(params: *`any`*, query: *`any`*, user?: *`JWTUser`*): `Promise`<`Array`<[Event](event.md)>>

*Defined in routes/EventRoute.ts:92*

Returns all events from the system that the user has access to based upon the given criteria.

**Parameters:**

| Name | Type |
| ------ | ------ |
| params | `any` |
| query | `any` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<`Array`<[Event](event.md)>>

___
<a id="findbyid"></a>

### `<Private>` findById

▸ **findById**(id: *`string`*, user?: *`JWTUser`*): `Promise`<[Event](event.md)>

*Defined in routes/EventRoute.ts:130*

Returns a single event from the system that the user has access to.

**Parameters:**

| Name | Type |
| ------ | ------ |
| id | `string` |
| `Optional` user | `JWTUser` |

**Returns:** `Promise`<[Event](event.md)>

___
<a id="initialize"></a>

### `<Private>` initialize

▸ **initialize**(): `Promise`<`void`>

*Defined in routes/EventRoute.ts:47*

Called on server startup to initialize the route with any defaults.

**Returns:** `Promise`<`void`>

___
<a id="validate"></a>

### `<Private>` validate

▸ **validate**(evt: *[Event](event.md)*, user: *`JWTUser`*): `void`

*Defined in routes/EventRoute.ts:57*

Performs validation of the given event object and user.

**Parameters:**

| Name | Type | Description |
| ------ | ------ | ------ |
| evt | [Event](event.md) |  The event to be validated. |
| user | `JWTUser` |  The user attempting to perform the action. |

**Returns:** `void`

___

