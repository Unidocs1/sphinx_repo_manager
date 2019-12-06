---
title: "TransactionRequest"
date: 2019-12-06T19:01:21.222Z
---

Describes an transaction request

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [type](#type) | The current type of the transaction. Award or Removal on available for trusted role | `string` |  | `TRADE` | false | false | true |
| [personaOneUid](#personaOneUid) | The unique identifier of the user that this inventory belongs to. | `string` | uuid | `""` | false | false | true |
| [personaTwoUid](#personaTwoUid) | The unique identifier of the persona that this inventory belongs to. Blank for Award or Removal | `string` | uuid | `""` | false | false | true |
| [personaOneInventoryItems](#personaOneInventoryItems) | The inventory items for persona one | `array` |  | `` | false | false | true |
| [personaTwoInventoryItems](#personaTwoInventoryItems) | The inventory items for persona two. Empty for Award or Removal | `array` |  | `` | false | false | true |

## Examples
### Request

```json
{
    "type": "string",
    "personaOneInventoryItems": [
        "InventoryItem"
    ],
    "personaTwoInventoryItems": [
        "InventoryItem"
    ]
}
```

### Response

```json
{
    "type": "string",
    "personaOneUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "personaTwoUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "personaOneInventoryItems": [
        "InventoryItem"
    ],
    "personaTwoInventoryItems": [
        "InventoryItem"
    ]
}
```


## Members

### type

Type: `string`

Default Value: `TRADE`

Required: `true`

The current type of the transaction. Award or Removal on available for trusted role

### personaOneUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the user that this inventory belongs to.

### personaTwoUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the persona that this inventory belongs to. Blank for Award or Removal

### personaOneInventoryItems

Type: `array`

Default Value: ``

Required: `true`

The inventory items for persona one

### personaTwoInventoryItems

Type: `array`

Default Value: ``

Required: `true`

The inventory items for persona two. Empty for Award or Removal

## References

This data model is referenced in the following endpoints.

// TODO