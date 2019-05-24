[persona_services](../README.md) > [PersonaStat](../classes/personastat.md)

# Class: PersonaStat

The `PersonaStat` is an instance of a specific `PersonaStatDefinition` that is assocaited with a particular `Persona`.

*__author__*: Jean-Philippe Steinmetz [info@acceleratxr.com](mailto:info@acceleratxr.com)

## Hierarchy

 `BaseMongoEntity`

**↳ PersonaStat**

## Index

### Constructors

* [constructor](personastat.md#constructor)

### Properties

* [_id](personastat.md#_id)
* [dateCreated](personastat.md#datecreated)
* [dateModified](personastat.md#datemodified)
* [personaUid](personastat.md#personauid)
* [statUid](personastat.md#statuid)
* [uid](personastat.md#uid)
* [value](personastat.md#value)
* [version](personastat.md#version)

---

## Constructors

<a id="constructor"></a>

###  constructor

⊕ **new PersonaStat**(other?: *`any`*): [PersonaStat](personastat.md)

*Overrides BaseMongoEntity.__constructor*

*Defined in models/PersonaStat.ts:32*

**Parameters:**

| Name | Type |
| ------ | ------ |
| `Optional` other | `any` |

**Returns:** [PersonaStat](personastat.md)

___

## Properties

<a id="_id"></a>

###  _id

**● _id**: *`ObjectID`*

*Inherited from BaseMongoEntity._id*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseMongoEntity.d.ts:12*

The internal unique identifier used by MongoDB.

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
<a id="personauid"></a>

###  personaUid

**● personaUid**: *`string`* = ""

*Defined in models/PersonaStat.ts:26*

The universally unique identifier of the `Persona` that this statistic is associated with.

___
<a id="statuid"></a>

###  statUid

**● statUid**: *`string`* = ""

*Defined in models/PersonaStat.ts:19*

The universally unique identifier of the `PersonaStatDefinition` this object represents.

___
<a id="uid"></a>

###  uid

**● uid**: *`string`*

*Inherited from BaseEntity.uid*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseEntity.d.ts:14*

The universally unique identifier of the entity.

___
<a id="value"></a>

###  value

**● value**: *`any`* =  undefined

*Defined in models/PersonaStat.ts:32*

The current value of the statistic.

___
<a id="version"></a>

###  version

**● version**: *`number`*

*Inherited from BaseEntity.version*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseEntity.d.ts:26*

The optimistic lock version.

___

