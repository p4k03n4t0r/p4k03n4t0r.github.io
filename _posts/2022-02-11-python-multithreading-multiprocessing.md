---
layout: post
title:  "Python Multithreading and Multiprocessing"
date:   2022-02-24
tags: []
---

_During technical interviews for a job I have often been asked what multithreading is. I could often explain what it does, but explaining how it works was a different piece of cake. When doing Python I even found out there's besides multithreading also multiprocessing, now I was completely lost. It took me some time to understand what made them different and also how and when to apply them. Still there's much more to learn about it, but I feel like I understand the basics of it. 

## What are threads and processes?

Although programming languages may look very different, under the hood they often use similar components. 


## Multithreading in Python

GIL + single core
Java uses multicore, multiple threads can run at the same time

Example with time comparison

## Multiprocessing in Python

Use system to orchestrate processes instead of programming language
Java can do it, but wouldn't recommend https://stackoverflow.com/questions/8001966/how-to-do-multiprocessing-in-java-and-what-speed-gains-to-expect

New process has relative more overhead than new thread
Show with example

## When to use which

Multiple long running work jobs -> either multithreading of processing
If work jobs contain lots of calculation and runs longer -> multiprocessing

## Pitfalls

GIL not 100% threadsafe

Passing variables between processes is tricky and could slow down the performance by a lot

## Conclusion