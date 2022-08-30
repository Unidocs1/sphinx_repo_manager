===============================================================================
Namespace: types
===============================================================================

Table of Contents
&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;

.. toctree::
   :caption: Classes

   ../classes/types/IntersectionClassA
   ../classes/types/IntersectionClassB

.. toctree::
   :caption: Type Aliases

   types#bar
   types#conditionaltype
   types#partialmappedtype
   types#readonlymapedtype
   types#intersectiontype
   types#objectliteraluniontype
   types#uniontype
   types#uniontypewithsymbols
   types#uniontypewithsymbolsdeclarations

.. toctree::
   :caption: Variables

   types#arraytype
   types#barbigint
   types#externalreference
   types#externalreferenceinsidetypeparams
   types#foobigint
   types#htmlelement
   types#literaltype
   types#objectliteraltype
   types#stringliteraltype
   types#stringtype
   types#tupletype
   types#typeoperatortype

.. toctree::
   :caption: Functions

   types#baz
   types#functionreflectiontype
   types#generic
   types#restuniontypes

Type Aliases
===============================================================================

Bar
-------------------------------------------------------------------------------

Ƭ **Bar**<`T`, `R`\>: (`foos`: ``ConditionalType` <types.rst#conditionaltype>`_<`T`\>[]) => `R`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`
    * - `R`

Type declaration
~~~~~~~~~~~~~~~~

▸ (`foos`): `R`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `foos`
      - ``ConditionalType` <types.rst#conditionaltype>`_<`T`\>[]

Returns
~~~~~~~

`R`

Defined in
==========

types.ts:115

___

ConditionalType
-------------------------------------------------------------------------------

Ƭ **ConditionalType**<`T`\>: `T` extends `string` ? ``"string"`` : `T` extends `number` ? ``"number"`` : `T` extends `boolean` ? ``"boolean"`` : `T` extends `undefined` ? ``"undefined"`` : ``"object"``

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`

Defined in
==========

types.ts:105

___

PartialMappedType
-------------------------------------------------------------------------------

Ƭ **PartialMappedType**<`T`\>: { [P in keyof T]?: T[P] }

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`

Defined in
==========

types.ts:97

___

ReadonlyMapedType
-------------------------------------------------------------------------------

Ƭ **ReadonlyMapedType**<`T`\>: { readonly [P in keyof T]: T[P] }

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`

Defined in
==========

types.ts:101

___

intersectionType
-------------------------------------------------------------------------------

Ƭ **intersectionType**: ``IntersectionClassA` <../classes/types/IntersectionClassA.rst>`_ & ``IntersectionClassB` <../classes/types/IntersectionClassB.rst>`_

Defined in
==========

types.ts:76

___

objectLiteralUnionType
-------------------------------------------------------------------------------

Ƭ **objectLiteralUnionType**: `string` \| { `z`: `string`  }

Defined in
==========

types.ts:95

___

unionType
-------------------------------------------------------------------------------

Ƭ **unionType**: ``"ease-in"`` \| ``"ease-out"``

Defined in
==========

types.ts:17

___

unionTypeWithSymbols
-------------------------------------------------------------------------------

Ƭ **unionTypeWithSymbols**: ``" "`` \| ``"string"`` \| ``"strong|with|pipes"`` \| ``"type`with`backticks"`` \| ``"*"``

Defined in
==========

types.ts:19

___

unionTypeWithSymbolsDeclarations
-------------------------------------------------------------------------------

Ƭ **unionTypeWithSymbolsDeclarations**: `Object`

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type |
| :------ | :------ |
| `bar` | ``" "`` \| ``"string"`` \| ``"strong\|with\|pipes"`` \| ``"type`with`backticks"`` \| ``"*"`` |

Defined in
==========

types.ts:26

Variables
===============================================================================

arrayType
-------------------------------------------------------------------------------

• `Const` **arrayType**: `string`[]

Defined in
==========

types.ts:78

___

barBigInt
-------------------------------------------------------------------------------

• `Const` **barBigInt**: `100n`

Defined in
==========

types.ts:119

___

externalReference
-------------------------------------------------------------------------------

• **externalReference**: `HTMLElement`

Defined in
==========

types.ts:6

___

externalReferenceInsideTypeParams
-------------------------------------------------------------------------------

• `Const` **externalReferenceInsideTypeParams**: ``ClassWithTypeParams` <../classes/generics/ClassWithTypeParams.rst>`_<`HTMLElement`, `Error`\>

Defined in
==========

types.ts:8

___

fooBigInt
-------------------------------------------------------------------------------

• `Const` **fooBigInt**: `bigint`

Defined in
==========

types.ts:118

___

htmlElement
-------------------------------------------------------------------------------

• **htmlElement**: `HTMLElement`

Defined in
==========

types.ts:4

___

literalType
-------------------------------------------------------------------------------

• **literalType**: `Object`

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type |
| :------ | :------ |
| `valueA?` | `number` |
| `valueB?` | `boolean` |
| `valueX` | { `valueA`: `number`[] ; `valueY`: (`z`: `string`) => { `a`: `string` ; `b`: `string`  } ; `valueZ`: `string`  } |
| `valueX.valueA` | `number`[] |
| `valueX.valueY` | (`z`: `string`) => { `a`: `string` ; `b`: `string`  } |
| `valueX.valueZ` | `string` |
| `valueY` | () => `string` |
| `valueZ` | `string` |

Defined in
==========

types.ts:30

___

objectLiteralType
-------------------------------------------------------------------------------

• `Const` **objectLiteralType**: `Object`

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type |
| :------ | :------ |
| `<` | `string` |
| `<foo>` | `string` |
| \n | `string` |
| `_` | `string` |
| `prop_with_underscore` | `string` |
| prop\`with\`backticks | `string` |
| prop\|with\|pipes | `string` |
| `valueA` | `number` |
| `valueB` | `boolean` |
| `valueX` | { `valueA`: `number`[] ; `valueY`: (`z`: `string`) => { `a`: `string` = 'test'; `b`: `string` = z } ; `valueZ`: `string` = 'foo' } |
| `valueX.valueA` | `number`[] |
| `valueX.valueY` | (`z`: `string`) => { `a`: `string` = 'test'; `b`: `string` = z } |
| `valueX.valueZ` | `string` |
| `valueY` | (`cbParam`: ``_someCallback_` <signatures.rst#_somecallback_>`_, `unionParam`: ``"a"`` \| ``"b"``, `_undercoreParam_`: `string`) => `string` |
| `valueZ` | `string` |
| \| | `string` |
| `~` | `string` |

Defined in
==========

types.ts:42

___

stringLiteralType
-------------------------------------------------------------------------------

• `Const` **stringLiteralType**: ``"blue"``

Defined in
==========

types.ts:15

___

stringType
-------------------------------------------------------------------------------

• **stringType**: `string`

Defined in
==========

types.ts:13

___

tupleType
-------------------------------------------------------------------------------

• **tupleType**: [`string`, `number`]

Defined in
==========

types.ts:71

___

typeOperatorType
-------------------------------------------------------------------------------

• `Const` **typeOperatorType**: unique `symbol`

Defined in
==========

types.ts:93

Functions
===============================================================================

baz
-------------------------------------------------------------------------------

▸ **baz**(`foos`): `string`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `foos`
      - ``"string"``[]

Returns
~~~~~~~

`string`

Defined in
==========

types.ts:116

___

functionReflectionType
-------------------------------------------------------------------------------

▸ **functionReflectionType**<`T`\>(`arg`): `T`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `arg`
      - `T`

Returns
~~~~~~~

`T`

Defined in
==========

types.ts:91

___

generic
-------------------------------------------------------------------------------

▸ **generic**<`T`\>(`arg`): `T`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `arg`
      - `T`

Returns
~~~~~~~

`T`

Defined in
==========

types.ts:87

___

restUnionTypes
-------------------------------------------------------------------------------

▸ **restUnionTypes**(`arg`, ...`args`): `any`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `arg`
      - `number` \| `boolean`[]
    * - `...args`
      - (`string` \| `number`)[]

Returns
~~~~~~~

`any`

Defined in
==========

types.ts:80
