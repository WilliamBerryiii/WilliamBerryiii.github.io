---
layout: post
title: A CI Migration Part III - Kiln, Jenkins & Web Hooks
date: '2014-02-10T21:58:00.000-08:00'
author: William Berry
tags:
- Kiln
- SCM
- Build Pipeline
- Mercurial
- Jenkins
- DevOps
- Web Hooks
modified_time: '2014-02-10T22:01:54.241-08:00'
thumbnail: http://1.bp.blogspot.com/-Ld73hmNt4KE/UrE7rPQARHI/AAAAAAAAAQI/hjjJxaFxV10/s72-c/SnipImage.JPG

---

For better or worse, the SCM I work with is Mercurial provided through 
Fogbugz' Kiln.  Yeah I know it's not GitHub, but I was ignorant of that 
decision as it was being made so, yeah.  Reviews, complaints, flamewars aside, 
working with it has not been bad and it has a reasonable feature set.  Of note 
is the ability to program web hooks to fire on a push to a repository. 

Configuring web hooks in Kiln is super easy and covered well in their online 
help 
[here](http://help.fogcreek.com/8111/web-hooks-integrating-kiln-with-other-services). 
 For our integration we will be using a custom web hook; in you admin panel 
select web hooks and a new hook for all repositories. 

[<img border="0" src="http://1.bp.blogspot.com/-Ld73hmNt4KE/UrE7rPQARHI/AAAAAAAAAQI/hjjJxaFxV10/s320/SnipImage.JPG" height="313" width="320" />](http://1.bp.blogspot.com/-Ld73hmNt4KE/UrE7rPQARHI/AAAAAAAAAQI/hjjJxaFxV10/s1600/SnipImage.JPG)
Once configured, Kiln will fire off a blob of JSON for a waiting web service 
to do something with.  We will primarily be interested in the pusher data, the 
repository group and the repository in the web hook data, though there is a 
wealth of other potentially relevant data.  We currently only use one master 
hook that listens for commits on all repository groups; primarily because the 
Jenkins Job Manager, covered in my [second article on CI migrations](http://www.lucidmotions.net/2013/12/a-ci-migration-part-ii-convention-over.html), 
filters an parses for relevant build related tasks. 

That said one should consider that there are endless possibilities for this 
information.  Consider the things we could do with web hooks: 

1. Trigger feature branch builds (as discussed). 
1. Keep a permanent log of commits by dev (regardless of feature branch 
destruction) 
1. Trigger round robin code reviews - good to give team members exposure to 
new elements. 
1. Send Chrome notification to dev to get up and walk around. 
1. Put pusher in the waiting room for next foosball game. 

Point being that once you have the data starting to work for you, the 
enterprise comes alive.  It is all about a loosely coupled, woven fabric of 
services and event streams working in a coordinated way to make everyone's 
life a little easier and more fun. 