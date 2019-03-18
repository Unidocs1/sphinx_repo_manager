---
title: "Statistic"
date: 2019-03-18T21:19:59.093Z
chapter: true
---

Describes a single metric by which users will be compared and filtered.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [name](#name) | The unique name of the statistic. | `string` |  | `""` | false | false | true |
| [value](#value) | The value of the statistic representing the combined average of all users on a ticket or match. | `object` |  | `undefined` | false | false | true |

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

The unique name of the statistic.

### value

Type: `object`

Default Value: `undefined`

Required: `true`

The value of the statistic representing the combined average of all users on a ticket or match.

## References

This data model is referenced in the following endpoints.

// TODO