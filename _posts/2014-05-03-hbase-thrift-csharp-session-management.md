---
layout: post
title: HBase, Thrift, & C# - Managing Sessions
date: '2014-05-03T14:41:00.001-07:00'
author: William Berry
tags:
- HBase
- Producer Consumer
- C#
- Queues
- Thrift
- Session Management
modified_time: '2014-05-17T23:39:25.965-07:00'
---

In my last post, [HBase, Thrift &amp; C# - First 
Connections](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-first-connections.html), 
I mentioned and included in the code, references to a Session Pool Manager.  I 
wanted to take the opportunity to discuss some of the behavioral aspects of 
this class.  Unfortunately, because this work is completely unrelated to any 
open source projects, I don't feel comfortable sharing the actual code.  That 
said, I won't hesitate to talk about how it works and discuss some of it's 
features, in the event you are looking to implement a session manager.   Don't 
forget to check the other posts in this series. 

Part 1 - [NuGet Servers, HBase, Thrift Code Generation and one sweet Jenkins CI Build](http://www.lucidmotions.net/2014/04/nuget-code-generation-jenkins-thrift-hbase.html) 
Part 2 - [HBase, Thrift &amp; C# - First Connections](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-first-connections.html) 
Part 3 - [HBase, Thrift, &amp; C# - Managing Sessions](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-session-management.html) 
Part 4 - [HBase, Thrift, &amp; C# - First Scanner and Leveraging Generics](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-generic-row-scanner.html) 

The Session Pool Manager (SPM) is actually a collection of interfaces and 
classes who's end functionality is very similar to that of the ADO.net SQL 
Connection Pool (details 
[here](http://msdn.microsoft.com/en-us/library/8xx3tyca(v=vs.110).aspx)).  
What we are looking to accomplish is decreasing the overhead of building and 
validating a connection to HBase.  Depending on your environment and 
implementation a connection to HBase might involve: 
1. Pinging a thrift server 
1. Running a health check on the thrift server. 
1. Opening a socket 
1. Building the protocol objects 
1. Building a client object 
1. Authentication via basic, kerberos, etc. 
1. Perhaps prefetching some data to make sure the connection is solid. 

Each of these steps by itself is inconsequential; but, in an API 
environment where you are constantly serving requests, paying the overhead can 
quickly become costly.  To combat the overhead we can create N instances of 
session objects, keep them in a queue and dole them out as needed to 
callers.

There are a few features of the pool manager we need to consider when 
working with HBase or other DBs that provide multiple routes to the data 
(think master-master or active-active arangements).  Typically, a thrift 
server instance will run on each of the region servers in your cluster.  That 
means that you have multiple machines that can service requests concurrently.  
Assuming that you have taken steps to properly design your row keys and your 
access patterns are sufficiently random to avoid disk hot spots, you can 
increase the bandwidth of the cluster by making requests to multiple thrift 
servers concurrently.

In our design we will need a connection object with an interface that can 
hold the connection details for each of the thrift servers.  For now I simply 
pull that information out of hard coded values in the web.config for the API.  
Obviously, the "right" way to do this, is to query another system that can 
dynamically report back the active and healthy region/thrift. 
We can leverage the DI framework to parse the config, build our connection 
objects and pass them to the Session Pool Manager's constructor.  In our case 
we have one Session Pool Manager per application pool.  When the pool 
recycles, so does the Session Pool Manager. 

The Pool Manger has several internal collections.  The first is a concurrent 
queue of prebuilt and available sessions.  When a caller requests a session, 
we simply pop it off the queue and hand it back to the caller.  As you saw in 
the previous post, the caller can get the session in a using statement: 

```csharp
using (var session = _sessionPoolManager.GetSession())
``` 
Since our session object implements IDisposable, the session's dispose method 
will be called as the using statement terminates.  The dispose method closes 
the open connection and simply calls Requeue(session) on the Pool Manager to 
put the session back in the SPM's queue. 

Let's suppose however, that the queue did not have any available sessions to 
hand out at the time.  If that's the case, then we simply build another 
session object, add it to the queue, pulse a monitor and the caller will get 
the newly created session to go and work with.  There is one caveat to this, 
the Session Pool Manager has a property MaxSessions.  If the total count of 
sessions has reached the MaxSessions count then the Pool Manager will simply 
block until a connection becomes available. 

Given the need to max out at a specific session count we will need to store 
the total count of sessions that have been created.  We can use one data 
structure to kill two features. 

As I noted previously, we have the opportunity to connect to multiple thrift 
servers on the cluster, meaning we can distribute our query load across the 
region servers.  For random reads, our case, the simple approach of a evenly 
balanced round robin distribution is actually the most efficient approach 
spreading load across available regions servers. 

To implement the load distribution, there is a second collection of 
*Dictionary&lt;Connection, int&gt;* where we keep the connection object 
created from config parsing and an int to track the count of instances.  
Finding the next connection to build a session with, is a matter of selecting 
the Min() of values from the dictionary.  Additionally, finding out if we have 
reached our MaxSessions can be as simple as running a Sum() across the values. 
 Obviously there are some potential threading issues with this approach, given 
that the increment &amp; decrement of the values in the dictionary cannot be 
done without locking the dictionary.  The reality however, is that the 
MaxSessions value is guidance.  If we end up blocking for a moment or 
accidentally creating an extra session, there is really no harm. 

The next feature we need is over on the Session object itself.  If, for some 
reason, we encountered an error while using the session, perhaps the socket 
closed or the read timed out, then we want to track that with the session. 

Here's the case: the session's connection encountered an error an timed out, 
the session was then re-queued into the Pool Managers Queue.  By storing the 
last know state (perhaps using an enum) you can test the connection with a 
high speed lookup before handing it to the next caller.  If your remote call 
fails, then you can pass the session to an async method for destruction and 
continue on by getting another session from the queue (one may be built for 
you in the background). 

Another possible issue is that a region server is down and therefore building 
any connections to it is a waste of time.  The simplest way to combat this is 
to continue to destroy failing connections and let your pool slowly migrate 
over to the other good thrift servers.  Each time a caller asks for a new 
session the dictionary look up will first return the down node, since it has 
the least number of active connections.  An attempt to connect will fail, the 
session can then be destroyed and the SPM tries again with the next least 
active session.  This loop continues until you have exhausted the list of 
connections in the dictionary. 

Testing the failed node can continue in through this process until it comes 
back on line, at which point we will want to begin to rebalance.  Rebalancing 
the pool is as simple as expiring old sessions before handing them out.  By 
keeping a created property on the session, you can asynchronously destroy old 
sessions when you come across them, before handing them back to callers. 

This whole approach to session pooling is a passive producer/consumer approach 
that supports a multi-threaded environment like a DataAPI.  I encourage you to 
do some research around the topics involved before writing your own.  For 
instance, Jon Skeet has a blog post that would be a great place to start for 
producer consumer multi-threading, available 
[here](http://www.yoda.arachsys.com/csharp/threads/deadlocks.shtml).  My last 
bit of caution is to keep management state light; try to keep your approach as 
functional as possible.  Feel free to ask questions or tell me I am an idiot 
in the comments section below. 