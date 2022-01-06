---
layout: post
title:  "Book review: The Unicorn Project"
date:   2021-10-13
tags: book
---

_The last time I did a book review was probably some time ago, I guess in highschool, but it might be fun to do another one. Although I still enjoy reading literature like George Orwells 1986, I also read books related to IT. The Unicorn Project is in its core also an IT book. The thing which makes this book interesting, is that it's not a book with only pure theory. The book actually contains a story via which it tries to teach you things, which made me really enjoy this book. Although The Unicorn Project has a precessor called 'The Phoenix Project', the first one named is more relevent for me. The Phoenix Project is written from the perspective of IT operations within a big organization, while The Unicorn Project is from the perspective of developers. Still, the Phoenix Project is interesting to read and even as a developer there are things you can learn from it._

## The story

The story follows Maxine, a senior developer with a few decades of experience. She is part of the company Parts Unlimited, a big organization which flourished a long time ago and currently is starting to fall behind its competitors. In the first few chapters of the book you learn that the company is slowly grinding to a standstill and is doomed to go bankrupt if it doesn't change. Maxine is moved from her well-functioning team to 'The Phoenix Project', an IT project which is the last hope of the company, but when she arrives there she is shocked. There is no working program or environment and she has to scavenger around to find all the things necessary to run the project, like source files, build instructions, credentials, etc. Basically after two years the project has never run in its fulness and no one knows how to do this. The cause is the different departments (development, QA, operations) aren't working together and keep blaming the other one for not delivering what is expected of them. Maxine spends her first two weeks through many different channels to get everything she needs to get a Phoenix build running, but even with her experience this seems like an impossible task. During this hunt she meets 'the rebellion', which is a small group of people from the different departments who are fed up with the current way of working and want to change it. The story continues as Maxine and the rebellion try to change the organisation and are faced with many challenges.

## The five ideals

During the book the rebellion receives help in the form of five ideals. These ideals guide them on solving the companies issues and prevent them from falling back into them. I want to illustrate each of them with a combintation of examples in the book and my own experience within the world of IT. A short description of the ideals can be found in a [blogpost](https://itrevolution.com/five-ideals-of-devops/) by Gene Kim, the author of the book.

### 1. Locality and Simplicity

In the book Maxine clearly struggles with the first ideal when she joins the Phoenix project. It's (nearly) impossible for her to get the build working on her machine. This clearly showed that there was no locality in the systems or simplicity in the depedencies of the project. I have a strong opinion that a person who is new on a project, independent of their programming experience, should be able to push a small change to production on their first day. If a team can't do this or can't even get close, I think it's a sign there still a lot of improvements possible (and necessary) on the first ideal.

In one of my teams I had this exact situation and had a discussion with the other team members about this when a new team member was about to join us. A person said that his experience when he joined the organization frightened him. There was a lot of help needed from the helpdesk to get access to the mail and other things. Thus he didn't want to put pressure on a new person to push anything to production. I agreed with him that there shouldn't be put any presure on new people joining the team, but getting a code change in production is just a measurement, not the goal. It's a good way to show issues in the locality and simplicity of the team. For example it could be necessary to install a lot of undocumented, unlogical depedencies on the laptop to get everything working. The people already on the team went through this and got everything working, so they don't think there are any issues. A new person with a clean laptop can painfully expose these.

Another person said that everyone has different approaches on how they start, some just want to read the documentation first. Although I understand everyone has different approaches, I think the goal of everyone on the team should be to deliver value. The way to do this is to add changes to the code and deploy these to production for the end user to use, not by reading documentation. Documentation is important, but it should be something to support the process. It's not the goal of the team. Just deploying a code change to production on your first day should make every developer happy and something to give you a big energy boost when you freshly join a project. This is actually part of the second ideal, joy.

In the book there was a architecture comitee, which I found quite funny. All big changes within the IT landscape of the company had to pass the comitee, but this rarely happened. For example they still found Apache Tomcat a risk, while this is used all over the internet. During a talk of the writer I saw this example was actually based on a real life example, so it wasn't something he just came up with. I also experienced this myself, where people were really scared of this new thing called 'the cloud'.

### 2. Focus, Flow and Joy

This ideal is about focus on value and working in the right flow resulting in joy. In the book Maxine didn't find any joy in the Phoenix project at first due the lack of focus and flow. She started with creating a flow for programmers so they could focus on delivering value, instead of just firefighting.

Based on Maxine's approach in the book and my own experience I came up with a list of steps to create a flow in which developers can focus on value:

- A stable environment is needed which is able to run everywhere. This prevents mismatches between different dev environments of programmers and test/production environments resulting in programs not running.
  - If the deployment to environments could be automated via Infrastructure as Code would be really cool. From my own experience this simplifies things so much, for example for a pen test you can just spin up a new environment within no time and destroy it after the test with just a few clicks.
  - If you use Infrastructure as Code, I learned that it should also be treated as code. Of course this sounds a bit self explanatory, but in hindsight this made things for the project I was on much easier. By applying best practices like DRY, versioning of releases and other design patterns, it prevents pitfalls they also fix for normal coding.
- Automated deployment (CI/CD) to test and production environments via a pipeline. Of course this pipeline can also be written in code, where the same things apply as the previous point. CI/CD as code should also be treated as code.
- Add test automation in the pipeline. Where I prefer integration and smoke tests above unit tests, since those actually test the whole infrastructur, resulting in catching more 'real' problems.
- Add automatic generation of security reports in the pipeline.
- Add documentation about the product for internal and external use.
- Have a clear process for merging changes using merge requests. Although it's quicker to not require a reviewer for each code change, even if it's just a single line, it prevents mistakes. This is not about not trusting each other, it's about embedding quality and safety in the process.

### 3. Improvement of Daily Work

The third ideal is about improvement of daily work, where Gene Kim gives some interesting ways to do this. For example he says that the most experienced developers should be working on improving on daily work instead of just work. These improvements have a much bigger impact, because they can impact multiple teams instead of just a single team. In many organizations these important tasks are assigned to juniors or even interns.

Another thing I learned from the book is that making mistakes is okay (even in production as illustrated in the book). By making mistakes you can learn from them and improve the next time. A way to do this are blameless post mortems. After reading the book I also did them after we had a production issue. At first I thought about the blameless post mortems too lightly and thought we would just look at the problem and prevent this specific problem from happening again. But they can add much more value, there's more to gain from them. By it being a concrete problem, it allows you to improve based a real problem, instead of fantasizing dubious solutions to a fictional problem. You can find improvements that actually work, because you can discuss whether it would prevent the problem from happening again. I have been in many meetings where solutions were given for fictional problems, which would lead to lengthy discussions without any knowledge being gained from it. They would often end in yes/no debate based on emotion instead of facts.

After finishing the Unicorn project I read the 'take time to slow down', which I think quite nicely summarizes an important part of the third ideal for me:

> Life teaches us through mistakes.\
When you make a mistake,\
simply ask yourself what you were meant to learn from it.\
When we accept such lessons with humility and gratitude,\
we grow that much more.

### 4. Psychological Safety

This ideal, psychological safety, is easy to overlook since it can't be put as an user story on the backlog. In the book Sarah embodies the opposite of psychological safety. She blames everyone for her own problems and has unrealistic expectations of others. As a character she was a funny addition to the book, but I hope I will never have to work with someone like her.

In my experience, I didn't expect psychological safety to be a problem, but I found it out that it doesn't always come naturally. I slowly found out that the team was being divided into two groups: me and the others. During discussions we didn't come to a conclusion. The discussions often ended with going for their way with a bit moved to my view, so I should be satisfied too. But I was getting more unhappy, because I wasn't being understood. This was during the Covid period where we worked remotely as a team for several months, so this didn't make it easier and was probably a big part of the problem. I realized that psychological safety was getting in the way of me delivering value and enjoying my work, because I wasn't being understood and often just gave up on trying to give my opinion.

### 5. Customer Focus

Lastly, but at least as important as the others the fifth ideal: customer focus. The IT products I built and the IT products in the book are mostly build for people, but actually asking people what he or she wants is something pretty rare. Maxine follows a short traineeship for in store personel and she sees the daily work of people working in the shops of the company. She learns that they have tablets with apps specifically made for them, but they don't use it because it's not user friendly.

From my experience actually talking with people who use it teaches me so much. I worked in a organisation which does scientific research, but the first few months I rarely talked at all with researchers while I was building a product for them. After reading The Unicorn Project I actually started talking with them and this gave me new insights on what they want (and what they don't want). I learned that the researchers were actually interested in something which was easy to build, but was really valuable for them.

## DevOps

The main theme of this book is DevOps, all of the ideals are part of being a good DevOps organisation. For me this is a vague thing, I thought it was just about Dev and Ops working together, but there's much more to it. This change brings so many improvements and solves many issues in current, big organisations. Some facts that Gene Kim (the writer) showed during one of his presentation really made the impact of DevOps clear for me:

| Measurement          | Elite                              | Low                  | Difference |
| -------------------- | ---------------------------------- | -------------------- | ---------- |
| Deployment frequency | On-demand (multiple times per day) | Monthly or quarterly | 208x       |
| Deployment lead time | < 1 hour                           | 1 week to 1 month    | 106x       |
| Deploy success rate  | 0-15%                              | 46-60%               | 7x         |
| Mean time to restore | < 1 hour                           | Less than one day    | 2,604x     |

_Difference between elite and low performers based on the [State of DevOps report of 2019](https://services.google.com/fh/files/misc/state-of-devops-2019.pdf)_

## Conclusion

It was fun to do another book review, although it was a bit different from the ones I did in highschool. I didn't give my opinion about the book that much, but I added a lot of my own experience to compensate. Which is a good plus point for the book, since it inspired me to think about these things and look at them from my own perspective. By it being written as a real life story, it helped me in looking at my current and previous working environment. It's fun to read the book with others and identify similar patterns on your own environment and improve these. So I definitely think the book is interesting to read and shows in a fun way the positive impact DevOps can have on every organisation.
