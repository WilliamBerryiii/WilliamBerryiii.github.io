---
layout: post
title: Personalizing the UpGuard Timeline with Powershell
date: '2015-09-17T23:34:00.001-07:00'
author: William Berry
tags:
- Automation
- APIs
- Powershell
- UpGuard
modified_time: '2016-01-28T09:43:37.721-08:00'
thumbnail: http://3.bp.blogspot.com/-PcgEWAAoGq0/VfurDRagyPI/AAAAAAAAAY0/zEV-EwywIYE/s72-c/ScriptrockTimeline.PNG
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-5733041626795895948
blogger_orig_url: http://www.lucidmotions.net/2015/09/upguard-events-with-corporate-favicon.html
---

The are few things more awesome then that sense of hacking some 
personalization into a product.  Whether it was huge gaudy epaulettes on my 
schweet Night Elf Druid or flames in the vacuform chain guards for my 
automation winches, I love adding that geeky special touch.  So when I 
encountered one of the more underrated features of UpGuard and found that you 
can personalize it, my inner (and outer) geek sprung into action.  "What 
feature?" you ask.  Why the Timeline! 
<div style="text-align: left;"> 
<div style="text-align: left;">Hiding out under the Report tab is this awesome 
little feature, the Timeline.  While clearly one of those things waiting for 
its breakout moment, I see plenty of potential in this feature's current 
incarnation; especially considering that the API allows you to post events 
into the timeline, meaning you can record metadata about infrastructure events 
(think deployments, windows updates, etc.)  <div style="text-align: left;"> 
<div style="text-align: left;">As part of the first tier of your UpGuard 
journey, you will need to come to terms with the Time element of your 
infrastructure; i.e. Change is inevitable, Change is a function of time, and 
capturing events throughout time helps orient and give perspective to Change.  
So plan on exploring this feature and folding it into your automation early in 
your integration journey.<div style="text-align: left;"> 
<div style="text-align: left;">What we are going to accomplish is the 
following:<div style="text-align: left;"> 
<div class="separator" style="clear: both; text-align: center;">[<img 
border="0" height="400" 
src="http://3.bp.blogspot.com/-PcgEWAAoGq0/VfurDRagyPI/AAAAAAAAAY0/zEV-EwywIYE/s400/ScriptrockTimeline.PNG" 
width="300" 
/>](http://3.bp.blogspot.com/-PcgEWAAoGq0/VfurDRagyPI/AAAAAAAAAY0/zEV-EwywIYE/s1600/ScriptrockTimeline.PNG)<div 
class="separator" style="clear: both; text-align: left;"> 
<div class="separator" style="clear: both; text-align: left;">See that sweet 
logo in both the timeline and the popup?  Well that's harvested from my 
employer's favicon and the hack is super simple.  <div class="separator" 
style="clear: both; text-align: left;"> 
<div class="separator" style="clear: both; text-align: left;">In the script 
below we have a few different things that need to be accomplished.  First 
we'll set up some variables to hold information about our corporate website, 
the UpGuard Appliance, and the event we want to post.  Then, using the 
powerful HTML parsing built into Powershell, we can harvest all the link tags, 
filter for the 'Shortcut Icon' and grab its HREF.  The remainder of the code 
is just about building the event and posting it to the timeline, where the 
only tricky bit is escaping the body's double quotes.  Doing the backtick 
escaping allows us to post a properly formatted JSON object while still 
enabling Powershell to do variable replacement for us, a win-win.<div 
class="separator" style="clear: both; text-align: left;"> 
<div class="separator" style="clear: both; text-align: left;">The API 
reference page can be found[ 
here](https://support.scriptrock.com/hc/en-us/articles/204138480-Events) and 
the Powershell to make the magic happen is below:<div class="separator" 
style="clear: both; text-align: left;"> 
<script 
src="https://gist.github.com/WilliamBerryiii/ca9113053b4f6ef7831c.js"></script> 
<div class="separator" style="clear: both; text-align: left;">Happy 
Scripting!<div style="text-align: left;"> 