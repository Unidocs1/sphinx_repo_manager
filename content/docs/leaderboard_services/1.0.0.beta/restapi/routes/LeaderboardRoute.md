---
title: "Leaderboard Routes"
date: 2019-10-28T17:42:16.105Z
---



## Routes

### FindAll
`GET /leaderboards`

Authentication: Optional

Returns all leaderboard definitions from the system that the user has access to based upon the given criteria.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /leaderboards
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /leaderboards`

Authentication: **Required**

Creates a new leaderboard definition.

#### Request
```http
POST /leaderboards
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "description": "string",
    "icon": "string",
    "compareFunc": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "0355a64f-5344-4a38-961a-032b80992621",
    "dateCreated": "2019-10-28T17:42:16.188Z",
    "dateModified": "2019-10-28T17:42:16.188Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "icon": "string",
    "compareFunc": "string"
}
```

### Truncate
`DELETE /leaderboards`

Authentication: **Required**

Deletes all leaderboard definitions from the service.

#### Request
```http
DELETE /leaderboards
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /leaderboards/count`

Authentication: Optional

Returns the count of leaderboard definitions based on the given criteria.

#### Request
```http
GET /leaderboards/count
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
`GET /leaderboards/{id}`

Authentication: Optional

Returns a single leaderboard definition from the system that the user has access to.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /leaderboards/{id}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "6d92679e-c8b4-46e1-a811-39c0350fdf95",
    "dateCreated": "2019-10-28T17:42:16.188Z",
    "dateModified": "2019-10-28T17:42:16.188Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "icon": "string",
    "compareFunc": "string"
}
```

### Update
`PUT /leaderboards/{id}`

Authentication: **Required**

Updates a single leaderboard definition.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /leaderboards/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "description": "string",
    "icon": "string",
    "compareFunc": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "489b1b72-d462-4ff5-9413-8068e582444d",
    "dateCreated": "2019-10-28T17:42:16.188Z",
    "dateModified": "2019-10-28T17:42:16.188Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "icon": "string",
    "compareFunc": "string"
}
```

### Delete
`DELETE /leaderboards/{id}`

Authentication: **Required**

Deletes the leaderboard from the service.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /leaderboards/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

