---
layout: post
title: EasyNetQ Advanced Bus from F#
date: '2016-04-21T23:00:00.001-07:00'
author: William Berry
tags:
- RabbitMq
- F#
- EasyNetQ
modified_time: '2016-04-21T23:00:15.586-07:00'
---

I've been working lately on our company's first production F# application, a 
simple logging application that spans between our transaction processing 
system and our Hadoop Cluster.  Initially we'll be logging some simple 
transaction meta data for internal reporting applications, but hope to expand 
it to other types of logging/audit data, eventually.  Given that application 
could be reactive in nature, I thought it would be fun to play with both the 
MailboxProcessor and the .Net Reactive Extensions library in this 
implementation. 

The basic architecture of the application uses EasyNetQ to consume a RabbitMq 
queue, an async recursive function to push data to HBase and an Rx Subject 
backed by a ConcurrentQueue to span the producer and consumers. 

I initially wrote an async recursive function to process the rabbit queue 
using the RabbitMq .Net client library.  I quickly realized however, that the 
yak shaving required to do everything other than consume the queue was 
generally a waste of my time, SO ... EasyNetQ.  The nice thing about EasyNetQ 
is that it wraps up the whole process nicely in a C# library.  The flip side 
is that it's a tried-and-true C# library and as such, is not as idomatic as 
one would like to use from F#. 

Since I am new to the F# world, I struggled a bit to get the type signatures 
together to implement the Advanced Bus from the EasyNetQ library.  The 
following gist is an example of setting up a synchronous message handler that 
bypasses the built in message de/serializer, instantiating a queue and then 
wrapping the Advanced Bus in a async block that we can kick off in the main 
body of our service. See 
[here](https://github.com/EasyNetQ/EasyNetQ/wiki/the-advanced-api) for details 
on the advanced API of RabbitMq. 

<script src="https://gist.github.com/WilliamBerryiii/132d7dc6c0571b5907ea0a9f6ad6949b.js"></script> 