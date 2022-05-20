---
layout: post
title:  "Kotlin learnings from Kotlin Dev Day 2022"
date:   2022-05-20
tags: kotlin
---

_On May 19th I visited the Kotlin Dev Day 2022, which is a yearly conference about Kotlin in the Netherlands. I recently started using Kotlin for my new job, so I was really curious about all the talks. Also, I never went to a conference, so I looked forward to it. In the end it was a really fun day and in this post I'll share my biggest learnings of that day._

## Kotlin best practices

In the last few months I really had to get used to Kotlin and I was a bit hesitant about it at first, but right now I'm liking it more and more. During the conference there were different talks about the features of the language. These are the biggest learnings for me (or things I already knew but should do more):

- Kotlin didn't invent something revolutionary, it mostly combines the best features of other programming languages. This makes it an intuitive language that has about everything you need to write clean and clear code.
- It's possible to create [extension functions](https://kotlinlang.org/docs/extensions.html#extension-functions), which allow functions to be added to an already existing class. I knew this existed in C# and was a big fan of it. It's encouraged to also use them in Kotlin, since it keeps the original class clean. For example, the `String` class in Kotlin only has a [handful of functions](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-string/#functions), while most functions are [extension functions](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-string/#extension-functions). 
- Use expression oriented programming instead of comparative programming. In Kotlin it's possible to use functions as a variable, which makes it possible to have [higher-order Functions](https://kotlinlang.org/docs/lambdas.html) (functions with a function as parameter or as return value). This is the biggest feature that made it hard for me to understand Kotlin at first, because it introduces a lot of small scopes, e.g. the scope within the parameter function. The biggest benefit of all these extra scopes is to have fewer side-effects in your code, because variables are limited to a much smaller scope now.
- Try to always use immutability, because it reduces the chance on side-effects. Kotlin already has a lot of language features to support immutability: `val`, `listOf` and `copy()`. 

## Kotlin decompiled

The `Kotlin dekompiled` talk was definitely my favorite, because it showed how many language features (e.g. the ones shown in the previous paragraph) work under the hood. The idea he used was actually quite simple, but really clever: he compiled Kotlin code to JVM byte code and used [CFR](https://www.benf.org/other/cfr/) to decompile the byte code in Java code. I'll definitely use this idea to also dive more into the Kotlin 'magic' myself.

So Kotlin and Java both compile to JVM byte code and are thus both also limited to the same possibilities that JVM byte code has. All the extra Kotlin features (aka 'magic') are made possible during the compilation to byte code. The Kotlin compile `kotlinc` compiles the Kotlin code to byte code and does a lot more code replacement in comparison to the Java compiler:

- It does simple replacements: replace [for (x: Int in 1..100) { ... }](https://github.com/The-Self-Taught-Software-Engineer/kotlin-decompiled/blob/master/src/main/kotlin/iterateoverrange/kotlin/IterateOverRange.kt#L5) with [do { n++; ... } while (n <= 100)](https://github.com/The-Self-Taught-Software-Engineer/kotlin-decompiled/blob/master/src/main/java/iterateoverrange/java/IterateOverRange.java#L9)
- It does more complex replacements: a sealed interface in [Kotlin](https://github.com/The-Self-Taught-Software-Engineer/kotlin-decompiled/blob/master/src/main/kotlin/sealedinterface/kotlin/SealedInterface.kt) and in [Java](https://github.com/The-Self-Taught-Software-Engineer/kotlin-decompiled/blob/master/src/main/java/sealedinterface/java/SealedInterface.java)
- The Kotlin compiler also add `@metadata` tags to the methods in the byte code. These don't do anything when the byte code is run, but allow Kotlin features to be persisted when the byte code is again imported as a library in another project. The `@metadata` annotation includes for example that a variable is not nullable, so the Kotlin code which uses the variable knows this. 

All these extra steps make compilation of Kotlin slower than Java, but at runtime it still runs at a similar speed. The code examples for all Kotlin features can be found [here](https://github.com/The-Self-Taught-Software-Engineer/kotlin-decompiled).


## Kotlin MultiPlatform

Besides Kotlin being able to run in the JVM, it's also possible to be run compiled to different platform: JS code and native code. Kotlin calls this [Kotlin Multiplatform](https://kotlinlang.org/docs/multiplatform.html). An use case for this might be to run the same piece of Kotlin code on both Android and iOS. This opens up a lot of possibilities that I still have to figure out. One of them is to see what the performance impact is for Kotlin code in a lambda when it's compiled for a different platform. During the Dev Day there was an interesting talk about porting a single piece of Kotlin code to multiple platforms, the code of it can be found [here](https://github.com/KodeinKoders/Playground-Demo-Crypto).

## Kotlin Coroutines

I already used coroutines a bit and I was impressed by how much quicker it made my code, but I didn't fully understand what I did. I sometimes just randomly changed my code until it worked (oops 😇). So here we go:

- There can be certain points within a function, e.g. network I/O, disk I/O, sleep, when the function has to wait and doesn't do anything
- At that point a function can be suspended and free the CPU to do something else until the function can be resumed
- A function can be made suspendable by adding the `suspend` keywords
- When the function gets suspended, the state it's in is saved and it can be used to resume the function execution again like it didn't get suspended
- The function execution does not have to be resumed on the thread it was stopped at, it will be resumed at the thread which is ready to pick up work
- Functions being able to be suspended makes it possible to do multiple things in parallel on a single thread
- A [CoroutineScope](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/index.html) is a scope within which coroutines (suspendable execution of functions) can be run
- The CoroutineScope object can be used to influence the child coroutines, for example: if one of the child coroutines has an error, all other child coroutines can be cancelled
- The CoroutineScope object contains configuration (coroutine context) about how the coroutines are run, of which an important one is the [CoroutineDispatcher](https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html)
- The type of the configured CoroutineDispatcher allows the coroutines to be ran on multiple threads.
- Kotlin has some [default CoroutineDispatchers](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-dispatcher/index.html), but it's also possible to configure your own
- The `runBlocking` command will start a coroutine and keep the thread it's called from running, which is not efficient except when: to go into coroutine context from the main method or for unit testing

## Conclusion

During the conference I saw a lot of cool presentations and it increased my Kotlin knowledge in width and depth. I'm starting to fall in love with Kotlin more and more. I think it's a versatile language which can be used in many situations due to the multiplatform possibilities. There's one big downside though that was also often joked about during the talks: Gradle sucks to work with. If it's possible, I'll definitely try to also go to the next Kotlin Dev Day conference.