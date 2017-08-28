---
layout: post
title: Timing Method Execution in C#
date: '2015-09-27T22:47:00.001-07:00'
author: William Berry
tags:
- Performance Monitoring
- C#
modified_time: '2015-09-27T22:53:21.326-07:00'

---

An awesome tweet from Jessica Kerr rolled by this morning in quite a timely 
fashion. 

<blockquote class="twitter-tweet" lang="en"><p lang="en" dir="ltr">To scale 
the rate of feature development, you have to constantly be working on your 
monitoring and automation.&#10;[@skamille](https://twitter.com/skamille) 
[#strangeloop](https://twitter.com/hashtag/strangeloop?src=hash)</p>&mdash; 
Jessica Kerr (@jessitron) [September 26, 
2015](https://twitter.com/jessitron/status/647787930442932224)</blockquote><script 
async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> 

I've been working hard for the last few days to really dial up the 
instrumentation and telemetry data collection in our primary transaction 
processing application.  We've always had a sufficient view into the 
operational characteristics of the application, but like the tweet above 
notes, the faster we want to move, the more data we need to collect. 

Given that instrumenting a mature application can be difficult at best and 
resisting the urge to perform a heavy refactoring is even harder, I've 
struggled to keep the surface area of change as small as possible. 

Throughout this work, the Siren's Call of rip and rewrite has been the most 
powerful in our data access code.  Like most n-tier apps, we have a flat layer 
of code that's wedged  between the business logic for transaction processing 
and the database, with all interactions flowing through just a handful of 
objects.  Though this architectural approach has fallen out of favor with me 
and begs to be changed, we must sometimes take the short road to higher ground 
and clean things up after building some space for reflection. 

My primary objective with this segment of the project was to add timing code 
around all the stored procedure calls.  Some of this timing data will be sent 
to windows performance counters, others bulk logged into HBase on our Hadoop 
cluster and others still, aggregated and recorded in our SQL Server logging 
tables, which record at the transaction level. 

The approach here is oriented around triage and batch analytics.  With 
performance counters we can quickly see, in near real-time, how sections of db 
calls are behaving.  We can then turn to SQL server to collect transaction 
profiles exhibiting higher latency and debug them in our development 
environment.  Lastly, we can get both audit functionality and custom 
performance analysis by writing analytics jobs on the cluster that encompass 
longer time frames. 

The following Gist is a simple example repository.  The repository has a small 
wrapper class which helps deal with SqlHelper exceptions and a connection 
string which are injected to improve testability.  Additionally, we have a 
simple method which will return a 'thingy' from the database given a 
thingy_id. 

<script src="https://gist.github.com/WilliamBerryiii/a01da8b9f53732bad4b4.js"></script> 

As I noted above, the goal is to instrument this method, timing the length of 
the stored procedure call.  The easy way out would be some local state in the 
class and a standard .Net stopwatch.  I don't have any particular problem with 
that approach, in fact it's where I started, but the main drawback is the 
verbosity.  Every method would end up looking like this: 

<script src="https://gist.github.com/WilliamBerryiii/b99e6aceb25f31a380f8.js"></script> 

Again the approach is not bad, per se, but it is verbose and repetitive if 
every method needs this change, which in this case we do. 

At the other extreme, we could use Aspect Oriented Programming with 
attributing and IL weaving to inject our instrumentation code around our 
methods.  The .Net library exemplar for this is 
[PostSharp](https://www.postsharp.net/aspects) with it's compile time AOP 
capabilities.  Amazing technology, but given that we are still trying to 
figure out what we really need from all this, I'd prefer a happy medium. 

So what I ended up with was the following: 

<script src="https://gist.github.com/WilliamBerryiii/d444f262444eb8e05249.js"></script> 

I've added a public property with a backing field that will be used to extract 
the timing data from our repository class - nothing special there.  Skipping 
over our data access method for a moment there is a new method at the bottom 
of the repository that will do our timing. 

The timing method takes two parameters, a func that returns a DataSet and a 
ref to our timing field.  Since we are pre-filling our method parameters, the 
timer function leverages the func(TResult) signature, getting some nice 
flexibility from the type system.  The ref timing field will be incremented 
using the Interlocked API so that we can handle some modest concurrency in the 
repository.  Otherwise, the method looks like an extract of the "simple" 
approach with a stopwatch. 

Back up in the data access method the Sql Executioner, wrapped in a lambda, 
and the timing field are passed to the Timer method and the remainder of the 
method is left nominally unchanged. 

This simple approach to timing method calls can be used with a fair amount of 
flexibility throughout an application.  Consider overloading the timer with an 
action delegate too, for even more flexibility ... happy coding! 

P.S. the following link goes to an interesting set of answers to this very 
problem on Stack Overflow: [wrapping stopwatch timing with a delegate or lambda](http://stackoverflow.com/questions/232848/wrapping-stopwatch-timing-with-a-delegate-or-lambda). 