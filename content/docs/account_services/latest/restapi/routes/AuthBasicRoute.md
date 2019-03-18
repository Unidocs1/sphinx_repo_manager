---
title: "AuthBasic Routes"
date: 2019-03-18T21:15:14.179Z
chapter: true
---



## Routes

### Authenticate
`GET /auth/password`

Authentication: **Required**

Authenticates the user using HTTP Basic and returns a JSON Web Token access token to be used with future API requests.

#### Request
```http
GET /auth/password
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "token": "string"
}
```

