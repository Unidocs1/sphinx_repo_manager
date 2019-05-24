---
title: "PersonaStatDefinition"
date: 2019-05-24T20:03:52.354Z
---

The `PersonaStatDefinition` describes a single statistic that an persona can have.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the ticket. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the ticket was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the ticket was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the statistic. | `string` |  | `""` | true | true | true |
| [type](#type) | The data type describing how the statistic's value is stored. | `string` |  | `int` | false | false | true |
| [min](#min) | The minimum possible value that can be used. | `string` |  | `""` | false | false | false |
| [max](#max) | The maximum possible value that can be used. | `string` |  | `""` | false | false | false |
| [values](#values) | A list of all possible values that can be used. | `string` |  | `""` | false | false | false |
| [default](#default) |  | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "name": "string",
    "type": "string",
    "default": "string"
}
```

### Response

```json
{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.765Z",
    "dateModified": "2019-05-24T20:03:52.765Z",
    "version": 0,
    "name": "string",
    "type": "string",
    "min": "string",
    "max": "string",
    "values": "string",
    "default": "string"
}
```


## Members

### uid

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the ticket.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the ticket was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the ticket was last modified.

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

The unique name of the statistic.

### type

Type: `string`

Default Value: `int`

Required: `true`

The data type describing how the statistic's value is stored.

### min

Type: `string`

Default Value: `""`

Required: `false`

The minimum possible value that can be used.

### max

Type: `string`

Default Value: `""`

Required: `false`

The maximum possible value that can be used.

### values

Type: `string`

Default Value: `""`

Required: `false`

A list of all possible values that can be used.

### default

Type: `string`

Default Value: `""`

Required: `true`



## References

This data model is referenced in the following endpoints.

// TODO