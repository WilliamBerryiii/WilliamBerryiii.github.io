---
layout: post
title: Integrating Jenkins and NUnit3
date: '2016-04-19T23:25:00.001-07:00'
author: William Berry
tags:
- NAnt
- Build Pipeline
- Jenkins
- NUnit
modified_time: '2016-04-19T23:25:28.593-07:00'
---

I've long been a fan of the deep integration of JUnit into the Jenkins CI 
ecosystem.  Unfortunately, because most of what we build with our CI server 
are .Net applications, we are very dependent on a number of plugins to shim 
between our .Net world and the more Java orientation of Jenkins.  One such 
plugin, that I've grown quite fond of, is the 
[NUnit Plugin](https://wiki.jenkins-ci.org/display/JENKINS/NUnit+Plugin) that does 
transforms between NUnit's test result output and the JUnit format that is 
used for the built in Test Result Trend Graphs. 

After adding NUnit3 to our build server and wiring up our NAnt scripts, 
my test builds began to fail with 'No NUnit test report files were found.'  
Browsing the target folder for the artifacts did show a result file that at 
first blush looked good, but after a bit of research, I came across 
[this thread](https://issues.jenkins-ci.org/browse/JENKINS-27906) which gives a 
pretty good hint about the issue at hand. While that thread proposes 
implementing a custom xslt transform, there is a much easier solution ... 
NUnit command line has options that include formatting output, 
[see here](https://github.com/nunit/dev/wiki/Command-Line-Options#output-specification-format). 
So with a simple modification to our NAnt script we can call the NUnit console 
specifying an output file and the NUnit2 result file format as follows: 

<script src="https://gist.github.com/WilliamBerryiii/64706aa2e98b6d0b7d304546ca63d927.js"></script> 