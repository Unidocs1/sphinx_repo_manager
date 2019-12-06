---
title: "InventoryItem"
date: 2019-12-06T19:01:21.222Z
---

Describes the inventory item

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the item. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the item was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the item was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [personaUid](#personaUid) | The unique identifier of the persona that this inventory belongs to. | `string` | uuid | `""` | true | false | true |
| [itemUid](#itemUid) | The UUID of the item | `string` | uuid | `""` | false | false | true |
| [quantity](#quantity) | The number of items in the inventory | `number` |  | `0` | false | false | true |

## Examples
### Request

```json
{
    "quantity": 0
}
```

### Response

```json
{
    "uid": "86a5b4e9-1325-4dae-927f-fbd8797b8700",
    "dateCreated": "2019-12-06T19:01:21.475Z",
    "dateModified": "2019-12-06T19:01:21.475Z",
    "version": 0,
    "personaUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "itemUid": "798d4cc9-aa46-454a-9f4c-09f32c07e40c",
    "quantity": 0
}
```


## Members

### uid

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the item.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the item was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the item was last modified.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic lock version.

### personaUid

Type: `string`

Default Value: `""`

Required: `true`

*Identifier*

The unique identifier of the persona that this inventory belongs to.

### itemUid

Type: `string`

Default Value: `""`

Required: `true`

The UUID of the item

### quantity

Type: `number`

Default Value: `0`

Required: `true`

The number of items in the inventory

## References

This data model is referenced in the following endpoints.

// TODO