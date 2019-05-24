---
title: "1.0.0.alpha"
---

This project provides user account management and authentication services.

Supported authentication methods are:

<ul>
    <li>HTTP Basic<li>
    <li>JSON Web Token</li>
    <li>Facebook</li>
    <li>Twitter</li>
    <li>Google</li>
</ul>

## Getting Started

To get started using this service first clone the source. It is highly recommended that you fork the project first.

```bash
$ git clone https://gitlab.com/AcceleratXR/Core/account_services.git
```

Once cloned you can begin customizing the various data model schema and adding additional code to the various processor functions.

## Data Model

The service has defined schema for the data models `User`, `Role` and `UserSecret`.

For the latest documentation view the [API docs](restapi/models/).

### User

The `User` model defines all data associated with a single individual or user of the platform. It potentially contains personally identifiable information such as name, e-mail and phone number. Note that passwords are **not** defined in this data structure. This is to separate and protect authentication data from user data for improved security.

For the latest documentation of this data model view the [API docs](restapi/models/user).

#### Default `admin` User

By default a single user named `admin` is created when the service first starts up with full administrative privileges. The properties (including name) of the default admin user can be configured by editing `adminUser` in the `config.js` file.

A default password is also created for this user. It is configured by editing the `adminUser:password` property in the `config.js` file. The service will create a new `UserSecret` object containing this password for the admin user. See `UserSecret` for more details on implementation.

#### Creating Users

When a new user account is created with the service, a `User` object is returned as well as a JSON Web Token (JWT) token. The JWT token is necessary in order to be able to create a `UserSecret` with an associated password (or other supported secret) immediately after user creation. If a `UserSecret` is not created following the creation of the user it will not be possible to authenticate ther user in the future.

### Role

A role is a collection of users for the purpose of organization and providing privileged access. Privileged access is control exclusively by implementing processing logic that searches for a given role associated with a user.

For the latest documentation of this data model view the [API docs](restapi/models/role).

### Default `admin` Role

By default a single role named `admin` is created when the service first starts up. It is intended that any user which is a member of this role has full administrative privileges to the platform. The properties (including name) of the default admin role can be configured by editing `adminRole` in the `config.js` file.

**NOTE**: Only members of this role can create new roles.

### UserSecret

The `UserSecret` schema defines how passwords and other authentication methods are stored for a given user. These are stored in isolation to the user itself in order to improve the security of the service as well as further protect and isolate personally identifying information (PII) of the user.

The schema has three important defined properties. These are `userId`, `type` and `secret`. Together these define a single method of authentication for a given user. Note that no restriction is made on the number of `UserSecret` entries in the database for any given combination of `userId` and `type`. Whenever more than one UserSecret exists for a given combination of `userId` and `type` the service will attempt to authenticate each until a match is found.

There are four different types of secrets that are supported.

-   `apikey` - An special alpha-numeric plan text secret used by other applications and services.
-   `device` - A deterministic unique device hash or password used for frictionless device login.
-   `mfa` - A multi-factor authentication token used to strengthen the security of existing secrets. There can only be one secret of this type per user.
-   `password` - A simple alpha-numeric plain text password. There can only one secret of this type per user.

For the latest documentation of this data model view the [API docs](restapi/models/usersecret).

#### API Key [`apikey`]

The API key secret type is used to provide external applications and services with access to a given user account. There is no limit to the number of secrets associated with a user account of this type. When creating an API key secret the service will either accept a pre-determined key as provided in the create request or will generate a random key if no value for secret is given. The create request will return the generated key in the response and will never be visible again. Updates to an api key secret are not possible.

#### Device [`device`]

A Device secret is intended to be used for frictionless device authentication. Unlike the API key type the client must provide a value for `secret` when the type is set to `device`. The value used must conform to the `password` requirements that have been configured for the service. It is recommended that a determistic value be chosen for this secret that can be generated by the originating device at each application start. An example is to use a hash of the device's universally unique identifier (e.g. IMEI).

An unlimited number of `device` secrets may be created for a single user account.

#### Multi-Factor Authentication [`mfa`]

Multi-factor authentication (aka: Two-Step Authentication or 2FA) is also supported by specifying the `mfa` secret type. Only one secret of type `mfa` may be created for a given user account. When sending a create request no `secret` value is required as the service will automatically generate the secret for the user. The response to the create request will contain the generated MFA secret and will never be visible again. Updates to the secret are not allowed.

See [Multi-factor Authentication](#Multi-factor Authentication) for more information.

#### Password [`password`]

The `password` secret type is a standard plain text alpha-numeric password that a user can use to authenticate their self with. There can only be one secret of type `password` for any given user account. The value of `secret` must be provided by a client when a create request is made. The value of `secret` will never be returned in a response.

## Authentication

Authentication is provided with a variety of schemes allowing maximum flexibility for users and developers alike. Out of the box, the service can support authentication with the following methods.

-   JSON Web Token (JWT)
-   API Key
-   Device login
-   Multi-factor Authentication (MFA / 2FA / TOTP)
-   Password
-   Single Sign-On
    -   Facebook
    -   Twitter
    -   Google

All successful authentication requests to the service will return a JSON Web Token (JWT). This token can be saved as a cookie or stored in program memory to authenticate all future requests to the service and other platform compatible services.

The payload of the JWT token when decrypted by another service contains a `User` object containing the following properties.

<table>
    <thead>
        <tr>
            <td>Name</td>
            <td>Type</td>
            <td>Description</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>`uid`</td>
            <td>`UUID`</td>
            <td>The universally unique identifier (UUID) of the user</td>
        </tr>
        <tr>
            <td>`name`</td>
            <td>`string`</td>
            <td>The unique identifying name of the user.</td>
        </tr>
        <tr>
            <td>`email`</td>
            <td>`string`</td>
            <td>The e-mail address that is registered to the user account. Check the verified property to ensure that the e-mail has been verified as valid.</td>
        </tr>
        <tr>
            <td>`roles`</td>
            <td>`array[string]`</td>
            <td>An array of unique role names indicating a set of privileges that the user has</td>
        </tr>
        <tr>
            <td>`externalIds`</td>
            <td>`array[string]`</td>
            <td>An array of external provider and unique identifier pairs that the user has linked to their account. External providers are commonly third-party sign on services such as Facebook, Twitter, Google, PSN, Xbox LIVE. The values are stored as a `:` separated pair (e.g. `facebook:92rj23098f203r209823`) with the first part of the pair denoting a unique provider name and the second part being the provider's unique identifier for the user. <p>Supported providers are:</p><ul><li>`facebook`</li><li>`twitter`</li><li>`google`</li></ul></td>
        </tr>
        <tr>
            <td>`verified`</td>
            <td>`boolean`</td>
            <td>Indicates if ther user's identity has been confirmed. Identity confirmation means that their provided e-mail address or phone number is valid.</td>
        </tr>
    </tbody>
</table>

### Schemes

The service supports a variety of authentication schemes including password, JSON Web Token, and OAuth compatible single-sign on such as Facebook, Twitter and Google.

#### API Key

The API key is a special kind of password that can be generated by the service and used by external applications and services in order to perform operations on behalf of a user. It is stored the same way as a password is stored using a one-way hash. Upon initial creation the value is returned in the HTTP response and will never be exposed again.

To create a new API key send a `POST` request to `/users/{uid}/secrets` containing a `UserSecret` object with the type `apikey`.

```txt
POST /users/00000000-0000-0000-0000-00000000001/secrets
Authorization: JWT jfo2389fh2iouf982fj3iu2f893y82fh23uf782h3i2hf27nf8o73h28f23un78932h3f32unh3789fhn
Content-Type: application/json
Content-Length: 124

{
    "userId": "00000000-0000-0000-0000-00000000001",
    "type": "apikey",
    "description": "My API key for application X"
}
```

The service will then generate a new value for the secret and return it in a response with status `200 OK`.

```txt
200 OK
Content-Type: application/json
Content-Length: 345

{
    "userId": "00000000-0000-0000-0000-00000000001",
    "type": "apikey",
    "secret": "ALKF83290F8DAFKLJAF",
    "description": "My API key for application X"
}
```

Now that an API key is created authentication can be accomplished using the standard `/auth/password` endpoint. This endpoint is compatible with HTTP BASIC authentication and requires the Authorization header be set.

```txt
GET /auth/password
Authorization: Basic MDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDE6QUxLRjgzMjkwRjhEQUZLTEpBRg==
```

A successful authentication will return a `200 OK` result containing a JWT token for use in all future requests.

```txt
200 OK
Content-Type: application/json
Content-Length: 259

{
    "token": "f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh"
}
```

#### Device

Device authentiation is an important feature that enables frictionless user experiences. With device authentication a unique determistic hash is used as the password for each device that is to be authenticated for the user automatically. The service supports any number of device secrets to be created but these secrets cannot be updated. It is also important to make sure that whatever unique hash is used for a given device that it not change or else you risk losing access to the account in question. Like API keys the device secret is stored in the database using a one-way hash as a security measure.

**WARNING**: When using device based authentication it is always recommended that the user register an `email` address as well as create a secret of type `password` in order to ensure an account can always be recovered.

To create a new API key send a `POST` request to `/users/{uid}/secrets` containing a `UserSecret` object with the type `device` and the unique device hash.

```txt
POST /users/00000000-0000-0000-0000-00000000001/secrets
Authorization: JWT jfo2389fh2iouf982fj3iu2f893y82fh23uf782h3i2hf27nf8o73h28f23un78932h3f32unh3789fhn
Content-Type: application/json
Content-Length: 124

{
    "userId": "00000000-0000-0000-0000-00000000001",
    "type": "device",
    "secret": "f0987f0oj32of8902jfo23fu09q8fjof2up0f92n309v87fn2pq9f8vuq298vfuqn32pf3q2v2q3f",
    "description": "Device Name"
}
```

The service will then return the newly created secret in a response with status `200 OK` with the `secret` field ommitted.

```txt
200 OK
Content-Type: application/json
Content-Length: 345

{
    "userId": "00000000-0000-0000-0000-00000000001",
    "type": "device",
    "description": "Device Name"
}
```

Now authentication can be accomplished using the standard `/auth/password` endpoint. This endpoint is compatible with HTTP BASIC authentication and requires the Authorization header be set.

```txt
GET /auth/password
Authorization: Basic MDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDE6ZjA5ODdmMG9qMzJvZjg5MDJqZm8yM2Z1MDlxOGZqb2YydXAwZjkybjMwOXY4N2ZuMnBxOWY4dnVxMjk4dmZ1cW4zMnBmM3EydjJxM2Y=
```

A successful authentication will return a `200 OK` result containing a JWT token for use in all future requests.

```txt
200 OK
Content-Type: application/json
Content-Length: 259

{
    "token": "f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh"
}
```

#### Password

A password is a simple text string that the user provides and is compared to the one stored in the database. Passwords are always encrypted using a one-way hash in the database in the event that access to the database is compromised. Passwords are also never transmitted back to a client upon request even if the requesting user is the owner.

To create a new password for a user simply send a `POST` request to `/users/{uid}/secrets` containing a `UserSecret` object with the type `password`.

```txt
POST /users/00000000-0000-0000-0000-00000000001/secrets
Authorization: JWT jfo2389fh2iouf982fj3iu2f893y82fh23uf782h3i2hf27nf8o73h28f23un78932h3f32unh3789fhn
Content-Type: application/json
Content-Length: 124

{
    "userId": "00000000-0000-0000-0000-00000000001",
    "type": "password",
    "secret": "MyP@ssw0rd!"
}
```

The response of the create request will be a copy of the secret as it was stored in the database with the value for secret ommitted.

```txt
200 OK
Content-Type: application/json
Content-Length: 89

{
    "userId": "00000000-0000-0000-0000-00000000001",
    "type": "password",
}
```

Once the password is created, it is easy to authenticate the user using the `/auth/password` endpoint. This endpoint is compatible with HTTP BASIC authentication and requires the Authorization header be set.

```txt
GET /auth/password
Authorization: Basic f982ufo2ijf2938uf2ofi98fj2oifj3298fj2fj3938fuj2o9ifj3o2jf32=
```

A successful authentication will return a `200 OK` result containing a JWT token for use in all future requests.

```txt
200 OK
Content-Type: application/json
Content-Length: 259

{
    "token": "f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh"
}
```

#### Multi-Factor Authentication (MFA / 2FA / TOTP)

The service also has support for Multi-factor authentication (aka: Two-Step Authentication). Enabling MFA for an account is a great way to strengthen the security of authentication. Only one `mfa` secret can be created for a given user account and it can never be updated. The underlying value of the secret is always generated by the service itself and is returned in the initial create response exactly once.

To enable MFA for a given user account send a `POST` request to `/users/{uid}/secrets` containing a `UserSecret` object with the type `mfa`.

```txt
POST /users/00000000-0000-0000-0000-00000000001/secrets
Authorization: JWT jfo2389fh2iouf982fj3iu2f893y82fh23uf782h3i2hf27nf8o73h28f23un78932h3f32unh3789fhn
Content-Type: application/json
Content-Length: 124

{
    "userId": "00000000-0000-0000-0000-00000000001",
    "type": "mfa",
    "description": "My MFA secret"
}
```

The service will generate an MFA secret and return a copy of the `UserSecret` object as it was stored in the database. The `secret` field will contain a URL that can be converted into a QR code or entered into any MFA compatible application as well as the secret itself to be used to generate valid MFA tokens.

```txt
200 OK
Content-Type: application/json
Content-Length: 89

{
    "userId": "00000000-0000-0000-0000-00000000001",
    "type": "mfa",
    "description": "My MFA secret",
    "secret": {
        "otpauth_url": "otpauth://totp/AcceleratXR%20(User76.21864902464002)?secret=OFEFUI2UOJ4WCI2IJUUXUMBENM4WGJDPNN2W65L2I5THITRZH4YHQKTHPNUHORJVHRHTGSRWIVBFMOD5FJXXI53XKZCUMSSFKQ4XSVA",
        "secret": "OFEFUI2UOJ4WCI2IJUUXUMBENM4WGJDPNN2W65L2I5THITRZH4YHQKTHPNUHORJVHRHTGSRWIVBFMOD5FJXXI53XKZCUMSSFKQ4XSVA"
    }
}
```

To complete the MFA enrollment process it is required to send a `PUT` request to the `/users/{userUid}/secrets/{secretUid}/enroll` endpoint with a content body containing a valid MFA token.

```txt
PUT /users/00000000-0000-0000-0000-00000000001/secrets/00000000-0000-0000-0000-00000000025/enroll
Authorization: JWT jfo2389fh2iouf982fj3iu2f893y82fh23uf782h3i2hf27nf8o73h28f23un78932h3f32unh3789fhn
Content-Type: application/json
Content-Length: 124

{
    "token": "123456"
}
```

If the provided MFA token is valid a `200 OK` status is returned and enrollment will be complete. All subsequent `password` login attempts will require MFA authentication. Once MFA is enabled the flow of login changes slightly. Clients still must make a call to the `/auth/password` endpoint but instead of receiving a valid JWT token in response a `302 REDIRECT` status is returned with the `location` header containing the endpoint of the MFA challenge.

```txt
GET /auth/password
Authorization: Basic f982ufo2ijf2938uf2ofi98fj2oifj3298fj2fj3938fuj2o9ifj3o2jf32=
```

A successful authentication will return a `302 REDIRECT` result with the `location` header set to the MFA challenge endpoint.

```txt
302 REDIRECT
Location: /auth/totp?jwt_token=f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh
```

Notice that the redirect URL contains a JWT token as a query parameter. This is a special JWT token with a very short lifespan (approximately 3 minutes) whose user data has been stripped to remove any privileges or PII. This is important as it reduces the potential for an attacker to hijack of the temporary token for malicious purposes when an account has been compromised. At this point the client must send a `POST` request to the redirect URL containing a valid MFA token in order to receive the final JWT token.

```txt
POST /auth/totp?jwt_token=f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh
Content-Type: application/json
Content-Length: 57

{
    "token": "123456"
}
```

The MFA token will then be validated and the service will return a `200 OK` result containing the final JWT token for use in all future requests.

```txt
200 OK
Content-Type: application/json
Content-Length: 259

{
    "token": "f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh"
}
```

#### Single-Sign On

##### Facebook

Authentication via Facebook Login is supported using the `/auth/facebook` endpoint. As Facebook sign-in is based upon the OAuth 2.0 standard it is not necessary to create a `UserSecret` record for a user account.

Some configuration is required to get Facebook Login working for your project. An `appID` and `secret` is required and must be set in the `facebook` section of the `config.js` file.

```javascript
"facebook": {
    "appID": "YOUR_APP_ID",
    "secret": "YOUR_APP_SECRET"
},
```

Once configured a client can send a `GET` request to the `/auth/facebook` endpoint providing an OAuth access token and refresh token as query parameters. Obtaining an access token is considered out of scope of this document. Please consult the Facebook documentation for further details.

```txt
GET /auth/facebook?oauth_token=937f23ijf92f32j2293...&oauth_refresh=098f23ojif98fu2f329...
```

A successful authentication will return a `200 OK` result containing a JWT token for use in all future requests.

```txt
200 OK
Content-Type: application/json
Content-Length: 259

{
    "token": "f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh"
}
```

If a user account doesn't exist for the authenticated Facebook user the service will automatically create one with the profile information provided by Facebook. Note that the profile must contain at least one e-mail address. Therefore it is important to ensure that the `email` scope is used when requesting the access token from Facebook's authentication service.

The service will first attempt to find an existing user account using the Facebook user id. If not found, the service will search for an existing user with the same e-mail address. If neither can be found a new user is created.

It is also possible to link a Facebook Login to an existing user account not previously associated with Facebook. This is accomplished by providing a valid JWT token along with the Facebook access token.

```txt
GET /auth/facebook?oauth_token=937f23ijf92f32j2293...&oauth_refresh=098f23ojif98fu2f329...
Authorization: JWT f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh
```

When provided a valid JWT token for an existing user, the service will link the authenticated Facebook user to the existing user and a new JWT token will be returned upon success. If the Facebook user was associated previously with a different account than the one specified by the JWT token then the previous link will be removed and the most recently authenticated user will gain the link.

##### Twitter

Twitter uses the OAuth 1.0 authentication scheme. This is supported by the service using the `/auth/twitter` and `/auth/twitter/reverse` endpoints.

Similar to other OAuth based authentication schemes some configuration is required. A `consumerKey` and `consumerSecret` is required to set in the `twitter` section of the `config.js` configuration file.

```javascript
"twitter": {
    "consumerKey": "CONSUMER_KEY",
    "consumerSecret": "CONSUMER_SECRET"
},
```

To authentication with Twitter it is first necessary to retrievea a request token from the service. This is done by performing a `GET` request to the `/auth/twitter/reverse` endpoint.

```txt
GET /auth/twitter/reverse
```

Upon success this will return a `200 OK` response containing the request token to pass on to Twitter's authentication service.

```
200 OK
Content-Type: application/json
Content-Length: 243

{ ... }
```

Using the request token the user must then be redirected to Twitter to obtain an OAuth access token. The details of obtaining an access token are considered out of scope for this document.

Once an OAuth access token is obtain from Twitter the client performs a `GET` request to the `/auth/twitter` endpoint, providing the access token as a query parameter.

```txt
GET /auth/twitter?oauth_token=937f23ijf92f32j2293...&oauth_refresh=098f23ojif98fu2f329...
```

A successful authentication will return a `200 OK` result containing a JWT token for use in all future requests.

```txt
200 OK
Content-Type: application/json
Content-Length: 259

{
    "token": "f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh"
}
```

If a user account doesn't exist for the authenticated Twitter user the service will automatically create one with the profile information provided by Twitter. Note that the profile must contain at least one e-mail address. Therefore it is important to ensure that the `email` scope is used when requesting the access token from Twitter's authentication service.

The service will first attempt to find an existing user account using the Twitter user id. If not found, the service will search for an existing user with the same e-mail address. If neither can be found a new user is created.

It is also possible to link a Twitter Login to an existing user account not previously associated with Google. This is accomplished by providing a valid JWT token along with the Twitter access token.

```txt
GET /auth/twitter?oauth_token=937f23ijf92f32j2293...&oauth_refresh=098f23ojif98fu2f329...
Authorization: JWT f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh
```

When provided a valid JWT token for an existing user, the service will link the authenticated Twitter user to the existing user and a new JWT token will be returned upon success. If the Twitter user was associated previously with a different account than the one specified by the JWT token then the previous link will be removed and the most recently authenticated user will gain the link.

##### Google

Authentication via Google Login is supported using the `/auth/google` endpoint. As Google sign-in is based upon the OAuth 2.0 standard it is not necessary to create a `UserSecret` record for a user account.

Some configuration is required to get Google Login working for your project. A `clientID` and `clientSecret` is required and must be set in the `google` section of the `config.js` file.

```javascript
"google": {
    "clientID": "myclientid.apps.googleusercontent.com",
    "clientSecret": "MY_CLIENT_SECRET"
},
```

Once configured a client can send a `GET` request to the `/auth/google` endpoint providing an OAuth access token and refresh token as query parameters. Obtaining an access token is considered out of scope of this document. Please consult the Google documentation for further details.

```txt
GET /auth/google?oauth_token=937f23ijf92f32j2293...&oauth_refresh=098f23ojif98fu2f329...
```

A successful authentication will return a `200 OK` result containing a JWT token for use in all future requests.

```txt
200 OK
Content-Type: application/json
Content-Length: 259

{
    "token": "f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh"
}
```

If a user account doesn't exist for the authenticated Google user the service will automatically create one with the profile information provided by Google. Note that the profile must contain at least one e-mail address. Therefore it is important to ensure that the `email` scope is used when requesting the access token from Google's authentication service.

The service will first attempt to find an existing user account using the Google user id. If not found, the service will search for an existing user with the same e-mail address. If neither can be found a new user is created.

It is also possible to link a Google Login to an existing user account not previously associated with Google. This is accomplished by providing a valid JWT token along with the Google access token.

```txt
GET /auth/google?oauth_token=937f23ijf92f32j2293...&oauth_refresh=098f23ojif98fu2f329...
Authorization: JWT f982uf3oj9ojf3oaw8jf92jn3iojf98i32jf98hjFUuihf298hfihFJKWEHFIwh
```

.
When provided a valid JWT token for an existing user, the service will link the authenticated Google user to the existing user and a new JWT token will be returned upon success. If the Google user was associated previously with a different account than the one specified by the JWT token then the previous link will be removed and the most recently authenticated user will gain the link.

## Authentication from a Trusted Service

It may be necessary to request data from another trusted service. While it is possible to have each service create their own user record and associated passwords on service startup it is much simpler to have the service generate a valid JWT token used for authentication with the required identity information.

In order to generate a proper JWT token the service must first create the user object that will be used to verify permissions and identity. The minimum information necessary for a valid user object is the `uid` and `groups` properties.

```javascript
const serviceUser = {
    uid: "00000000-0000-0000-0000-000000000000",
    groups: ["admin"],
};
```

Once the user object is created the next step is to generate the JWT token, using the user object as the payload.

```javascript
const jwt = require("jsonwebtoken");
var token = jwt.sign({ profile: serviceUser.toJSON() }, "PRIVATE_KEY", {
    expiresIn: "7 days",
    audience: "mydomain.com",
    issuer: "api.mydomain.com",
});
```

Now that you have a proper authentication token it can be attached to any API request. See the [Security](/docs/security) chapter for more information on how to attach the token to requests.

## Recovering Account Access

It happens all the time. People forget their password or are unable to login via the other supported providers for various reasons. To address this problem a special `/users/{id}/recover` endpoint is provided by the service allowing users to reset access to their account.

To reset access to an account the client sends a `GET` request to the `/users/{id}/recover` endpoint. The `id` parameter can be any valid unique identifier for the user account such as `uid`, `name`, `email` or even `phone`.

```txt
GET /users/mrsmith/reset
```

The service will then send an e-mail to the registered e-mail address of the user account in question containing a link allowing the user to set a new password for their account. The link will contain a valid JWT token for the user to authenticate with.

The contents of the e-mail can be configured in the `auth:recovery` section of the `config.ts` configuration file.

## REST API

To view the latest REST API documentation view the [API Docs](restapi/).
