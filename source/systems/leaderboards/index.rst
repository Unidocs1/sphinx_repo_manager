============
Leaderboards
============

.. toctree::
    :hidden:

    architecture

The following key concepts and terminology will be used throughout the rest of this documentation.

Leaderboard
===========

The ``Leaderboard`` contains the metadata associated with a particular leaderboard. It contains useful information such as the ``name``, ``description``, ``sort`` order and an ``icon`` that can be used when displaying to users.

LeaderboardRecord
=================

The ``LeaderboardRecord`` stores a single best persona's entry into the leaderboard set. Users can submit any number of records they desire but only the best score is kept. The data contains information about the achieved ``score``, the date and time that the record was created as well as the global rank of the record in relation to others.

Note that the REST API does not allow retrieval of a single record and only allows retrieval of a collection. The collection will always be sorted in the order with which the leaderboard has been configured. It is possible to specify a ``personaUid`` as a search query and receive all results starting at that persona's rank and beyond.
