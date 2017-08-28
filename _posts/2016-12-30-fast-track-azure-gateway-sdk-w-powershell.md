---
layout: post
title: Using PowerShell to Fast Track Azure IoT Gateway SDK Projects
date: '2016-12-30T13:15:00.000-08:00'
author: William Berry
tags:
- Azure
- Modbus
- Powershell
- Azure IoT Gateway SDK
modified_time: '2016-12-30T18:07:00.549-08:00'
---

[<img border="0" height="200" src="https://upload.wikimedia.org/wikipedia/commons/2/2f/PowerShell_5.0_icon.png" width="200" />](https://upload.wikimedia.org/wikipedia/commons/2/2f/PowerShell_5.0_icon.png)

I've been working with the [Azure IoT Gateway SDK](https://github.com/Azure/azure-iot-gateway-sdk) quite a bit lately and 
the project setup experience is not only repetitive, but also somewhat error 
prone.  Make a dozen settings changes here. Forget a setting there. Edit a few 
CmakeLists files.\Watch the build explode. Fix. Build AGAIN. Rinse and repeat. 

I figure it was time to not only document the whole process, but encode it 
with PowerShell; 'cause "infrastructure as code" and if computers do anything 
well, it's to at least make the same mistakes in a repeatable fashion.  So 
let's whip up a script that will perform the following tasks: 

1. Create a new project directory 
1. Clone the Azure IoT Gateway SDK from GitHub 
1. Clone the Modbus sample module for the Gateway from GitHub 
1. Edit the relevant CMake files to include the sample Modbus module 
1. Build the SDK 
1. Create a Modbus module configuration file with all the correct settings to 
just 'work' 

While this example is tuned to building the Gateway SDK's [Modbus Sample module](https://github.com/Azure/iot-gateway-modbus), it could quite easily be 
adapted to build and configure any of the SDK's [included samples](https://github.com/Azure/azure-iot-gateway-sdk/tree/master/samples) 
or other add-on sample modules like the [OPC-UA Client](https://github.com/Azure/iot-gateway-opc-ua).

I'm a fan of constrained and declarative input so let's start by defining 
an Enum with the allowable transports for the IoT Hub.  The available options 
are 'AMQP', 'HTTP' and 'MQTT'.
 
<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=transport_enum.ps1"></script> 

We can then sett up all the pieces of configuration for the project, the 
IoT Hub, the device mapping and the Modbus Read module.
 
<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=settings.ps1"></script> 

After some troubles getting the environmental variable set up for the 
SDK's build script, I turned to Stack Overflow for some assistance and was we 
well rewarded.  Bill Stewart stepped up with a few functions to make the 
process easier; [his reply to my question](http://stackoverflow.com/a/41399983/1276028) includes his great 
Windows IT Pro blog post on the topic of PowerShell environment variable 
imports ... well worth a read.  For the sake of simplicity we'll just add them 
directly to the script.
 
<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=helper-funcs.ps1"></script> 

Next, we'll create the project directory and use `git` to clone the 
relevant repositories there.  Note that git uses stderr output for some output 
that is not really an error and the use of the `--quiet` or `-q` option for 
`clone` does not truly silence the stderr output.  There are some details in 
[this Posh-Git issue](https://github.com/dahlbyk/posh-git/issues/109).
 
<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=git.ps1"></script> 

We can now move the Modbus module and associated sample into the SDK 
repository and amend the relevant CMake files to have them built when we build 
the SDK.
 
<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=pre-build.ps1"></script> 

Let's move into the SDK directory and copy the current state of the 
session's environment variables for restore after the build. 

<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=env.ps1"></script> 

To build the SDK on Windows, the documentation notes that we need to run 
from a Visual Studio Command Prompt.  Behind the scenes, this special command 
prompt calls a batch file that sets up IDE options and tooling for building, 
debugging and deploying.  If you right click and check the properties for the 
shortcuts you'll find a call that looks like this:
 
```%comspec% /k ""C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat"" amd64_x86```

The operational gist here is to open a command prompt and keep it open, 
using the `/k` switch, after running the `vcvarsall` batch script with, in 
this case, the x64/x86 argument.  We'll leverage the functions I noted earlier 
to call this batch file directly, adding the environmental variables to our 
current PowerShell session, and the call the SDK's build script.  Note that 
we'll skip running the SDK's unit tests and finish by restoring the 
environmental variables to their original state.

<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=build.ps1"></script> 

As of the writing of this post, the build will complete with a few 
warning from the compiler as noted in this [Modbus module issue](https://github.com/Azure/iot-gateway-modbus/issues/4).

We can now turn our attention to setting up the gateway's configuration 
file for execution.  We'll want to reference the template configuration file 
for the Modbus gateway module and read it into a PowerShell object.
 
<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=config-template.ps1"></script> 

From here, we can pick out the various parts of the configuration file 
settings that need values and can conclude by serializing the configuration to 
a file in the SDK's build directory.  Take note that the parsing library that 
supports the gateway can only parse ASCII and UTF-8 encoded configuration 
files.  PowerShell's default encoding for the Out-File function is Unicode and 
without specifying the encoding the gateway will blowup with a non-descriptive 
error at run-time.

<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=settings.ps1"></script> 
 
You can now navigate to the compiled Modbus sample (`cd 
.\build\samples\modbus\Debug`) and run the compiled Modbus gateway sample with 
the following command: 

```  .\modbus_sample.exe .\modbus_win.json``` 

The complete script can be found here.  Open up an Administrator 
PowerShell ISE session, paste the code, modify the various settings for your 
demo project and run. 

<script src="https://gist.github.com/WilliamBerryiii/90d233de838bfd0d24f9c23cb0f314dc.js?file=script.ps1"></script> 
 
Happy Coding! 