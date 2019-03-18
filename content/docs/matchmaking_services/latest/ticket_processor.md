---
title: "Ticket Processor"
date: 2019-03-15T20:09:14-07:00
---

The Ticket Processor is a special program that is responsible for performing the actual search and match algorithm during the matchmaking process.

## Search Algorithm

The AcceleratXR Core matchmaking system takes a very different approach from other search algorithms. Each matchmaking ticket that has been submitted to the service is processed individually within it's own separate thread or process, called a Ticket Processor. The Ticket Processor performs the desired matchmaking algorithm by first retrieving a subset of tickets from the entire database that are best suited for the ticket being processed. After the subset has been retrieved, a fitness score is computed for each ticket corresponding to the potential match quality that the two tickets share. These scores are then sorted from best fit to least fit. Finally, the processor attempts to create the match using the top selection of tickets. Should any of the selected tickets have already been claimed by another match the algorithm starts over after a brief sleep period.

This approach is made possible by exploiting the transactional atomicity of certain databases. More specifically, this system utilizes the [Redis](https://redis.io/) database and its native [Transactions](https://redis.io/topics/transactions) support in order to gaurantee atomic locking during match creation. What this means in practice is that while a single ticket may fail to successfully create a match on its own there is a high probability that another ticket will successfully match that same ticket in another process.

### Ticket Subset

At the beginning of each search pass the processor begins its work by first retrieving a subset of tickets from the global queue that matches the search criteria for the assigned ticket. This allows the algorithm to remove large numbers of unmatchable tickets in a manner similar to [Sweep and Prune](https://en.wikipedia.org/wiki/Sweep_and_prune).

As search criteria can be arbitrarily defined by a client it is important for the generated query to be meaningful and efficient. This is why criteria can only use primitive types as values. The criteria definition has been specifically designed to be able to easily describe complex queries with `AND` and `OR` relations and `==`, `<=`, `>=` comparisons.

Take for example a ticket with the following criteria.

```javascript
[
    { name: "skill", minValue: 1250, maxValue: 1750 },
    { name: "skill", minValue: 750, maxValue: 1000 },
    { name: "gameMode", minValue: 1, maxValue: 1 },
];
```

In English, this ticket will match against any ticket that:

-   Has a `skill` value between `[750, 1000]` _or_ `[1250,1750]`
-   Has a `gameMode` value that equals `1`

If translated into SQL, the resulting query would be:

```sql
SELECT * FROM Ticket WHERE
    gameMode == 1 AND
    (
        (statistics.name == skill AND statistics.value >= 750 AND statistics.value <= 1000)
        OR
        (statistics.name == skill AND statistics.value >= 1250 AND statistics.value <= 1750)
    );
```

The ticket criteria isn't the only factor included in the query however. This is because each ticket specifies a desired team size and number of teams. This is in order to provide support for team based matchmaking in addition to free-for-all.

Assuming it is desired to create matches with two teams of five players each tickets should have the values `2` and `5` set for the `numTeams` and `teamSize` Ticket properties respectively. If a free-for-all is desired then `numTeams` is set to a value of `1` and `teamSize` is set to the total number of desired players.

Expanding this further, take for example the following matchmaking Ticket.

```javascript
{
    "numTeams": 2,
    "teamSize": 5,
    "criteria": [
        { "name":"skill", "minValue": 1250, "maxValue": 1750 },
        { "name":"skill", "minValue": 750, "maxValue": 1000 },
        { "name":"gameMode", "minValue": 1, "maxValue": 1 }
    ]
    ...
}
```

In English, the final resulting search criteria is therefore:

-   Has a `numTeams` value that equals `2`
-   Has a `teamSize` value that equals `5`
-   Has a `criteria.skill` value between `[750, 1000]` _or_ `[1250,1750]`
-   Has a `criteria.gameMode` value that equals `1`

Translated to SQL, the resulting query would be:

```sql
SELECT * FROM Ticket WHERE
    numTeams == 2 AND
    teamSize == 5 AND
    criteria.gameMode == 1 AND
    (
        (criteria.statistics.name == skill AND criteria.statistics.value >= 750 AND criteria.statistics.value <= 1000)
        OR
        (criteria.statistics.name == skill AND criteria.statistics.value >= 1250 AND criteria.statistics.value <= 1750)
    );
```

## Fitness Score

The fitness score is a computed value that determines the potential quality of a match between two tickets. The lower the value of the score, the more likely that matching the two tickets will be of good quality. The value is a weighted multi-variable summation of selected statistic deltas between the two tickets.

More simply, the algoirthm uses a list of desired statistic values that have been pre-configured with a given weight. For each desired statistic value a difference is calculated between the two tickets and the weight is applied to the result. Then each resulting delta is added together to form the final fitness score.

Written as a math formula:

```
TODO: insert fitness formula
```

Now for an example. Assume the processor was pre-configured with the following statistic weights.

| Statistic | Weight |
| --------- | ------ |
| skill     | 0.75   |
| ping      | 0.25   |

In this scenario the developer wishes for `skill` to represent 75% of the total fitness score while `ping` represents only 25%. The algorithm thus will generate matches where `skill` is 3 times more important than `ping`.

Now take for example the following set of statistics from two tickets.

```javascript
// Ticket 1
"statistics": [
    { "name": "skill", "value": 1500 },
    { "name": "ping", "value": 65 }
]

// Ticket 2
"statistics": [
    { "name": "skill", "value": 1750 },
    { "name": "ping", "value": 35 }
]
```

The resulting fitness score of Ticket 2 relative to Ticket 1 will be.

```
F = (abs(1750 - 1500) * 0.75) + (abs(35-65) * 0.25) = 195
```

Once all fitness scores have been computed for each ticket in the subset they are put into a list and sorted from lowest value to highest. Tickets with the lowest score are the best matches.

### Team Assignment

The next stage in the search algorithm is to perform team assignment. This process goes through the sorted list of candidates and attempts to assign the players represented to the first team with enough available slots in alternating order.

As an example lets assume the following sorted list of players and their fitness scores.

| Player | Score |
| ------ | ----- |
| 1      | 35    |
| 2      | 75    |
| 3      | 85    |
| 4      | 115   |
| 5      | 127   |
| 6      | 159   |

By alternating between each team as the list of candidates is traversed the following team assignments will result.

| Player | Score | Team |
| ------ | ----- | ---- |
| 1      | 35    | 0    |
| 2      | 75    | 1    |
| 3      | 85    | 0    |
| 4      | 115   | 1    |
| 5      | 127   | 0    |
| 6      | 159   | 1    |

The combined score value of both teams will be `247` and `349`.

### Ticket Locking

Now that the candidates and teams have been selected its time to create the match. In order to eliminate race conditions resulting from the assignment of the same ticket in different matches a transactional database capable of performing atomic operations is required. AcceleratXR Core's ticket processor uses the Redis database for this purpose.

When creating a match each ticket processor will first attempt to lock each candidate ticket in a single transaction before proceeding further. Once all tickets in the match have been successfully locked the processor creates the Match record and inserts it into the primary service database for clients to retrieve via the matchmaking service API. The processor then updates each ticket, setting the status to `MATCH_FOUND` and `matchUid` with the ID of the match object for clients to discover.

In the event that any one ticket is unable to be locked the operation fails and the match is immediately disbanded. The processor then goes into a brief sleep and starts the entire search algorithm again. The amount of sleep time is staggered so as to ensure that tickets have the best opportunity to complete successfully.

Once a match has been found or if the processor discovers that its ticket has been matched by another processor, the program performs any database cleanup and exits.
