---
title: "File Routes"
date: 2019-05-24T20:03:25.798Z
---



## Routes

### FindAll
`GET /files`

Authentication: **Required**

Returns all files from the system that the user has access to based upon the given criteria.

#### Request
```http
GET /files
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /files`

Authentication: **Required**

Create a new file.

#### Request
```http
POST /files
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "sha256sum": "string",
    "uri": "string",
    "mimetype": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "62e8e331-02cd-4b6b-be7a-63f722536ebd",
    "dateCreated": "2019-05-24T20:03:30.561Z",
    "dateModified": "2019-05-24T20:03:30.561Z",
    "version": 0,
    "name": "string",
    "sha256sum": "string",
    "uri": "string",
    "mimetype": "string"
}
```

### Count
`GET /files/count`

Authentication: **Required**

Returns the count of files matching the given criteria.

#### Request
```http
GET /files/count
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
`GET /files/{id}`

Authentication: **Required**

Returns file from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /files/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "ad8d9e9b-3143-4f18-aea6-e8c21d11a441",
    "dateCreated": "2019-05-24T20:03:30.563Z",
    "dateModified": "2019-05-24T20:03:30.563Z",
    "version": 0,
    "name": "string",
    "sha256sum": "string",
    "uri": "string",
    "mimetype": "string"
}
```

### DownloadFile
`GET /files/{id}/download`

Authentication: **Required**

Returns the contents of the file with the given id.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /files/{id}/download
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: */*
```

### ProcessUploads
`POST /upload`

Authentication: **Required**

Uploads multiple files storing each stream into a configured storage device and returns the resulting metadata.

#### Request
```http
POST /upload
Content-Type: multipart/form-data
Authorization: jwt <token>

{}
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

