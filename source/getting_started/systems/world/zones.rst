=====
Zones
=====

When creating an online virtual world its often helpful to think of that world much like that of the Earth, as a
collection of geographical regions connected together by arbitrary boundaries. Each particular region may have a
different size but in a game its typical to associate each of these regions with a single map as defined in the game
engine. We call these regions Zones in the Virtual World System. Therefore, a Zone is synonymous with a single game
engine map or region of your virtual world.

Linking Zones
=============

Zones define a particular region or space within the virtual world. They can connect to other zones by aligning the
boundaries of two zones together on a particular side or boundary line. The system is a coordinate-agnostic system,
meaning that it defines no rules with regards to how you define your world coordinate system. If you prefer to
build each map using global coordinates or prefer localized coordinates the system will function the same.

The only thing the system cares about is the relationship between zones. When you define a zone within the
Virtual World System you define all zones that share a physical boundary with it, referencing only the unique
id of the adjacent zone. This allows for the creation of virtual worlds of any complexity, whether that be
zones which lay side-by-side one another or stack in three-dimensional space. The choice is yours.

Population Limits
=================

Each Zone definition has a ``maxShardUsers`` and ``autoCreateShards`` property that can be used to control the creation
of shards and the number of players that are able to connect to each server instance.

The ``maxShardUsers`` property is used to determe the population capacity for the zone when deciding how to scale the
number of shard instances according to the defined Scaling Policies. Therefore, if you define ``100`` users as the
maximum number of users per shard, then each game server shard instance will allowed up to 100 users to join it. Once
the shard has reached maximum capacity, no additional players will be allowed to join. The system will also add an
additional shard when the total population capacity reaches a particular threshold as defined by the scaling policy
in order to increase the total number of users the system can handle automatically.

Limiting User Access
====================

It is also possible to limit access to a particular zone by defining a list of allowed user id's and role names. The
``allowed`` property takes a list of all the user identifiers and role names that are permissioned to join the zone.
When specifying the user id, users must match the authenticated universally unique identifier of the user attempting
to join the zone. When specifying a role name, the authenticated user trying to join the zone must be a member of the
defined role.

This may be useful to gate access to particular zones based on their product subscription level, or purchase history,
or by their participation in a beta program. This may be also useful to isolate zones to particular teams or groups
of players during development.

Zone Metadata
=============

It is possible to describe any metadata you desire in a Zone definition. However, there are a few metadata properties
that are important when it comes to deployment and scaling of the game servers that will ultimately serve players
in your virtual world. Each property described below is considered **optional** and will not impact the performance
of the system if they are ommitted from the Zone definition.

buildVersions
-------------

The ``buildVersions`` metadata property allows you to define a Zone that only works for particular build versions
of you game or application. This may be useful when developing zones that are specific to a particular version of the
product such as a content patch or a version 2.0. This may also be desirable to create specific virtual world topologies
during testing or prototyping where you don't want to expose a particular zone to other developers or branches.

Example:

.. code-block: json

    {
        "data": {
            "buildVersions": [
                "1.0.0",
                "1.1.0"
            ]
        }
    }

initOptions
-----------

The ``initOptions`` metadata property is used to specify initialization options or parameters that will be sent to the
game server instance when a shard is assigned for the given zone. This is useful to identify which map to load, what
gameplay mode to use or other gameplay options specific to your zone. It is defined as a list of arguments that will
be sent to the server. The server is then responsible for interpreting the list accordingly.

Example:

.. code-block: json

    {
        "data": {
            "initOptions": [
                "MyMapName",
                "gameMode=Dungeon"
            ]
        }
    }

regions
-------

The `regions` metadata property is used to limit the datacenter regions that a Zone shard will be launched within. This
can be useful when testing new zones for a particular regional audience or for providing region-specific content in order
to comply with local government regulations. The system will only launch shards in the regions listed. If no regions
are listed, the default behavior is to launch at least one shard in every available region.