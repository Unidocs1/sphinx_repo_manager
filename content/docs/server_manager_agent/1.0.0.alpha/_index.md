---
title: "1.0.0.alpha"
---

Agent process that runs on box to start , stop and update state of servers

# Spawn process

Leverages ServerDownload object from Server_Manager_Services. When spawning process will use the base install directory configuration plus the other items from the ServerDownload.
The Following default parameters will be passed to the process

```
--serverManagerId=<Server Manager Id>
--serverId=<Server Id>
--token=<JWT Token for auth>
--axrApiUrl=<AXR Services base URL>
```

Docker running

```
docker -e AXR_API_URL=https://axr-api-url server_manager_agent:latest
```
