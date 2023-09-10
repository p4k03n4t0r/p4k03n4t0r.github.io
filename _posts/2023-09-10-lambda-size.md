---
layout: post
title: 'How big should a Lambda function be?'
date: 2023-09-10
tags: lambda function, lambda
---

_For the last two years I have been working with AWS Lambda function. This gave me a lot of joy and headache at the same time. It made some things much easier in comparison to running applications in containers. But I also had to revisit some concepts I thought were 'good pratices'. One of the biggest things I was struggling with was: how big should a Lambda function be? Coming from this movement of monolith to smaller microservices, it felt that Lambda functions was one more step in the direction of 'making it even smaller'. Now after having some experience with Lambda functions, I feel I can give my take on it based on what I learned from practice so far._

## Hard limits of a Lambda function

One thing I think is important to know before diving into this subject, is knowing the hard limits of a Lambda function. The limits for a single function are a 15 minutes timeout, 10,240 MB memory and 10GB code size, see [Lambda quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html). It looks like Lambda function can handle large code bases, as long as the (monolithic) application doesn't have long running taks of over 15 minutes or requires large amounts of memory. This still doesn't answer the question how big a Lambda function should be, but it at leasts sets some boundaries for the discussion later on.

## What is a Lambda for?

Before I can say something about the size of a Lambda function, I should answer a different question to make sure we're talking about the same thing: what is a Lambda function for? The answer is pretty simple if you ask me: it depends on the context you're in. Nowadays there is a wide range of teams running their code in the cloud: feature teams, platform teams, data science, CCoE, security, quality assurance and many more. Each team has different goals and thus will use the cloud in a different way. I think one thing they all have in common is that they want to achieve a task using the services that AWS offers. For a lot of these tasks AWS offers specific services (e.g. for a SQL database or a WAF), but I hardly know any use case where just using out-of-the-box AWS services is enough. There is always a need to add customization to it and the way to do this is to write code and where do you run this code in AWS? Exactly: Lambda functions.

Whenever an AWS service is not sufficient enough, the answer is often to write a Lambda function to do it. The almost too obvious example is when you write custom business logic for your user-facing application. But also within for example the security context you could deploy a Lambda function containing code that does a custom company security check: are all AWS resources tagged according to the company data classification rules?. The CCoE team might deploy a Lambda function to make sure all AWS sandbox accounts don't have any unused AWS resources running to reduce the total AWS costs. Even a feature team could use Lambda functions for non-user facing features: to automatically rotate the password of a database.

As is shown with the above examples is that Lambda functions do not serve a single purpose, but that doesn't help me answering my question. To still give an answer, I'll scope the topic to what is probably what you expected: how big should a Lambda function containing business logic for customer features be? What I mean with this is that the Lambda function is for example (part of) an user-facing API or part of an event-driven flow to process user information.

## Smaller vs bigger

With the discussion scoped, it's now time to see what the options are and what their benefits are. Looking at the question again, it's hard to make it specific. Saying that 'a Lambda function should be 1GB in size' doesn't make sense. It makes more sense to see the question as a slider with at one end being 'as many small Lambda functions as possible' and the other end being 'as few big Lambda functions as possible'. So let's see what the advantages for each extreme are.

### Many small Lambda functions

Choosing for this option means that you try to cut up Lambda functions as much as possible. The advantages of this are:

- Less impact on a wrong deployment, since the rest of the Lambda functions still work.
- Clear (domain) boundaries between functions, which makes replacing Lambda functions much easier. Since the code size in a function is smaller, there are less internal code dependencies, making it easier to 'untangle' the code and make changes. The total code complexity within a Lambda function is less, making this setup more flexible.
- Each function can be individually tuned and monitored, since this could be different for each one. This could save costs and could make pinpointing a problem more easy, since it can be pinpointed to a specific, small Lambda function.

### Few big Lambda functions

Choosing for this option means that you try to combine Lambda function as much as possible. The advantages of this are:

- Deployments are faster, since you have to build, package and deploy less Lambda functions.
- The setup is often easier, since the dependencies are often between parts within a single Lambda function. For example you don't need a package for shared logic, but can just directly reference the shared logic from different places within the same Lambda function.
- Less Lambda functions to monitor, since there are less in total. This makes the infrastructure landscape easier to monitor.
- A single Lambda function contains more code of the application, making it easier to test and debug locally. From A to Z is all in the software, so you don't need to 'simulate' AWS infrastructure locally (e.g. local SQS, DynamoDB, etc.).

### The actual choice

There's a lot of advantages for each setup and I think it all boils down to the following choice:

- Do you want the complexity (code dependencies, deployments, monitoring, etc.) to be in the infrastructure (many small Lambda functions) or in the software (few big Lambda functions)?

## The sweet middle spot

If you ask me the previous consideration shows what I said earlier: the choice depends on the context. If you ask ten different people, you'll get ten different answers, so let me give my take on it.

I think that the choice is different based on the maturity of the project that I work in. In the beginning when there are a lot of unknowns and value should be delivered quickly, the few big Lambda functions setup works best. Since the domain is probably unclear, it's hard to tell what the right boundaries are for each Lambda. Later on when you start to get a feeling for this, it's easier to split up a single big Lambda function than to move code between many smaller ones. Having to do the latter one is very time consuming, time that you probably don't have.

Another advantage is that with a few big Lambda functions it's much easier to start delivering value more quickly. You don't have to bother with creating packages to share logic, since you would have to figure out how to deploy a library package, how to consume it, how to version it and how to keep it up-to-date in all places. With a few big Lambda's it's easy to make a lot of miles early and postpone a few complexities for later during the project.

At some point, when the application is being used, when the domain is starting to become clear, is the time to gradually cut up Lambda functions. This should really solve some things that have been annoying for some time, like monitoring not being granular enough. Of course it would have been nice if you started with smaller functions straight away, than you wouldn't have to refactor which seems more efficient. From my experience this is almost impossible, due to the many unknowns. You know you're going to shoot yourself in your foot, because you're not going to get it right in one try. At least when working with bigger Lambda functions, the wound is less severe and easier to recover from.

So know you probably think: so I'm going to cut up these big Lambda functions, how should I decicide how I cut it? These are some rules that help me decide on this:

- If the Lambda function has different input and output types, it should be split up per type. For example if a Lambda function is triggered event driven by an SQS queue and triggered on a scheduled basis by EventBridge Scheduler, it should be cut up in a Lambda function for each trigger. This way there is less boilerplate code necessary (no logic needed to decide the type of input) and thus reduces the complexity of the code and chance on bugs (pick wrong trigger type). The same applies for the output type, for an SQS queue it might be necessary to return a batch response, while for an API Gateway an rest response must be returned.
- Another rule is around the functionalities of the function: each functionality should/could be it's own Lambda function. For example a Lambda function calls a database and is called based on events. It receives events with information that should be put in the database and events with requests for information. Within the context of this application, the first type of events is vital and should always be processed as quickly as possible. The second type of event is less important and it's okay if it's slower and fails. The one big flaw here is that the second type of event has influence on the first, vital type of event. Because both are in a single function, it's hard to separate them. If the times the function fails is monitored, how do we know it's from a vital event and the standby team should receive an alert? Each situtation is different, but in this one it's clear that splitting the function up is a good thing.
- Don't mix (sub)domains in a single Lambda function. I think you could even go as far as saying that each Lambda function should just result in a single entity. If it's about more than one entity (e.g. deciding ), it's a bad idea. 
- Should result in something about a single entity

Different inputs & outputs -> hard to monitor & requires extra logic to parse input and output
Lambda does one thing, is about one domain object

## Conclusion
