---
layout: post
title:  "Random network error"
date:   2022-01-11
tags: []
---

_Intro_

VPN, couldn't reach internal websites
Checking whether there was something wrong with my VPN, no result, must be my laptop
Could reinstall Linux, but that takes some time and effort
Instead try to find the issue
Redacted and changed some info to hide sensitive info

Didn't have any experience with this, so had to start form 0
Using VPNC as VPN. Connection with VPN is successful
Look at the syslogs, but nothing weird in there.
Could reach sites on the internet, but not internal websites
Nslookup works, but curl failed
It's not at the HTTP level, but a network layer deeper.
Dive layer deeper

Connect with IP: use traceroute
Traceroute to internal website hangs
Interesting fact: the ip address the packet leaves from is different between external and internal website
ifconfig shows that internal website leaves from a br interface
This is a bridge interface
Let's look at the routes: ip route show
Shows the ip address of the internal website is within the subnetmask which points to the bridge interface
This confirms our internal website is handled by the br interface
With curl we can test whether using the tun0 (tunnel of VPN) interface works:
curl --interface tun0 https://internal.com
curl --interface br-1b3127d0ef29  https://internal.com
This works!

What is this br interface? Can we just remove it?
It's a bit a wild guess, but I know Docker uses bridge networks to port forward from docker networks to the host.
Use docker network ls
Use docker inspect <name> -> IPAM -> Config -> Subnet matches with what is shown in ifconfig
The network was created by running a docker-compose, so can just be removed.
After removing everything works again! Yay.

Conclusion
I have no clue how it works, but it works, I just use HTTP. Instead of guessing, it's best to dive into it and try to find out what's happening. There's always a command to see what's happening under the hood. Still more to figure out, like how does DNS work combined with a tunnel, but for now how it works looks as follows:

<image>
DNS (nslookup) -> Get IP Address -> ip route show: decide on interface -> Use interface to find route to the target
Interface tun0 is a tunnel