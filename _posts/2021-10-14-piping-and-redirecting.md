---
layout: post
title:  "Piping and redirecting in shell"
date:   2021-10-14
tags: [linux, shell]
---

_Almost daily I have used `<`, `>` and `|` in my Linux shell to get things working, but I never understood exactly what they did.
By diving into how they work I have learned how they work and also learned some new tricks with them._

## Redirecting input and output to/from a file

Piping makes it possible to directly work with files while running a command. 
This makes it easier to supply complex input and it also makes it easier to persist the result of the command in a file.

```zsh
mycommand < input.txt > output.txt
# < for the input
# > for the output
```

The output of the process is saved in `output.txt`, but if the process has some error as output, it won't be saved in the file.
This is due to it being sent to a different file descriptor.
In short file descriptors are files opened for the process started by a command, to which text can be written to be used by a program and from which text can be read which was outputted by the program. 
This sounds very similar to the piping, where text is also written to and read from a file.
The file descriptor are actual files and can be found under the `/proc/PID/fd` of the process:

```zsh
sleep 1m
# open a different shell to find this process
ps -aux | grep sleep
# in my case the PID was 1519
ls /proc/1519/fd
# this shows the file descriptors of the process, indicated by numbers
```

By default there are always three file descriptors, these will be important later on:

* 0 stdin: the input for the program
* 1 stdout: the output of the program
* 2 stderror: the error logs of the program

With this we can actually something funny:

```zsh
echo "hello" > /proc/1519/fd/1
# this should output 'hello' to the sleep process
```

So each process has three actual files containing the input and output, but how does this relate to piping?
In the above example `<` and `>` are just shortcuts for interfacing with the file descriptors of the process.
To show this, let's take a look at some examples:

```zsh
# we have a file 'input.txt' with in there the value 'hello\n'
cat < input.txt
cat 0< input.txt
# both print the same output, since '<' is just short for the value of stdin 

echo "hello" > output.txt
echo "hello" 1> output1.txt
# both files have the same content, since '>' is just short for the value of stdout 

nonexistingcommand 2> stderror.txt
# the file 'stderror.txt' contains the error that the command doesn't exist

# with this we can fully control the input and output via files:
cat < input.txt > output.txt 2> error.txt
# for '0<' and '1>' the shortcut can be used
```

There are some more useful tricks:

```zsh
# send stdout and stderror to the same file
mycommand > output.txt 2>&1
# shorter version
mycommand &> output.txt

# discard the output of a file descriptor by sending it to '/dev/null'
mycommand > output.txt 2> /dev/null

# append to a file, instead of overwriting it
echo "hello" >> output.txt
echo "hello" >> output.txt
# the file contains the word 'hello' twice
```

## Piping values to another command

One more addition is '|', which allows you to use the output of one process as an argument for another one.
This is useful for filtering the output of a command, for example with 'grep' or 'sed', before using it.

```zsh
# we already used it for finding the process id
# we filter the output of the process list for only the processes that contain 'bash'
ps -aux | grep bash > output.txt
```

In this case the value of stdout of 'ps -aux' is sent to the stdin of 'grep'.
Sometimes we want to use the output of a process as an argument, instead of stdin.
This can be achieved with command substitation.
This is a whole chapter on itself, but just to show you how it works:

```zsh
# the file 'args.txt' has the content '-l'
ls $(cat args.txt)
# the command 'ls' is executed with flag '-l'
# one step further (where 'command.txt' has the content 'ls'):
$(cat command.txt) $(cat args.txt)
# executes 'ls -l'
```
