---
title: "1.0.0.alpha"
date: 2019-07-12T00:24:32.539Z
---

Provides server side in-app purchase validation for various storefronts such as Apple Store and Google Play.

## Premium Feature

Note that this is a premium feature and is only available to AcceleratXR Self-Hosted and Managed Services customers.

## Getting Started

To get started using this service first clone the source. It is highly recommended that you fork the project first.

```bash
git clone https://gitlab.com/AcceleratXR/acceleratxr-premium/validation_services.git
```

## Running the Service

Open up a new shell to the cloned folder and build the Docker image using `docker-compose`.

```bash
docker-compose build
```

You can now run the server with the following command.

```bash
docker-compose up
```

## Debugging

[Visual Studio Code](https://code.visualstudio.com/) is the recommended IDE to develop with. The project includes workspace and launch configuration files out of the box.

To debug while running via Docker Compose select the `Docker: Attach Debugger` configuration and hit the `F5` key. If you want to run the server directly and debug choose the `Launch Server` configuration.

## Validating Purchases

The service supports validating in-app product purchases for a variety of digital store fronts.

-   Apple Store [iOS / Mac]
-   Google Play [Android / Chrome]

## Apple Store

To validate an in-app purchase a `POST` request is sent to the `/validate/apple` endpoint with the following request body.

A valid request will look like the following...

```
POST /validate/apple HTTP/1.1
Content-Type: application/json
Content-Length: 153
Authorization: jwt 0f97823p9fuqp9nvf79p8f7.f90237vf289qf73q.29v0r7fq329b8789q27f3q97q29f7q327329329f7329

{
    "receipt": "BASE64_ENCODED_RECEIPT_PROVIDED_BY_APPLE"
```

If the purchase was validated successfully the service will return a `200 OK` or `204 NO CONTENT` response containing no content. If the purchase was invalid or the service was unable to successfully communicate with the Google Play store a `400 BAD REQUEST` response is returned.

## Google Play

### Creating a Service Account

Before you can validate purchases with the Google Play store it is necessary to setup a Service Account that will allow the service to perform server-to-server authentication.

1. From the [Google Developers Console](https://cloud.google.com/console), select your project or create a new one.
2. Under "APIs & auth", click "Credentials".
3. Under "OAuth", click the "Create new client ID" button.
4. Select "Service account" as the application type and click "Create Client ID".
5. The key for your new service account should prompt for download automatically. Note that your key is protected with a password. IMPORTANT: keep a secure copy of the key, as Google keeps only the public key.

6. Convert the downloaded key to PEM, so we can use it from the Node crypto module.

    To do this, run the following in Terminal:

    `openssl pkcs12 -in downloaded-key-file.p12 -out your-key-file.pem -nodes`

    You will be asked for the password you received during step 5.

### Service Configuration

Once you have created your service account and obtained the necessary key file place key file somewhere in this folder's directory and then edit the `src/config.ts` file with the necessary information as follows.

```
    ...
    google: {
        ...
        jwt: {
            email: "<serviceaccountemail>",
            keyFile: "/path/to/key.pem",
        },
    },
```

### Performing Purchase Validation

To validate an in-app purchase a `POST` request is sent to the `/validate/google` endpoint with the following request body.

A valid request will look like the following...

```
POST /validate/google HTTP/1.1
Content-Type: application/json
Content-Length: 153
Authorization: jwt 0f97823p9fuqp9nvf79p8f7.f90237vf289qf73q.29v0r7fq329b8789q27f3q97q29f7q327329329f7329

{
    "packageName": "com.yourcompany.appName",
    "productId": "YOUR_PRODUCT_ID",
    "token": "TOKEN_PROVIDED_BY_GOOGLE",
    "type": "product"
}
```

If the purchase was validated successfully the service will return a `200 OK` or `204 NO CONTENT` response containing no content. If the purchase was invalid or the service was unable to successfully communicate with the Google Play store a `400 BAD REQUEST` response is returned.
