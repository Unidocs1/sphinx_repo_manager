---
title: "Snapshot"
date: 2019-05-24T20:03:25.798Z
---

A `Snapshot` describes a catalog of versioned assets at a given point in time. The `Snapshot` is considered immutable and should not be modified once created.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the snapshot expressed as a version string using the regex `^(\d+\.)?(\d+\.)?(\d+)?(-?[a-zA-Z0-9]+)?$`. | `string` |  | `""` | true | true | true |
| [assets](#assets) | The list of unique identifiers for each asset described in the snapshot. | `array` | uuid | `` | false | false | true |
| [description](#description) | The textual description of the snapshot. | `string` |  | `""` | false | false | true |
| [environment](#environment) | The application's deployment environment that the snapshot has been created for. | `string` |  | `development` | false | false | true |
| [notes](#notes) | A textual list of notes pertaining to the version of assets contained in the snapshot (aka release notes). | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "name": "string",
    "assets": [
        "string"
    ],
    "description": "string",
    "environment": "string",
    "notes": "string"
}
```

### Response

```json
{
    "uid": "7a0a70c5-8c33-4cf7-8fc2-1c4718662630",
    "dateCreated": "2019-05-24T20:03:30.516Z",
    "dateModified": "2019-05-24T20:03:30.516Z",
    "version": 0,
    "name": "string",
    "assets": [
        "string"
    ],
    "description": "string",
    "environment": "string",
    "notes": "string"
}
```


## Members

### uid

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the object.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the object was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the object was last modified.

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

The unique name of the snapshot expressed as a version string using the regex `^(\d+\.)?(\d+\.)?(\d+)?(-?[a-zA-Z0-9]+)?$`.

### assets

Type: `array`

Default Value: ``

Required: `true`

The list of unique identifiers for each asset described in the snapshot.

### description

Type: `string`

Default Value: `""`

Required: `true`

The textual description of the snapshot.

### environment

Type: `string`

Default Value: `development`

Required: `true`

The application's deployment environment that the snapshot has been created for.

### notes

Type: `string`

Default Value: `""`

Required: `true`

A textual list of notes pertaining to the version of assets contained in the snapshot (aka release notes).

## References

This data model is referenced in the following endpoints.

// TODO