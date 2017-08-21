---
layout: post
title: HBase, Thrift & C# - First Connections
date: '2014-05-03T00:21:00.001-07:00'
author: William Berry
tags:
- HBase
- C#
- Thrift
modified_time: '2014-05-17T23:39:48.739-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-5568222696367618036
blogger_orig_url: http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-first-connections.html
---

I seemingly have a bad habit of never writing part two of a series.  So to 
buck the trend, this piece is a follow up to [NuGet Servers, HBase, Thrift 
Code Generation and one sweet Jenkins CI 
Build](http://www.lucidmotions.net/2014/04/nuget-code-generation-jenkins-thrift-hbase.html). 
 You don't need to read the whole post; but, familiarizing yourself with 
section III and on is important.  Don't forget to check other posts in this 
series. 

Part 1 - [NuGet Servers, HBase, Thrift Code Generation and one sweet Jenkins 
CI 
Build](http://www.lucidmotions.net/2014/04/nuget-code-generation-jenkins-thrift-hbase.html) 
Part 2 - [HBase, Thrift &amp; C# - First 
Connections](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-first-connections.html) 
Part 3 - [HBase, Thrift, &amp; C# - Managing 
Sessions](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-session-management.html) 
Part 4 - [HBase, Thrift, &amp; C# - First Scanner and Leveraging 
Generics](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-generic-row-scanner.html) 

<div style="text-align: center;">*** 
Let's take a quick look at establishing connectivity to our HBase Thrift 
server.  The example connection code in the thrift C# solution is a great 
primer and what we will use as the base here. 

For the majority of the code in the rest of this series, we will take a 
simplistic page from NHibernate's architecture.  Let's start with a simple 
Interface called ISession which implements IDisposable.  The implementation of 
IDisposable is so we can build sessions within a using statement, letting the 
framework do our heavy lifting. 

Further, we will build a class called Session that implements the Interface 
ISession.  Its constructor will take a reference to our Pool Manager class and 
will take a Connection object that has configuration data in it. 

<div><pre><span style="color: teal;">  1 <span style="color: blue;">public 
<span style="color: blue;">class Session : ISession 
<span style="color: teal;">  2 { 
<span style="color: teal;">  3     <span style="color: blue;">private <span 
style="color: blue;">readonly IConnection _connection; 
<span style="color: teal;">  4     <span style="color: blue;">private <span 
style="color: blue;">readonly ISessionPoolManager _manager; 
<span style="color: teal;">  5     <span style="color: blue;">private <span 
style="color: blue;">readonly TSocket _transport; 
<span style="color: teal;">  6     <span style="color: blue;">private 
Hbase.Hbase.Client _client; 
<span style="color: teal;">  7 
<span style="color: teal;">  8     <span style="color: blue;">public 
Session(ISessionPoolManager manager, IConnection connection) 
<span style="color: teal;">  9     { 
<span style="color: teal;"> 10          Guid = Guid.NewGuid(); 
<span style="color: teal;"> 11          _connection = connection; 
<span style="color: teal;"> 12          _manager = manager; 
<span style="color: teal;"> 13          _transport = <span style="color: 
blue;">new TSocket(Connection.Name, Connection.Port); 
<span style="color: teal;"> 14          var protocol = <span style="color: 
blue;">new TBinaryProtocol(_transport); 
<span style="color: teal;"> 15          _client = <span style="color: 
blue;">new Hbase.Hbase.Client(protocol); 
<span style="color: teal;"> 16     }</pre> 
The class has a private method called OpenConnection() that is used to, well, 
open a connection to HBase via Thrift. This code is very straight forward: 

<div><pre><span style="color: teal;">  1 <span style="color: blue;">private 
Hbase.Hbase.Client OpenConnection() 
<span style="color: teal;">  2 { 
<span style="color: teal;">  3      _transport.Open(); 
<span style="color: teal;">  4      IsConnected = _transport.IsOpen; 
<span style="color: teal;">  5      <span style="color: blue;">return _client; 
<span style="color: teal;">  6 }</pre> 
For completeness let's implement a CloseConnection(): 

<div><pre><span style="color: teal;">  1 <span style="color: blue;">private 
<span style="color: blue;">void CloseConnection() 
<span style="color: teal;">  2 { 
<span style="color: teal;">  3       _transport.Close(); </pre><pre><span 
style="color: teal;">  4       IsConnected = _transport.IsOpen; 
</pre><pre><span style="color: teal;">  5 }</pre> 
Because the Session class implements the IDisposable interface we are required 
to have a Dispose method.  The Dispose method calls our internal close on the 
transport and re-queues this object in Pool Manager's queue. 

<div><pre><span style="color: teal;">  1 <span style="color: blue;">public 
<span style="color: blue;">void Dispose() 
<span style="color: teal;">  2 { 
<span style="color: teal;">  3      CloseConnection(); 
<span style="color: teal;">  4      _manager.Requeue(<span style="color: 
blue;">this); 
<span style="color: teal;">  5 }</pre> 
In the next article we will look at implementing a table scanner for HBase and 
the structure to support it. 

<div style="text-align: center;"> 