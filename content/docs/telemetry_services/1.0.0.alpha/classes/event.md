[telemetry_services](../README.md) > [Event](../classes/event.md)

# Class: Event

Describes a single telemetry event. A telemetry event is when something occurs in the system.

*__author__*: Jean-Philippe Steinmetz [info@acceleratxr.com](mailto:info@acceleratxr.com)

## Hierarchy

 `SimpleMongoEntity`

**↳ Event**

## Index

### Constructors

* [constructor](event.md#constructor)

### Properties

* [_id](event.md#_id)
* [environment](event.md#environment)
* [origin](event.md#origin)
* [timestamp](event.md#timestamp)
* [type](event.md#type)
* [uid](event.md#uid)
* [userId](event.md#userid)

---

## Constructors

<a id="constructor"></a>

###  constructor

⊕ **new Event**(other?: *`any`*): [Event](event.md)

*Overrides SimpleMongoEntity.__constructor*

*Defined in models/Event.ts:42*

**Parameters:**

| Name | Type |
| ------ | ------ |
| `Optional` other | `any` |

**Returns:** [Event](event.md)

___

## Properties

<a id="_id"></a>

###  _id

**● _id**: *`ObjectID`*

*Inherited from SimpleMongoEntity._id*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/services_common/dist/types/models/SimpleMongoEntity.d.ts:13*

The internal unique identifier used by MongoDB.

___
<a id="environment"></a>

###  environment

**● environment**: *`string`* = "prod"

*Defined in models/Event.ts:18*

The name of the environment that the event originated from. This is typically `dev` or `prod`.

___
<a id="origin"></a>

###  origin

**● origin**: *`string`* = ""

*Defined in models/Event.ts:24*

The unique name of the service or client that the event originated from.

___
<a id="timestamp"></a>

###  timestamp

**● timestamp**: *`Date`* =  new Date()

*Defined in models/Event.ts:30*

The date and time that the event occured.

___
<a id="type"></a>

###  type

**● type**: *`string`* = ""

*Defined in models/Event.ts:36*

The type of event being recorded.

___
<a id="uid"></a>

###  uid

**● uid**: *`string`*

*Inherited from BaseEntity.uid*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/services_common/dist/types/models/SimpleEntity.d.ts:11*

The universally unique identifier of the entity.

___
<a id="userid"></a>

###  userId

**● userId**: *`string`* = ""

*Defined in models/Event.ts:42*

The universally unique identifer of the user that sent the event.

___

