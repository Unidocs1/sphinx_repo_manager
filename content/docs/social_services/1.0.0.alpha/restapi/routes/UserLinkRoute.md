---
title: "UserLink Routes"
date: 2019-07-05T22:50:13.161Z
---



## Routes

### FindAll
`GET /links`

Authentication: **Required**

Returns all links from the system that the user has access to

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /links
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /links`

Authentication: **Required**

Create a new link.

#### Request
```http
POST /links
Content-Type: application/json
Authorization: jwt <token>

{
    "status": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.328Z",
    "dateModified": "2019-07-05T22:50:13.328Z",
    "version": 0,
    "userUid": "29a1895a-8fd3-4894-863b-5521142158e8",
    "otherUid": "af0c6c05-3603-4fb4-a4fb-bc364eed11e9",
    "status": "string"
}
```

### Count
`GET /links/count`

Authentication: **Required**

Returns the count of links

#### Request
```http
GET /links/count
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
`GET /links/{id}`

Authentication: **Required**

Returns a single link from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /links/{id}
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
    "userUid": "327635df-a4d6-40fa-92e8-303497d01197",
    "otherUid": "bdc71f6f-5887-4962-b85a-a60033e58eea",
    "status": "string"
}
```

### Update
`PUT /links/{id}`

Authentication: **Required**

Updates a single link

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /links/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "status": "string"
}
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
    "userUid": "a032fb42-5860-4c76-bd96-955e234d3532",
    "otherUid": "c58ef7be-b41a-4762-8200-a3393b49b525",
    "status": "string"
}
```

### Delete
`DELETE /links/{id}`

Authentication: **Required**

Deletes the link

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /links/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### FindByUserUid
`GET /{userUid}/links`

Authentication: **Required**

Returns all links associated with a given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
GET /{userUid}/links
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.329Z",
    "dateModified": "2019-07-05T22:50:13.329Z",
    "version": 0,
    "userUid": "3c23a6e2-2ae2-4e8c-aea7-44d3a20b5cc8",
    "otherUid": "e6d99ad0-3866-4163-8256-97697ccebbd4",
    "status": "string"
}
```

### CreateByUserUid
`POST /{userUid}/links`

Authentication: **Required**

Creates a new link for a given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
POST /{userUid}/links
Content-Type: application/json
Authorization: jwt <token>

{
    "status": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.329Z",
    "dateModified": "2019-07-05T22:50:13.329Z",
    "version": 0,
    "userUid": "c95fe86a-a9c2-4534-857b-747b2de04bf2",
    "otherUid": "8a88ba16-b58f-4526-a2f6-4cb74bab1e22",
    "status": "string"
}
```

### SetByUserUid
`PUT /{userUid}/links`

Authentication: **Required**

Sets the list of all links for a given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
PUT /{userUid}/links
Content-Type: application/json
Authorization: jwt <token>

{}
```

#### Response
```http
200 OK
```

### DeleteByUserUid
`DELETE /{userUid}/links`

Authentication: **Required**

Deletes all links for a given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
DELETE /{userUid}/links
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### FindByIdAndUserUid
`GET /{userUid}/links/{id}`

Authentication: **Required**

Returns a single link for the given user and id.

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
GET /{userUid}/links/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.329Z",
    "dateModified": "2019-07-05T22:50:13.329Z",
    "version": 0,
    "userUid": "e2e81d72-70ba-4863-8eee-0c57029db056",
    "otherUid": "5d8c3c05-d1db-4a3d-b694-7a689bc4f9f8",
    "status": "string"
}
```

### UpdateByIdAndUserUid
`PUT /{userUid}/links/{id}`

Authentication: **Required**

Updates a single link for a given user and id.

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
PUT /{userUid}/links/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "status": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.329Z",
    "dateModified": "2019-07-05T22:50:13.329Z",
    "version": 0,
    "userUid": "4c38116c-817a-4791-95e3-95ce1ac1c3e7",
    "otherUid": "319e6d42-d1d4-44d8-b41e-d89e0bae5070",
    "status": "string"
}
```

### DeleteByIdAndUserUid
`DELETE /{userUid}/links/{id}`

Authentication: **Required**

Deletes the link for the given user and id.

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
DELETE /{userUid}/links/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

