---
title: "Event Scraper"
date: 2019-11-07T21:58:38.095Z
---

The `EventScraper` is a background service with the responsibility of retrieving events from the [`telemetry_services`](/docs/telemetry_services) system.

The scraper operates by first building a list of all telemetry event types to monitor. This list is pushed into a redis list with the key name `qs.event_types`.

Upon each runtime execution of the background service the scraper then queries [`telemetry_services`](/docs/telemetry_services) for the latest set of events and pushes them onto a redis queue with the key name `qs.events`.

The scraper attempts to pull events in groups of 1,000 during each run cycle. Redis is then used to synchronize the last retrieved event in order to prevent multliple instances from scraping the same set at the same time.
