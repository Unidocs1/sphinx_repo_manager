---
title: "AuthGoogle Routes"
date: 2019-03-18T21:15:14.179Z
chapter: true
---



## Routes

### Authenticate
`GET /auth/google`

Authentication: **Required**

Authenticates the user using a provided Google access token and returns a JSON Web Token access token to be used with future API requests.

#### Request
```http
GET /auth/google
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

