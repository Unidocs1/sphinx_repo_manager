===============================================================================
Namespace: signatures
===============================================================================

Table of Contents
&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;

.. toctree::
   :caption: Classes

   ../classes/signatures/ClassWithConstructor

.. toctree::
   :caption: Interfaces

   ../interfaces/signatures/CallableSignature

.. toctree::
   :caption: Type Aliases

   signatures#user
   signatures#_somecallback_

.. toctree::
   :caption: Functions

   signatures#commentsinreturn
   signatures#functionreturningafunction
   signatures#functionreturninganobject
   signatures#functionwithdefaults
   signatures#functionwithnamedparams
   signatures#functionwithnamedparamsandcomments
   signatures#functionwithnestedparams
   signatures#functionwithoptionalparam
   signatures#functionwithparameters
   signatures#functionwithpipesinparamsandcomments
   signatures#functionwithreferencetype
   signatures#functionwithrest
   signatures#functionwithtypeparams
   signatures#functionwithuniontypes
   signatures#multiplesignatures
   signatures#privatefunction
   signatures#promisereturningasymbol
   signatures#promisereturninganobject
   signatures#swtch
   signatures#variablefunction

Type Aliases
===============================================================================

User
-------------------------------------------------------------------------------

Ƭ **User**: `Object`

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type |
| :------ | :------ |
| `data` | `string` |
| `id` | `string` |

Defined in
==========

signatures.ts:218

___

\_someCallback\_
-------------------------------------------------------------------------------

Ƭ **\_someCallback\_**: (`name`: `string`, `value`: `unknown`) => `void`

Type declaration
~~~~~~~~~~~~~~~~

▸ (`name`, `value`): `void`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `name`
      - `string`
    * - `value`
      - `unknown`

Returns
~~~~~~~

`void`

Defined in
==========

signatures.ts:159

Functions
===============================================================================

commentsInReturn
-------------------------------------------------------------------------------

▸ **commentsInReturn**(): `boolean`

Comments with a return definition

Returns
~~~~~~~

`boolean`

Return comments

Defined in
==========

signatures.ts:137

___

functionReturningAFunction
-------------------------------------------------------------------------------

▸ **functionReturningAFunction**(): <T\>(`x`: `string`) => `boolean`

Comments for function

Returns
~~~~~~~

`fn`

Return comments

▸ <`T`\>(`x`): `boolean`

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
    * - `x`
      - `string`

Returns
~~~~~~~

`boolean`

Defined in
==========

signatures.ts:129

___

functionReturningAnObject
-------------------------------------------------------------------------------

▸ **functionReturningAnObject**(): `Object`

Comments for function

Returns
~~~~~~~

`Object`

Return comments

| Name | Type |
| :------ | :------ |
| `x` | `number` |
| `y` | `number` |

Defined in
==========

signatures.ts:121

___

functionWithDefaults
-------------------------------------------------------------------------------

▸ **functionWithDefaults**(`valueA?`, `valueB?`, `valueC?`, `valueD?`, `valueE?`, `valueF?`): `string`

This is a function with a parameter that has a default value.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Default value
      - Description
    * - `valueA`
      - `string`
      - `'defaultValue'`
      - A parameter with a default string value.
    * - `valueB`
      - `number`
      - `100`
      - A parameter with a default numeric value.
    * - `valueC`
      - `number`
      - `Number.NaN`
      - A parameter with a default NaN value.
    * - `valueD`
      - `boolean`
      - `true`
      - A parameter with a default boolean value.
    * - `valueE`
      - `boolean`
      - `null`
      - A parameter with a default null value.
    * - `valueF`
      - `string`
      - `'<foo>'`
      - -

Returns
~~~~~~~

`string`

Defined in
==========

signatures.ts:49

___

functionWithNamedParams
-------------------------------------------------------------------------------

▸ **functionWithNamedParams**(`__namedParameters`): `string`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `__namedParameters`
      - `Object`

Returns
~~~~~~~

`string`

Defined in
==========

signatures.ts:104

___

functionWithNamedParamsAndComments
-------------------------------------------------------------------------------

▸ **functionWithNamedParamsAndComments**(`__namedParameters?`, `anotherParam`): `void`

FOO

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `__namedParameters`
      - `Object`
      - various options
    * - `__namedParameters.bar?`
      - `number`
      - -
    * - `__namedParameters.foo?`
      - `number`
      - -
    * - `anotherParam`
      - `string`
      - -

Returns
~~~~~~~

`void`

Defined in
==========

signatures.ts:167

___

functionWithNestedParams
-------------------------------------------------------------------------------

▸ **functionWithNestedParams**(`params`, `context`): `boolean`

Some nested params.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `params`
      - `Object`
      - The parameters passed to the method.
    * - `params.name`
      - `string`
      - The name of the new group.
    * - `params.nestedObj`
      - `Object`
      - A nested object.
    * - `params.nestedObj.name`
      - `string`
      - -
    * - `params.nestedObj.obj`
      - `Object`
      - -
    * - `params.nestedObj.obj.name`
      - () => `void`
      - -
    * - `params.nestedObj.value`
      - `number`
      - -
    * - `params.parent?`
      - `number`
      - -
    * - `context`
      - `any`
      - The context of the method call.

Returns
~~~~~~~

`boolean`

Defined in
==========

signatures.ts:197

___

functionWithOptionalParam
-------------------------------------------------------------------------------

▸ **functionWithOptionalParam**(`requiredParam`, `optionalParam?`): `void`

This is a function with a parameter that is optional.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `requiredParam`
      - `string`
      - A normal parameter.
    * - `optionalParam?`
      - `string`
      - An optional parameter.

Returns
~~~~~~~

`void`

Defined in
==========

signatures.ts:35

___

functionWithParameters
-------------------------------------------------------------------------------

▸ **functionWithParameters**(`paramZ`, `paramG`, `paramA`): `number`

This is a function with multiple arguments and a return value.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `paramZ`
      - `string`
      - This is a string parameter.
    * - `paramG`
      - `any`
      - This is a parameter flagged with any.<br />     This sentence is placed in the next line.
    * - `paramA`
      - `any`
      - This is a **parameter** pointing to an interface.

Returns
~~~~~~~

`number`

Defined in
==========

signatures.ts:12

___

functionWithPipesInParamsAndComments
-------------------------------------------------------------------------------

▸ **functionWithPipesInParamsAndComments**(`n`): `number` \| ``null``

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `n`
      - `number`
      - a\|b

Returns
~~~~~~~

`number` \| ``null``

Defined in
==========

signatures.ts:178

___

functionWithReferenceType
-------------------------------------------------------------------------------

▸ **functionWithReferenceType**(`descriptor`): `boolean`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `descriptor`
      - `TypedPropertyDescriptor`<`any`\>

Returns
~~~~~~~

`boolean`

Defined in
==========

signatures.ts:184

___

functionWithRest
-------------------------------------------------------------------------------

▸ **functionWithRest**(...`rest`): `string`

This is a function with rest parameter.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `...rest`
      - `string`[]
      - The rest parameter.

Returns
~~~~~~~

`string`

Defined in
==========

signatures.ts:65

___

functionWithTypeParams
-------------------------------------------------------------------------------

▸ **functionWithTypeParams**<`Item`\>(): `boolean`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `Item`
      - `string` \| `boolean`

Returns
~~~~~~~

`boolean`

Defined in
==========

signatures.ts:115

___

functionWithUnionTypes
-------------------------------------------------------------------------------

▸ **functionWithUnionTypes**(`arg`, ...`args`): `any`

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

signatures.ts:93

___

multipleSignatures
-------------------------------------------------------------------------------

▸ **multipleSignatures**(`value`): `string`

This is the first signature of a function with multiple signatures.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `value`
      - `string`
      - The name value.

Returns
~~~~~~~

`string`

Defined in
==========

signatures.ts:74

▸ **multipleSignatures**(`value`): `string`

This is the second signature of a function with multiple signatures.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `value`
      - `Object`
      - An object containing the name value.
    * - `value.name`
      - `string`
      - A value of the object.

Returns
~~~~~~~

`string`

Defined in
==========

signatures.ts:82

___

privateFunction
-------------------------------------------------------------------------------

▸ `Private` **privateFunction**(): `string`

Returns
~~~~~~~

`string`

Defined in
==========

signatures.ts:111

___

promiseReturningASymbol
-------------------------------------------------------------------------------

▸ **promiseReturningASymbol**(): `Promise`<``User` <signatures.rst#user>`_\>

Returns
~~~~~~~

`Promise`<``User` <signatures.rst#user>`_\>

Defined in
==========

signatures.ts:223

___

promiseReturningAnObject
-------------------------------------------------------------------------------

▸ **promiseReturningAnObject**(): `Promise`<{ `data`: `string` ; `id`: `string`  }\>

Returns
~~~~~~~

`Promise`<{ `data`: `string` ; `id`: `string`  }\>

Defined in
==========

signatures.ts:229

___

swtch
-------------------------------------------------------------------------------

▸ **swtch**<`T`, `R`\>(`value`, ...`cases`): (`def`: `R`) => `R`

Shorthand switch/case helper function. Cases arguments list is a tuple
consisting of case (`T`) and returned result (`R`). Returns a function where a default value is provided.

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`
    * - `R`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `value`
      - `T`
      - Value to test against
    * - `...cases`
      - [`T`, `R`][]
      - Tuple of case and the result if `value` and `case` is equal

Returns
~~~~~~~

`fn`

Function for which to provide the default value

▸ (`def`): `R`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `def`
      - `R`

Returns
~~~~~~~

`R`

Defined in
==========

signatures.ts:149

___

variableFunction
-------------------------------------------------------------------------------

▸ **variableFunction**(`someParam`): `number`

This is a function that is assigned to a variable.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `someParam`
      - `number`
      - This is some numeric parameter.

Returns
~~~~~~~

`number`

Defined in
==========

signatures.ts:25
