---
layout: post
title: HBase, Thrift & C# - First Connections
date: '2014-05-03T00:21:00.001-07:00'
author: William Berry
tags:
- HBase
- C#
- Thrift

---

I seemingly have a bad habit of never writing part two of a series.  So to 
buck the trend, this piece is a follow up to [NuGet Servers, HBase, Thrift Code Generation and one sweet Jenkins CI Build](http://www.lucidmotions.net/2014/04/nuget-code-generation-jenkins-thrift-hbase.html). 
 You don't need to read the whole post; but, familiarizing yourself with 
section III and on is important.  Don't forget to check other posts in this 
series. 

Part 1 - [NuGet Servers, HBase, Thrift Code Generation and one sweet Jenkins CI Build](http://www.lucidmotions.net/2014/04/nuget-code-generation-jenkins-thrift-hbase.html) 
Part 2 - [HBase, Thrift & C# - First Connections](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-first-connections.html) 
Part 3 - [HBase, Thrift, & C# - Managing Sessions](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-session-management.html) 
Part 4 - [HBase, Thrift, & C# - First Scanner and Leveraging Generics](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-generic-row-scanner.html) 

 
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

```csharp
public class Session : ISession
{ 
    private readonly IConnection _connection;
    private readonly ISessionPoolManager _manager;
    private readonly TSocket _transport;
    private Hbase.Hbase.Client _client; 
 
    public Session(ISessionPoolManager manager, IConnection connection)
    { 
         Guid = Guid.NewGuid(); 
         _connection = connection; 
         _manager = manager; 
         _transport = new TSocket(Connection.Name, Connection.Port);
         var protocol = new TBinaryProtocol(_transport);
         _client = new Hbase.Hbase.Client(protocol);
    }
``` 

The class has a private method called OpenConnection() that is used to, well, 
open a connection to HBase via Thrift. This code is very straight forward: 

```csharp
private Hbase.Hbase.Client OpenConnection()
{ 
     _transport.Open(); 
     IsConnected = _transport.IsOpen; 
     return _client; 
}
```

For completeness let's implement a CloseConnection(): 

```csharp
private void CloseConnection()
{ 
      _transport.Close(); 
      IsConnected = _transport.IsOpen; 
}
```

Because the Session class implements the IDisposable interface we are required 
to have a Dispose method.  The Dispose method calls our internal close on the 
transport and re-queues this object in Pool Manager's queue. 

```csharp
public void Dispose()
{ 
     CloseConnection(); 
     _manager.Requeue(this); 
}
```

In the next article we will look at implementing a table scanner for HBase and 
the structure to support it. 
