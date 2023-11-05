---
layout: post
title: 'Multi-AZ Aurora: roulette edition'
date: 2023-11-05
tags: rds, aurora, multi-az
---

_For a project I worked on we were looking for a serverless database that allowed aggregations, so that logical choice we ended up with was RDS Aurora. My expectation was that I didn't have to bother with certain infrastructure challenges like high availability, since the service is serverless. It turned out the Aurora had some hidden suprises for me, namely a multi-AZ roulette which in certain situation would result in cluster that was not highly available. In this blog post I'll dive into this situation and how to prevent leaving the AZ placement to luck._

Disclaimer: RDS aurora can be an expensive service, although it's called 'serverless', it still costs money even if you don't use it.

## Serverless expectations

For most applications it's necessary that each resource is deployed redundantly to ensure [high availability](https://aws.amazon.com/blogs/startups/how-to-get-high-availability-in-architecture/). When choosing serverless, this responsibility is shifted to AWS. This is one of the selling points for serverless on AWS, as can be read [here](https://aws.amazon.com/serverless/). This is especially for databases a nice feature, since setting up a database cluster with multiple nodes introduces many challenges: data replication, data consistency, failover and more.

How Aurora works with AZs: cluster is region bound, instance is AZ bound
https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraHighAvailability.html

Expectation: they will divide the instances over AZs (similar to what EC2 does: https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html#arch-AutoScalingMultiAZ)

## The situation: changing the cluster instance type of the instances

- Run cluster with 2 instances: writer + reader
- Want to replace it with different type or instance size, so spin up two new instances (old instances are not kept by default)
- Possibility: two new instances are in same AZ
- Than remove old two instances, no data is lost en writer permission is transferred to other nodes
- Result: two remaining instances in same AZ
- Expectation: Aurora notices this and rebalances one instance to another AZ, except it doesn't

## Preventing the RDS roulette

Can't set the AZ, but you can influence it by the following logic (expectation is that the AZ has 3 regions, as most regions have: https://aws.amazon.com/about-aws/global-infrastructure/regions_az/):

- If there are two instances in two AZ's and you create a new one: it will always be in places in the third AZ
- If there are three instances in three AZ's, when you create a new instance it's roulette style placed in one of the three AZs
- Thus: can't directly control the AZ, but can indirectly control it by not leaving it to luck where the AZ is placed

Steps:

- Add them one by one:
- Add new reader
- Remove old reader
- Add new writer
- Remove old writer

Or: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/blue-green-deployments-creating.html

## Conclusion

- Test on non-production and/or in simplified situation
