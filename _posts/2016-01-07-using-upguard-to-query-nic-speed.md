---
layout: post
title: Using UpGuard & Powershell Queries to Monitor your NIC Speed
date: '2016-01-07T14:20:00.001-08:00'
author: William Berry
tags:
- Powershell
- DevOps
- UpGuard
modified_time: '2016-01-28T09:41:49.052-08:00'
thumbnail: http://2.bp.blogspot.com/-G8_LRFAf7F0/Vo7ivMl7tmI/AAAAAAAAAcA/fMAmDdEjqOA/s72-c/NetworkAdapters.PNG

---

One of the sweetest features of UpGuard is the ability to add custom queries 
for node scans.  Though the standard battery of queries that the product 
provides is very through and well selected, it does have some blind spots.  
Previously, I've written about using UpGuard to [monitor Disk Space](http://www.lucidmotions.net/2015/10/simple-disk-space-check-w-scriptrock.html) 
on server drives and to [track changes to Active Directory](http://www.lucidmotions.net/2015/12/scan-active-directory-users-groups-with-powershell.html). 
 In this post we are going to look at a more nefarious problem that we ran 
into lately and leverage UpGuard to help monitor for changes. 

The other day, our ETL pump began to experience SQL connection timeouts 
with one of our database servers.  As we dug deeper into the issue, we 
discovered that a primary NIC on that cluster node was running at 100% 
utilization and the jump to discover that the NIC had reset itself from its 
originally configured 1GB speed to 100MB, was short.  Under normal loads this 
would not have posed much of an issue since most SQL connections are small 
payloads over short duration connections. In this case a large log shipping 
job was running in the background putting additional pressure on the pipe.  

Whether or not this issue had historical relevancy, which it does, I 
would still turn to UpGuard to at least get a daily heads up that something 
might be wrong.  Since the NIC resets tend to occur after server restarts, I 
moved all our database machines to their own environment and set the scan time 
to kick off in the last minute of our standard maintenance window, increasing 
the chance that the daily scan would catch the drift.  The last piece of the 
puzzle is the actual query...

Since most all the Powershell to do this stuff has been written before I 
turned to Google for a little help.  A simple query of 'Get NIC speed with 
Powershell' turned up [this StackOverflow answer](http://stackoverflow.com/a/3002568/1276028) that has a great place to 
jump off from. The code simply gets all the network adapter data, filtering on 
a non-null speed and MAC address setting and then dumps four properties to a 
table, a'la 

<script src="https://gist.github.com/WilliamBerryiii/bbcb2f2ad902c9f38cdd.js"></script> 

Unfortunately, UpGuard won't be too happy with the formatted table of 
results so we need to modify the script slightly to shape the data correctly. 

<script src="https://gist.github.com/WilliamBerryiii/f8e1ad9ef6fa15e42676.js"></script> 

Here we have simply replaced the call to 'Format-Table' with a 'Select-Object 
-Property' call with the same property list. 

The last step is to add this script to our custom query section and set a Key 
Name to NetConnectionID so that each eligible NIC is listed under it common 
name. 

[<img border="0" height="156" src="/images/NetworkAdapters.PNG" width="640" />](/images/NetworkAdapters.PNG) 

With our query configured, our next scan will produce the output below. 

[<img border="0" height="80" src="/images/NetworkAdapters2.PNG" width="200" />](/images/NetworkAdapters2.PNG) 

With that we are done, Happy UpGuard'in !<div> 

PS.  I wanted to post a quick update to show the use of a calculated property 
for link speed.  So here you go: 

<script src="https://gist.github.com/WilliamBerryiii/0ef15deda29d462b7f34.js"></script> 