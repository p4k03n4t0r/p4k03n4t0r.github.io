---
layout: post
title:  "Documenting Serverless with C4"
date:   2022-07-16
tags: serverless,c4,documentation
---

_
What is more difficult than asking a developer to write tests for their code? It is writing documentation for it, because good code and clear tests should already be enough documentation. This might be true for monoliths or microservices, but not for serverless. With serverless the pieces of code are even smaller and logic is partially moved to infrastructure. In this post I'll be giving my answer for the questions: how do you get people to see the importance of documentation in a serverless landscape? I'll be using AWS and its Lambda's as example, but this could be applied to every serverless solution. 
_

## Why documentation for serverless is (extra) important

Before I dive into this, just to get one thing straight: if I talk about 'documentation' I mean a handful of diagrams which make it easy to comprehend how the system looks and highlight the important design decisions.

Microservices cut up monolith into smaller, easier to understand parts, while serverless takes this even one step further. The microservices are split up into seperate functions and the linking of these functions (e.g. a pub/sub mechanism) is moved to Cloud components (e.g. SQS). This makes it easy to lose the overview of the landscape. What did this Lambda do again? It receives a message from this SNS topic, but who publishes to this SNS topic? I can say from my own experience: good luck with figuring that out...

When I'm new on a project the first thing I do to understand the system is to dive into the Git repositories and cloud portal. I want to understand what is there and how it all links together, so I can have this picture in my head which components there are and how they fit together. From my experience this is pretty difficult with serverless. I can look at all the individual Lambda's in an AWS environment, but the only way to see which belong together and understand what they do, is to check them one by one to see which CloudFormation stack they belong to (while hoping these stacks make any sense). 

Even if I dive into it and right now understand how all these little puzzle pieces fit together, will I still remember how all the pieces fit together and what the completed puzzle looks like? The amount of puzzle piecies (Lambda's, SQS queues, DynamoDB tables, SNS topics, etc) is much higher than a microservice landscape. Imagine a new (junior) developer starting in the team, would he/she even know where to start?

## Power of C4

At one project I worked at I got introduced to C4. There's already plenty of resources online about what C4 is, see [here](https://c4model.com/). So to just give a short summary:
- Describes your architecture in 4 layers (Context, Container, Component, Code)
- Each layer is a zoomed in version of the above layer, you could see it like: the parts in the context are boxes, which you can open to see the next layer, each box in that layer can be opened again to get to the next layer, until you hit the lowest layer
- Each layer has its own level of abstractions, e.g. you don't mention which AWS resource you use at the Container level, but instead mention which Cloud Provider you use. It's tempting to mix this up, but the power of C4 is that if it's applied consistently, it's really easy to understand.

The last point is IMO really important and later on I'll give some examples that show (if it's applied consistently) how powerful serverless and C4 can be.

## How C4 and serverless could look like

- Context: smallest, often just show single system, which is your own, and all other systems/actors it communicates with
- Container: opens up your system and shows all features you provide (e.g. some internal components might be shared, but this diagram is not too technical yet). Each container shows the major technical decisions on how it's build (e.g. Cloud provider/location, serverless/microservice, auth service to use).
- Component: opens up each feature and show it's components: each component has its own technical purpose, e.g. Gateway, Database, Event Processor, etc. Within AWS each component would be a CloudFormation Stack or CDK Construct. This can be mentioned for each AWS component, so each component can easily be found in the console. Each component contains it's technical choices, (which AWS Service is used), e.g. DynamoDB as DB, for Lambda's which programming language is chosen, API Gateway as Gateway, etc.
- Code: it could be possible to also map out each component and describe each AWS resource that it contains, but this wouldn't be worth the effort and it's hard to keep documentation in sync with the truth. If you want this, you can use tools like the CloudFormation Designer to generate a diagram of how the stack looks like. Anyway you can always generate this live in AWS, so even exporting this allows documentation & truth to be out of sync. Instead it would be more useful to design common patterns. E.g. you have a pattern on how to do batch processing (EventRule to trigger lambda which reads from DB and puts message in SQS, etc).


## Documentation as code

- One final advantage: when building something new, they really help in discussions on how to approach this. IMO nothing can be more clear to just change an existing diagram to the proposed changes or create a new diagram and show how it fits in with existing components in other diagrams. Next time you pick up the discussion, the diagram is good reference to straight away deep dive into the discussion again.

One of the challenges mentioned before, and one which applies in general for documentation, is that some developers don't like it. Simply because it's not writing code and not helping in progression of an user story. Well there's this cool thing where you write code and document at the same time: documentation as code. There are probably multiple options for this, but I'm using PlantUML. So far it always worked great for me, so I didn't really look for an alternative. 

- PlantUML example

## Conclusion

Documentation is even more relevant within serverless architecture. Although it might be hard to get it started, it should be done. This is just one way to do it, but it depends on the people what works best for each team. I'm curious to your experience!
