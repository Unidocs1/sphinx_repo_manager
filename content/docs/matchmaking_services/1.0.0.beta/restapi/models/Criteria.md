---
title: "Criteria"
date: 2019-05-24T20:04:07.747Z
---

Describes a single statistic by which to filter all matchmaking search results. Each criteria must have a corresponding `Statistic` object with the same `name`.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [name](#name) | The unique name of the criteria to consider. | `string` |  | `""` | false | false | true |
| [minValue](#minValue) | The minimum value that the criteria will consider. | `object` |  | `undefined` | false | false | true |
| [maxValue](#maxValue) | The maximum value that the criteria will consider. | `object` |  | `undefined` | false | false | true |

## Examples
### Request

```json
{
    "name": "string"
}
```

### Response

```json
{
    "name": "string"
}
```


## Members

### name

Type: `string`

Default Value: `""`

Required: `true`

The unique name of the criteria to consider.

### minValue

Type: `object`

Default Value: `undefined`

Required: `true`

The minimum value that the criteria will consider.

### maxValue

Type: `object`

Default Value: `undefined`

Required: `true`

The maximum value that the criteria will consider.

## References

This data model is referenced in the following endpoints.

// TODO