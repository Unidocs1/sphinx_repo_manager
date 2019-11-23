---
title: "Archetype Routes"
date: 2019-11-22T23:48:48.249Z
---



## Parameters
| Name       | Description                           |  Type |
| ---------- | ------------------------------------- | ----- |
|  |  |  |

## Routes

### FindAll
`GET /personas/{personaUid}/archetypes`

Authentication: Optional

Returns all archetypes that the given persona has activated.

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
GET /personas/{personaUid}/archetypes
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### DeactivateAll
`DELETE /personas/{personaUid}/archetypes`

Authentication: **Required**

Stops tracking all progress for all archetypes and persona.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Request
```http
DELETE /personas/{personaUid}/archetypes
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

### Count
`GET /personas/{personaUid}/archetypes/count`

Authentication: Optional

Returns the count of archetypes that a persona has activate.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Request
```http
GET /personas/{personaUid}/archetypes/count
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
`GET /personas/{personaUid}/archetypes/{archetypeUid}`

Authentication: Optional

Returns the archetype definition.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| archetypeUid |

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /personas/{personaUid}/archetypes/{archetypeUid}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "76c00149-ba50-4dbf-98bf-eb16ffd5f8be",
    "dateCreated": "2019-11-22T23:48:48.414Z",
    "dateModified": "2019-11-22T23:48:48.414Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "skills": [
        "string"
    ]
}
```

### Deactivate
`DELETE /personas/{personaUid}/archetypes/{archetypeUid}`

Authentication: **Required**

Stops tracking all progress for the given archetype and persona.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| archetypeUid |

#### Request
```http
DELETE /personas/{personaUid}/archetypes/{archetypeUid}
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

### Toggle
`PUT /personas/{personaUid}/archetypes/{archetypeUid}`

Authentication: **Required**

Toggles the activation state of all skill progress for a given archetype and persona.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| archetypeUid |

#### Request
```http
PUT /personas/{personaUid}/archetypes/{archetypeUid}
Content-Type: application/json
Authorization: jwt <token>

{
    "enabled": false
}
```

#### Response
```http
204 NO CONTENT
```

