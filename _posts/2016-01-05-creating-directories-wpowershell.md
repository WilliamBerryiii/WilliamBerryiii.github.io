---
layout: post
title: Creating Directories w/Powershell for Developers
date: '2016-01-05T23:44:00.002-08:00'
author: William Berry
tags:
- Powershell
modified_time: '2016-01-05T23:44:58.885-08:00'
---

I was recently converting one of my open source projects from Nuget to Paket 
and encountered a classic headache for Windows developers ... adding a ".foo" 
directory to a project folder.  The leading period is a historical *nix 
technique employed to prevent the 'ls' command from showing the directory when 
not using the -a flag.  E.G. a folder structured like: 

```
- projectDirectory 
    | - .vs 
    | - .paket 
    | - Jenkins-FSharp 
```

The 'ls -a' command would display the following results: 

```shell
drwxr-----. root root {size} {date} .vs 
drwxr-----. root root {size} {date} .paket 
drwxr-----. root root {size} {date} Jenkins-FSharp 
```

and this using just the 'ls' command without the '-a' option: 

```
drwxr-----. root root {size} {date} Jenkins-FSharp 
```

For those of us in the Windows world, the use of a period as a prefix to a 
folder or a file is a nominal headache that needs to be consistently overcome. 
 The reason? Windows Explorer.  Unfortunately, Windows Explorer will not allow 
you to create a folder with a '.' prefix from the UI.  I am sure there are 
great reasons for this that are beyond both my pay grade and comprehension; 
either way, we are stuck with workarounds to accomplish our task. 

The old standby, which is short and succinct, is to open a cmd prompt in the 
current folder and issue the command 'mkdir .foo'. 

Conversely, for those like myself that live with a Powershell terminal window 
open, we have an even more succinct command - 'md .foo'.  'md' is an alias for 
the mkdir cmdlet which leverages the New-Item cmdlet to create your directory. 

In a similar fashion, you could use the more verbose method of calling the 
`New-Item` cmdlet directly using the `-Name` and `-ItemType` arguments.  The 
command looks like `New-Item -Name {folderName} -ItemType directory`. 

With our new folder created - Happy Codin' & Powershell'in! 