---
layout: post
title:  "A random error message"
date:   2022-01-04
tags: [vscode]
---

_I've been using Visual Studio Code for quite a while as an editor, but recently I got some random error message when I opened it from the command line. It wasn't a clear error message and VSCode didn't act weird, so I just ignored it for a while. But after some time it starting annoying me that I didn't know why the error was there, I had to find out. In this post I'll take you on my journey of finding out what the cause is of a random error message. Spoiler alert: it turned out to be a bit of a rabbit hole, so I didn't get quite tot he bottom of it. Still I did find out a lot about the cause and learned a lot on the way._

## It all started with...

I always use my terminal to go around the file system and when I have to open a directory or file I use code to open it. But suddenly I got the following error when I did this:

![Screenshot]({{ site.url }}/assets/2022-01-04-random-error-message/screenshot.png)

Let's dissect the message to better understand what it says.

## /usr/local/lib/AppProtection/libAppProtection.so

The first part mentions the file `/usr/local/lib/AppProtection/libAppProtection.so`. Let's find out what this file is:

```zsh
➜  ~ file /usr/local/lib/AppProtection/libAppProtection.so         
/usr/local/lib/AppProtection/libAppProtection.so: symbolic link to /usr/local/lib/AppProtection/libAppProtection.so.1.6.7.26
➜  ~ file /usr/local/lib/AppProtection/libAppProtection.so.1.6.7.26
/usr/local/lib/AppProtection/libAppProtection.so.1.6.7.26: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=bb695530d7a28feb6c8d69e844168513b0e09724, stripped
➜  ~ head -n 10 /usr/local/lib/AppProtection/libAppProtection.so
ELF>�[@p(@8@LL gibberish ...
```

The file points to a shared object (interchangeably used with shared library). The definition is:

> A shared object is an indivisible unit that is generated from one or more relocatable objects. Shared objects can be bound with dynamic executables to form a runable process. As their name implies, shared objects can be shared by more than one application. [Source](https://docs.oracle.com/cd/E19120-01/open.solaris/819-0690/6n33n7f8u/index.html)

Actually there are already a lot of shared object files on a Linux machine under the `/lib` folder, where arguably the most used one is libc:

>  The term "libc" is commonly used as a shorthand for the "standard C library", a library of standard functions that can be used by all C programs (and sometimes by programs in other languages). Because of some history (see below), use of the term "libc" to refer to the standard C library is somewhat ambiguous on Linux. By far the most widely used C library on Linux is the GNU C Library ⟨http://www.gnu.org/software/libc/⟩, often referred to as glibc.  This is the C library that is nowadays used in all major Linux distributions. <br>
[Source](https://man7.org/linux/man-pages/man7/libc.7.html) or run `man libc`.

We can easily check the loaded shared objects using GDB, for example for a simple command like `ls`:

```zsh
➜  ~ gdb ls           
GNU gdb (Ubuntu 9.2-0ubuntu1~20.04) 9.2
...
pwndbg> run
Starting program: /usr/bin/ls 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
 Desktop     Downloads  Pictures	Templates     
 Documents   Music      snap      Videos 
[Inferior 1 (process 16590) exited normally]
pwndbg> info sharedlibrary
From                To                  Syms Read   Shared Object Library
0x00007ffff7fd0100  0x00007ffff7ff2674  Yes (*)     /lib64/ld-linux-x86-64.so.2
0x00007ffff7da7b90  0x00007ffff7dbd22f  Yes (*)     /usr/local/lib/AppProtection/libAppProtection.so
0x00007ffff7d68040  0x00007ffff7d7f4fd  Yes (*)     /lib/x86_64-linux-gnu/libselinux.so.1
0x00007ffff7b94630  0x00007ffff7d0920d  Yes         /lib/x86_64-linux-gnu/libc.so.6
0x00007ffff7b53ae0  0x00007ffff7b634d5  Yes         /lib/x86_64-linux-gnu/libpthread.so.0
0x00007ffff7b47220  0x00007ffff7b48179  Yes         /lib/x86_64-linux-gnu/libdl.so.2
0x00007ffff7a220c0  0x00007ffff7aab766  Yes (*)     /lib/x86_64-linux-gnu/libX11.so.6
0x00007ffff79e8620  0x00007ffff79fb699  Yes (*)     /lib/x86_64-linux-gnu/libxcb.so.1
0x00007ffff7899160  0x00007ffff7981452  Yes (*)     /lib/x86_64-linux-gnu/libstdc++.so.6
0x00007ffff77eb460  0x00007ffff77f5d1b  Yes (*)     /lib/x86_64-linux-gnu/libXi.so.6
0x00007ffff775b2e0  0x00007ffff77bed8e  Yes (*)     /lib/x86_64-linux-gnu/libpcre2-8.so.0
0x00007ffff7754360  0x00007ffff7755052  Yes (*)     /lib/x86_64-linux-gnu/libXau.so.6
0x00007ffff774b1a0  0x00007ffff774ca03  Yes (*)     /lib/x86_64-linux-gnu/libXdmcp.so.6
0x00007ffff76093c0  0x00007ffff76aff18  Yes         /lib/x86_64-linux-gnu/libm.so.6
0x00007ffff75e25e0  0x00007ffff75f3045  Yes (*)     /lib/x86_64-linux-gnu/libgcc_s.so.1
0x00007ffff75ce5e0  0x00007ffff75d884e  Yes (*)     /lib/x86_64-linux-gnu/libXext.so.6
0x00007ffff75b4e40  0x00007ffff75c2e69  Yes (*)     /lib/x86_64-linux-gnu/libbsd.so.0
                                        No          linux-vdso.so.1
(*): Shared library is missing debugging information.
```

We can see libc.so is loaded and also some other shared objects. But wait, there's also another library which looks familiar... It's the library that is also mentioned in the error message. The command `ls` doesn't throw an error, but it does load the library. I checked some other basic commands like `cd` and `file` and these also load `libAppProtection.so`. That's interesting and scary... Could this be a virus? It silently loads for every command I run and I'm not sure what it does. Maybe the rest of the error message tells us more about it.

## /etc/ld.so.preload

The next part of the error message mentions another file: `/etc/ld.so.preload`. Let's find out more about this file:

```zsh
➜  ~ file /etc/ld.so.preload                                                         
/etc/ld.so.preload: ASCII text
➜  ~ cat /etc/ld.so.preload              
/usr/local/lib/AppProtection/libAppProtection.so
```

So this `ld.so.preload` file contains a reference to the loaded shared object. Using the magic internet I found there is a man page `ld.so`:

> **ld.so: dynamic linker/loader**<br>
The programs ld.so and ld-linux.so* find and load the shared
objects (shared libraries) needed by a program, prepare the
program to run, and then run it.<br>
...<br>
**FILES**<br>
/etc/ld.so.preload<br>
File containing a whitespace-separated list of ELF shared
objects to be loaded before the program. ... /etc/ld.so.preload has
a system-wide effect, causing the specified libraries to
be preloaded for all programs that are executed on the
system.  (This is usually undesirable, and is typically
employed only as an emergency remedy, for example, as a
temporary workaround to a library misconfiguration issue.<br>
[Source](https://man7.org/linux/man-pages/man8/ld.so.8.html) or `man ld.so`

So this is the cause for the AppProtection SO being loaded for every program, even when running a simple `ls`. I didn't know this existed it and although it could be handy for virus scanners, it also could be abused by the exact thing they try to prevent. Let's find out more about this AppProtection binary.

## AppProtection: What is it?

AppProtection is a shared object which VSCode uses, so it's not part of VSCode itself but could technically be used by other programs. 
VSCode works fine although the shared object isn't loaded as the error message stated. An assumption could be that an installation of another program placed AppProtection in ld.so.preload and that VSCode triggers an error in the shared object. Let's try to find who might have installed AppProtection.

After some searching online I find [AppProtection by Citrix](https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/secure/app-protection.html). I recently installed this client, so there's a big chance this is the same AppProtection. (Also Citrix being more Windows focussed and the files being in camel-case might already be a good hint)
I don't know where the application is installed, so let's find out.
I boot the program, run htop and filter (F4) for Citrix:

![htop]({{ site.url }}/assets/2022-01-04-random-error-message/htop.png)

It turns out Citrix Workspace is located in the /opt/Citrix/ICAClient folder:

```
➜  ICAClient ls
adapter            eula.txt             OPUS.DLL            UtilDaemon         VDSCARD.DLL
ADPCM.DLL          gtk                  PDCRYPT1.DLL        VDBROWSER.DLL      VDSCARDV2.DLL
aml                help                 PDCRYPT2.DLL        VDCAM.DLL          VDTUI.DLL
AUDALSA.DLL        icasessionmgr        PKCS#11             VDGSTCAM.DLL       VDWEBRTC.DLL
AUDOSS.DLL         icons                pkginf              VDHSSPI.DLL        VORBIS.DLL
AuthManagerDaemon  keyboard             PrimaryAuthManager  VDIME.DLL          wfica
cef                keystore             selfservice         VDMM.DLL           wfica.sh
CHARICONV.DLL      lib                  ServiceRecord       VDMRVC.DLL
clsync             libproxy.so          site                VDMSSPI.DLL
config             NativeMessagingHost  SPEEX.DLL           VDNSAP.DLL
desktop            nls                  util                VDPORTFORWARD.DLL
```

More capitalized letters, even the file extensions are now in capital case.
There are quite a few executables in there, so let's use the tree function in htop to find out the one responsible for booting the program:

![htop2]({{ site.url }}/assets/2022-01-04-random-error-message/htop2.png)

There's many processes and subprocesses running. To find the actual one, I just closed the Citrix Workspace program and the following tree disappeared: `/opt/Citrix/ICAClient/selfservice --icaroot /opt/Citrix/ICAClient`. Running this results in what we expect: the program boots. 

A simple fix would be to disable the loading of AppProtection in LD_PRELOAD. I tried this and even the Citrix Client still worked as expected. Still I wasn't happy with this, because it didn't explain why the error was thrown for VS Code and not for other programs.

## Diving in the shared object

As said before, the shared object is an ELF binary. This means it boils down to assembly and system calls. The assembly contains the logic, but the system calls tell more about what the program tries to do. For example syscalls can be reading from or writing to sockets or files. A full list for the x86 syscall can be found [https://filippo.io/linux-syscall-table/](here). When you have a specific system call, it's also possible to just use `man`, so for example: `man mmap`.

There's many ways to dissect the binary, but let's start simple. Using `strace` we can get a dump of all system calls which are done. Maybe this shows the system call leading to the error:

```
➜  strace code . 2> out.txt
➜  cat out.txt
...
# open filedescriptor to the shared library file, where the number of the filedescriptor is 3
openat(AT_FDCWD, "/usr/local/lib/AppProtection/libAppProtection.so", O_RDONLY|O_CLOEXEC) = 3
# read 832 bytes from file descriptor 3 into a buffer
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\220[\0\0\0\0\0\0"..., 832) = 832
# get the status of the file descriptor, I don't know what is done with it
fstat(3, {st_mode=S_IFREG|0755, st_size=142960, ...}) = 0
# create new space in the memory which the program can use
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f998aacb000
mmap(NULL, 2246088, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f998a8a6000
mprotect(0x7f998a8c8000, 2093056, PROT_NONE) = 0
mmap(0x7f998aac7000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x21000) = 0x7f998aac7000
mmap(0x7f998aac9000, 5576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f998aac9000
# close the file descriptor
close(3)  
...
```

There's a lot of system calls being done and most are probably part of the regular behaviour of VS Code. Searching through the file, I found the above. It looks like a file descriptor for the AppProtection SO get opened, some content of it is read and finally the file descriptor gets closed. Besides that also some memory gets allocated, which is interesting. In the original error there was also something about mapping memory: `failed to map segment from shared object`. Could it be that the library is being loaded, but something goes wrong with mapping it into memory?

The way LD_PRELOAD SO's are loaded is part of all gcc compiled binary: https://stackoverflow.com/questions/58565970/how-does-ld-preload-update-the-library-function. This means we would have to dive into the way the SO binaries are loaded. I tried to debug this using GDB, but with my limited knowledge it's a maze with no end. A possibility to make this easier, is to have the symbols with it. This allows mapping of assembly and system calls to the original programming language it was written in. 

I tried to debug with gdb to see whether I could find the cause of the error, but without symbols it's a maze with no end. Luckily VS Code is [open source](https://github.com/microsoft/vscode), which means I can compile it locally and include the debug symbols. But unfortunately when this VS Code is ran, no error is thrown...

## Snap sandbox

I was a bit stuck now, but a friend of mine gave me a good hint. All applications installed via Snap run in a sandbox environment, kind of similar as a Docker container. If VS Code was installed with Snap, it could mean the sandbox blocks the call to load the shared library. And indeed VS Code is installed with Snap:

```
➜  ~ whereis code
code: /snap/bin/code /snap/bin/code.url-handler
```

This also explains why the VS Code compiled from source, doesn't throw the error. It's not running within the Snap sandbox. To confirm Snap is indeed the culprit, let's start another app installed via Snap:

```
➜  ~ snap list       
Name                             Version                     Rev    Tracking         Publisher     Notes
code                             ccbaa2d2                    82     latest/stable    vscode✓       classic
postman                          8.12.5                      149    v8/stable        postman-inc✓  -
➜  ~ postman          
ERROR: ld.so: object '/usr/local/lib/AppProtection/libAppProtection.so' from /etc/ld.so.preload cannot be preloaded (failed to map segment from shared object): ignored.
ERROR: ld.so: object '/usr/local/lib/AppProtection/libAppProtection.so' from /etc/ld.so.preload cannot be preloaded (cannot open shared object file): ignored.
ERROR: ld.so: object '/usr/local/lib/AppProtection/libAppProtection.so' from /etc/ld.so.preload cannot be preloaded (cannot open shared object file): ignored.
... and more errors
```

After looking around on the internet, I found out [more people have this error](https://forum.snapcraft.io/t/ld-so-error-on-debian-on-raspberry-pi/13887). There's a lot more information about the [Snap sandbox](https://snapcraft.io/docs/security-sandboxing) online, but that's something for the next time. 

## Conclusion

There's a lot more to the single error line than I expected. I learned a lot of new things about how Linux works when trying to find the cause of the error. And I think this is the most important take-away from me besides the technical knowledge. It's easy to just ignore errors and not caring about them, but by diving into it, you'll better understand how things actually work. So stay curious! :)
