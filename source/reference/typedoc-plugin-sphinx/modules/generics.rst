===============================================================================
Namespace: generics
===============================================================================

Table of Contents
&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;

.. toctree::
   :caption: Classes

   ../classes/generics/ClassWithTypeParams

.. toctree::
   :caption: Type Aliases

   generics#generic1
   generics#generic2
   generics#generic3
   generics#nestedgenerics

.. toctree::
   :caption: Functions

   generics#functionwithgenericconstraints
   generics#functionwithtypeparam
   generics#functionwithtypeparams
   generics#genericswithdefaults

Type Aliases
===============================================================================

Generic1
-------------------------------------------------------------------------------

Ƭ **Generic1**<`T`\>: ``Generic2` <generics.rst#generic2>`_<``Generic3` <generics.rst#generic3>`_<`T`\>\>

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`

Defined in
==========

generics.ts:35

___

Generic2
-------------------------------------------------------------------------------

Ƭ **Generic2**<`T`\>: `T`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`

Defined in
==========

generics.ts:36

___

Generic3
-------------------------------------------------------------------------------

Ƭ **Generic3**<`T`\>: `T`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `T`

Defined in
==========

generics.ts:37

___

nestedGenerics
-------------------------------------------------------------------------------

Ƭ **nestedGenerics**: ``Generic1` <generics.rst#generic1>`_<``Generic2` <generics.rst#generic2>`_<``Generic3` <generics.rst#generic3>`_<`string`\>\>\>

Defined in
==========

generics.ts:39

Functions
===============================================================================

functionWithGenericConstraints
-------------------------------------------------------------------------------

▸ **functionWithGenericConstraints**<`Type`, `Key`\>(`obj`, `key`): `Type`[`Key`]

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `Type`
      -       - `Type`
    * - `Key`
      - extends `string` \| `number` \| `symbol`

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `obj`
      - `Type`
    * - `key`
      - `Key`

Returns
~~~~~~~

`Type`[`Key`]

Defined in
==========

generics.ts:28

___

functionWithTypeParam
-------------------------------------------------------------------------------

▸ **functionWithTypeParam**<`A`\>(): `boolean`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
    * - `A`

Returns
~~~~~~~

`boolean`

Defined in
==========

generics.ts:11

___

functionWithTypeParams
-------------------------------------------------------------------------------

▸ **functionWithTypeParams**<`A`, `B`, `C`\>(): `boolean`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
      - Description
    * - `A`
      - extends ``ClassWithTypeParams` <../classes/generics/ClassWithTypeParams.rst>`_<`string`, `number`, `A`\>
      - Comment for type `A`
    * - `B`
      - `string` \| `boolean`
      - Comment for type `B`
    * - `C`
      - `string`
      - -

Returns
~~~~~~~

`boolean`

Defined in
==========

generics.ts:18

___

genericsWithDefaults
-------------------------------------------------------------------------------

▸ **genericsWithDefaults**<`Type`\>(): `void`

Type parameters
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

    * - Name
      - Type
    * - `Type`
      - extends `boolean` = `boolean`

Returns
~~~~~~~

`void`

Defined in
==========

generics.ts:24
