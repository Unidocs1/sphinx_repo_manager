---
title: "AuthTwitter Routes"
date: 2019-03-18T05:50:55.822Z
chapter: true
---



## Routes

### Authenticate
`GET /auth/twitter`

Authentication: **Required**

Authenticates the user using a provided Twitter access token and returns a JSON Web Token access token to be used with future API requests.

#### Request
```http
GET /auth/twitter
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

### AuthenticateReverse
`GET /auth/twitter/reverse`

Authentication: Optional

Retrieves a request token to use for Twitter authentication.

#### Request
```http
GET /auth/twitter/reverse
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

