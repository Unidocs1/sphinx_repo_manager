======
Shards
======

A Shard is a single game server instance of a particular Zone within the virtual world. Shards are created
automatically by the system based on the user population and Scaling Policies rules as defined by the
developer.

The system will create at least one shard for each combination of build version and region supported by the system.
The number of shards are then scaled automatically based on the population demand of that particular region/build.

By default two scaling policies are created at system startup. The first policy adds a new shard every time
the user population reaches 70% capacity in a particular zone/region/build combination. The second policy
removes a shard every time the user population falls below 40% capacity in a particular zone/region/build
combination. This allows for efficient resource usage to ensure games are running at optimal cost.

Regions
=======

By default, the Virtual World System will create a Shard for each available datacenter region unless
explicitly defined otherwise in the Zone definition metadata. When defined, new shard instances will
only be created for the regions listed.

Build Versions
==============

By default, the Virtual World System will create a Shard for each available build version of the application unless
explicitly defined otherwise in the Zone definition metadata. When defined, new shard intances will only
be created for the build versions listed.

Shard Selection (by Latency)
============================

The Virtual World System also features an intelligent shard selector. This is available at the service endpoint
``/zones/:zoneUid/shards/preferred``. When a ``GET`` request is sent to this endpoint by an authenticated user
the system will look up all available shards for the given zone and return a sorted list in order from closest
to furthest from the user's geographical location in the real world. Thus ensuring that users are able to join
the shard with the lowest possible latency to them.

Shard Selection (by Social Relevancy) **[STUDIO]**
=======================================================

.. attention::
    Requires license to AcceleratXR **Studio** and above.

In addition to sorting shards by their geographical location the system will also rank shards based on the social
relevancy of users already joined in relation to the user performing the request. This is accomplished by querying
the user's social UserLinks and computing a relative rank for each available shard. The shards are then sorted
based upon this rank, with tie breakers being further sorted by closet geographical location, and returned to
the client in order of highest rank to lowest.

Shard Ranking
-------------

When performing intelligent shard selection each shard is given a rank based on the social relevancy of the given
shard to a particular user. This is achieved by evaluating what users are currently connected to the shard and
applying a computed score based on each user's relationship to the user retrieving the shard list.

Ranks are adjusted for each UserLink according to the following table.

.. list-table::
   :header-rows: 1

   * - UserLink Type
     - Score
   * - ``BLOCK``
     - ``-1``
   * - ``ENCOUNTER``
     - ``+1``
   * - ``FOLLOW``
     - ``+2``
   * - ``FRIEND``
     - ``+3``

To understand this in more finite terms lets take an example of two shards. The first shard has two friends of the user
and one user whom has been blocked by the user. The second server has two encounter users.

.. math::

    Rank (Shard One):
      + 3  (Friend A)
      + 3  (Friend B)
      - 1  (Block C)
    ______
        5

    Rank (Shard Two):
      + 1  (Encounter A)
      + 1  (Encounter B)
    ______
        2

In the above example shard One has a rank of ``5`` and shard Two has a rank of ``2``. Therefore the user will receive a
sorted list with Shard One preceding Shard Two.

.. code-block:: javascript

    [
        {
            // Shard One
        },
        {
            // Shard Two
        }
    ]