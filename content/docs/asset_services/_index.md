---
title: "Asset Services"
date: 2019-07-05T22:50:13.161Z
weight: 13
---

The `asset services` system provides for the management of versioned file, binary data and text assets as well as the localization of those assets. Individual assets are identified with a unique name (or key) and a particular version that maps to a set of localized files or text based upon IETF BCP 47 region codes. The system primarily manages metadata as is not directly intended as a storage system. The system is designed to work with both local and remote file storage systems in order to provide a simple solution for the total management of assets. As a result, as a developer you can deploy this service into a cluster and upload any number of asset files desired and it will be stored on the configured storage device. You can also use the system as purely a metadata manager and only create asset resources that link to another storage medium (e.g. physical disc).
