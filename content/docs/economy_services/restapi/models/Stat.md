---
title: "Stat"
date: 2019-12-06T19:01:21.222Z
---

Describes a single stat for an item

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [name](#name) | The unique name of the stat. | `string` |  | `""` | false | false | true |
| [value](#value) | The value of the stat | `object` |  | `undefined` | false | false | true |

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

The unique name of the stat.

### value

Type: `object`

Default Value: `undefined`

Required: `true`

The value of the stat

## References

This data model is referenced in the following endpoints.

// TODO