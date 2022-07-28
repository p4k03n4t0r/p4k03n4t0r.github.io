---
layout: post
title:  "Documenting Serverless (with C4)"
date:   2022-07-16
tags: serverless,c4,documentation
---

_What is more difficult than asking a developer to write tests for their code? It is writing documentation for it, because good code and clear tests should already be enough documentation. This might be true for monoliths or microservices, but not for serverless. With serverless the pieces of code are even smaller and logic is partially moved to infrastructure. In this post I'll be giving my answer for the question: how do you get people to see the importance of documentation in a serverless landscape? The examples will be with AWS and its Lambda's, but this could be applied to every serverless solution._

## Why to write documentation at all

If I talk about 'documentation' I don't specifically mean pages of text and detailed diagrams, but clear code and tests are also documentation. Actually I much prefer these to describe what the system does and how it fits together. When I'm new on a project the first thing I do to understand the system, is to dive into the Git repositories and deployed cloud resources. I want to understand what is there and how it all links together, so I can have this picture in my head how everything fits together. 

I understand that this is just my approach and this works differently for other (starting) developers. Besides if I have to touch something which I worked on a few months ago, I probably don't remember the made choices. It would be time intensive to have to do this deep-dive every time, so this is where other types of documentation can be useful. I don't mean long pages of text and really complex diagrams, but diagrams which you can understand without needing pages of text.

## Why documentation for serverless is (extra) important

To answer this question, it's necessary to understand the difference between serverless and what came before it. The microservice trend was already a big improvement over monoliths, since it isolated code into clear, small parts which offer one or a few functionalities. Serverless takes this even one step further, since a single microservice can be cut up in multiple serverless functions. A serverless function actually does just a single thing. It sounds like this would make documentation even less relevant, since this function is as isolated as possible and thus can be easily described with clear code and tests. This is true, but it also introduces new challenges.

Serverless cuts up a system in a lot of small puzzle pieces, in a big application this can be hundredths of serverless functions and cloud components (queues, topics, databases, etc). We might understand a single puzzle piece, but how where does it go into the big picture of the puzzle? I think everyone can agree that solving a puzzle with 10 pieces is much easier than solving one with 100 pieces or more. There's a lot more connections with serverless and these are done on infrastructure level. 

Let's give an example of a situation I encountered: I have this single Lambda that receives an event, does a calculation and stores it in the database, but where does the data in the event come from? I managed to follow the breadcrumbs in the AWS Cloud Console via SQS, Lambda, EventBridge, Lambda, until I stumbled on a SNS topic. The trail of breadcrumbs ends here, because there's [no easy way to figure out who published to this SNS topic](https://stackoverflow.com/a/59586350). Dang, if I just had some documentation to figure out where in this huge jigsaw puzzle I was...

All in all serverless moves the complexity to the infrastructure. Since there are so many puzzle piecies, it's harder to understand how the puzzle pieces fit together in comparison to a microservice landscape. An added downside is that it's easier to create a big spaghetti mess of the landscape. All these infrastructre as code solutions make it easy to chain the whole landscape together. Which is nice, until you hit the point where no one understands what the effects are of putting an event into a SQS queue. Does anyone know whether things will break if we make changes to the events that go into the queue?

## Power of C4

So documentation using clear code and tests can't fully describe a serverless landscape. In my opinion currently the best way to document this is using diagrams. At one project I worked at I got introduced to C4 and when I started working in a serverless landscape it seemed like a good fit. But before I tell more about why, let's give a short summary of C4:

- It describes your architecture in 4 layers (Context, Container, Component, Code).
- Each layer is a zoomed in version of the above layer, you can see it like boxes which contain smaller, more detailed boxes, which containing even smaller and more detailed boxes.
- Each layer has its own level of abstraction; higher layers contain big design choices (e.g. Cloud provider), while lower levels contain small design choices (e.g. type of database).

Since this is not a blog about how C4 works, I would recommend to just look online for [a more detailed description](https://c4model.com/).

Of course there are more documentation methods, but for me these are the advantages of C4 for serverless:

- C4 gives structure via different abstraction layers to these hundredths of small, deployed components in the cloud.
- It's easy to navigate through the cloud components using C4, since all layers (boxes) are linked together. Via C4 it would be easy to answer the before question about who publishes to a SNS topic.
- C4 can nicely fit your cloud setup: each CloudFormation stack could be a C4 Component. 

## How C4 and serverless could look like

I set up an example project using PlantUML to describe how I would document serverless using C4: [p4k03n4t0r/c4-for-serverless](https://github.com/p4k03n4t0r/c4-for-serverless). This should be used as an inspiration, because it would depend on how a system is setup (monorepo vs multiple repo's, single stack vs multiple stacks, etc). The most important thing is to find what works for your team and stick to it. Consistency is the key! 

The above repository uses 'documentation as code', because which programmer doesn't prefer writing code over getting annoyed at moving lines in a Visio diagram?

## Conclusion

If you don't have any diagrams to describe your serverless architecture, you'll pay the price in the future. It might take some time to set up C4, but in my opinion it's worth it in the long run. It helps understanding people what is there, makes it easier to have discussions about new/extending functionality and helps with a consistent architecture. What I described here is just one way that works for me, but this is different for every team. I'm curious to your experience!
