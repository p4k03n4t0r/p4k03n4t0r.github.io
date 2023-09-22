---
layout: post
title: 'Storage first pattern'
date: 2023-09-22
tags: storage first, aws, pattern, dynamodb
---

_In a serverless landscape services get smaller and infrastructure gets complexer. In my experience architecture patterns in infrastructure are thus getting more important than the ones in code. In this blog I'll be looking at one pattern that helped me a lot in an event driven setup: the storage first pattern. I'll be describing what it is and when to apply it._

## Event driven landscape challenges

In an event driven landscape it's common as a team to have multiple sources to receive data from. Each source could make the data available in a different way. One team offers a S3 Bucket which can be read, another one an EventBridge and maybe even an API. Ideally there is a single way to consume data within the IT landscape, but from my experience this is rarely the case. For a new service to consume an external data source it costs quite some time to design, build and test the connection. Each new service consuming this external data source has to go through this process again.

Each new service using this single external data source will increase the load on it. Meaning the costs and possibility of outtages increases.

- Upstream availability
- Debugging issues: is it me or an external party?
- Dependant on other team to replay events

## Storing all incoming data

- Solves previous issues
- Store data as is

## Shortcomings

- Extra costs
- Need some way to not send replayed events to upstream parties

## Conclusion

There's more detail to this pattern. E.g. how to store and group the events?
How long to retain data and when overwrite older data?
But that's something for a next blog.
