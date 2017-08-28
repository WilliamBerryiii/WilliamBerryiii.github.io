---
layout: post
title: Simple Active Directory Users & Groups Scan w/Powershell v2 and UpGuard
date: '2015-12-01T12:18:00.000-08:00'
author: William Berry
tags:
- Active Directory
- UpGuard
modified_time: '2016-01-28T09:41:32.957-08:00'

---

The feature of UpGuard I enjoy the most is the ability to write and run custom 
Powershell queries to monitor my Windows nodes.  Recently one of our system 
administrators came to me and asked about using UpGuard to monitor for changes 
on our active directory nodes.  Never backing down form a chance to use some 
Powershell to Automate a process I figured I would give the project a go! 

NOTE: This is a Tier 1 monitoring solution and is only good for alerting 
your users of very course changes to AD Users and Groups.  I would not rely on 
this as your only form of monitoring AD User and Group Changes!!!

There are effectively two things we want to monitor.  First, we want to 
look for changes in the Active Directory Schema.  That can be easily 
accomplished with an already posted UpGuard article, [see 
here](https://support.scriptrock.com/hc/en-us/articles/204779790-Scan-Options-Scanning-for-changes-in-Active-Directory-schema). 

The next piece is monitoring users and their group memberships.  For that 
we will use Powershell's built in Active Directory Module that should be 
installed with the Active Directory role on the target server.  

Form a configuration and isolation perspective, I have set up a dedicated 
environment for the monitored AD nodes to be in.  This will allow for custom 
email settings and prevent the AD changes from being mixed into the other 
daily environment reports.  Additionally, I set up a node group for all Active 
Directory nodes where the custom Powershell queries will go. 

While the schema script above from UpGuard creates a single file like 
element, I have opted to break out each user into its own "object" so that 
identifying expected changes across scans is a bit easier to parse. 

<script src="https://gist.github.com/WilliamBerryiii/40138d8dd7034e10c32d.js"></script> 

The script starts out with a simple Try/Catch to make sure that the 
module can be imported.  It then pulls the host name to ensure that for each 
AD command that will be issued, it is querying the targeted host.  Lastly we 
read all the users into a local variable and iterate across them building a 
custom object that represents the user's distinguished name, sam account name, 
enabled status, email address, the whenCreated and whenChanged properties 
along with a flattened list of group memberships. 

Optionally, if you had lots of users (we only have a few hundred per domain) 
you could flatten out the users collection similar to how the schema script 
noted above does.  That would look something like this: 

<script src="https://gist.github.com/WilliamBerryiii/6b022ea6533942e9497e.js"></script> 

EDIT: One quick note about the use of whenChanged ... this property is updated 
any time the user object is written. See here for more details on [when 'whenChanged' changes](http://www.morgantechspace.com/2014/12/Active-Directory-whenChanged-vs-usnChanged.html). 

Happy UpGuardin' 