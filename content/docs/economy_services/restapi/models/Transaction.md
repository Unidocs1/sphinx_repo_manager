---
title: "Transaction"
date: 2019-12-06T19:01:21.222Z
---

Describes an inventory change

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the transaction. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the transaction was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the transaction was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [status](#status) | The current status of the transaction | `string` |  | `PENDING` | false | false | true |
| [type](#type) | The current type of the transaction | `string` |  | `TRADE` | false | false | true |
| [personaOneUid](#personaOneUid) | The unique identifier of the user that this inventory belongs to. | `string` | uuid | `""` | false | false | true |
| [personaTwoUid](#personaTwoUid) | The unique identifier of the persona that this inventory belongs to. | `string` | uuid | `""` | false | false | true |
| [personaOneInventoryItemsBefore](#personaOneInventoryItemsBefore) | The snapshot of inventory items before transaction. | `array` |  | `` | false | false | true |
| [personaOneInventoryItemsAfter](#personaOneInventoryItemsAfter) | The snapshot of inventory items after transaction. | `array` |  | `` | false | false | true |
| [personaTwoInventoryItemsBefore](#personaTwoInventoryItemsBefore) | The snapshot of inventory items before transaction. Empty if not a trade | `array` |  | `` | false | false | true |
| [personaTwoInventoryItemsAfter](#personaTwoInventoryItemsAfter) | The snapshot of inventory after transaction. Empty if not a trade | `array` |  | `` | false | false | true |

## Examples
### Request

```json
{
    "status": "string",
    "type": "string",
    "personaOneInventoryItemsBefore": [
        "InventoryItem"
    ],
    "personaOneInventoryItemsAfter": [
        "InventoryItem"
    ],
    "personaTwoInventoryItemsBefore": [
        "InventoryItem"
    ],
    "personaTwoInventoryItemsAfter": [
        "InventoryItem"
    ]
}
```

### Response

```json
{
    "uid": "c5d83837-1b09-4ac8-a7a8-f33afe5d04a3",
    "dateCreated": "2019-12-06T19:01:21.532Z",
    "dateModified": "2019-12-06T19:01:21.532Z",
    "version": 0,
    "status": "string",
    "type": "string",
    "personaOneUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "personaTwoUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "personaOneInventoryItemsBefore": [
        "InventoryItem"
    ],
    "personaOneInventoryItemsAfter": [
        "InventoryItem"
    ],
    "personaTwoInventoryItemsBefore": [
        "InventoryItem"
    ],
    "personaTwoInventoryItemsAfter": [
        "InventoryItem"
    ]
}
```


## Members

### uid

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the transaction.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the transaction was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the transaction was last modified.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic lock version.

### status

Type: `string`

Default Value: `PENDING`

Required: `true`

The current status of the transaction

### type

Type: `string`

Default Value: `TRADE`

Required: `true`

The current type of the transaction

### personaOneUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the user that this inventory belongs to.

### personaTwoUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the persona that this inventory belongs to.

### personaOneInventoryItemsBefore

Type: `array`

Default Value: ``

Required: `true`

The snapshot of inventory items before transaction.

### personaOneInventoryItemsAfter

Type: `array`

Default Value: ``

Required: `true`

The snapshot of inventory items after transaction.

### personaTwoInventoryItemsBefore

Type: `array`

Default Value: ``

Required: `true`

The snapshot of inventory items before transaction. Empty if not a trade

### personaTwoInventoryItemsAfter

Type: `array`

Default Value: ``

Required: `true`

The snapshot of inventory after transaction. Empty if not a trade

## References

This data model is referenced in the following endpoints.

// TODO