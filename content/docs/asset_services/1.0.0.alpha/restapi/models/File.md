---
title: "File"
date: 2019-05-24T20:03:25.798Z
---

Defines the metadata associated with a particular file such as the URI of the file's location, the sha256 checksum and the mime type. The `File` is considered immutable and should not be modified once created. When the actual file data changes that a `File` describes then a new `File` record should be created for that version.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the file. | `string` |  | `""` | true | false | true |
| [sha256sum](#sha256sum) | The SHA256 checksum of the file's contents. | `string` |  | `""` | false | false | true |
| [uri](#uri) | The universal resource identifier of the file. e.g. it's location on the Internet. | `string` |  | `""` | false | false | true |
| [mimetype](#mimetype) | The type of data that the file contains. | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "name": "string",
    "sha256sum": "string",
    "uri": "string",
    "mimetype": "string"
}
```

### Response

```json
{
    "uid": "7bc3d0e8-c2f0-4209-93f5-291c3c42d8db",
    "dateCreated": "2019-05-24T20:03:30.395Z",
    "dateModified": "2019-05-24T20:03:30.395Z",
    "version": 0,
    "name": "string",
    "sha256sum": "string",
    "uri": "string",
    "mimetype": "string"
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

The unique name of the file.

### sha256sum

Type: `string`

Default Value: `""`

Required: `true`

The SHA256 checksum of the file's contents.

### uri

Type: `string`

Default Value: `""`

Required: `true`

The universal resource identifier of the file. e.g. it's location on the Internet.

### mimetype

Type: `string`

Default Value: `""`

Required: `true`

The type of data that the file contains.

## References

This data model is referenced in the following endpoints.

// TODO