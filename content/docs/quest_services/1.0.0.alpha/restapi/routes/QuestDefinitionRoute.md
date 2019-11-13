---
title: "QuestDefinition Routes"
date: 2019-11-07T21:58:38.095Z
---



## Routes

### FindAll
`GET /quests`

Authentication: Optional

Returns all quest definitions from the system that the persona has access to based upon the given criteria.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /quests
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /quests`

Authentication: **Required**

Creates a new quest definition.

#### Request
```http
POST /quests
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "requirements": [
        "QuestRequirement"
    ],
    "rewards": [
        "QuestReward"
    ],
    "dateAvailable": "2019-11-07T21:58:38.302Z",
    "dateFinished": "2019-11-07T21:58:38.302Z",
    "frequency": "string",
    "unlockRequirements": [
        "QuestRequirement"
    ],
    "autostart": false
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "fe657a43-a268-49f5-8364-a59f96375646",
    "dateCreated": "2019-11-07T21:58:38.302Z",
    "dateModified": "2019-11-07T21:58:38.302Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "entityUid": "string",
    "requirements": [
        "QuestRequirement"
    ],
    "rewards": [
        "QuestReward"
    ],
    "dateAvailable": "2019-11-07T21:58:38.302Z",
    "dateFinished": "2019-11-07T21:58:38.302Z",
    "frequency": "string",
    "unlockRequirements": [
        "QuestRequirement"
    ],
    "autostart": false
}
```

### Truncate
`DELETE /quests`

Authentication: **Required**

Deletes all quest definitions from the service.

#### Request
```http
DELETE /quests
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /quests/count`

Authentication: Optional

Returns the count of quest definitions based on the given criteria.

#### Request
```http
GET /quests/count
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
`GET /quests/{id}`

Authentication: Optional

Returns a single quest definition from the system that the persona has access to.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /quests/{id}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "62b088b9-7569-4a1a-bf0c-73d2e6ca9744",
    "dateCreated": "2019-11-07T21:58:38.303Z",
    "dateModified": "2019-11-07T21:58:38.303Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "entityUid": "string",
    "requirements": [
        "QuestRequirement"
    ],
    "rewards": [
        "QuestReward"
    ],
    "dateAvailable": "2019-11-07T21:58:38.303Z",
    "dateFinished": "2019-11-07T21:58:38.303Z",
    "frequency": "string",
    "unlockRequirements": [
        "QuestRequirement"
    ],
    "autostart": false
}
```

### Update
`PUT /quests/{id}`

Authentication: **Required**

Updates a single quest definition.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /quests/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "requirements": [
        "QuestRequirement"
    ],
    "rewards": [
        "QuestReward"
    ],
    "dateAvailable": "2019-11-07T21:58:38.303Z",
    "dateFinished": "2019-11-07T21:58:38.303Z",
    "frequency": "string",
    "unlockRequirements": [
        "QuestRequirement"
    ],
    "autostart": false
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "f9d44cdb-4598-4018-8302-325bc41c03bc",
    "dateCreated": "2019-11-07T21:58:38.303Z",
    "dateModified": "2019-11-07T21:58:38.303Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "entityUid": "string",
    "requirements": [
        "QuestRequirement"
    ],
    "rewards": [
        "QuestReward"
    ],
    "dateAvailable": "2019-11-07T21:58:38.303Z",
    "dateFinished": "2019-11-07T21:58:38.303Z",
    "frequency": "string",
    "unlockRequirements": [
        "QuestRequirement"
    ],
    "autostart": false
}
```

### Delete
`DELETE /quests/{id}`

Authentication: **Required**

Deletes the quest from the service.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /quests/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

