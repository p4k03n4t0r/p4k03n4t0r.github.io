---
layout: post
title:  "Thanks Docker"
date:   2022-01-18
tags: []
---

_I was just minding my daily programming and all of a sudden the VPN I use for work didn't work anymore. After a lot of rabbit-holing I found out that it was something which seemd completely unrelated: Docker. I'll take you with my journey on finding out how I got there, hopefully it's interesting and you can learn something from as I did._

## My VPC is broken

During my regular daily work I suddenly couldn't reach any internal websites anymore when using my VPN. At first I thought there was something wrong with my VPN. I could reach external websites, but not internal anymore. A `nslookup` for an internal website did return the right IP, but I couldn't resolve it. Since I'm not a VPN or Linux networking expert, I assumed it could be my VPN configuration which prevents reaching the internal IP addresses. After a lot of debugging I didn't find the issue and was almost at the point where I thought it was easier to just reinstall Linux. Instead I gave it a last try to find the issue, this time by zooming out a bit first.

## Zooming out

So I can do a DNS call, but I can't do a HTTP call with for example cURL. cURL showed that it couldn't connect with the IP address, so it's not a problem at the HTTP layer. I'll have to dive a layer deeper to find out more. 

```
➜  nslookup internal.website
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
Name:	internal.website
Address: 172.22.1.18

➜  curl https://internal.website
curl: (7) Failed to connect to internal.website port 443: No route to host
➜  curl google.com
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>

```

For this I use `traceroute`, which shows the packets on IP level. The traceroute also hangs, but does show something interesting: the source IP address of the call. When doing a `traceroute` call to an external website it shows a different source IP. 

```zsh
➜ traceroute 172.22.1.18
traceroute to 172.22.1.18 (172.22.1.18), 30 hops max, 60 byte packets
 1  paul-laptop (172.22.0.1)  3050.424 ms !H  3050.379 ms !H  3050.369 ms !H
```

The IP address ends with a 1, which often indicates that it's the gateway of a network. Let's find out more about this IP address. In `ifconfig` all the network interfaces are listed with their IP. And it showed something interesting: the source IP addresses matches with that of one of the interfaces:

```zsh
➜  ifconfig           
br-20ae57582e2: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.22.0.1  netmask 255.255.0.0  broadcast 172.22.255.255
        ether 02:42:a2:97:44:76  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
... other network interfaces
```

Before diving into this interface, it's still not clear to me why external and internal calls get picked up by different network interfaces. The answer to this can be found by using `ip route show`:

```zsh
➜  ip route show
default dev tun0 proto static scope link metric 50 
172.22.0.0/16 dev br-20ae57582e2 proto kernel scope link src 172.22.0.1 linkdown 
... other rules
```

It shows that all IP addresses within the 172.22.0.0/16 subnet will be routed using the br interface. If an IP is not within this subnet (or within the other rules which I left out), it will be picked up by the the `default` rule and the `tun0` interface is used. This is the interface of the VPN, which explain the difference in routing. It's actually quite easy to try out whether the internal websites can be reached using the tun0 interface instead of the br one:

```zsh
➜  curl --interface br-20ae57582e2 https://internal.website
curl: (7) Failed to connect to internal.website port 443: No route to host
➜  curl --interface tun0 https://internal.website
<html><body>Welcome!</body></html>
```

This works, I love cURL! :D

## Finding the villain

So what is this magic br interface? Can we just remove it or is it something important? After searching online it turns out br stands for bridge. It's a bit a wild guess, but I know Docker uses bridge networks to port forward from docker networks to the host. Let's find out:

```zsh
➜  docker network ls          
NETWORK ID     NAME                             DRIVER    SCOPE
5b085d79382a   bridge                           bridge    local
4c90568f477c   host                             host      local
e33e017585e2   http-request-smuggling_default   bridge    local
➜  docker inspect e33e017585e2            
[
    {
        "Name": "http-request-smuggling_default",
        "Scope": "local",
        "Driver": "bridge",
        "IPAM": {
            "Driver": "default",
            "Config": [
                {
                    "Subnet": "172.22.0.0/16",
                    "Gateway": "172.22.0.1"
                }
            ]
        }
    }
]

```

So now the pieces fell into place. I was using docker-compose and when running `docker-compose up`, a new Docker network will always be created. This network is a bridge network and it overlapped with the IP addresses of the internal websites I wanted to reach. That's some bad luck! Since it's a disposable Docker network, I just remove it and everything works as expected again.

## Conclusion

Again I learned something new about computers (in the hard way). I went through all the possible causes of the issue and when I got stuck I zoomed out. This helped me think outside of the box and in the end find the issue. For the next time I encounter another problem (which is sure to happen), the gained knowledge might be helpful. There's still more to figure out, like how the `tun0` tunnel interface works, but that's something for another time to dive into.
