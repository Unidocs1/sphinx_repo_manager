---
title: "QuestReward"
date: 2019-11-07T21:58:38.095Z
---

Defines a single reward that will be given once a quest is fulfilled.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [type](#type) | The type of reward that will be given. | `` |  | `PROGRESS` | false | false | true |
| [quantity](#quantity) | The quantity amount to reward. | `number` |  | `0` | false | false | true |
| [entityUid](#entityUid) | The universally unique identifier of the entity that will be rewarded. | `string` |  | `""` | false | false | true |

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
    "quantity": 0,
    "entityUid": "string"
}
```


## Members

### type

Type: ``

Default Value: `PROGRESS`

Required: `true`

The type of reward that will be given.

### quantity

Type: `number`

Default Value: `0`

Required: `true`

The quantity amount to reward.

### entityUid

Type: `string`

Default Value: `""`

Required: `true`

The universally unique identifier of the entity that will be rewarded.

## References

This data model is referenced in the following endpoints.

// TODO