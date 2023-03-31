================
Scaling Policies
================

Scaling policies are used to determine how shard instances are created and destroyed within the system based on changes
to population demand within a given zone.

Policies work by specifying a minimum population percentage (``minPopulation``) at which the policy will begin applying,
a maximum population percentage (``maxPopulation``) at which the policy will stop being applied and an ``amount`` value
to apply during each application of the policy. In addition, an ``interval`` is specified to indicate how often the
policy can take effect (e.g. ``1m`` for every minute).

Intervals
=========

Each scaling policy requires an interval to be defined. The interval is the time in between each application of a given
policy for a given block of time. Meaning, if a scaling policy to add ``1`` new shard every minute once the population
reaches ``70%`` capacity is executed, it cannot be executed again until one minute has passed.

.. danger::
    Specifying too short of an interval such as ``1s`` can create a runaway scaling policy that can increase the number of
    shards seemingly exponentially.

Stacking Policies
=================

Scaling Policies can be stacked, allowing for multiple additions or removals in a given time interval. This makes it
possible to define additional policies that can take effect in extreme circumstances; such as when populations are
exceedingly high and several additional instances need to spawned in a given interval instead of waiting for a
single instance per interval.

.. caution::
    Use stacking policies with caution so as not to create runaway shard scaling.

Limiting to Specific Zones
==========================

Scaling policies can be limited to only apply to a specific set of zones. This is often useful when a zone is more popular
than another and requires a quicker response to player demand in order to reduce server downtime or queue times.