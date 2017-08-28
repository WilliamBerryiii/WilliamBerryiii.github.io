---
layout: post
title: HBase, Thrift, & C# - Batch Reads
date: '2014-05-17T23:38:00.003-07:00'
author: William Berry
tags: 
modified_time: '2014-05-17T23:47:15.197-07:00'
---

Continuing the epic series on Hbase, Thrift and C#, this installment is the 
code for a batch scanner by leveraging inheritance and generics to provide a 
broad based solution.  If you have not done so please check out the other 
parts of the series: 

* Part 1 - [NuGet Servers, HBase, Thrift Code Generation and one sweet Jenkins CI Build](http://www.lucidmotions.net/2014/04/nuget-code-generation-jenkins-thrift-hbase.html) 
* Part 2 - [HBase, Thrift &amp; C# - First Connections](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-first-connections.html) 
* Part 3 - [HBase, Thrift, &amp; C# - Managing Sessions](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-session-management.html) 
* Part 4 - [HBase, Thrift, &amp; C# - First Scanner and Leveraging Generics](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-generic-row-scanner.html) 

Feeling the PAIN of single reads off HBase, I hacked up a little method to 
allow for batch reads off the HBase Thrift interface.  Like the other versions 
in my last HBase post, this one makes use of the table scanner. 

```csharp
public virtual List<T> BatchSelectWithPrefixScanner<T>(string identifier, int batchSize)
    where T : IHBaseEntity, new() 
{ 
    var col = new List<byte[]>(); 
    col.AddRange(Columns.Select(x => x.GetBytes())); 
  
    var tableName = string.Format(TableNameTemplate, RetailerId);
  
    var scanner = HBaseClient.scannerOpenWithPrefix( 
        tableName.GetBytes(), 
        identifier.GetBytes(), 
        col, 
        new Dictionary<byte[], byte[]>() 
        ); 
    return GetBatchRows<T>(batchSize, scanner); 
}
```

Yet again we have leveraged generics to return a List<T>. 