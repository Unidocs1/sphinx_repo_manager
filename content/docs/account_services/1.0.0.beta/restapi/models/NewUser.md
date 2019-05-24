---
title: "NewUser"
date: 2019-05-24T20:08:59.489Z
---

The object that is returned when a new user is created containing the user and authentication token.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [token](#token) | The token that future requests can be made with to authenticate the user. | `string` | JWT | `""` | false | false | true |
| [user](#user) | The user that was successfully registered with the service. | `object` |  | `undefined` | false | false | true |

## Examples
### Request

```json
{
    "token": "string"
}
```

### Response

```json
{
    "token": "string"
}
```


## Members

### token

Type: `string`

Default Value: `""`

Required: `true`

The token that future requests can be made with to authenticate the user.

### user

Type: `object`

Default Value: `undefined`

Required: `true`

The user that was successfully registered with the service.

## References

This data model is referenced in the following endpoints.

// TODO