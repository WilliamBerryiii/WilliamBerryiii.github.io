---
layout: post
title: Azure IoT Gateway SDK Build Problems
date: '2016-09-08T09:04:00.000-07:00'
author: William Berry
tags:
- Azure
- Gateway
- CMake
- IoT
modified_time: '2016-09-08T09:04:06.936-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-4884324456457166601
blogger_orig_url: http://www.lucidmotions.net/2016/09/azure-iot-gateway-sdk-build-problems.html
---

I've had the opportunity to start exploring the Azure IoT product suite lately 
and over all first impressions are very positive.  I've rolled a few F# 
solutions for device management and simulation with good success.  The next 
step of this project has lead me to the Azure IoT Gateway SDK in an attempt to 
implement a custom filtering/batching/grouping/compression gateway for a field 
array.  Unfortunately, after adding the C++ options to Visual Studio, 
installing CMake a few times and adding it to my path, I was stuck.  Running 
the included `build.cmd` or CMake by hand lead to a string of errors like: 

<script 
src="https://gist.github.com/WilliamBerryiii/33f9b7e28a8d34e87c621e38890a6414.js"></script> 
After some lamenting that this happens every time someone lets me near C code 
I checked the [issues 
list](https://github.com/Azure/azure-iot-gateway-sdk/issues/3#issuecomment-245637619) 
and found that I cannot follow directions.  Aside from making sure that your 
path to the checked out repo is under 20 characters, because `Windows`, you 
need to make sure to include the recursive flag in the clone from GitHub.  
Here is the command for the lazy: 

`git clone --recursive https://github.com/Azure/azure-iot-gateway-sdk.git` 

Happy coding! 
<span style="font-size: x-small;"> 
<span style="font-size: x-small;"> 
<span style="font-size: x-small;">Friendly Disclaimer: I now work for 
Microsoft in DX 