---
layout: post
title: NuGet Servers, HBase, Thrift Code Generation and one sweet Jenkins CI Build
date: '2014-04-26T23:21:00.005-07:00'
author: William Berry
tags:
- Automation
- NTLM
- Build Pipeline
- NuGet
- Continuous Integration
- Jenkins
- ProGet
modified_time: '2014-04-26T23:23:50.561-07:00'
thumbnail: http://3.bp.blogspot.com/-xzJFMfVgMs8/U1wpZjkQvyI/AAAAAAAAARw/2nhM2agjsLQ/s72-c/SnipImage+copy+4.JPG
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-3115882263462139722
blogger_orig_url: http://www.lucidmotions.net/2014/04/nuget-code-generation-jenkins-thrift-hbase.html
---

Its always a bit of a joy when pet and client projects align on similar goals, 
the proverbial 'killing of two birds with one stone'.  Admittedly though, I 
applied a touch of coercion to get these in sync. 
<div> 
<div>The client project: <div>1. HBase Thrift connector in C#, which has a 
code generation step to convert the HBase thrift file into a C# lib. 
The pet project(s): <div>1. Internal NuGet Server 
1. Scripts for Jenkins to run a code generation process 
1. Scripts for Jenkins to build NuGet packages 
1. Programmatically building a C# Visual Studio project 
Though it is not the specific focus of this post, I will lightly cover the 
HBase thrift connector for those that are interested.  So without further 
adieu, lets get to work…## Step 1 - Build the NuGet Server<div>I screwed 
around for a while with the NuGet package that lets you build your own self 
hosted server.  For those that have the unnatural desire to tweak all the nobs 
… try it out.  I admit, I gave up very early in the process after realizing 
I could:<div>1. Use a pre-baked solution that was a snap to install and 
configure. 
1. Throw money at someone when our dependency on the product finally warranted 
support. 
<div>[ProGet (from Inedo)](http://inedo.com/proget/overview) was a great fit.  
Product is a snap to install, and configure.  I simply set up an IIS website 
as follows: <div>1. Define a default localhost:port binding (this was 
configured when installing the product). 
1. Define a redirect binding of nuget.{server}.{domain}.com to the localhost 
setup. 
1. Under the site's authentication settings, enable Windows Authentication, 
disable anonymous, remove the Negotiate provider from the Windows 
Authentication provider. 
1. Under authorization rules, add an entry for your group as "allow". 
1. Ping your IT/Active Directory team to add the redirect url to the groups 
trusted sites list. 
<div>In our department, we primarily use IE and Chrome, both honor the GPO 
trusted sites list though the setting does not always stick the first time 
through.  If that's the case for you, and the site is asking for 
authentication, be sure to kill IE &amp; Chrome, run a "gpupdate /force", then 
log out and back in again … it *should* work now. 

Lastly, NuGet Package Manager in Visual Studio works seamlessly with Windows 
NTLM Authentication.  With the site running, you now have a group 
authenticated, nominally secured internally hosted NuGet Server.  I think that 
deserves a "Sweet, Right On!"<div> 
## Step 2 - Configure NuGet<div>We have a few things to configure to get NuGet 
up and running after installation.  The developer's workstations will need to 
be patched to the new server so they can find your internally hosted packages 
and all build machines, plus their slaves, will need an additional 
configuration file.<div> 
<div>First things first, lets get the URL for our new server; this had me 
stumped for a bit.  Visit your new site in your browser of choice, select 
"Browse Packages" and then click on the RSS Feed button on the presented 
page.<div> 
<div class="separator" style="clear: both; text-align: center;">[<img 
border="0" 
src="http://3.bp.blogspot.com/-xzJFMfVgMs8/U1wpZjkQvyI/AAAAAAAAARw/2nhM2agjsLQ/s1600/SnipImage+copy+4.JPG" 
height="96" width="400" 
/>](http://3.bp.blogspot.com/-xzJFMfVgMs8/U1wpZjkQvyI/AAAAAAAAARw/2nhM2agjsLQ/s1600/SnipImage+copy+4.JPG)<div> 
<div>You will be presented with a page that has the Atom XML data, just grab 
the Url and fire up Visual Studio.<div> 
<div>The Visual Studio changes are a snap.  Under *Tools* -&gt; *NuGet Package 
Manager*, select "*Manage NuGet Packages for Solution*."  You will be 
presented with the hopefully familiar screen:<div> 
<div class="separator" style="clear: both; text-align: center;">[<img 
border="0" 
src="http://3.bp.blogspot.com/-Pyvthj9PqLc/U1wqTVQ-E1I/AAAAAAAAAR4/NqftVA0BTLI/s1600/SnipImage+copy+2.JPG" 
height="265" width="400" 
/>](http://3.bp.blogspot.com/-Pyvthj9PqLc/U1wqTVQ-E1I/AAAAAAAAAR4/NqftVA0BTLI/s1600/SnipImage+copy+2.JPG)<div> 
<div>Clicking on *Settings* in the lower left corner will bring you to the 
Visual Studio "*Options*" Window with *Package Sources* Settings in 
focus.<div> 
<div class="separator" style="clear: both; text-align: center;">[<img 
border="0" 
src="http://3.bp.blogspot.com/-BKeGoAsUhWY/U1wq5vSpcbI/AAAAAAAAASA/WMrfD-sqsOI/s1600/SnipImage+copy+3.JPG" 
height="322" width="400" 
/>](http://3.bp.blogspot.com/-BKeGoAsUhWY/U1wq5vSpcbI/AAAAAAAAASA/WMrfD-sqsOI/s1600/SnipImage+copy+3.JPG)<div> 
<div>In the upper right corner click the "*+*" button and add the url you 
copied from your browser earlier, and a name for your new NuGet Server.  
Select "*OK*."<div> 
<div>The next point to address is configuring the Build Server(s) and any 
slaves that perform NuGet Package Restores.  <div> 
<div>For almost all of our projects, we enable Nuget Package Restore.  This 
can be done by adding the following markup in your Nant target right before 
the call to MS Build. 

<div><pre><span style="color: #a65700;">&lt;<span style="color: 
#5f5035;">setenv<span style="color: #a65700;">&gt; 
    <span style="color: #a65700;">&lt;<span style="color: #5f5035;">variable 
<span style="color: #274796;">name<span style="color: #808030;">=<span 
style="color: #0000e6;">"<span style="color: 
#0000e6;">EnableNuGetPackageRestore<span style="color: #0000e6;">" <span 
style="color: #274796;">value<span style="color: #808030;">=<span 
style="color: #0000e6;">"<span style="color: #0000e6;">true<span style="color: 
#0000e6;">" <span style="color: #a65700;">/&gt; 
<span style="color: #a65700;">&lt;/<span style="color: #5f5035;">setenv<span 
style="color: #a65700;">&gt; 
</pre><pre><span style="color: #a65700;"> 
</pre><div>No matter which NuGet executable is called, the one included in 
your project or one installed on the host itself, the program can use a global 
config file located in "C:\ProgramData\NuGet".  Create the NuGet folder if it 
does not exist and add a file called *NuGetDefaults.config*.  You can Google 
plenty of resources on what can go in this file; but, what is essential is the 
following markup: 

<div><pre><span style="color: #004a43;">&lt;?<span style="color: maroon; 
font-weight: bold;">xml<span style="color: #004a43;"> <span style="color: 
#074726;">version<span style="color: #808030;">=<span style="color: 
#0000e6;">"<span style="color: #7d0045;">1.0<span style="color: 
#0000e6;">"<span style="color: #004a43;"> <span style="color: 
#074726;">encoding<span style="color: #808030;">=<span style="color: 
#0000e6;">"<span style="color: #0000e6;">UTF-8<span style="color: 
#0000e6;">"<span style="color: #004a43;">?&gt; 
<span style="color: #a65700;">&lt;<span style="color: 
#5f5035;">configuration<span style="color: #a65700;">&gt; 
    <span style="color: #a65700;">&lt;<span style="color: 
#5f5035;">packageSources<span style="color: #a65700;">&gt; 
        <span style="color: #a65700;">&lt;<span style="color: #5f5035;">add 
<span style="color: #274796;">key<span style="color: #808030;">=<span 
style="color: #0000e6;">"<span style="color: #0000e6;">nuget.org<span 
style="color: #0000e6;">" </pre><pre><span style="color: #274796;">            
 value<span style="color: #808030;">=<span style="color: #0000e6;">"<span 
style="color: #0000e6;">https://www.nuget.org/api/v2/<span style="color: 
#0000e6;">" <span style="color: #a65700;">/&gt; 
        <span style="color: #a65700;">&lt;<span style="color: #5f5035;">add 
<span style="color: #274796;">key<span style="color: #808030;">=<span 
style="color: #0000e6;">"<span style="color: #0000e6;">Nuget Source<span 
style="color: #0000e6;">" </pre><pre><span style="color: #274796;">            
 value<span style="color: #808030;">=<span style="color: #0000e6;">"<span 
style="color: #0000e6;">http://nuget.myserver.com/nuget/NugetFeed<span 
style="color: #0000e6;">" <span style="color: #a65700;">/&gt; 
    <span style="color: #a65700;">&lt;/<span style="color: 
#5f5035;">packageSources<span style="color: #a65700;">&gt; 
<span style="color: #a65700;">&lt;/<span style="color: 
#5f5035;">configuration<span style="color: #a65700;">&gt; 
</pre><pre><span style="color: #a65700;"> 
</pre><div>The markup here simply adds the sources that the build server may 
restore packages from; in this case both [nuget.org](http://nuget.org/) and 
our internal site.<div> 
<div>NOTE: *there are some pretty slick options when it comes to ProGet which 
you should look into.  You can have your local server act as a proxy for 
nuget.org and filter out packages with licenses that are incompatible with 
your environment.  Obviously it does not keep a dev from subverting legal 
requirements by simply including a package with the source commit; but, it can 
help stop accidental usage.*<div> 
<div>With our config file set up on the build server(s) and the dev 
environments patched, we can turn our attention back to getting our first 
package up on the new NuGet server.<div> 
## Step 3 - Thrift C# Code Generation<div>Though its a bit of a tangent to the 
core of this post, I am going to use the building of the C# classes for a 
Thrift to HBase connector as the example.<div> 
<div>Our first step is to set up a blank, no frills Visual Studio class 
library project.  Once that's up, go into the NuGet Package Manager and import 
the "Thrift" package by the *Apache Software Foundation*.  As of the writing 
of this article the version is *0.9.1.3*.  There are really only two important 
things in this package:<div>1. A precompiled Windows Thrift compiler, 
*thrift.exe*. 
1. The *Thrift.dll* which you will provide the common implementation code for 
your thrift interface. 
<div>NOTE: *quite obviously, both of these projects are publicly available.  
Though there is some complexity to compiling them yourself, you could for 
example, set up Jenkins to poll the github repository, scrape the tags on 
master, pull the most recent branch, version and build both the compiler and 
the core thrift.dll, posting the output automatically to your NuGet server.  
You *COULD* do that; but personally, I would rather just link the existing 
thrift NuGet package.*<div> 
<div>With the thrift NuGet package pulled into out project we are only missing 
the base.thrift file from the trunk of the apache HBase project, found 
[here](http://svn.apache.org/viewvc/hbase/trunk/hbase-thrift/src/main/resources/org/apache/hadoop/hbase/thrift/Hbase.thrift?view=markup). 
 Pull this file into a folder in your project, I put it under 
CodeGen\ThriftFiles.  <div> 
<div>One stupid note about this file.  As with most cross platform GitHub 
projects the line endings can be nearly random.  As of the writing of this 
post, they are old school Mac '\r', which may or may not screw things up.  
Regardless, you will see in the code generation script that I normalize the 
file to Windows' line endings as a precaution. <div> 
<div>We will be writing a PowerShell script to accomplish the code generation. 
 You can obviously use what ever you like.  I selected PowerShell … 
*because*.  Nuff-said and no comments on this from the peanut gallery. <div> 
<div>The basic flow of our script is as follows:<div>1. Clean the line endings 
of the thrift file. 
1. Create the output folder if it does not exist, if it does clean it. 
1. Pass the hbase.thrift file into the thrift compiler and generate the C# 
classes. 
1. Get the names of all the generated files. 
1. Open the .csproj file, select any existing nodes to remove and add the 
generated files. 
1. Save the .csproj file. 
<div>NOTE:  *I do not claim any responsibility for the code I am about to 
present.  As a recent migrant to PowerShell, I am putting myself and my code 
out there without warranties or promisses that it is either A) written well or 
B) even remotely how it should be done.  I so encourage commentary from the 
peanut gallery on this, if there is any.  I do appreciate learning how things 
could/should be done correctly.* 
<i> 
</i><div>Let's start by setting up some variables: 

<div><pre><span style="color: teal;">  1 <span style="color: 
#35687d;">$ErrorActionPreference = <span style="color: maroon;">"Stop" 
<span style="color: teal;">  2 <span style="color: #35687d;">$TargetDir        
     = <span style="color: maroon;">'.\src\ThriftInterface\autogen\' 
<span style="color: teal;">  3 <span style="color: #35687d;">$ThriftExecutable 
     = <span style="color: 
maroon;">'.\src\packages\Thrift.0.9.1.3\tools\thrift-0.9.1.exe' 
<span style="color: teal;">  4 <span style="color: #35687d;">$HBaseThriftFile  
     = <span style="color: 
maroon;">'.\src\CodeGeneration\ThriftFiles\hbase.thrift' 
<span style="color: teal;">  5 <span style="color: #35687d;">$Language         
     = <span style="color: maroon;">'csharp' </pre> 
<div>Fix the line endings in the thrift file as noted earlier: 

<div><pre><span style="color: teal;">  1 (<span style="color: 
#2b91af;">Get-Content <span style="color: #35687d;">$BaseThriftFile) | 
<span style="color: teal;">  2          <span style="color: 
blue;">Foreach-Object { 
<span style="color: teal;">  3                  <span style="color: 
#35687d;">$_ -replace <span style="color: maroon;">'`r`n' , <span 
style="color: maroon;">'`r' -replace <span style="color: maroon;">'`n' , <span 
style="color: maroon;">'`r' 
<span style="color: teal;">  4          } | 
<span style="color: teal;">  5          <span style="color: 
#2b91af;">Set-Content <span style="color: 
#35687d;">$BaseThriftFile</pre><pre></pre><div>Create the target output folder 
if it does not exist, clear its contents either way: 

<div><pre><span style="color: teal;">  1 <span style="color: 
#2b91af;">Write-Host <span style="color: maroon;">"Checking for existance of 
$TargetDir" 
<span style="color: teal;">  2 <span style="color: blue;">if(!(<span 
style="color: #2b91af;">Test-Path -Path <span style="color: 
#35687d;">$TargetDir )){ 
<span style="color: teal;">  3     <span style="color: #2b91af;">Write-Host 
<span style="color: maroon;">"Target does not exist, creating $TargetDir" 
<span style="color: teal;">  4     <span style="color: #2b91af;">New-Item 
-ItemType directory -Path <span style="color: #35687d;">$TargetDir 
<span style="color: teal;">  5 } 
<span style="color: teal;">  6 
<span style="color: teal;">  7 <span style="color: #2b91af;">Write-Host <span 
style="color: maroon;">"Clearing contents of $TargetDir" 
<span style="color: teal;">  8 <span style="color: #35687d;">$tardir = <span 
style="color: #35687d;">$TargetDir + <span style="color: maroon;">'\*.*' 
<span style="color: teal;">  9 <span style="color: #2b91af;">Remove-Item <span 
style="color: #35687d;">$tardir -recurse -force </pre> 
<div>Pass the cleansed file into the thrift compiler, specify the target 
language and direct the output: 

<div><pre><span style="color: teal;">  1 <span style="color: 
#2b91af;">Write-Host <span style="color: maroon;">"Begining code generation 
phase; output set to $TargetDir" 
<span style="color: teal;">  2 <span style="color: #35687d;">$arguments = 
<span style="color: maroon;">"-out $TargetDir --gen $Language $BaseThriftFile" 
<span style="color: teal;">  3 <span style="color: #2b91af;">Invoke-Expression 
<span style="color: maroon;">"$ThriftExecutable $arguments" 
<span style="color: teal;">  4 <span style="color: #2b91af;">Write-Host <span 
style="color: maroon;">"Finding Auto-generated Code in Directory: $TargetDir" 
<span style="color: teal;">  5 <span style="color: #35687d;">$tardir = <span 
style="color: #35687d;">$TargetDir + <span style="color: maroon;">'\HBase\*.*' 
<span style="color: green;"># HBase is the namespace 
<span style="color: teal;">  6 <span style="color: #35687d;">$autogenFileNames 
= <span style="color: #2b91af;">Get-ChildItem <span style="color: 
#35687d;">$tardir | 
<span style="color: teal;">  7                     <span style="color: 
blue;">Where-Object {<span style="color: #35687d;">$_.Extension -eq <span 
style="color: maroon;">".cs"} </pre> 
<div>Read the .csproj file into a variable: 

<div><pre><span style="color: teal;">  1 <span style="color: #35687d;">$proj = 
[xml](<span style="color: #2b91af;">get-content </pre><pre>                 
(<span style="color: #2b91af;">Resolve-Path <span style="color: 
maroon;">'.\src\ThriftInterface\ThriftInterface.csproj'))</pre> 
<div>Typically most project files only have one compile Item Group definition. 
 We will want access to that node later for the additions, so select it into a 
variable.  Then find any existing auto-generated file nodes and remove them. 

<div><pre><span style="color: teal;">  1 <span style="color: 
#35687d;">$ParentNode =  <span style="color: 
#35687d;">$proj.Project.ItemGroup.Compile.ParentNode | 
<span style="color: teal;">  2                <span style="color: 
#2b91af;">Select-Object -First <span style="color: maroon;">1 
<span style="color: teal;">  3 <span style="color: #35687d;">$removeElements = 
<span style="color: #35687d;">$proj.Project.ItemGroup.Compile | 
<span style="color: teal;">  4                   ? { <span style="color: 
#35687d;">$_.Include -Match <span style="color: maroon;">"autogen" } 
<span style="color: teal;">  5 <span style="color: blue;">if (<span 
style="color: #35687d;">$removeElements) { <span style="color: 
#35687d;">$removeElements | 
<span style="color: teal;">  6                        % { <span style="color: 
#35687d;">$_.ParentNode.RemoveChild(<span style="color: #35687d;">$_) } 
<span style="color: teal;">  7                      } </pre> 
<div>Finally, we want to loop the folder where the compiler put the generated 
code, add those files into the compile item group and save the project file. 

<div><pre><span style="color: teal;">  1 <span style="color: blue;">foreach 
(<span style="color: #35687d;">$fileName <span style="color: blue;">in <span 
style="color: #35687d;">$autogenFileNames.Name) { 
<span style="color: teal;">  2          <span style="color: #35687d;">$xmlElt 
= <span style="color: #35687d;">$proj.CreateElement(<span style="color: 
maroon;">"Compile", <span style="color: #35687d;">$nameSpace) 
<span style="color: teal;">  3          <span style="color: #35687d;">$xmlAtt 
= <span style="color: #35687d;">$proj.CreateAttribute(<span style="color: 
maroon;">"Include") 
<span style="color: teal;">  4          <span style="color: 
#35687d;">$xmlAtt.Value = <span style="color: 
maroon;">"autogen\Hbase\$fileName" 
<span style="color: teal;">  5          <span style="color: 
#35687d;">$xmlElt.Attributes.Append(<span style="color: #35687d;">$xmlAtt) 
<span style="color: teal;">  6          <span style="color: 
#35687d;">$ParentNode.AppendChild(<span style="color: #35687d;">$xmlElt) 
<span style="color: teal;">  7 } 
<span style="color: teal;">  8 
<span style="color: teal;">  9 <span style="color: #35687d;">$proj.Save((<span 
style="color: #2b91af;">Resolve-Path <span style="color: 
maroon;">".\src\ThriftInterface\ThriftInterface.csproj")) 
<span style="color: teal;"> 10 exit </pre> 
<div>So there you have it.  In 30 lines of code we have converted a .thrift 
file into a functioning Visual Studio Project! 

<div>## Step 4 - Script NuGet Package Creation<div>Our next task is to create 
a light script that can wrap up our project into a NuGet package. This 
requires all of about 8 lines of code. 

<div><pre><span style="color: teal;">  1 <span style="color: 
#35687d;">$ErrorActionPreference = <span style="color: maroon;">"Stop" 
<span style="color: teal;">  2 <span style="color: #35687d;">$curpath= <span 
style="color: maroon;">".\src\ThriftInterface\" 
<span style="color: teal;">  3 <span style="color: #35687d;">$projectName= 
<span style="color: maroon;">"ThriftInterface.csproj" 
<span style="color: teal;">  4 
<span style="color: teal;">  5 NuGet Pack <span style="color: 
maroon;">"$curpath$projectName" -Properties Configuration=Release 
-OutputDirectory <span style="color: #35687d;">$curpath 
<span style="color: teal;">  6 
<span style="color: teal;">  7 <span style="color: #35687d;">$package = 
@(<span style="color: #2b91af;">Get-ChildItem <span style="color: 
#35687d;">$curpath -include *.nupkg -recurse | <span style="color: 
#2b91af;">Sort-Object) 
<span style="color: teal;">  8 <span style="color: #35687d;">$key = <span 
style="color: maroon;">"*********************" 
<span style="color: teal;">  9 
<span style="color: teal;"> 10 nuget push -Source <span style="color: 
maroon;">"http://nuget.myserver.com/nuget/TreNugetFeed" <span style="color: 
#35687d;">$package[-<span style="color: maroon;">1] <span style="color: 
#35687d;">$key 
<span style="color: teal;"> 11 exit  </pre> 
<div>The script sets up some locals, runs *nuget pack* on the project with the 
proper build settings and calls *nuget push* on the package with the Api key 
to the NuGet server url. 

## Step 5 - Put It All Together With JenkinsFinal step here is to wrap the 
whole project up with a Jenkins job.  We need to commit our project shell to 
source control: Git/HG/SVN. Whatever works.  All of our projects include a 
moderately stock Nant script that sets up package structure for the binaries; 
which we will run in this example.  Even though the NuGet script in Step 4 
also performs a build, the Nant build will generate the artifacts for the 
binary repository.  And there is no real issue with building it twice. 

<div class="separator" style="clear: both; text-align: center;">[<img 
border="0" 
src="http://4.bp.blogspot.com/-EEf0j0jnxwU/U1xKbc12VQI/AAAAAAAAASQ/MLlSfDhzNpQ/s1600/SnipImage.JPG" 
height="286" width="640" 
/>](http://4.bp.blogspot.com/-EEf0j0jnxwU/U1xKbc12VQI/AAAAAAAAASQ/MLlSfDhzNpQ/s1600/SnipImage.JPG) 
Under the build in Jenkins we will configure the execution of out code 
generation script.  Since the PowerShell script is not yet signed, we need to 
set the execution policy to unrestricted. 

<div><pre><span style="color: teal;">  1 powershell.exe -command -<span 
style="color: #2b91af;">set-executionpolicy unrestricted   </pre> 
<div>Follow that up with a call to restore the Thrift NuGet package we 
included in the Visual Studio Project. 

<div><pre><span style="color: teal;">  1 nuget.exe -restore 
.\src\ThriftInterface.sln</pre> 
<div>This call will ensure that we have the compiler and thrift core dll on 
hand for the code generation and build steps.  With everything in place we can 
call out code generation script and follow that with the Nant build. 

<div><pre><span style="color: teal;">  1 .\src\CodeGeneration\CodeGen.ps1 
</pre> 
<pre></pre><div>Assuming compilation success we can add a post build task to 
run our NuGet packaging script. 

<div class="separator" style="clear: both; text-align: center;">[<img 
border="0" 
src="http://3.bp.blogspot.com/-Nui9a7M0oKM/U1xMucveXJI/AAAAAAAAASc/22pxsb0qsyw/s1600/SnipImage+copy.JPG" 
height="276" width="640" 
/>](http://3.bp.blogspot.com/-Nui9a7M0oKM/U1xMucveXJI/AAAAAAAAASc/22pxsb0qsyw/s1600/SnipImage+copy.JPG) 
<div>Again we need to set the environment execution policy to unrestricted. 

<div><pre><span style="color: teal;">  1 powershell.exe -command -<span 
style="color: #2b91af;">set-executionpolicy unrestricted  </pre> 
<div>And finally call our NuGet packaging script. 

<div><pre><span style="color: teal;">  1 
.\deployment_scripts\nuget_package.ps1</pre> 
<div>With everything set up, save the configuration, scroll back to the top of 
your Jenkin job, and press the magical "*build now*" button.  With luck on 
your side you should be able to browse your NuGet server and see your new 
package. 

There will likely be an upcoming post that builds upon this one, delving into 
creating a Linq provider on top of the HBase thrift lib generated here.  Feel 
free to comment here or ping me on Twitter 
[@williamberryiii](https://twitter.com/williamberryiii) with questions. 