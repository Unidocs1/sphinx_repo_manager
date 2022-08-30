===============================================================================
Namespace: comments
===============================================================================

Table of Contents
&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;

.. toctree::
   :caption: Classes

   ../classes/comments/CommentClass

.. toctree::
   :caption: Type Aliases

   comments#literalwithblockcomments

.. toctree::
   :caption: Variables

   comments#commentwithdoclinks
   comments#commentswithfencedblock
   comments#commentswithhtml
   comments#commentswithincludes
   comments#commentswithsymbollinks
   comments#commentswithtags

.. toctree::
   :caption: Functions

   comments#commentsinreturn

Type Aliases
===============================================================================

literalWithBlockComments
-------------------------------------------------------------------------------

Ƭ **literalWithBlockComments**: `Object`

Some comments

Type declaration
~~~~~~~~~~~~~~~~

| Name | Type | Description |
| :------ | :------ | :------ |
| `prop` | `string` | Comment for prop |

Defined in
==========

comments.ts:99

Variables
===============================================================================

commentWithDocLinks
-------------------------------------------------------------------------------

• `Const` **commentWithDocLinks**: ``true``

See ```CommentClass`` <../classes/comments/CommentClass.rst>`_ and `CommentClass's comment property <../classes/comments/CommentClass.rst#comment>`_.
Also, check out `Google <https://www.google.com>`_ and
`GitHub <https://github.com>`_.

Taken from [JsDoc](http://usejsdoc.org/tags-inline-link.html).

Defined in
==========

comments.ts:8

___

commentsWithFencedBlock
-------------------------------------------------------------------------------

• `Const` **commentsWithFencedBlock**: ``true``

Some comments with fence blocks

```typescript
someFunction()
```

```js
anotherFunction()
```

Defined in
==========

comments.ts:64

___

commentsWithHTML
-------------------------------------------------------------------------------

• `Const` **commentsWithHTML**: ``true``

<p>
You can write <strong>HTML</strong> tags directly in comments
</p>
<ul>
<li>List item</li>
</ul>

Defined in
==========

comments.ts:28

___

commentsWithIncludes
-------------------------------------------------------------------------------

• `Const` **commentsWithIncludes**: ``true``

This is an example of include

This is a simple example on how to use include.

![My image alt text](../media/logo.png)

This is an example of handlebars include

This is a simple example on a handlebars file.

Defined in
==========

comments.ts:39

___

commentsWithSymbolLinks
-------------------------------------------------------------------------------

• `Const` **commentsWithSymbolLinks**: ``true``

Additionally you can link to other classes, members or functions using double square brackets.

- Link to an external reflection: `CommentClass <../classes/comments/CommentClass.rst>`_
- Link to an internal reflection: `commentsInReturn <comments.rst#commentsinreturn>`_
- Link to an undefined reflection: [[VOID]]

Defined in
==========

comments.ts:18

___

commentsWithTags
-------------------------------------------------------------------------------

• `Const` **commentsWithTags**: ``true``

**`name`** Tag description on same line

**`description`**
Tag description on new line

- Tag description on another line

**`deprecated`**
Another tag description

Defined in
==========

comments.ts:51

Functions
===============================================================================

commentsInReturn
-------------------------------------------------------------------------------

▸ **commentsInReturn**(): `void`

Comments with a return definition

Returns
~~~~~~~

`void`

Return comments

Defined in
==========

comments.ts:70
