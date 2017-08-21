---
layout: post
title: HBase, Thrift, & C# - Batch Reads
date: '2014-05-17T23:38:00.003-07:00'
author: William Berry
tags: 
modified_time: '2014-05-17T23:47:15.197-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-1027936388976476719
blogger_orig_url: http://www.lucidmotions.net/2014/05/hbase-thrift-c-batch-reads.html
---

Continuing the epic series on Hbase, Thrift and C#, this installment is the 
code for a batch scanner by leveraging inheritance and generics to provide a 
broad based solution.  If you have not done so please check out the other 
parts of the series: 

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

Feeling the PAIN of single reads off HBase, I hacked up a little method to 
allow for batch reads off the HBase Thrift interface.  Like the other versions 
in my last HBase post, this one makes use of the table scanner. 

<div><pre><span style="color: teal;">  1 <span style="color: blue;">public 
<span style="color: blue;">virtual List&lt;T&gt; 
BatchSelectWithPrefixScanner&lt;T&gt;(<span style="color: blue;">string 
identifier, <span style="color: blue;">int batchSize) 
<span style="color: teal;">  2     where T : IHBaseEntity, <span style="color: 
blue;">new() 
<span style="color: teal;">  3 { 
<span style="color: teal;">  4     var col = <span style="color: blue;">new 
List&lt;<span style="color: blue;">byte[]&gt;(); 
<span style="color: teal;">  5     col.AddRange(Columns.Select(x =&gt; 
x.GetBytes())); 
<span style="color: teal;">  6 
<span style="color: teal;">  7     var tableName = <span style="color: 
blue;">string.Format(TableNameTemplate, RetailerId); 
<span style="color: teal;">  8 
<span style="color: teal;">  9     var scanner = 
HBaseClient.scannerOpenWithPrefix( 
<span style="color: teal;"> 10         tableName.GetBytes(), 
<span style="color: teal;"> 11         identifier.GetBytes(), 
<span style="color: teal;"> 12         col, 
<span style="color: teal;"> 13         <span style="color: blue;">new 
Dictionary&lt;<span style="color: blue;">byte[], <span style="color: 
blue;">byte[]&gt;() 
<span style="color: teal;"> 14         ); 
<span style="color: teal;"> 15     <span style="color: blue;">return 
GetBatchRows&lt;T&gt;(batchSize, scanner); 
<span style="color: teal;"> 16 }</pre> 
Yet again we have leveraged generics to return a List&lt;T&gt;. 