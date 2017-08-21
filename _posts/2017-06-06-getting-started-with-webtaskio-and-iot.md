---
layout: post
title: Getting Started with Webtask.io and IoT
date: '2017-06-06T09:50:00.002-07:00'
author: William Berry
tags:
- JavaScript
- Webtask.io
- IoT
modified_time: '2017-06-06T10:10:20.093-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-8421420275609080370
blogger_orig_url: http://www.lucidmotions.net/2017/06/getting-started-with-webtaskio-and-iot.html
---

I was in a very interesting workshop this past weekend on 
[Webtask.io](http://webtask.io/) presented by [Auth0](https://auth0.com/)'s 
Glenn Block.  Webtask.io brings to the table a thoughtfully designed 
in-browser editor, a powerful CLI and impressive startup times that live up to 
their messaging of "run(ning) code in 30 seconds".  While the tool chain 
appears to favor reactive implementations akin to AWS Lambda or Azure 
Functions, they do offer the capability to run jobs on a cron like schedule.  
What better way to explore this feature set than to implement a trivial IoT 
device simulator ... so let's get started. 
<div> 
<div>Get started by installing the Webtask CLI available 
[here](https://webtask.io/docs/101).  <div> 
<div>Open a Powershell terminal, create a new folder in your source directory 
and cd into it: `mkdir webtaks; cd webtasks`<div> 
<div>Kick off `npm init` and set up a basic package/project scaffold.<div>1. 
package name: `webtask` 
1. version: `1.0.0` 
1. description: `My First Webtask` 
1. entry point: `main.js` 
<div>Add the Azure IoT Device SDK for Node: `npm install azure-iot-device-amqp 
--save`<div> 
<div>Open VS Code in the project folder and create a new file called `main.js` 

In main.js, add a shell function for the webtask that includes a callback to 
indicate function completion as follows: 

<script 
src="https://gist.github.com/WilliamBerryiii/b6001c23247afdbfc31e1a6f28407f09.js?file=main.js_shell"></script> 
Remove the body of the above function and add the Azure IoT Device library, a 
connection string and create a device client.  You can follow [these 
instructions 
](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-node-node-getstarted)to 
learn how to create an IoT Hub, add a test device and get a device connection 
string. 

<script 
src="https://gist.github.com/WilliamBerryiii/b6001c23247afdbfc31e1a6f28407f09.js?file=iot_hub_data.js"></script> 
We'll now define an array to hold logging data, create a simple logging method 
and alias the function completion callback passing it our log data. 

<script 
src="https://gist.github.com/WilliamBerryiii/b6001c23247afdbfc31e1a6f28407f09.js?file=log_complete.js"></script> 
The last elements we need are a callback for the client connect function and a 
call for the client to open it's connection to IoT Hub. 

<script 
src="https://gist.github.com/WilliamBerryiii/b6001c23247afdbfc31e1a6f28407f09.js?file=connect.js"></script><div> 
<div>Open a Powershell command prompt and create a scheduled Webtask: `wt cron 
schedule "*/1 * * * *" .\main.js `.  This will create a new Webtask that will 
send our device data to Azure IoT Hub every minute.<div> 
<div>The newly created Webtask can then be monitored via the CLI by simply 
issuing `wt logs`.  Take note however that this is a feed of all Webtasks 
running under your account.  If everything is configured correctly you should 
see output similar to the following:<div> 
<div><script 
src="https://gist.github.com/WilliamBerryiii/b6001c23247afdbfc31e1a6f28407f09.js?file=wt_logs.txt"></script><div>To 
clean up the Webtask, simply issue `wt cron rm webtask` 

The full demo source code is available 
[here](https://gist.github.com/WilliamBerryiii/b6001c23247afdbfc31e1a6f28407f09.js?file=main.js). 

Happy Coding! 