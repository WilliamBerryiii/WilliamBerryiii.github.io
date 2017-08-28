---
layout: post
title: Preventing Scans of UpGuard Nodes During Deployments w/Powershell v3.0+
date: '2015-09-15T23:31:00.001-07:00'
author: William Berry
tags:
- Automation
- APIs
- DevOps
- UpGuard
modified_time: '2016-01-28T09:49:42.480-08:00'

---

As we move our UpGuard installation into production I have a few security 
issues to contend with.  The most significant concern is preventing a UpGuard 
scan from pulling down unencrypted configuration data during a deployment.  In 
theory if a scan were to be triggered while secure data was being migrated 
from an old web.config to a new config, the scan could pick up IT eyes only 
data making it available to non-IT analysts with accounts on the appliance.  
Currently the Scriptrock API does not support a "disable scans" toggle for a 
node, so lets go hacking! 

In the script below we are going to leverage 
the fact that we do not currently have any Agent based nodes configured on the 
appliance, everything thus far is SSH or WinRM.  So for the node being 
deployed to, the simple fix is to temporarily change the Medium Type to 
'Agent' while the automation runs.  The script below can be converted into a 
function that takes a lambda that represents the body of your deployment 
script, thereby effectively "wrapping" your deployment scripts with this 
toggle.

<script src="https://gist.github.com/WilliamBerryiii/5bf63a2601341ac49b63.js"></script> 


## UPDATE: Alan Sharp-Paul from UpGuard , sent 
me a tweet to let me know about a feature of the API that can perform a 
similar function as noted above, that being the [Scheduled Jobs](https://support.scriptrock.com/hc/en-us/articles/204586534-Scheduled-Jobs) 
endpoint.  Depending on how you have set up your environments set up this may 
work quite well for you.  In our case, we have nodes in an environment that 
span functionality, so a deployment may not cut across all of them.  Given 
that, I see it as advantageous to disable the node as noted above, record the 
deployment event and then restore the node, allowing the other machines in 
that environment to be scanned if we run over in to the scheduled job.  One 
alternative could be to check if the job is running, if so kill it, run the 
deployment and update the next scheduled run time to be shortly in the future 
(expect a post on this in the near future). 

Happy Scripting! 