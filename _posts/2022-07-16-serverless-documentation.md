---
layout: post
title:  "Documenting Serverless with C4"
date:   2022-07-16
tags: serverless,c4,documentation
---

_
Reason: own challenges with 'selling' documentation
Goal: show how C4 nicely fits serverless architecture
Own experience: documentation as code is cool! (writing code > manually making diagrams)
Note: I'll be talking about AWS Lambda's, but feel free to replace this with any other serverless (e.g. Azure Functions)
_

## Why documentation for serverless is important + general documentation challenges

IMO: documentation should just be a few diagrams, not lengthy text documents. So For me if I say 'documentation', I mostly mean diagrams.

- Serverless is even more scattered than Microservices. Big part of the design is moved from within a single service to infrastructure level.
- It's easy to lose to the overview: what did this Lambda do? It received a message from this SNS topic, but who publishes to this SNS topic? (good luck with figuring that out)
- In general getting developers hooked onto documentation is hard (I want to code, I don't want to write boring documentation, I know how the system looks like). But do you remember in 6 months? Especially for Serverless, you write a lot more Lambda's in comparison to microservercies. Good luck with remembering that. Also new people will have a hard time figuring out what this Lambda with a long, semi-auto-generated name does. 
- One final advantage: when building something new, they really help in discussions on how to approach this. IMO nothing can be more clear to just change an existing diagram to the proposed changes or create a new diagram and show how it fits in with existing components in other diagrams. Next time you pick up the discussion, the diagram is good reference to straight away deep dive into the discussion again.

## Power of C4

At one project I worked at I got introduced to C4. There's already plenty of resources online about what C4 is, see [here](https://c4model.com/). So just giving a short summary:
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

One of the challenges mentioned before, and one which applies in general for documentation, is that some developers don't like it. Simply because it's not writing code and not helping in progression of an user story. Well there's this cool thing where you write code and document at the same time: documentation as code. There are probably multiple options for this, but I'm using PlantUML. So far it always worked great for me, so I didn't really look for an alternative. 

- PlantUML example

## Conclusion

Documentation is even more relevant within serverless architecture. Although it might be hard to get it started, it should be done. This is just one way to do it, but it depends on the people what works best for each team. I'm curious to your experience!