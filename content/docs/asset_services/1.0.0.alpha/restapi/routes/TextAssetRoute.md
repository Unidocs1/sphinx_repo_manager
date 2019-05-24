---
title: "TextAsset Routes"
date: 2019-05-24T20:03:25.798Z
---



## Routes

### FindAll
`GET /assets/text`

Authentication: **Required**

Returns all assets from the system that the user has access to

#### Request
```http
GET /assets/text
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /assets/text`

Authentication: **Required**

Create a new text asset

#### Request
```http
POST /assets/text
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "text": {
        "default": "message of the day",
        "en": "message of the day"
    },
    "description": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "9c3f4138-5011-410c-8637-ab2ba2514798",
    "dateCreated": "2019-05-24T20:03:30.565Z",
    "dateModified": "2019-05-24T20:03:30.565Z",
    "version": 0,
    "name": "string",
    "text": {
        "default": "message of the day",
        "en": "message of the day"
    },
    "description": "string"
}
```

### Count
`GET /assets/text/count`

Authentication: **Required**

Returns the count of text assets

#### Request
```http
GET /assets/text/count
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
`GET /assets/text/{id}`

Authentication: **Required**

Returns a single text asset from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /assets/text/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "7d76decf-33c0-4c0e-a2e3-340cd7dd9836",
    "dateCreated": "2019-05-24T20:03:30.566Z",
    "dateModified": "2019-05-24T20:03:30.566Z",
    "version": 0,
    "name": "string",
    "text": {
        "default": "message of the day",
        "en": "message of the day"
    },
    "description": "string"
}
```

### Update
`PUT /assets/text/{id}`

Authentication: **Required**

Updates a single text asset

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /assets/text/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "text": {
        "default": "message of the day",
        "en": "message of the day"
    },
    "description": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "697ff737-d02a-4fb7-a858-40b11456317d",
    "dateCreated": "2019-05-24T20:03:30.567Z",
    "dateModified": "2019-05-24T20:03:30.567Z",
    "version": 0,
    "name": "string",
    "text": {
        "default": "message of the day",
        "en": "message of the day"
    },
    "description": "string"
}
```

### Delete
`DELETE /assets/text/{id}`

Authentication: **Required**

Deletes the file

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /assets/text/{id}
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

