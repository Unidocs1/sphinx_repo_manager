---
title: "Message Routes"
date: 2019-07-05T22:50:13.161Z
---



## Routes

### FindAll
`GET /messages`

Authentication: **Required**

Returns all messages from the system that the user has access to

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /messages
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /messages`

Authentication: **Required**

Create a new message.

#### Request
```http
POST /messages
Content-Type: application/json
Authorization: jwt <token>

{
    "subject": "string",
    "body": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.327Z",
    "dateModified": "2019-07-05T22:50:13.327Z",
    "version": 0,
    "receiverUid": "e08ccad7-fb7f-498b-a8e6-cae613ff978b",
    "senderUid": "3a97a896-abaf-4f61-9d56-1816a0886aca",
    "subject": "string",
    "body": "string"
}
```

### Count
`GET /messages/count`

Authentication: **Required**

Returns the count of messages

#### Request
```http
GET /messages/count
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "count": 0
}
```

### FindById
`GET /messages/{id}`

Authentication: **Required**

Returns a single message from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /messages/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.327Z",
    "dateModified": "2019-07-05T22:50:13.327Z",
    "version": 0,
    "receiverUid": "3f7f33ee-72e5-4b1a-98e2-1b058835a0b2",
    "senderUid": "1d4b0d2d-4430-413b-9fa6-6db82fa6db77",
    "subject": "string",
    "body": "string"
}
```

### Delete
`DELETE /messages/{id}`

Authentication: **Required**

Deletes the message

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /messages/{id}
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

### MarkRead
`GET /messages/{id}/read`

Authentication: **Required**

Marks the message with the given id as having been read by the user.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /messages/{id}/read
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

### FindInboxByUserUid
`GET /{userUid}/messages/inbox`

Authentication: **Required**

Returns all of the messages from the system that have been sent to the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
GET /{userUid}/messages/inbox
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.327Z",
    "dateModified": "2019-07-05T22:50:13.327Z",
    "version": 0,
    "receiverUid": "5c075198-823d-4fe0-b1e5-d3815290cc3e",
    "senderUid": "77431e42-dcb9-4ee7-bf93-bc7ba80a949b",
    "subject": "string",
    "body": "string"
}
```

### DeleteInboxByUserUid
`DELETE /{userUid}/messages/inbox`

Authentication: **Required**

Deletes all messages sent to the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
DELETE /{userUid}/messages/inbox
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

### FindSentByUserUid
`GET /{userUid}/messages/sent`

Authentication: **Required**

Returns all of the messages from the system that have been sent by the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
GET /{userUid}/messages/sent
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.327Z",
    "dateModified": "2019-07-05T22:50:13.327Z",
    "version": 0,
    "receiverUid": "0fea90a2-4399-40ce-b6a6-5796b832032e",
    "senderUid": "b2e58d95-5e9f-462a-a6d2-f76600f679a0",
    "subject": "string",
    "body": "string"
}
```

### DeleteSentByUserUid
`DELETE /{userUid}/messages/sent`

Authentication: **Required**

Deletes all messages sent by the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
DELETE /{userUid}/messages/sent
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

### FindByIdAndUserUid
`GET /{userUid}/messages/{id}`

Authentication: **Required**

Returns the messages from the system with the given id that was sent to the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /{userUid}/messages/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.328Z",
    "dateModified": "2019-07-05T22:50:13.328Z",
    "version": 0,
    "receiverUid": "8ba5d251-73b7-4aae-95a9-fc18148aa5fa",
    "senderUid": "984ee202-4d47-42a0-8460-0ee56a1f859a",
    "subject": "string",
    "body": "string"
}
```

### DeleteByIdAndUserUid
`DELETE /{userUid}/messages/{id}`

Authentication: **Required**

Deletes the message with the given id that sent to the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /{userUid}/messages/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### MarkReadByIdAndUserId
`GET /{userUid}/messages/{id}/read`

Authentication: **Required**

Marks the message with the given id as having been read by the user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /{userUid}/messages/{id}/read
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

