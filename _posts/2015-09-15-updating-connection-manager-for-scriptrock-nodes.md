---
layout: post
title: Updating the Connection Manager for a list of Scriptrock Nodes using Powershell
  v3.0+
date: '2015-09-15T00:04:00.000-07:00'
author: William Berry
tags:
- APIs
- Powershell
- Scriptrock
modified_time: '2015-09-17T23:38:24.027-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-3918349347779295670
blogger_orig_url: http://www.lucidmotions.net/2015/09/updating-connection-manager-for-scriptrock-nodes.html
---

In my last 
[post](http://www.lucidmotions.net/2015/09/getting-node-list-from-scriptrock.html), 
we looked at how to get our list of nodes from our Scriptrock appliance.  Now 
let's take our collection of nodes, and using Powershell's list filtering and 
selecting capabilities, we can put that data to good work.  Here is the 
original node select script: 
<div style="text-align: center;"><div style="text-align: left;"> 

<script 
src="https://gist.github.com/WilliamBerryiii/7dc2c9004647c4e486a4.js"></script> 
<div style="text-align: left;">In the following simple example we will iterate 
the list of nodes, filter for operating_system_family_id and then update each 
node's connection_manager_group_id:<div style="text-align: left;"> 

<script 
src="https://gist.github.com/WilliamBerryiii/9a35f1ff85620012475f.js"></script> 
<div style="text-align: left;"> 