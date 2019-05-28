---
title: "Storage"
date: 2019-05-28T17:01:42-07:00
---

The `asset services` system provides for the storage of file data using a pre-configured storage driver. Storage drivers are available for both local and remote file systems. Any file that is uploaded to the service is stored in the configured storage device and referenced in the `File` resource that is created for it. The service will automatically calculate a SHA 256 hash during upload and properly version the file if the same file is uploaded multiple times.

The supported file storage drivers are:

-   `Local`
-   `Amazon S3`
-   `Azure`
-   `Google Cloud Platform`

## Local

Files can be stored on the local file system using the `LocalStorageDriver` driver. It only takes one required configuration setting which is the `location` to store all the files.

| Name       | Default Value        | Description                                       |
| ---------- | -------------------- | ------------------------------------------------- |
| `driver`   | `LocalStorageDriver` |                                                   |
| `location` | `./files`            | The file system path to store all uploaded files. |

### `config.ts`

```javascript
{
    ...
    file_storage: {
        driver: "LocalStorageDriver",
        location: "./files",
    },
    ...
}
```

## Amazon S3

The system supports storing of files in an Amazon S3 bucket using the `S3StorageDriver` storage driver.

| Name                | Default Value     | Description                                                                                     |
| ------------------- | ----------------- | ----------------------------------------------------------------------------------------------- |
| `driver`            | `S3StorageDriver` |                                                                                                 |
| `location`          | `.`               | The sub-folder within the bucket to store files.                                                |
| `access_key_id`     |                   | The access key id to authenticate with.                                                         |
| `secret_access_key` |                   | The access secret to authenticate with.                                                         |
| `region`            |                   | The name of the AWS region that the S3 bucket resides.                                          |
| `bucket`            |                   | The name of the AWS S3 bucket to upload files to.                                               |
| `cdn_base_url`      |                   | The base URL that will be prepended to the `File` `uri` that can be used to download the asset. |

### `config.ts`

```javascript
{
    ...
    file_storage: {
        driver: "S3StorageDriver",
        location: "",
        access_key_id: "ACCESS_KEY",
        secret_access_key: "ACCESS_SECRET",
        region: "REGION",
        bucket: "BUCKET_NAME",
        cdn_base_url: "CDN_DOMAIN_BASEURL",
    },
    ...
}
```

## Azure

The system supports storing of files on Microsoft's Azure platform using the `AzureStorageDriver` storage driver.

| Name           | Default Value        | Description                                                                                     |
| -------------- | -------------------- | ----------------------------------------------------------------------------------------------- |
| `driver`       | `AzureStorageDriver` |                                                                                                 |
| `location`     | `.`                  | The sub-folder within the container to store files.                                             |
| `account_name` |                      | The Azure access name to authenticate with.                                                     |
| `access_key`   |                      | The access key to authenticate with.                                                            |
| `container`    |                      | The Azure container to upload files to.                                                         |
| `cdn_base_url` |                      | The base URL that will be prepended to the `File` `uri` that can be used to download the asset. |
| `host`         |                      | The Azure host address to use. [Optional]                                                       |

### `config.ts`

```javascript
{
    ...
    file_storage: {
        driver: "AzureStorageDriver",
        account_name: "ACCOUNT_NAME",
        access_key: "ACCOUNT_ACCESS_KEY",
        container: "",
        cdn_base_url: "CDN_DOMAIN_BASEURL",
        host: "AZURE_HOST_ADDRESS", // Optional
    },
    ...
}
```

## Google Cloud Platform

The system supports storing of files in a Google Cloud Platform bucket using the `GoogleStorageDriver` storage driver.

| Name           | Default Value         | Description                                                                                     |
| -------------- | --------------------- | ----------------------------------------------------------------------------------------------- |
| `driver`       | `GoogleStorageDriver` |                                                                                                 |
| `project_id`   |                       | The unique identifier of the Google project associated with the storage bucket.                 |
| `location`     | `.`                   | The sub-folder within the bucket to store files.                                                |
| `bucket`       |                       | The bucket name to store files within.                                                          |
| `key_file`     |                       | The key file to authenticate with.                                                              |
| `cdn_base_url` |                       | The base URL that will be prepended to the `File` `uri` that can be used to download the asset. |

### `config.ts`

```javascript
{
    ...
    file_storage: {
        driver: "GoogleStorageDriver",
        project_id: "PROJECT_ID",
        bucket: "GOOGLE_BUCKET",
        key_file: "KEY_FILE",
        location: "files",
        cdn_base_url: "https://storage.googleapis.com",
    },
    ...
}
```
