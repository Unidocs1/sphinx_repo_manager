---
title: "PersonaStat Routes"
date: 2019-05-24T20:03:52.354Z
---



## Routes

### FindAll
`GET /personas/stats`

Authentication: **Required**

Returns all persona stats from the system that the user has access to

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /personas/stats
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /personas/stats`

Authentication: **Required**

Create a new stat for an persona

#### Request
```http
POST /personas/stats
Content-Type: application/json
Authorization: jwt <token>

{
    "value": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.853Z",
    "dateModified": "2019-05-24T20:03:52.853Z",
    "version": 0,
    "statUid": "60639020-6c78-4f0b-936c-7792c5f02ff4",
    "personaUid": "242131fd-a2f8-43d8-b6cb-ff30c6ca495b",
    "value": "string"
}
```

### Count
`GET /personas/stats/count`

Authentication: **Required**

Returns the count of persona stats

#### Request
```http
GET /personas/stats/count
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
`GET /personas/stats/{id}`

Authentication: **Required**

Returns a single persona stat from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /personas/stats/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.854Z",
    "dateModified": "2019-05-24T20:03:52.854Z",
    "version": 0,
    "statUid": "ac852ff6-5fca-4cae-b1a5-a4066c1b437f",
    "personaUid": "a338f7ba-1121-49e9-9052-2eb1e6fa5ae4",
    "value": "string"
}
```

### Update
`PUT /personas/stats/{id}`

Authentication: **Required**

Updates a single persona stat

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /personas/stats/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "value": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.856Z",
    "dateModified": "2019-05-24T20:03:52.856Z",
    "version": 0,
    "statUid": "e66ca348-4ab9-4023-b129-0068f341497f",
    "personaUid": "c323f588-8870-4465-8c3d-cb0a3c04c545",
    "value": "string"
}
```

### Delete
`DELETE /personas/stats/{id}`

Authentication: **Required**

Deletes the persona stat

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /personas/stats/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### FindAllByPersonaId
`GET /personas/{personaUid}/stats`

Authentication: **Required**

Returns all persona stats from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /personas/{personaUid}/stats
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### FindByIdAndPersonaId
`GET /personas/{personaUid}/stats/{statUid}`

Authentication: **Required**

Returns a single persona stat from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| statUid |

#### Request
```http
GET /personas/{personaUid}/stats/{statUid}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.857Z",
    "dateModified": "2019-05-24T20:03:52.857Z",
    "version": 0,
    "statUid": "725a5194-ba95-4edc-a87f-c69da97e1fcc",
    "personaUid": "4f32098c-d94a-48a9-bdfe-db0301f96dfe",
    "value": "string"
}
```

### UpdateByPersonaId
`PUT /personas/{personaUid}/stats/{statUid}`

Authentication: **Required**

Updates a single persona stat

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| statUid |

#### Request
```http
PUT /personas/{personaUid}/stats/{statUid}
Content-Type: application/json
Authorization: jwt <token>

{
    "value": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.859Z",
    "dateModified": "2019-05-24T20:03:52.859Z",
    "version": 0,
    "statUid": "041adb30-2a0b-4761-a14c-3e95362677a6",
    "personaUid": "79427117-2e84-4f22-85d0-407de47f90d7",
    "value": "string"
}
```

### DeleteByPersonaId
`DELETE /personas/{personaUid}/stats/{statUid}`

Authentication: **Required**

Deletes the persona stat

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| statUid |

#### Request
```http
DELETE /personas/{personaUid}/stats/{statUid}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

