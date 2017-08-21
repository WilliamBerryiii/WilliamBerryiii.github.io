---
layout: post
title: Generate Passwords with Membership Provider
date: '2014-05-20T10:40:00.005-07:00'
author: William Berry
tags: 
modified_time: '2014-05-20T10:40:58.536-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-114604735526611132
blogger_orig_url: http://www.lucidmotions.net/2014/05/generate-passwords-with-membership.html
---

To solidly rip off DotNetRocks ... today's installment of "Better Know a 
Framework's Methods", we bring you the [Generate 
Password](http://msdn.microsoft.com/en-us/library/system.web.security.membership.generatepassword.aspx) 
method of the Membership class in System.Web.Security namespace. 

<div><pre><span style="color: teal;">  1 <span style="color: blue;">public 
<span style="color: blue;">static <span style="color: blue;">string 
GeneratePassword( 
<span style="color: teal;">  2     <span style="color: blue;">int length, 
<span style="color: teal;">  3     <span style="color: blue;">int 
numberOfNonAlphanumericCharacters 
<span style="color: teal;">  4 )</pre> 
The method is clearly super simple to use, taking in an overall length of 
password and count of non-alphanumeric characters to seed the password with.  
I am sure there are all sorts of pitfalls to using this; but frankly, for a 
fast solution to generating passwords for zip files... this fits the bill 
nicely. 