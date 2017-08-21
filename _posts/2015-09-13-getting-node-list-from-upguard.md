---
layout: post
title: Getting Node List from UpGuard using Powershell v3.0+
date: '2015-09-13T14:51:00.002-07:00'
author: William Berry
tags:
- Powershell
- DevOps
- UpGuard
modified_time: '2016-01-28T09:51:54.697-08:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-5057004279118242246
blogger_orig_url: http://www.lucidmotions.net/2015/09/getting-node-list-from-upguard.html
---

I'm completely perplexed by people who dislike Powershell.  As someone who has 
built 1,000+ line Powershell deployment scripts, the scripting language can be 
a bit like bacon flavored chocolate; you'll try it, some folks swear by it, 
but for the most part my conclusion is ... "meh".  That said, Powershell as a 
SHELL is outstanding.  Frankly it smokes any experience I've ever had on the 
Unix/Linux side of the fence and it's got everything to do with direct access 
to .Net.  So let's put the scripting language aside and look at some things 
you can do with the shell and my new favorite tool UpGuard. 
<div> 
<div style="text-align: center;">***<div style="text-align: center;"> 
<div style="text-align: left;">Connecting to UpGuard from Powershell and 
pulling down the node list is very straight forward.  Though you'll find some 
Powershell 2.0 examples in the [API section of the UpGuard 
site](https://support.upguard.com/hc/en-us/sections/200706424-API-Reference), 
the following is an approach using the Powershell v3.0+ Cmdlet 
[Invoke-RestMethod](https://technet.microsoft.com/en-us/library/hh849971(v=wps.630).aspx) 
which will automatically deserialize the JSON response into objects - super 
cool! 

<script 
src="https://gist.github.com/WilliamBerryiii/7dc2c9004647c4e486a4.js"></script> 
<div> 
The UpGuard API rightly enforces pagination, so the above script uses a while 
loop to pull out the nodes from each Cmdlet response and adds them to a master 
array, breaking when there are no further nodes in the response. 

Happy Scripting! 