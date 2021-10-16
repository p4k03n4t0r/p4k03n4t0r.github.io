---
layout: post
title:  "One layer deeper"
date:   2021-10-16
tags: debugging, way-of-thinking
---

_Although I have not been a programmer for a long time, I have found out being to go one layer deeper when programming helped me a lot. Being able to do this, really made the difference for me in whether I was able to find an issue and solve it. Looking around I can clearly see that people who are able to do this, are the ones who really understand how things work and leverage this power to do cool things. In this post I'm going to talk a bit more about what I mean with 'going one layer deeper' and give five tools of my toolbet which help me to dive deeper._

## Why should I go deeper?

The world of IT is built up of layers on top of other layers. This goes from applications, to code, to assembly, all the way to the actual hardware. Of course when programming in for example Python, you don't want to be bothered with writing binary executables, that's exactly why you use a programming language. But sometimes things don't work out when working at an upper layer and you encounter a weird error. The power to be able to dive deeper could help you in understanding what is happening and solve the issue in the right way. I see the opposite happening a lot: people googling and copy-paste answers from Stackoverflow till they see the output they expect, but in the end they don't understand what they did. Although diving one layer deeper is a lot more effort than this, for me I learn a lot by it. This knowledge I take with me and I found out that it often comes in useful later on. 

> Programming languages and frameworks may change, but the principles underlaying them often stay the same. A computer still has a CPU, memory, network connectivity, although what is on top has changed a lot and will surely change in the future. 

## Tools that might help

Being able to dive deeper is not some talent, but it's a skill you can learn. As long as you want to dive deeper and really understand what is going on, you'll be to learn it. For me it takes times and a lot of trying, failing, trying more, failing more and finally figuring it out. While going through this process a lot of times I have acquired different tools. When I encounter a new problem, I often try to dive deeper with these tools. By sharing them, I hope this might be a start for others to peel off the first layer in diving deeper.

### Websites: Chrome DevTools

For debugging websites I often use the [Chrome DevTools](https://developer.chrome.com/docs/devtools/). When using Chrome or a Chromium based browser, you already have the DevTools out-of-the-box available. It allows you to view the network calls made from the browser, which is useful to see why a call failed or find hanging calls. DevTools has many more features, personally I have just skimmed the surface of them.

### HTTP(S): Fiddler

Often it happened that HTTP(S) calls were being made by a program I used or a framework I chose that resulted in something that I didn't expect. For me it helps to use [Fiddler](https://www.telerik.com/fiddler/fiddler-everywhere) in these cases. It allows you to view all the HTTP and decrypted HTTPS calls made from your computer. The nice thing is that it also allows the replaying of made calls and editing them. This saves a lot of time to debug why a certain call does or doesn't work, since triggering the call sometimes requires minutes of restarting a program.

### Network traffic: Wireshark

Fiddler is nice for debugging HTTP(S) traffic, but it's just the top of the iceberg of network traffic. If you want to go deeper and look at TCP level or take a look at different protocols, like DNS, I think [Wireshark](https://www.wireshark.org/) is the best tool. It might need a bit of figuring out how the filtering works, but if you understand how it works, it's a really powerful tool. I also use it to debug network traces from machines on which I don't have a GUI. I do this by capturing the traffic on a network card using [tshark](https://www.wireshark.org/docs/man-pages/tshark.html) and viewing the gathered data in my own Wireshark.

### Programming languages: VSCode Debugger

Although it seems like a no-brainer to use a debugger when programming in for example Python or C#, I see people not fully using its power. A debugger is often able to do much more than just the code you wrote, it's also able to debug the libraries you use. Sometimes when using a function of a library, the documentation isn't sufficient. The best thing to do is just take a look at the code of the library while it is ran. If you can write and debug your own code in a language, why wouldn't you be able to understand a library in the same language? A small bonus is that you can learn from code being written by others.

Personally I use VSCode as my IDE, since it supports all the languages that I use and is fairly light-weight. In here it's really simple to also debug the code of libraries. For example in Python you just have to set the [`justMyCode`](https://code.visualstudio.com/docs/python/debugging#_justmycode) flag to `true`. Of course debugging is possible in almost every IDE and this feature is surely available in different IDE's and programming languages. It's just the question whether you want to find it ;).

### Linux: gdb + pwndbg

When you execute a command in Linux, for example a simple `ls`, a process is started. This is also the case when you run a complex Python program with `python main.py`. In the end Python is just there for programmers to make it easier to write a program while not having to focus on basic things like memory allocation. But it's good to realize that Python, or any other programming language, is just an extra layer which can be peeled of. Of course Python is there so you shouldn't have to do this, but understanding what Python does for you helps you improve writing better Python. It also makes it easier for you to pick up other programming languages (C#, Java, etc), since they are also just layers on top of Linux processes. 

Taking a look at the Linux processes is a bit scary, since it goes to the core of what a computer is. It's not something you can understand by reading a few books, but I think only if you write an operating system yourself. Still already understanding the basics can help you a lot. For Linux I have found myself using [gdb](https://www.gnu.org/software/gdb/) with [pwndbg](https://github.com/pwndbg/pwndbg) as plugin. Taking a look at just a simple process like `ls` with gdb can already be really overwhelming. For me it helped to take it step by step and be okay with not understanding all of it straight away.

### Windows: Sysinternals

For Windows applies the same as Linux, really understanding it takes years and years of practicing, but having the right tools helps you in this quest. For Windows [Sysinternals](https://docs.microsoft.com/en-us/sysinternals/) is a set of tools which basicly has everything you need. I would recommend to watch the talks of Mark Russinovich, the original creater, to better understand the usage of each tool. Especially the series [The Case of the Unexplained](https://docs.microsoft.com/en-us/sysinternals/resources/webcasts) are interesting and besides that also entertaining.