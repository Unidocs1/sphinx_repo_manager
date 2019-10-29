---
title: "Architecture"
date: 2019-10-28T17:42:16.105Z
---

The architecture used by Leaderboard Services is similar to that of other AcceleratXR services with one notibeable difference. The `LeaderboardRecord` data is stored in two places. First, records are inserted into a `MongoDB` database collection and serves as the principle long term storage for archival. The data is also copied to a `redis` database which provides the required fast and efficient sorting and retrieval of data set. Each record that is submitted to the service will be stored in both `MongoDB` and `redis` databases simultaneously. The record data stored in `redis` is stored in a `Sorted Set`. This Sorted Set handles global ranking calculation. When a collection of records are retrieved from the service, they are retrieved directly from the redis sorted set and returned to the client, bypassing the MongoDB database entirely. Each leaderboard is stored in its own `sorted set` in order to keep the system as efficient as possible.

## Performance

The performance of the system is quite good and is capable of supporting millions of daily active users. Internal testing measured using budget level hardware with only a single CPU core (and 2-4GB RAM) for the databases and two CPU cores (and 2-8GB RAM) for the service showed performance of greater than 600 requests per second for record insert operations, 200 requests per second for record set retrieval and an average of 500 requests per second for combined read/write operations. This roughly equates to 200,000 concurrent users (CCU) and 4.8M daily active users (DAU).

The following sections detail these results and what you can expect with different hardware configurations.

### Record Insert Test

This test simulates the insertion of leaderboard records by a defined set of simulated users.

| Service Resources | DB Resources  | Service Usage         | MongoDB Usage         | Redis Usage           | Requests per Second | CCU     |
| ----------------- | ------------- | --------------------- | --------------------- | --------------------- | ------------------- | ------- |
| 2 vCPUs / 2GB     | 1 vCPUs / 2GB | 53% (CPU) / 19% (RAM) | 74% (CPU) / 29% (RAM) | 15% (CPU) / 34% (RAM) | 580                 | 174,004 |
| 2 vCPUs / 2GB     | 2 vCPUs / 4GB | 56% (CPU) / 17% (RAM) | 25% (CPU) / 11% (RAM) | 4% (CPU) / 8% (RAM)   | 624                 | 187,147 |
| 4 vCPUs / 8GB     | 2 vCPUs / 4GB | 30% (CPU) / 6% (RAM)  | 36% (CPU) / 30%       | 9% (CPU) / 27% (RAM)  | 681                 | 204,257 |

### Sorted Record Retrieval Test

The test simulates retrieval of top 100 sorted leaderboard records by a set of simulated users.

| Service Resources | DB Resources  | Service Usage         | MongoDB Usage        | Redis Usage           | Requests per Second | CCU    |
| ----------------- | ------------- | --------------------- | -------------------- | --------------------- | ------------------- | ------ |
| 2 vCPUs / 2GB     | 1 vCPUs / 2GB | 51% (CPU) / 16% (RAM) | 1% (CPU) / 31% (RAM) | 55% (CPU) / 35% (RAM) | 206                 | 61,680 |
| 4 vCPUs / 8GB     | 2 vCPUs / 4GB | 26% (CPU) / 8% (RAM)  | 1% (CPU) / 38% (RAM) | 31% (CPU) / 34% (RAM) | 253                 | 75,797 |

### Combined Record Insert & Sorted Retrieval Test

This test simulates the insertion of leaderboard records as well as the retrieval of the top 100 sorted records by a set of simulated users.

| Service Resources | DB Resources  | Service Usage         | MongoDB Usage         | Redis Usage           | Requests per Second | CCU     |
| ----------------- | ------------- | --------------------- | --------------------- | --------------------- | ------------------- | ------- |
| 2 vCPUs / 2GB     | 1 vCPUs / 2GB | 57% (CPU) / 19% (RAM) | 35% (CPU) / 32% (RAM) | 40% (CPU) / 41% (RAM) | 509                 | 152,680 |
| 4 vCPUs / 8GB     | 2 vCPUs / 4GB | 28% (CPU) / 8% (RAM)  | 36% (CPU) / 38% (RAM) | 20% (CPU) / 37% (RAM) | 613                 | 183,954 |
