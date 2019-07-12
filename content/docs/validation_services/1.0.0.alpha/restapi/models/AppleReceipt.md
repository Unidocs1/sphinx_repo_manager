---
title: "AppleReceipt"
date: 2019-07-12T00:24:32.539Z
---

Describes an in-app product purchase made with the Apple Store.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [receipt](#receipt) | The Apple receipt to validate. | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "receipt": "string"
}
```

### Response

```json
{
    "receipt": "string"
}
```


## Members

### receipt

Type: `string`

Default Value: `""`

Required: `true`

The Apple receipt to validate.

## References

This data model is referenced in the following endpoints.

// TODO