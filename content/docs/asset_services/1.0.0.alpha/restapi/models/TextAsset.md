---
title: "TextAsset"
date: 2019-05-24T20:03:25.798Z
---

A `TextAsset` provides a definition of localized text associated with a given unique key. The localized text is defined using IETF BCP 47 language and region codes. The `TextAsset` is considered an immutable object and should not be modified once created. When the data of the localized text changes a new record should be created with a new version specified.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name or key of the asset. | `string` |  | `""` | true | false | true |
| [text](#text) | The map of IETF BCP 47 region codes to the localized text for each region. | `object` |  | `undefined` | false | false | true |
| [description](#description) | A textual description of the asset. | `string` |  | `""` | false | false | true |
| [roles](#roles) | The list of unique role names that a user must have in order to view the asset. | `` |  | `undefined` | false | false | false |

## Examples
### Request

```json
{
    "name": "string",
    "text": {
        "default": "message of the day",
        "en": "message of the day"
    },
    "description": "string"
}
```

### Response

```json
{
    "uid": "d5ad2460-9cd1-464f-ba0a-a023eec05937",
    "dateCreated": "2019-05-24T20:03:30.436Z",
    "dateModified": "2019-05-24T20:03:30.436Z",
    "version": 0,
    "name": "string",
    "text": {
        "default": "message of the day",
        "en": "message of the day"
    },
    "description": "string"
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

*Identifier*

The unique name or key of the asset.

### text

Type: `object`

Default Value: `undefined`

Required: `true`

The map of IETF BCP 47 region codes to the localized text for each region.

### description

Type: `string`

Default Value: `""`

Required: `true`

A textual description of the asset.

### roles

Type: ``

Default Value: `undefined`

Required: `false`

The list of unique role names that a user must have in order to view the asset.

## References

This data model is referenced in the following endpoints.

// TODO