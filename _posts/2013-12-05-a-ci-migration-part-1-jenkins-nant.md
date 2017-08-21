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
modified_time: '2013-12-06T01:04:17.159-08:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-5956522040264772246
blogger_orig_url: http://www.lucidmotions.net/2013/12/a-ci-migration-part-1-jenkins-nant.html
---

I am deep in the throws of a slow migration that is laying the groundwork for 
a continuous integration style build =&gt; unit test =&gt; deploy =&gt; 
integration test, pipeline.  I have shaped Jenkins enough to get builds and 
unit tests to function smoothly; however, recompilation is still happening 
during the packaging step using an existing NAnt build system and not 
Jenkins.<br><div><br><div>Problem:<div>Get packaging step, scripts written in 
NAnt, to pull and use latest compiled artifacts from 
Jenkins.<div><br><div>Solution:<div>This process was pretty straight forward, 
until I got to the NAnt packaging scripts<br><br>In Jenkins under *Post Build 
Actions* for your job, select "Archive the Artifacts".  Then in the *Files to 
archive* setting, I entered "package/**", as the final step of our NAnt build 
script neatly puts the compiled artifacts into a folder aptly named 
"package".<br><br>With the build job set up, fire off a build now and visit 
http://your.jenkins.server.com/job/JobName/lastSuccessfulBuild/artifact/*zip*/archive.zip 
in your browser.  If all has gone well you will be downloading the zipped 
artifacts from the last successful build.<br><br>Armed with a functioning url, 
fire up the [NAnt 
docs](http://nant.sourceforge.net/release/0.91/help/tasks/get.html) for 
reference and drop this little gem in your script to pull the archived 
artifacts:<br><span style="font-family: monospace, 'Courier New', Courier; 
font-size: 14px;"><br>&lt;get 
src="http://jenkins.server.com/job/JobName/lastSuccessfulBuild/artifact/*zip*/archive.zip" 
dest="{build.current.outputdir}" /&gt;<br>And ... Run.<br><br><span 
style="font-family: monospace, 'Courier New', Courier; font-size: 14px;">BUILD 
FAILED<br><br>C:\Foo\Bar\default.build(48,10):<br>Unable to download 
'http://your.jenkins.server.com/job/JobName/lastSuccessfulBuild/artifact/*zip*/archive.zip' 
to 'C:\your\working\dir\'. The remote server returned an error: (401) 
Unauthorized.<br><span style="font-family: monospace, 'Courier New', Courier; 
font-size: 14px;"><br>Right, pesky authentication. <br><br><div 
style="text-align: center;">***<br>We need to get off track here for a moment 
to discuss some environmental details.  Jenkins is highly configurable and is 
flexible enough to run in many environments.  With the backdrop of Windows and 
and Active Directory I have currently opted for the following setup:<br>1. 
Jenkins as Windows Service - instructions 
[here](https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+as+a+Windows+service). 
1. IIS site that does url rewriting to forward requests to Jenkins via an 
inbound reverse proxy with Windows Authentication. 
"Why? Dear God, Why?" You ask.<br><br>Active Directory. <br><br>While I am 
sure some people posses the magically delicious lucky charms to make the 
Jenkins AD plug-in and their AD services play ball, I had no such luck.  Plan 
B.  Use Windows Authentication through a forwarding site in IIS to proxy 
authentication.  This may seem ugly on the face of it; but, in an AD world 
this actually takes some of the pain out of configuring the whole environment 
- let the tools do the work.<br><br>The forwarding site is a snap to set up, 
relatively speaking:<br>1. Bind Jenkins to Localhost on your favorite port - 
instructions 
[here](https://wiki.jenkins-ci.org/display/JENKINS/Starting+and+Accessing+Jenkins) 
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
<div><span style="font-family: monospace, 'Courier New', Courier; font-size: 
14px;">get-childitem -Path C:\inet\logfile\path -recurse | <br><span 
style="font-family: monospace, 'Courier New', Courier; font-size: 
14px;">where-object {$_.lastwritetime -lt (get-date).addDays(-N)} | <br><span 
style="font-family: monospace, 'Courier New', Courier; font-size: 
14px;">Foreach-Object { del $_.FullName } get-childitem -Path 
C:\inet\logfile\path\service | <br><span style="font-family: monospace, 
'Courier New', Courier; font-size: 14px;">where-object {$_.lastwritetime -lt 
(get-date).addDays(-N)} | <br><span style="font-family: monospace, 'Courier 
New', Courier; font-size: 14px;">Foreach-Object { del $_.FullName }<span 
style="font-family: monospace, 'Courier New', Courier; font-size: 
xx-small;">**<br><span style="font-family: monospace, 'Courier New', Courier; 
font-size: 14px;"><br><span style="font-family: monospace, 'Courier New', 
Courier; font-size: xx-small;">**Loose reference from 
[here](http://stackoverflow.com/questions/17707757/powershell-to-output-folder-based-on-content-lastwritetime)<br><br>You 
may want to archive these logs rather than plainly deleting them depending on 
your security and bookkeeping needs.  Be aware that the log files will fill 
quickly with devs using Chrome notifiers, etc.  For Chrome, I use [Build 
Reactor](https://chrome.google.com/webstore/detail/buildreactor/agfdekbncfakhgofmaacjfkpbhjhpjmp?hl=en) 
and [Hudson 
Monitor](https://chrome.google.com/webstore/detail/hudson-monitor/lnalnbkkohdcnaapeeceifjabgmdfgah?hl=en), 
where Build Reactor monitors all active jobs on the server an Hudson Monitor 
covers my personal jobs.<br><span style="font-family: monospace, 'Courier 
New', Courier; font-size: 14px;"><br>At this point your engineers can access 
Jenkins from their browser with built in authentication and IT gets to 
centralize access control through AD ... Win-Win in my book!<br><br><div 
style="text-align: center;">***<br>And here we are, back at our original 
problem where the NAnt script cannot authenticate to Jenkins through IIS.  
There are a few options at this juncture:<br>1. Simply embed authentication in 
the get nAnt task - not much more to say than "ewww" 
1. Little bit of C# embedded in a nAnt script - this ought to get the job done 
nicely. 
<div>Begin by building up a new target to hold our embedded script and add 
some error handling:<div><br><div><span style="font-family: monospace, 
'Courier New', Courier; font-size: 14px;">&lt;target 
name="utility.getartifacts"&gt;<div><span style="font-family: monospace, 
'Courier New', Courier; font-size: 14px;">        &lt;fail 
message="util.getartifacts requires the outputdir property to be set." 
unless="${property::exists('outputdir')}" /&gt;<div><span style="font-family: 
monospace, 'Courier New', Courier; font-size: 14px;">...<br>Next we need 
a<span style="font-family: 'Helvetica Neue Light', HelveticaNeue-Light, 
helvetica, arial, sans-serif;"> script tag and the relevant references and 
imports for our work.  Since we need to make a network request for our 
compiled artifacts and save them locally to disk we will want the System DLL 
and bring in the Net and IO namespaces.<div><br><span style="font-family: 
monospace, 'Courier New', Courier; font-size: 14px;">&lt;script language="C#" 
prefix="resource" &gt;<br>            &lt;references&gt;<br>                
&lt;include name="System.dll" /&gt;<br>            &lt;/references&gt;<br>     
       &lt;imports&gt;<br>                &lt;import namespace="System.Net" 
/&gt;<br>                &lt;import namespace="System.IO" /&gt;<br>            
&lt;/imports&gt;<br><span style="font-family: monospace, 'Courier New', 
Courier; font-size: 14px;"><br>The core work of our script will be to build a 
WebClient and write the output of a download call to our output file location. 
 The work of setting up windows authentication for our WebClient is done 
through *UseDefaultCredentials = true*.  What we are gaining here is the 
ability for the user running our packaging script to have their credentials 
auto-negotiated by the WebClient.<br><br><span style="font-family: monospace, 
'Courier New', Courier; font-size: 14px;">    &lt;code&gt;<br>         
&lt;![CDATA[<br>            [TaskName("get_artifacts")]<br>            public 
class ArtifactTask : Task {<br><br>                
[TaskAttribute("resourceUrl", Required=true)]<br><span style="font-family: 
monospace, 'Courier New', Courier; font-size: 14px;">                
[StringValidator(AllowEmpty = false)]<br>                public string 
ResourceUrl{ get; set; }<br><span style="font-family: monospace, 'Courier 
New', Courier; font-size: 14px;"><br>                
[TaskAttribute("outputFile", Required=true)]<br><span style="font-family: 
monospace, 'Courier New', Courier; font-size: 14px;">                
[StringValidator(<span style="font-family: monospace, 'Courier New', Courier; 
font-size: 14px;">AllowEmpty = false<span style="font-family: monospace, 
'Courier New', Courier; font-size: 14px;">)]<br><span style="font-family: 
monospace, 'Courier New', Courier; font-size: 14px;">                public 
string OutputFile{ get; set; }<br>              <br>                public 
void GetArtifacts()<br>                {<br>                    WebClient  
client = new WebClient();<br>                    client.UseDefaultCredentials 
= true;<br>                    client.Headers["User-Agent"] =<br>              
      "Mozilla/4.0 (Compatible; Windows NT 5.1; MSIE 6.0) " +<br>              
      "(compatible; MSIE 6.0; Windows NT 5.1; " +<br>                    ".NET 
CLR 1.1.4322; .NET CLR 2.0.50727)";<br><br>                    // Download 
data.<br>                    File.WriteAllBytes(OutputFile,<br><span 
style="font-family: monospace, 'Courier New', Courier; font-size: 14px;">      
                  client.DownloadData(ResourceUrl));<br>                
}<br><br>                protected override void ExecuteTask() {<br>           
         GetArtifacts();<br>                }<br>            }<br>        
]]&gt;<br>    &lt;/code&gt;<br><span 14px="" courier="" font-size:="" 
monospace="" new="" ourier=""><br>Most of the preceding code is self 
explanatory; a few attributes to do some validation, an override and our meat 
and potatoes method GetArtifacts.<br><br>The final step is to put everything 
together into 5 simple calls: build an output directory, make a reference to 
the output file, download the zip of the artifacts, unzip the artifacts, and 
delete the zip to clean things up.<br><br><span style="font-family: monospace, 
'Courier New', Courier; font-size: 14px;">        &lt;mkdir 
dir="${build.current.outputdir}" /&gt;<br>        &lt;property 
name="build.current.artifacts" value="${project::get-base-               <br>  
          directory()}\${build.current.outputdir}\archive.zip" /&gt;<br>       
 &lt;get_artifacts resourceUrl="<br><span style="font-family: monospace, 
'Courier New', Courier; font-size: 
14px;">http://your.jenkins.server.com/job/JobName/lastSuccessfulBuild/artifact/*zip*/archive.zip" 
outputFile="C:\your\working\dir\<span style="font-family: monospace, 'Courier 
New', Courier; font-size: 14px;">archive.zip<span style="font-family: 
monospace, 'Courier New', Courier; font-size: 14px;">" /&gt;<br><span 
style="font-family: monospace, 'Courier New', Courier; font-size: 14px;">      
  &lt;unzip zipfile="${build.current.artifacts}" /&gt;<br>        &lt;delete 
file="${build.current.artifacts}" /&gt;<br><br>This is just the first in a 
series of posts where I will try to record my path to CI.  I cannot by any 
means say that this is the right way to do it; but, it is "a" way to do it.  
Feel free to rail on this in the comments below … we can all learn from an 
open discussion.  I suppose the most important notes to take away are as 
follows:<br><br>1. You need to be doing Continuous Integration/Automated 
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
<div><br> 