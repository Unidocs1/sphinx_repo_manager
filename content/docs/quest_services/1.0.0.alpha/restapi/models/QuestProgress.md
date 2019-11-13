---
title: "QuestProgress"
date: 2019-11-07T21:58:38.095Z
---

Tracks the persona's progress of a single requirement for a given quest.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [type](#type) | The requirement type of the quest being tracked. | `string` |  | `""` | false | false | true |
| [value](#value) | The current value of the player's progress. | `number` |  | `0` | false | false | true |

## Examples
### Request

```json
{
    "type": "string",
    "value": 0
}
```

### Response

```json
{
    "type": "string",
    "value": 0
}
```


## Members

### type

Type: `string`

Default Value: `""`

Required: `true`

The requirement type of the quest being tracked.

### value

Type: `number`

Default Value: `0`

Required: `true`

The current value of the player's progress.

## References

This data model is referenced in the following endpoints.

// TODO