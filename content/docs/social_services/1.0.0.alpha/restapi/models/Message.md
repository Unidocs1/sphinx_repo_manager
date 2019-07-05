---
title: "Message"
date: 2019-07-05T22:50:13.161Z
---

The `Message` is a persistent message or notification that is sent from one user to another.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the message. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the message was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the message was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [receiverUid](#receiverUid) | The unique identifier of the user that is to receive the message. | `string` | uuid | `""` | false | false | true |
| [senderUid](#senderUid) | The unique identifier of the user that sent the message. | `string` | uuid | `""` | false | false | true |
| [subject](#subject) | The summary of the message contents. | `string` |  | `""` | false | false | true |
| [body](#body) | The message contents. | `string` |  | `""` | false | false | true |
| [attachments](#attachments) | A map of key-value pairs representing a list of attachments that have been appended to the message. The key of each pair is the name of the attachment and the value must be an encoded string. The string can represent any data including binary data using base64 encoding. | `object` |  | `undefined` | false | false | true |

## Examples
### Request

```json
{
    "subject": "string",
    "body": "string"
}
```

### Response

```json
{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.280Z",
    "dateModified": "2019-07-05T22:50:13.280Z",
    "version": 0,
    "receiverUid": "e29c612a-c477-4eca-b4b7-16e5bf5c64bc",
    "senderUid": "eb3dc858-7867-42a1-9136-6e9ee1bceb61",
    "subject": "string",
    "body": "string"
}
```


## Members

### uid

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the message.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the message was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the message was last modified.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic lock version.

### receiverUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the user that is to receive the message.

### senderUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the user that sent the message.

### subject

Type: `string`

Default Value: `""`

Required: `true`

The summary of the message contents.

### body

Type: `string`

Default Value: `""`

Required: `true`

The message contents.

### attachments

Type: `object`

Default Value: `undefined`

Required: `true`

A map of key-value pairs representing a list of attachments that have been appended to the message. The key of each pair is the name of the attachment and the value must be an encoded string. The string can represent any data including binary data using base64 encoding.

## References

This data model is referenced in the following endpoints.

// TODO