---
title: "Skill Routes"
date: 2019-11-22T23:48:48.249Z
---



## Parameters
| Name       | Description                           |  Type |
| ---------- | ------------------------------------- | ----- |
|  |  |  |
|  |  |  |

## Routes

### FindAllByArchetype
`GET /personas/{personaUid}/archetypes/{archetypeUid}/skills`

Authentication: Optional

Returns progress data for all skills that the given persona and archetype has started or completed.

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
GET /personas/{personaUid}/archetypes/{archetypeUid}/skills
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### TruncateByArchetype
`DELETE /personas/{personaUid}/archetypes/{archetypeUid}/skills`

Authentication: **Required**

Resets all the persona's skill progress for the given archetype.

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
DELETE /personas/{personaUid}/archetypes/{archetypeUid}/skills
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### CountByArchetype
`GET /personas/{personaUid}/archetypes/{archetypeUid}/skills/count`

Authentication: Optional

Returns the count of skills that a persona and archetype has in progress or has completed.

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
GET /personas/{personaUid}/archetypes/{archetypeUid}/skills/count
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
`GET /personas/{personaUid}/archetypes/{archetypeUid}/skills/{skillUid}`

Authentication: Optional

Returns the progress for a given skill and persona and archetype.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| archetypeUid |

#### Parameters
| Name       |
| ---------- |
| skillUid |

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /personas/{personaUid}/archetypes/{archetypeUid}/skills/{skillUid}
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Delete
`DELETE /personas/{personaUid}/archetypes/{archetypeUid}/skills/{skillUid}`

Authentication: **Required**

Deletes the persona's progress for a given skill and archetype.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| archetypeUid |

#### Parameters
| Name       |
| ---------- |
| skillUid |

#### Request
```http
DELETE /personas/{personaUid}/archetypes/{archetypeUid}/skills/{skillUid}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### AddProgress
`POST /personas/{personaUid}/archetypes/{archetypeUid}/skills/{skillUid}/progress`

Authentication: Optional

Adds the given progress data to the specified skill.

#### Parameters
| Name       |
| ---------- |
| personaUid |

#### Parameters
| Name       |
| ---------- |
| archetypeUid |

#### Parameters
| Name       |
| ---------- |
| skillUid |

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
POST /personas/{personaUid}/archetypes/{archetypeUid}/skills/{skillUid}/progress
Content-Type: application/json

{}
```

#### Response
```http
204 NO CONTENT
```

### FindAll
`GET /personas/{personaUid}/skills`

Authentication: Optional

Returns progress data for all skills that the given persona has started or completed.

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
GET /personas/{personaUid}/skills
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Count
`GET /personas/{personaUid}/skills/count`

Authentication: Optional

Returns the count of skills that a persona has in progress or has completed.

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
GET /personas/{personaUid}/skills/count
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "count": 0
}
```

