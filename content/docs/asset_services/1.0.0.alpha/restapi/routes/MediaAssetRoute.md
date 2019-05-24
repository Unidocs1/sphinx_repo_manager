---
title: "MediaAsset Routes"
date: 2019-05-24T20:03:25.798Z
---



## Routes

### FindAll
`GET /assets/media`

Authentication: **Required**

Returns all assets from the system that the user has access to

#### Request
```http
GET /assets/media
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /assets/media`

Authentication: **Required**

Create a new media assist

#### Request
```http
POST /assets/media
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "files": {
        "default": {
            "mimetype": "image/jpeg",
            "name": "beer2.jpg",
            "sha256sum": "30156ccd7935729edfac7882d317f64ef0ed57bb24b6f416e1a7592ff576450c",
            "uri": "https://storage.googleapis.com/assets.slendargame.com/files/c213f4b65bc856efc1f6c03a7d3d2425",
            "uid": "476da6b2-0eea-4a79-8c36-cac6d6d3a486",
            "dateCreated": "2018-07-16T04:10:04.993Z",
            "dateModified": "2018-07-16T04:10:04.997Z",
            "version": 0
        }
    },
    "description": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "ce9135c1-ea4a-41ea-a2df-6b245386f61c",
    "dateCreated": "2019-05-24T20:03:30.569Z",
    "dateModified": "2019-05-24T20:03:30.569Z",
    "version": 0,
    "name": "string",
    "files": {
        "default": {
            "mimetype": "image/jpeg",
            "name": "beer2.jpg",
            "sha256sum": "30156ccd7935729edfac7882d317f64ef0ed57bb24b6f416e1a7592ff576450c",
            "uri": "https://storage.googleapis.com/assets.slendargame.com/files/c213f4b65bc856efc1f6c03a7d3d2425",
            "uid": "476da6b2-0eea-4a79-8c36-cac6d6d3a486",
            "dateCreated": "2018-07-16T04:10:04.993Z",
            "dateModified": "2018-07-16T04:10:04.997Z",
            "version": 0
        }
    },
    "description": "string"
}
```

### Count
`GET /assets/media/count`

Authentication: **Required**

Returns the count of media assets

#### Request
```http
GET /assets/media/count
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
`GET /assets/media/{id}`

Authentication: **Required**

Returns a single media asset from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /assets/media/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "c238b16a-65e7-4b5d-8f37-76897f862b15",
    "dateCreated": "2019-05-24T20:03:30.571Z",
    "dateModified": "2019-05-24T20:03:30.571Z",
    "version": 0,
    "name": "string",
    "files": {
        "default": {
            "mimetype": "image/jpeg",
            "name": "beer2.jpg",
            "sha256sum": "30156ccd7935729edfac7882d317f64ef0ed57bb24b6f416e1a7592ff576450c",
            "uri": "https://storage.googleapis.com/assets.slendargame.com/files/c213f4b65bc856efc1f6c03a7d3d2425",
            "uid": "476da6b2-0eea-4a79-8c36-cac6d6d3a486",
            "dateCreated": "2018-07-16T04:10:04.993Z",
            "dateModified": "2018-07-16T04:10:04.997Z",
            "version": 0
        }
    },
    "description": "string"
}
```

### Update
`PUT /assets/media/{id}`

Authentication: **Required**

Updates a single media asset

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /assets/media/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "files": {
        "default": {
            "mimetype": "image/jpeg",
            "name": "beer2.jpg",
            "sha256sum": "30156ccd7935729edfac7882d317f64ef0ed57bb24b6f416e1a7592ff576450c",
            "uri": "https://storage.googleapis.com/assets.slendargame.com/files/c213f4b65bc856efc1f6c03a7d3d2425",
            "uid": "476da6b2-0eea-4a79-8c36-cac6d6d3a486",
            "dateCreated": "2018-07-16T04:10:04.993Z",
            "dateModified": "2018-07-16T04:10:04.997Z",
            "version": 0
        }
    },
    "description": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "fe0f4605-7884-4ea3-a59a-f6e5616ca269",
    "dateCreated": "2019-05-24T20:03:30.572Z",
    "dateModified": "2019-05-24T20:03:30.572Z",
    "version": 0,
    "name": "string",
    "files": {
        "default": {
            "mimetype": "image/jpeg",
            "name": "beer2.jpg",
            "sha256sum": "30156ccd7935729edfac7882d317f64ef0ed57bb24b6f416e1a7592ff576450c",
            "uri": "https://storage.googleapis.com/assets.slendargame.com/files/c213f4b65bc856efc1f6c03a7d3d2425",
            "uid": "476da6b2-0eea-4a79-8c36-cac6d6d3a486",
            "dateCreated": "2018-07-16T04:10:04.993Z",
            "dateModified": "2018-07-16T04:10:04.997Z",
            "version": 0
        }
    },
    "description": "string"
}
```

### Delete
`DELETE /assets/media/{id}`

Authentication: **Required**

Deletes the media asset

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /assets/media/{id}
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

