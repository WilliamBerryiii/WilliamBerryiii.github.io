---
layout: post
title: 'IIS getting in the way of a beautiful Jenkins and Artifactory Engagement '
date: '2014-01-08T22:03:00.001-08:00'
author: William Berry
tags:
- Artifactory
- NTLM
- Continuous Integration
- Jenkins
- DevOps
- Window's Authentication
- IIS
modified_time: '2014-01-08T22:03:29.435-08:00'
---

My Jenkins installation had turned into a bit of a saga lately.  I have been 
interested in trying out 
[Artifactory](http://www.jfrog.com/home/v_artifactory_opensource_overview) by 
JFrog to store not only our produced binaries; but, additionally to proxy 
external dependancies and provide a host for general software used across the 
enterprise. 

Most of the installation went pretty well, pulled a fresh JDK and JRE on the 
machine and ran the Installer.bat.  With the service up and running, I added 
some detailed connection information to the Tomcat config so that the 
Artifactory install would not conflict with the Jenkins install; namely to 
have it listen on localhost and an alternate port. 

As with the Jenkins installation, I created a proxy site with a URL rewrite, 
added NTLM Windows authentication, and updated the engineer's GPO to include 
the new url 'artifactory.host.domain.com'.  A few 'gpupdate /forces' and the 
new Artifactory site was up and running with auto-login. 

I created a repository for our main SaaS product and turned my focus to 
Jenkins. 

In Jenkins, I was able to quickly add the artifactory plugin and begin the 
process of wiring Jenkins to Artifactory.  Unfortunately, I have slammed 
solidly into a brick wall with an issue. 

When I attempt to test the connection from Jenkins to Artifactory via the 
Jenkins plugin, I get an 'unauthorized' exception.  Checking the service logs 
for Artifactory in IIS, I see requests arriving from Jenkins without any 
authentication information.  I would expect that IIS would respond to the 
authentication challenge from the Artifactory site with the application pools 
identity and properly negotiate.  In this case that is not happening. 

Since Jenkins and Artifactory are on the same host, I could reroute Jenkins to 
the localhost ip and bypass the NTLM authentication; but, then all my URLs for 
the links in Jenkins to Artifactory would have URLs that are inaccessible to 
human users. 

At this point I do not have a solution.  So if anyone reading this wants to 
chime in with any ideas … feel free to tell me I am doing it all wrong in 
the comments. 