===============================================================================
Namespace: declarations
===============================================================================

Table of Contents
&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;

.. toctree::
   :caption: Enumerations

   ../enums/declarations/EnumDeclarations

.. toctree::
   :caption: Type Aliases

   declarations#anyfunctiontype

.. toctree::
   :caption: Variables

   declarations#__double_underscores_declaration__
   declarations#callabledeclaration
   declarations#indexabledeclaration
   declarations#objectliteralasconstdeclaration
   declarations#objectliteraldeclaration
   declarations#stringconstwithdefaultvalue
   declarations#stringletwithdefaultvalue
   declarations#typeliteraldeclaration
   declarations#undefinednumberdeclaration

.. toctree::
   :caption: Functions

   declarations#functiondeclaration

Type Aliases
===============================================================================

AnyFunctionType
-------------------------------------------------------------------------------

Ƭ **AnyFunctionType**<`A`\>: (...`input`: `any`[]) => `A`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `A`
      - `any`

Type declaration
~~~~~~~~~~~~~~~~

▸ (...`input`): `A`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `...input`
      - `any`[]

Returns
~~~~~~~

`A`

Defined in
==========

declarations.ts:90

Variables
===============================================================================

\_\_DOUBLE\_UNDERSCORES\_DECLARATION\_\_
-------------------------------------------------------------------------------

• `Const` **\_\_DOUBLE\_UNDERSCORES\_DECLARATION\_\_**: typeof ``__DOUBLE_UNDERSCORES_DECLARATION__` <declarations.rst#__double_underscores_declaration__>`_

Defined in
==========

declarations.ts:88

___

callableDeclaration
-------------------------------------------------------------------------------

• **callableDeclaration**: `Object`

Call signature
~~~~~~~~~~~~~~

▸ (`someArg`): `boolean`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `someArg`
      - `number`

Returns
~~~~~~~

`boolean`

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type |
| :------ | :------ |
| `arg1` | `string` |
| `arg2` | `number` |

Defined in
==========

declarations.ts:65

___

indexableDeclaration
-------------------------------------------------------------------------------

• **indexableDeclaration**: `Object`

Index signature
~~~~~~~~~~~~~~~

▪ [index: `number`]: `string`

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type |
| :------ | :------ |
| `arg1` | `string` |

Defined in
==========

declarations.ts:71

___

objectLiteralAsConstDeclaration
-------------------------------------------------------------------------------

• `Const` **objectLiteralAsConstDeclaration**: `Object`

Comments

**`param`** Comment for object.

**`param`** Comment for Prop1.

**`param`** Comment for Prop2.

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type |
| :------ | :------ |
| `Prop1` | ``"Prop1"`` |
| `Prop2` | ``"Prop2"`` |
| `Prop3` | ``"Prop3"`` |

Defined in
==========

declarations.ts:82

___

objectLiteralDeclaration
-------------------------------------------------------------------------------

• `Const` **objectLiteralDeclaration**: `Object`

**`param`** description for valueX

**`param`** description for valueZ

**`param`** description for valueY

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type | Description |
| :------ | :------ | :------ |
| `valueA` | `number` | Comment for valueA |
| `valueB` | `boolean` | - |
| `valueC` | {} | - |
| `valueX` | { `valueA`: `number`[] ; `valueZ`: `string` = 'foo' } | Comment for valueX |
| `valueX.valueA` | `number`[] | - |
| `valueX.valueZ` | `string` | - |
| `valueY` | () => `string` | Comment for value Y |
| `valueZ` | `string` | Comment for valueZ |

Defined in
==========

declarations.ts:12

___

stringConstWithDefaultValue
-------------------------------------------------------------------------------

• `Const` **stringConstWithDefaultValue**: ``"hello"``

Defined in
==========

declarations.ts:1

___

stringLetWithDefaultValue
-------------------------------------------------------------------------------

• **stringLetWithDefaultValue**: `string` = `'hello'`

Defined in
==========

declarations.ts:2

___

typeLiteralDeclaration
-------------------------------------------------------------------------------

• **typeLiteralDeclaration**: `Object`

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type | Description |
| :------ | :------ | :------ |
| `valueA?` | `number` | Comments for valueA |
| `valueB?` | `boolean` | - |
| `valueC` | { `[dataId: string]`: ``"ok"`` \| ``"ko"``;  } | - |
| `valueX` | { `valueA`: `number`[] ; `valueY`: (`z`: `string`) => { `a`: `string` ; `b`: `string`  } ; `valueZ`: `string`  } | Comment for valueX |
| `valueX.valueA` | `number`[] | - |
| `valueX.valueY` | (`z`: `string`) => { `a`: `string` ; `b`: `string`  } | - |
| `valueX.valueZ` | `string` | Nested comment for valueZ |
| `valueY` | () => `string` | - |
| `valueZ` | `string` | Comment for valueZ |

Defined in
==========

declarations.ts:38

___

undefinedNumberDeclaration
-------------------------------------------------------------------------------

• **undefinedNumberDeclaration**: `number`

Defined in
==========

declarations.ts:5

Functions
===============================================================================

functionDeclaration
-------------------------------------------------------------------------------

▸ **functionDeclaration**(`someArg`): `boolean`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `someArg`
      - `number`

Returns
~~~~~~~

`boolean`

Defined in
==========

declarations.ts:63
