---
title: "MediaAsset"
date: 2019-05-24T20:03:25.798Z
---

A `MediaAsset` provides a definition of localized files associated with a given unique key. The `MediaAsset` is considered an immutable object and should not be modified once created. When a new version of a `File` is created a new `MediaAsset` referencing that `File` should also be created for the new version.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name or key of the asset. | `string` |  | `""` | true | true | true |
| [files](#files) | The map of IETF BCP 47 region codes to the localized file objects for each region. | `object` |  | `undefined` | false | false | true |
| [description](#description) |  | `string` |  | `""` | false | false | true |
| [roles](#roles) | The list of unique role names that a user must have in order to view the asset. | `` |  | `undefined` | false | false | false |

## Examples
### Request

```json
{
    "name": "string",
    "files": {
        "default": {
            "mimetype": "image/jpeg",
            "name": "beer2.jpg",
            "sha256sum": "30156ccd7935729edfac7882d317f64ef0ed57bb24b6f416e1a7592ff576450c",
            "uri": "https://storage.googleapis.com/assets.slendargame.com/files/c213f4b65bc856efc1f6c03a7d3d2425",
            "uid": "476da6b2-0eea-4a79-8c36-cac6d6d3a486",
            "dateCreated": "2018-07-16T04:10:04.993Z",
            "dateModified": "2018-07-16T04:10:04.997Z",
            "version": 0
        }
    },
    "description": "string"
}
```

### Response

```json
{
    "uid": "4afa41ec-e173-42c1-bf04-d1dd8fd67c23",
    "dateCreated": "2019-05-24T20:03:30.477Z",
    "dateModified": "2019-05-24T20:03:30.477Z",
    "version": 0,
    "name": "string",
    "files": {
        "default": {
            "mimetype": "image/jpeg",
            "name": "beer2.jpg",
            "sha256sum": "30156ccd7935729edfac7882d317f64ef0ed57bb24b6f416e1a7592ff576450c",
            "uri": "https://storage.googleapis.com/assets.slendargame.com/files/c213f4b65bc856efc1f6c03a7d3d2425",
            "uid": "476da6b2-0eea-4a79-8c36-cac6d6d3a486",
            "dateCreated": "2018-07-16T04:10:04.993Z",
            "dateModified": "2018-07-16T04:10:04.997Z",
            "version": 0
        }
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

*Unique* *Identifier*

The unique name or key of the asset.

### files

Type: `object`

Default Value: `undefined`

Required: `true`

The map of IETF BCP 47 region codes to the localized file objects for each region.

### description

Type: `string`

Default Value: `""`

Required: `true`



### roles

Type: ``

Default Value: `undefined`

Required: `false`

The list of unique role names that a user must have in order to view the asset.

## References

This data model is referenced in the following endpoints.

// TODO