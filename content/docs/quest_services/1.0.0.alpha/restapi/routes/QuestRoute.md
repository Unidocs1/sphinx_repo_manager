---
title: "Quest Routes"
date: 2019-11-07T21:58:38.095Z
---



## Parameters
| Name       | Description                           |  Type |
| ---------- | ------------------------------------- | ----- |
|  |  |  |

## Routes

### FindAll
`GET /personas/{personaUid}/quests`

Authentication: Optional

Returns progress data for all quests that the given persona has started or completed.

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
GET /personas/{personaUid}/quests
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /personas/{personaUid}/quests`

Authentication: **Required**

Starts progress of the given quest for the specified persona.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Request
```http
POST /personas/{personaUid}/quests
Content-Type: application/json
Authorization: jwt <token>

{
    "progress": [
        "QuestProgress"
    ],
    "completions": 0,
    "dateLastCompleted": "2019-11-07T21:58:38.303Z",
    "dateLastStarted": "2019-11-07T21:58:38.303Z",
    "unlocked": false,
    "unlockProgress": [
        "QuestProgress"
    ]
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "a4783b87-68f2-482e-ba8a-e8f13eb8472d",
    "dateCreated": "2019-11-07T21:58:38.303Z",
    "dateModified": "2019-11-07T21:58:38.303Z",
    "version": 0,
    "questUid": "string",
    "personaUid": "string",
    "progress": [
        "QuestProgress"
    ],
    "completions": 0,
    "dateLastCompleted": "2019-11-07T21:58:38.304Z",
    "dateLastStarted": "2019-11-07T21:58:38.304Z",
    "unlocked": false,
    "unlockProgress": [
        "QuestProgress"
    ]
}
```

### Truncate
`DELETE /personas/{personaUid}/quests`

Authentication: **Required**

Deletes all the persona's quest progress.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Request
```http
DELETE /personas/{personaUid}/quests
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /personas/{personaUid}/quests/count`

Authentication: Optional

Returns the count of quests that a persona has in progress or has completed.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Request
```http
GET /personas/{personaUid}/quests/count
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
`GET /personas/{personaUid}/quests/{questUid}`

Authentication: Optional

Returns the progress for a given quest and persona.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| questUid |

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /personas/{personaUid}/quests/{questUid}
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Delete
`DELETE /personas/{personaUid}/quests/{questUid}`

Authentication: **Required**

Deletes the persona's progress for a given quest.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| questUid |

#### Request
```http
DELETE /personas/{personaUid}/quests/{questUid}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Start
`GET /personas/{personaUid}/quests/{questUid}/start`

Authentication: Optional

Starts tracking the persona's progress for a given quest.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| questUid |

#### Request
```http
GET /personas/{personaUid}/quests/{questUid}/start
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Unlock
`GET /personas/{personaUid}/quests/{questUid}/unlock`

Authentication: Optional

Marks the quest has unlocked and able to be started by the specified persona.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| questUid |

#### Request
```http
GET /personas/{personaUid}/quests/{questUid}/unlock
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

