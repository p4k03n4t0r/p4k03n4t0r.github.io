---
layout: post
title: 'How do I validate data in an event driven AWS architecture?'
date: 2023-12-01
tags: aws, event driven, dynamodb, glue, athena, s3, data validation
---

_Having worked on a complex event driven landscape in AWS, one of the biggest challenges that I faced was: how do I validate the data that goes through it? For me this felt like the paradox of the tortoise and Achilles: by the time I thought I had caught up, the data had already moved on. Within the landscape events were being processed realtime and in parallel, which meant that the current state was always changing. How can you validate that everything works as expected when it's always changing? In this blog I'll dive a bit more into the challenge and than come up with different ways how you could do data validation within AWS specifically._

## The challenge

All applications of feature teams have code that follow business rules and more and more of these follow an [event driven architecture](https://thenewstack.io/the-rise-of-event-driven-architecture/). Quickly after you start with such an architecture, the following question will arise: does the data that we expect actually comes out at the end based on the events that we receive as input? Depending on the type of the data this could be easier or harder. If the amount of events that are processed is in the hundreths, you could enable debugging everywhere and validate each of them manually. But when the events coming in are for example IoT data, there will be at least thousands or even millions coming in each day. This will be very costly AWS and labour wise, so now things get more difficult.

At some point the inevitable answer to the question before will be no, so what could be the reason? It could be many things: components are not called in the right order, business rules are not applied correctly in component X, an external team suddenly starting sending different data, there is an error in a component or the infrastructure. The last could be ruled out by having proper observability, so let's assume you have this in place and this is not the issue. The reason is actually data related: there's data going in and data going out, but it's not what's expected.

An event driven landscape can be a big black box with a lot of cogs and wheels, so where's the part where it goes wrong? Pinpointing this in an event driven landscape is harder than it seems. Let's say you found an entity that came out at the end that had a different result than expected, how do you figure out what the state of this entity was when it went through the landscape? Logging all event sent everywhere could work, but that's often too expensive if system has millions of events going through it. Let's look at some 'tools' that could help you find the answer within an AWS event driven landscape.

## Border control for data

One question to answer first is: is the cause in an application of my team or is it in an external system that provides events to us. In an ideal situation, there's an event format for every event and it's ensured that events always follow this schema. I haven't found this situation yet, so maybe I'm just unlucky or it's just an utopia.

One way to get more grip on this is by applying the storage first principle. This says that before you further process an incoming event, you store it first. One big benefit for this is that events are not lost, but looking at it from data validation perspective there's also another big benifit: we can validate the raw event we received from the external party.

There are multiple ways to do this in AWS, one option is storing all input events in a DynamoDB table. I would say this is the best suited service, since it's relatively cheap (much cheaper than e.g. RDS) and can scale quickly (to handle sudden spikes in events). Diving in how you chould set up the storage first principle using DynamoDB is a topic of it's own, but these are at least the relevant considerations you'll have to make:

- How long do you want to keep data? You could expire old data using a [TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html).
- Do you want to store all events or just keep the latest X events for an entity or based on some other condition?
- How will you be able to validate the data in the table? I have used the combination of EventBridge Scheduler + DynamoDB export to S3 + Glue + Athena for this. An example can be found [here](https://aws.amazon.com/blogs/database/simplify-amazon-dynamodb-data-extraction-and-analysis-by-using-aws-glue-and-amazon-athena/).

Can be hooked anywhere (internal (audit trail) and external (inlet))

<IMAGE of DynamoDB>

## Validating events in motion

Entities going through an event driven landscape often get updates, for example an order can change status from scheduled to intransit and finally delivered. This causes the status in a data store to be overwritten. Let's say we check to see whether there are any orders with an intransit status: there are currently none. Is this actually expected (since there are actually none at the moment) or this is an actual data issue? We feel the need to have some time machine to also see what the system looks like one or two hours ago. That's the only way to know for sure whether there is a data issue or not.

One way to build this 'time machine' is adding event trails at a point where events pass through the system (EventBridge, SNS). This logs all events that go through a certain checkpoint in the landscape. In here we could see whether there were any intransit events in the past 24 hours. In AWS I think there are multiple ways to do this:

- Subscribe with a CloudWatch loggroup, an example can be found [here](https://www.boyney.io/blog/2021-04-15-debug-eventbridge-events-with-cloudwatch).
- Subscribe a Lambda function which puts all events in a DynamoDB table, which can use the previously mentioned 'DynamoDB scheduled export to Athena' setup.

## Export all data stores to single place

In AWS there is wide range of data stores available including also [a long list of databases](https://aws.amazon.com/products/databases/). From my experience there's not a single one that fits all use cases, it could be possible that you pick different data stores in different places in your landscape. Still you want to validate the data in each of them. From my experience it helps to support these data validation questions in a single place regardless of the data store that they originate from. This makes it easier to do data validation (just need to learn a single query language) and also allows running queries across different data stores.

In AWS there are different options:

- Make the data available in a central data lake within the company, as long as this process is not too time consuming (other wise the second option might be more interesting).
- Within your team create your own data lake within your team using S3 & Athena. This seems like a big step, but I think it doesn't have to be complicated and definetily pays back in the long run. Again the same 'DynamoDB scheduled export to Athena' setup can be used. Other data stores, like RDS, also [allow exporting to S3](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/postgresql-s3-export.html). The infrastructure code to create the scheduled export could be generalized, making it very easy to enable for (new) data stores and it could event be shared with other teams.

## Monitor business metrics

CloudWatch metrics: https://docs.powertools.aws.dev/lambda/typescript/latest/core/metrics/

## Conclusion
