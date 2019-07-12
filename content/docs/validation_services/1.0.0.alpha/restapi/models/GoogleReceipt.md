---
title: "GoogleReceipt"
date: 2019-07-12T00:24:32.539Z
---

Describes an in-app product purchase made with the Google Play store.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [packageName](#packageName) | The unique name of the app or package involved in the purchase. | `string` |  | `""` | false | false | true |
| [productId](#productId) | The unique identifier of the product that was purchased. | `string` |  | `""` | false | false | true |
| [token](#token) | The Google Play token to validate. | `string` |  | `""` | false | false | true |
| [type](#type) | Indicates whether the purchase is for a `product` or `subscription`. | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "packageName": "string",
    "productId": "string",
    "token": "string",
    "type": "string"
}
```

### Response

```json
{
    "packageName": "string",
    "productId": "string",
    "token": "string",
    "type": "string"
}
```


## Members

### packageName

Type: `string`

Default Value: `""`

Required: `true`

The unique name of the app or package involved in the purchase.

### productId

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the product that was purchased.

### token

Type: `string`

Default Value: `""`

Required: `true`

The Google Play token to validate.

### type

Type: `string`

Default Value: `""`

Required: `true`

Indicates whether the purchase is for a `product` or `subscription`.

## References

This data model is referenced in the following endpoints.

// TODO