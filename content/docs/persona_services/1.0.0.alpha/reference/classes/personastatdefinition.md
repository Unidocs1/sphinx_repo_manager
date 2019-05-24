[persona_services](../README.md) > [PersonaStatDefinition](../classes/personastatdefinition.md)

# Class: PersonaStatDefinition

The `PersonaStatDefinition` describes a single statistic that an persona can have.

*__author__*: Jean-Philippe Steinmetz [info@acceleratxr.com](mailto:info@acceleratxr.com)

## Hierarchy

 `BaseMongoEntity`

**↳ PersonaStatDefinition**

## Index

### Constructors

* [constructor](personastatdefinition.md#constructor)

### Properties

* [_id](personastatdefinition.md#_id)
* [dateCreated](personastatdefinition.md#datecreated)
* [dateModified](personastatdefinition.md#datemodified)
* [default](personastatdefinition.md#default)
* [max](personastatdefinition.md#max)
* [min](personastatdefinition.md#min)
* [name](personastatdefinition.md#name)
* [type](personastatdefinition.md#type)
* [uid](personastatdefinition.md#uid)
* [values](personastatdefinition.md#values)
* [version](personastatdefinition.md#version)

---

## Constructors

<a id="constructor"></a>

###  constructor

⊕ **new PersonaStatDefinition**(other?: *`any`*): [PersonaStatDefinition](personastatdefinition.md)

*Overrides BaseMongoEntity.__constructor*

*Defined in models/PersonaStatDefinition.ts:56*

**Parameters:**

| Name | Type |
| ------ | ------ |
| `Optional` other | `any` |

**Returns:** [PersonaStatDefinition](personastatdefinition.md)

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
<a id="default"></a>

###  default

**● default**: *`any`* =  undefined

*Defined in models/PersonaStatDefinition.ts:56*

The default value of the stat that will be designed to `Persona` instances.

___
<a id="max"></a>

###  max

**● max**: *`any`* =  undefined

*Defined in models/PersonaStatDefinition.ts:44*

The maximum possible value that can be used.

___
<a id="min"></a>

###  min

**● min**: *`any`* =  undefined

*Defined in models/PersonaStatDefinition.ts:38*

The minimum possible value that can be used.

___
<a id="name"></a>

###  name

**● name**: *`string`* = ""

*Defined in models/PersonaStatDefinition.ts:20*

The unique name of the statistic.

___
<a id="type"></a>

###  type

**● type**: *`string`* = "number"

*Defined in models/PersonaStatDefinition.ts:32*

The data type describing how the statistic's value is stored.

Possible values are

*   `"boolean"`
*   `"number"`
*   `"object"`
*   `"string"`

___
<a id="uid"></a>

###  uid

**● uid**: *`string`*

*Inherited from BaseEntity.uid*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseEntity.d.ts:14*

The universally unique identifier of the entity.

___
<a id="values"></a>

###  values

**● values**: *`any`[]* =  []

*Defined in models/PersonaStatDefinition.ts:50*

A list of all possible values that can be used.

___
<a id="version"></a>

###  version

**● version**: *`number`*

*Inherited from BaseEntity.version*

*Defined in C:/Users/jpsaxr/gitlab/persona_services/node_modules/@acceleratxr/services_common/dist/types/models/BaseEntity.d.ts:26*

The optimistic lock version.

___

