---
title: "Item"
date: 2019-12-06T19:01:21.222Z
---

Describes an item

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the item. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the item was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the item was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [name](#name) | The item name | `string` |  | `""` | true | true | true |
| [description](#description) | Description of the item | `string` |  | `""` | false | false | true |
| [cost](#cost) | The cost of the item | `number` |  | `0` | false | false | true |
| [stats](#stats) | The list of stats for the item. | `array` |  | `` | false | false | true |
| [assetId](#assetId) | The string identifier of the asset | `string` |  | `""` | false | false | true |
| [iconAssetId](#iconAssetId) | The string identifier of the icon for the asset | `string` | uuid | `""` | false | false | true |
| [parentUID](#parentUID) | The UUID of the parent item to inherit stats, description, etc | `string` | uuid | `""` | false | false | true |
| [metaData](#metaData) |  | `object` |  | `undefined` | false | false | true |

## Examples
### Request

```json
{
    "name": "Pew Pew Gun",
    "description": "string",
    "cost": 0,
    "stats": [
        "Stat"
    ],
    "assetId": "string",
    "iconAssetId": "66e86ecf-c6f7-4722-87d5-935e128cbb40",
    "parentUID": "581008a4-9319-49bc-93a1-c401fb974319"
}
```

### Response

```json
{
    "uid": "767be631-a386-4243-a86f-d5fa8812a574",
    "dateCreated": "2019-12-06T19:01:21.436Z",
    "dateModified": "2019-12-06T19:01:21.436Z",
    "version": 0,
    "name": "Pew Pew Gun",
    "description": "string",
    "cost": 0,
    "stats": [
        "Stat"
    ],
    "assetId": "string",
    "iconAssetId": "66e86ecf-c6f7-4722-87d5-935e128cbb40",
    "parentUID": "581008a4-9319-49bc-93a1-c401fb974319"
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

### name

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The item name

### description

Type: `string`

Default Value: `""`

Required: `true`

Description of the item

### cost

Type: `number`

Default Value: `0`

Required: `true`

The cost of the item

### stats

Type: `array`

Default Value: ``

Required: `true`

The list of stats for the item.

### assetId

Type: `string`

Default Value: `""`

Required: `true`

The string identifier of the asset

### iconAssetId

Type: `string`

Default Value: `""`

Required: `true`

The string identifier of the icon for the asset

### parentUID

Type: `string`

Default Value: `""`

Required: `true`

The UUID of the parent item to inherit stats, description, etc

### metaData

Type: `object`

Default Value: `undefined`

Required: `true`



## References

This data model is referenced in the following endpoints.

// TODO