---
title: "PersonaStat"
date: 2019-05-24T20:03:52.354Z
---

The `PersonaStat` is an instance of a specific `PersonaStatDefinition` that is assocaited with a particular `Persona`.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the ticket. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the ticket was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the ticket was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [statUid](#statUid) | The unique identifier of the `PersonaStatDefinition` this object represents. | `string` | uuid | `""` | false | false | true |
| [personaUid](#personaUid) | The unique identifier of the `Persona` that this statistic is associated with. | `string` | uuid | `""` | false | false | true |
| [value](#value) | The current value of the statistic. | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "value": "string"
}
```

### Response

```json
{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.810Z",
    "dateModified": "2019-05-24T20:03:52.810Z",
    "version": 0,
    "statUid": "db251b80-4282-40ef-9f2a-608ed98d2e55",
    "personaUid": "11f259fa-b62e-407e-9c09-929963f2844c",
    "value": "string"
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

### statUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the `PersonaStatDefinition` this object represents.

### personaUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the `Persona` that this statistic is associated with.

### value

Type: `string`

Default Value: `""`

Required: `true`

The current value of the statistic.

## References

This data model is referenced in the following endpoints.

// TODO