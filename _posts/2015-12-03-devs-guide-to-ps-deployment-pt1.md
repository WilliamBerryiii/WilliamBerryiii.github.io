---
layout: post
title: A Developer's Guide to Powershell Deployment Automation
date: '2015-12-03T22:27:00.001-08:00'
author: William Berry
tags:
- Automation
- Deployment
- Powershell
modified_time: '2015-12-03T22:27:28.737-08:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-2176731761040825375
blogger_orig_url: http://www.lucidmotions.net/2015/12/devs-guide-to-ps-deployment-pt1.html
---

<div><u>PART I</u><div> 
<div>*Scene notes*It's Sunday night.  9:30 pm to be exact. The kids are 
finally asleep. The hiss of the record needle stings Bill from across the room 
as a Jawbone wafts Mancini.  One rock gently spins, melting in a finger of 
Scotch.  It's clearly deployment time.  Bill wonders where his RSA key is as 
he rifles through his tattered Ted Baker bag (clearly a prized possession).  
He sighs heavily and begins muttering "The VPN is acting up AGAIN.  Go figure. 
*pause*  I'm in.  *pause* Where's IT? Late again ..." The chat window opens. 
<div> 
<div>Br:     Hey Bill, you here?<div>B:      Yeah man, sup?<div>Br:     
Ready?<div>B:      As I'll ever be, I suppose.<div>Br:     Stopping the 
service on TUBES.<div>B:      OK.<div>Br:     Copying the files over.<div>B:   
   Ok ... just ping me when it's done and I'll test.<div>...<div>Br:     The 
copy failed.  Let me try this again.<div>...<div>B:       K.<div> 
<div>(5 min. later)<div>Br:     Ok TUBES is done.  Moving onto SOCKETS<div>B:  
    Testing.<div> 
<div>(45 min. later)<div>B:      Can you just stop the service on all of them 
and deploy the backups?<div>Br:     Where are they? <div>B:      The services 
or the backup files?<div>Br:     The backup files.<div>B:      Um, where ever 
you put them?  Is this a trick question?<div>Br:     I didn't copy them 
anywhere, was I supposed to?<div>B:      It's the second step in the word doc 
dude ... <div>B:      Brb.  Need more whiskey. <div>Br:     K <div>**cries 
pierce through the jawbone now playing Ed Thigpen**<div>B:      Little one is 
up again.  Look can you just get the files from last Sunday's deployment off 
the share and copy them back over onto all the servers?  I'll be right 
back.<div>Br:     Ok, but do I have to stop the service if it's 
running?<div>B:      FOLLOW THE BACKOUT INSTRUCTION IN THE WORD DOC ... I'll 
brb.<div>(scene) <div> 
<div style="text-align: center;">***<div> 
<div>Let me start by saying, I get it.  I know where you are.  I've been 
there.  It's not pretty, but it works.   This is how it has to work sometimes. 
 But ... it can be better.  And getting there is not dramatic or scary.  It's 
not their fault.  It's not IT's fault.  You're the developer.  You need to get 
in there and get this straightened out.  And we can do it.  We can do it 
together. 