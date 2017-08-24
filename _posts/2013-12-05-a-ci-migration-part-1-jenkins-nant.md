---
layout: post
title: A CI Migration Part 1 - Jenkins, NAnt & Window's Authentication
date: '2013-12-05T22:35:00.001-08:00'
author: William Berry
tags:
- Automation
- NAnt
- Build Pipeline
- Continuous Integration
- Jenkins
- Window's Authentication
---

I am deep in the throws of a slow migration that is laying the groundwork for 
a continuous integration style build => unit test => deploy => 
integration test, pipeline.  I have shaped Jenkins enough to get builds and 
unit tests to function smoothly; however, recompilation is still happening 
during the packaging step using an existing NAnt build system and not 
Jenkins.

## Problem:
Get packaging step, scripts written in 
NAnt, to pull and use latest compiled artifacts from 
Jenkins.
## Solution:
This process was pretty straight forward, 
until I got to the NAnt packaging scripts. In Jenkins under *Post Build 
Actions* for your job, select "Archive the Artifacts".  Then in the *Files to 
archive* setting, I entered "package/**", as the final step of our NAnt build 
script neatly puts the compiled artifacts into a folder aptly named 
"package".

With the build job set up, fire off a build now and visit 
http://your.jenkins.server.com/job/JobName/lastSuccessfulBuild/artifact/*zip*/archive.zip 
in your browser.  If all has gone well you will be downloading the zipped 
artifacts from the last successful build.

Armed with a functioning url, fire up the [NAnt 
docs](http://nant.sourceforge.net/release/0.91/help/tasks/get.html) for 
reference and drop this little gem in your script to pull the archived 
artifacts:

```
get 
src="http://jenkins.server.com/job/JobName/lastSuccessfulBuild/artifact/*zip*/archive.zip" 
dest="{build.current.outputdir}"
```
And ... Run.

BUILD FAILED
C:\Foo\Bar\default.build(48,10):
Unable to download 'http://your.jenkins.server.com/job/JobName/lastSuccessfulBuild/artifact/*zip*/archive.zip' 
to 'C:\your\working\dir\'. The remote server returned an error: (401) 
Unauthorized.

Right, pesky authentication. 

We need to get off track here for a moment 
to discuss some environmental details.  Jenkins is highly configurable and is 
flexible enough to run in many environments.  With the backdrop of Windows and 
and Active Directory I have currently opted for the following setup:

1. Jenkins as Windows Service - instructions 
[here](https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+as+a+Windows+service). 
1. IIS site that does url rewriting to forward requests to Jenkins via an 
inbound reverse proxy with Windows Authentication. 
"Why? Dear God, Why?" You ask.

Active Directory. 

While I am sure some people posses the magically delicious lucky charms to make the 
Jenkins AD plug-in and their AD services play ball, I had no such luck.  Plan 
B.  Use Windows Authentication through a forwarding site in IIS to proxy 
authentication.  This may seem ugly on the face of it; but, in an AD world 
this actually takes some of the pain out of configuring the whole environment 
- let the tools do the work.

The forwarding site is a snap to set up, 
relatively speaking:

1. Bind Jenkins to Localhost on your favorite port - 
instructions [here](https://wiki.jenkins-ci.org/display/JENKINS/Starting+and+Accessing+Jenkins) 
1. Build new site in IIS 
1. Disable all authentication except Windows Authentication 
1. Enable URL Rewriting 
1. Add inbound reverse proxy rule to rewrite jenkins.yourdomain.com to the 
localhost address for Jenkins. 
1. Create an AD GPO for your engineers to allow access to 
jenkins.yourdomain.com (you likely need to do this because the nice address 
will not be implicitly trusted by browsers as being part of the local domain) 
1. Set up logging in IIS 
1. Set up log rotation/deletion using the Task Scheduler 
1.  You can use a simple PowerShell script along these lines to do the heavy 
lifting: 

```powershell
get-childitem -Path C:\inet\logfile\path -recurse | 
where-object {$_.lastwritetime -lt (get-date).addDays(-N)} | 
Foreach-Object { del $_.FullName } get-childitem -Path C:\inet\logfile\path\service | 
where-object {$_.lastwritetime -lt (get-date).addDays(-N)} | 
Foreach-Object { del $_.FullName }
```

Loose reference from 
[here](http://stackoverflow.com/questions/17707757/powershell-to-output-folder-based-on-content-lastwritetime)

You may want to archive these logs rather than plainly deleting them depending on 
your security and bookkeeping needs.  Be aware that the log files will fill 
quickly with devs using Chrome notifiers, etc.  For Chrome, I use [Build Reactor](https://chrome.google.com/webstore/detail/buildreactor/agfdekbncfakhgofmaacjfkpbhjhpjmp?hl=en) 
and [Hudson Monitor](https://chrome.google.com/webstore/detail/hudson-monitor/lnalnbkkohdcnaapeeceifjabgmdfgah?hl=en), 
where Build Reactor monitors all active jobs on the server an Hudson Monitor 
covers my personal jobs.

At this point your engineers can access Jenkins from their browser with built in authentication and IT gets to 
centralize access control through AD ... Win-Win in my book!

And here we are, back at our original problem where the NAnt script cannot authenticate to Jenkins through IIS.  
There are a few options at this juncture:

1. Simply embed authentication in the get nAnt task - not much more to say than "ewww" 
1. Little bit of C# embedded in a nAnt script - this ought to get the job done nicely. 

Begin by building up a new target to hold our embedded script and add 
some error handling:

```
target name="utility.getartifacts">
fail message="util.getartifacts requires the outputdir property to be set." 
unless="${property::exists('outputdir')}"
```

Next we need a script tag and the relevant references and 
imports for our work.  Since we need to make a network request for our 
compiled artifacts and save them locally to disk we will want the System DLL 
and bring in the Net and IO namespaces.

```
<script language="C#" prefix="resource" /> 
<references>
  <include name="System.dll" />
</references>     
<imports>
  <import namespace="System.Net" />                
  <import namespace="System.IO" />            
</imports>
```

The core work of our script will be to build a 
WebClient and write the output of a download call to our output file location. 
 The work of setting up windows authentication for our WebClient is done 
through *UseDefaultCredentials = true*.  What we are gaining here is the 
ability for the user running our packaging script to have their credentials 
auto-negotiated by the WebClient.

```
<code>      
<![CDATA[
  [TaskName("get_artifacts")]            
  public class ArtifactTask : Task {
    [TaskAttribute("resourceUrl", Required=true)]
    [StringValidator(AllowEmpty = false)]
    public string ResourceUrl{ get; set; }
    
    [TaskAttribute("outputFile", Required=true)]
    [StringValidator(AllowEmpty = false)]
    public string OutputFile{ get; set; }
    public void GetArtifacts()
    {
      WebClient client = new WebClient();
      client.UseDefaultCredentials = true;
      client.Headers["User-Agent"] = 
        "Mozilla/4.0 (Compatible; Windows NT 5.1; MSIE 6.0) " +
        "(compatible; MSIE 6.0; Windows NT 5.1; " +
        ".NET CLR 1.1.4322; .NET CLR 2.0.50727)";
        // Download data.
        File.WriteAllBytes(OutputFile, client.DownloadData(ResourceUrl));

    }
    protected override void ExecuteTask() {
      GetArtifacts();
    }
  }
]]>    
</code>
```
Most of the preceding code is self 
explanatory; a few attributes to do some validation, an override and our meat 
and potatoes method GetArtifacts.

The final step is to put everything together into 5 simple calls: build an output directory, make a reference to 
the output file, download the zip of the artifacts, unzip the artifacts, and 
delete the zip to clean things up.

```
<mkdir dir="${build.current.outputdir}" />
<property name="build.current.artifacts" value="${project::get-base-directory()}\${build.current.outputdir}\archive.zip" />
<get_artifacts resourceUrl="http://your.jenkins.server.com/job/JobName/lastSuccessfulBuild/artifact/*zip*/archive.zip" 
outputFile="C:\your\working\dir\archive.zip />      
  <unzip zipfile="${build.current.artifacts}" />
  <delete file="${build.current.artifacts}" />
```

This is just the first in a series of posts where I will try to record my path to CI.  I cannot by any 
means say that this is the right way to do it; but, it is "a" way to do it.  
Feel free to rail on this in the comments below … we can all learn from an 
open discussion.  I suppose the most important notes to take away are as 
follows:

1. You need to be doing Continuous Integration/Automated 
Builds - "everyone" can't be wrong. 
1. Don't try to do it all in one go - the risk is just too high and 
disruptions in the build environment can ripple across an organization. 
1. Don't try to do it all in one go - your Devs will hate you for a massive 
process change. 
1. Don't make anyone's life harder - we are automating here, so the users 
lives should get easier, no matter what.  This may mean you have to sacrifice 
the easy and straight forward path for a convoluted hack-fest, just to get the 
ball rolling. 
1. Momentum is powerful - once you show everyone that this stuff is useful 
they will be inspired and might even help the effort.  No matter what, you 
won't be making things worse. 
1. Share your stories - everyone is yelling from the hills that you need to be 
doing CI; but few have been honest and open about how they are actually 
getting it done. 
1. Don't be a hero - realize that change takes time.  You want process to 
evolve organically … revolution will just piss everyone off. 