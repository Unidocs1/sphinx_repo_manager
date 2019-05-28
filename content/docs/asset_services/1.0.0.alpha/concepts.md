---
title: "Concepts"
date: 2019-05-28T17:01:42-07:00
---

This systems primary role of responsibility is to manage and serve the binary and text data that makes up a game or product. This can be everything from textures to 3D models, sounds, maps and levels as well as configuration files, scripts and text translations. Each asset stored in the system has a unique name and version associated with it. This record is considered immutable and can never be updated. Using the `PUT` endpoints for an asset will create a new record with a new version of the given data. It may be best to think of the system as a source control like service that is intended to manage data that ships live with your product and allows updates to be published seamlessly.

## File

The `File` is the basic building block for all binary based assets. It maintains the record of a particular file or binary blob of data within the system at a given point in time. File records are considered immutable and cannot be modified once created. the critical aspects of information in the `File` record are the `name`, `sha256sum` and `uri` which tells you how to reference the file (by `name`), the SHA 256 hash that you can use to validate the data hasn't been modified or altered during storage or transfer and the exact location used to retrieve the data.

### Example

An example of a file resource is.

```javascript
{
    "name": "avatar.fbx",
    "dateCreated": "2019-05-28T17:01:42-07:00",
    "dateModified": "2019-05-28T17:01:42-07:00",
    "version": 0,
    "mimetype": "application/octet-stream",
    "sha256sum": "f098273ro2hf39o8yah3oi8yno892fy229o",
    "uri": "https://cdn.yourproduct.com/f098273ro2hf39o8yah3oi8yno892fy229o",
}
```

## MediaAsset

The `MediaAsset` is the meat and bones of the asset system when dealing with binary files and data. `MediaAsset` resources are actually a collection of `File` resource identifiers tagged with a unique `name` and `version` using a map of `files`. This map of files is intended to be localized using IETF BCP 47 region codes for each `File` identifier. This makes it possible to define an abstract asset resource with different media representations within your game or application depending on the region that the user is in.

### Example

For example imagine you need to display the flag for the country of origin of the player. Instead of tracking and managing a separate asset for each country's flag you could have a single `flag` asset that uses the region codes to link to the specific region's flag data.

```javascript
{
    "name": "flag",
    "dateCreated": "2019-05-28T17:01:42-07:00",
    "dateModified": "2019-05-28T17:01:42-07:00",
    "version": 0,
    "files": {
        "en-US": "25587db5-3a0d-4697-b3ef-5bbe29a56dc7",
        "en-UK": "8018b628-0a41-4ba7-b5cb-91d9a8e1ad15",
        "fr-FR": "02676a01-1419-4261-aac0-97305e48b2bc",
        "de-DE": "6dc2766e-5eb1-49ba-92cb-bbcf164c8c21",
        ...
    },
    "description": "The flag of the player's country of origin."
}
```

### Roles

One feature of the `MediaAsset` is the ability to specific a set of `roles`. The `roles` property of `MediaAsset` is used to limit the view of the asset to specific sub-groups of users. When this property is set requests to retrieve `MediaAsset` data will filter out any users that are not included in the list of approved roles. This is useful in protected specific versions of unpublished assets or limiting the view of specific assets from one part of a team to another. It can also be used to manage things like A-B testing so that only one set of users have access to a group of assets while the others do not.

```javascript
{
    "name": "flag",
    ...
    "roles": [
        "group_a",
        "group_b",
        ...
    ]
}
```

## TextAsset

The `TextAsset` is used to manage localized textual information. Similar to the `MediaAsset` each `TextAsset` resource has a unique identifying `name` as well as a map of IETF BCP 47 region codes to the respective textual translation for that particular language and region.

### Example

```javascript
{
    "name": "motd",
    "dateCreated": "2019-05-28T17:01:42-07:00",
    "dateModified": "2019-05-28T17:01:42-07:00",
    "version": 0,
    "text": {
        "en-US": "Hello and welcome!",
        "en-UK": "Cheers and welcome!",
        "fr-FR": "Bonjour et bienvenue!",
        "de-DE": "Hallo und Willkommen!",
        ...
    },
    "description": "Message of the day."
}
```

### Roles

One feature of the `TextAsset` is the ability to specific a set of `roles`. The `roles` property of `TextAsset` is used to limit the view of the asset to specific sub-groups of users. When this property is set requests to retrieve `TextAsset` data will filter out any users that are not included in the list of approved roles. This is useful in protected specific versions of unpublished assets or limiting the view of specific assets from one part of a team to another. It can also be used to manage things like A-B testing so that only one set of users have access to a group of assets while the others do not.

```javascript
{
    "name": "motd",
    ...
    "roles": [
        "group_a",
        "group_b",
        ...
    ]
}
```

## Snapshot

The `Snapshot` resource provides a versioned catalog of assets (both `MediaAsset` and `TextAsset` resources) that can be used to create a singular package with a tagged `version`. The primary purpose of the `Snapshot` is that of a game or application patch. Often times it is desired to roll up many changes of a given product release to be distributed to users. The `Snapshot` is the mechanism for publishing these changes.

```javascript
{
    "name": "1.1.0",
    "assets": [
        "0bcd7d85-3bf3-41a0-b46c-657e560bab3a",
        ...
    ],
    "description": "All assets for the 1.1.0 release.",
    "environment": "production",
    "notes": "What's changed in this release..."
}
```
