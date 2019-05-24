[persona_services](../README.md) > [Persona](../classes/persona.md)

# Class: Persona

An `Persona` is a unique persona of a user within the system. Users can have multiple personas per account and the persona can have associated data such as inventory, progress, achievements, etc.

*__author__*: Jean-Philippe Steinmetz [info@acceleratxr.com](mailto:info@acceleratxr.com)

## Hierarchy

 `BaseMongoEntity`

**↳ Persona**

## Index

### Constructors

* [constructor](persona.md#constructor)

### Properties

* [_id](persona.md#_id)
* [attributes](persona.md#attributes)
* [dateCreated](persona.md#datecreated)
* [dateModified](persona.md#datemodified)
* [description](persona.md#description)
* [name](persona.md#name)
* [uid](persona.md#uid)
* [userUid](persona.md#useruid)
* [version](persona.md#version)

---

## Constructors

<a id="constructor"></a>

###  constructor

⊕ **new Persona**(other?: *`any`*): [Persona](persona.md)

*Overrides BaseMongoEntity.__constructor*

*Defined in models/Persona.ts:38*

**Parameters:**

| Name | Type |
| ------ | ------ |
| `Optional` other | `any` |

**Returns:** [Persona](persona.md)

___

## Properties

<a id="_id"></a>

###  _id

**● _id**: *`ObjectID`*

*Inherited from BaseMongoEntity._id*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseMongoEntity.d.ts:12*

The internal unique identifier used by MongoDB.

___
<a id="attributes"></a>

###  attributes

**● attributes**: *`any`* =  undefined

*Defined in models/Persona.ts:38*

An arbitrary map of key-value pairs containing the characteristics of the persona.

___
<a id="datecreated"></a>

###  dateCreated

**● dateCreated**: *`Date`*

*Inherited from BaseEntity.dateCreated*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseEntity.d.ts:18*

The date and time that the entity was created.

___
<a id="datemodified"></a>

###  dateModified

**● dateModified**: *`Date`*

*Inherited from BaseEntity.dateModified*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseEntity.d.ts:22*

The date and time that the entity was last modified.

___
<a id="description"></a>

###  description

**● description**: *`string`* = ""

*Defined in models/Persona.ts:32*

A textual description of the persona.

___
<a id="name"></a>

###  name

**● name**: *`string`* = ""

*Defined in models/Persona.ts:26*

The unique name of the persona.

___
<a id="uid"></a>

###  uid

**● uid**: *`string`*

*Inherited from BaseEntity.uid*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseEntity.d.ts:14*

The universally unique identifier of the entity.

___
<a id="useruid"></a>

###  userUid

**● userUid**: *`string`* = ""

*Defined in models/Persona.ts:18*

The universally unique identifier of the user that the persona belongs to.

___
<a id="version"></a>

###  version

**● version**: *`number`*

*Inherited from BaseEntity.version*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseEntity.d.ts:26*

The optimistic lock version.

___

