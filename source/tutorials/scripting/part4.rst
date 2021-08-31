===================
Background Services
===================

Greetings and welcome back to our five part series on custom scripting with the AcceleratXR Live Scripting system. So far we’ve learned how to respond to web requests to transact and process data. This is great for what is likely the vast majority of use cases you’ll encounter. However it doesn’t solve every problem. Sometimes you need something proactive instead of reactive.

This week’s topic is all about background services. A background service (aka job) in AcceleratXR is a special class that is executed on a regular schedule. Execution begins at service startup and will continue running indefinitely at the interval you specify in code until the server is shut down. This is particularly helpful for tasks like data processing and real-time game simulation.

Before we write a background service from scratch let’s start by taking a look at an existing one. Every project in the AcceleratXR platform comes with one pre-defined background service; the MetricsCollector. The MetricsCollector is a background job whose responsibility is collecting aggregate metrics data about the service and updating the Prometheus state. This allows each service to provide important reporting data about the system that can be monitored in real-time.

Open up your test workspace that you created in part one. Look for the file named MetricsCollector.ts in the jobs folder and open it.

.. image:: /images/tutorials/scripting/part4_diagram1.png

A background service is very simple. It’s any regular class that extends the BackgroundService base class. The base class exposes a few required abstract functions that you must implement. They are:

* run()
* schedule()
* start()
* stop()

The run function is the heart of the background service. It is the function that the system will execute on each interval of the set schedule. It is where the bulk of processing work should take place.

The startand stop functions on the other hand are executed at service startup and service shut down respectively. They are intended for job initialization and cleanup. This is useful if you need to establish a connection to a remote server or initialize any default state.

The schedule function is actually a getter and it returns a crontab-like string that defines the interval of execution. If you need help defining your schedule there’s a great online tool that can help with that.

In the case of our MetricsCollector class you’ll notice that the only thing defined in it is the schedule. The schedule is set to */5 * * * * * which means that the job will execute once every 5 seconds. The remaining interface functions (run, start and stop) are all empty with no implementation. So let’s fill them in with an example.

Following on from part three we are going to create a new metric called total_characters that will report the current total number of characters stored by the service. In order to do that however we will need access to the Character repository. We can easily get access to this by creating a new variable that uses the @MongoRepository(Character) decorator. This decorator will ensure that the correct repository is injected on creation of the background job.

.. code-block:: javascript
   :linenos:

   @MongoRepository(Character)
   private repo?: Repository<Character>;

We’ll also need to define a metric container that will store the information we are going to expose through Prometheus. For this instance the Gauge is a suitable data type as it tracks a single value that changes over time (up or down). This works perfectly for tracking something like the character count.

.. code-block:: javascript
   :linenos:

   private totalCharacters: prom.Gauge = new prom.Gauge({
       name: “total_characters”,
       help: “The total number of characters.”,
   });

Now it’s to implement the main logic of our job. Each time the job is run we will retrieve the total number of characters in the database and set the value of our metric. It’s as simple as that.

.. code-block:: javascript
   :linenos:

   public async run(): Promise<void> {
       const result: number = await this.repo.count();
       this.totalCharacters.set(result);
   }
   
Notice that in order to make this code work we had to change the signature of the run function be async. In the code above we retrieve the total number of characters using the count function and set the result to our total_characters metric.

Now let’s try writing a background service from scratch. For our example we’re going to create a job to replenish a character’s health and mana at a regular interval. This is quite common in many games and is a perfect use case for this tutorial.

Let’s start by creating a new file in the jobs folder called CharacterRegen.ts. Copy and paste the following stub code into your file.

.. code-block:: javascript
   :linenos:

   import { BackgroundService, MongoRepository } from “@acceleratxr/service-core”;
   import { MongoRepository as Repository } from “typeorm”;
   import Character from “../models/Character”;
   export default class CharacterRegen extends BackgroundService {
       @MongoRepository(Character)
       private repo?: Repository<Character>;
       constructor(config: any, logger: any) {
           super(config, logger);
       }
       public get schedule(): string | undefined {
           return “*/10 * * * * *”;
       }
       public async run(): Promise<void> {
       }
       public async start(): Promise<void> {}
       public async stop(): Promise<void> {}
   }

You’ll first notice that the schedule has been defined as */10 * * * * *. This means that the job will execute once every ten seconds. That means every ten seconds we’ll regenerate a bit of each character’s health and mana. We’ll need a few variables to know exactly how much and what the max should be.

.. code-block:: javascript
   :linenos:

   const REGEN_HEALTH: number = 5;
   const REGEN_MANA: number = 10;
   const MAX_HEALTH: number = 100;
   const MAX_MANA: number = 100;

Now to the heart of the job. We want to regenerate 5 health and 10 mana of each character in the game every 10 seconds. To do this we’ll need to pull a list of all characters and then update their values accordingly, making sure not to exceed the maximum value of 100 for each.

.. code-block:: javascript
   :linenos:

   public async run(): Promise<void> {
       const chars: Character[] = await this.repo.find();
       for (const char of chars) {
           char.health = Math.min(char.health + REGEN_HEALTH, MAX_HEALTH);
           char.mana = Math.min(char.mana + REGEN_MANA, MAX_MANA);
           char.dateModified = new Date();
           char.version += 1;
           await this.repo.save(char);
       }
   }

In the above example we retrieved the list of every character and applied an addition to the health and mana variables with a capped max. You’ll also notice that we increase the version number and set a new dateModified. This is important to maintain the optimistic locking protection protection (described in part  three) as it is not done automatically. Then we call saveon the repository to persist the changes to the database.

While this solution is perfectly suitable its far from optimized. The problem is that it iterates over all characters, even those that are already at maximum health and mana. This means we’ll be unnecessarily updating character records that don’t actually have any changes.

To reduce the number of characters we’re processing let’s add search criteria. This search criteria will return only those characters whose health or mana values are less than the maximum, as they are the only records we actually care about.

.. code-block:: javascript
   :linenos:

   const chars: Character[] = await this.repo.find({
       $or: [
           { health: { $lt: MAX_HEALTH }},
           { mana: { $lt: MAX_MANA }},
       ]
   });
   for (const char of chars) {
       char.health = Math.min(char.health + REGEN_HEALTH, MAX_HEALTH);
       char.mana = Math.min(char.mana + REGEN_MANA, MAX_MANA);
       char.dateModified = new Date();
       char.version += 1;
       await this.repo.save(char);
   }

This is a huge improvement over our original code. Now save and publish your new background service. The job will automatically register itself and start executing.

In the final installment of the Custom Scripting series we will learn how to use events to reset the character’s health and mana every time a user logs in, completes a quest or levels up.