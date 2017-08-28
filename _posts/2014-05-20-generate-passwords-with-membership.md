---
layout: post
title: Generate Passwords with Membership Provider
date: '2014-05-20T10:40:00.005-07:00'
author: William Berry
tags: 
modified_time: '2014-05-20T10:40:58.536-07:00'

---

To solidly rip off DotNetRocks ... today's installment of "Better Know a 
Framework's Methods", we bring you the [Generate Password](http://msdn.microsoft.com/en-us/library/system.web.security.membership.generatepassword.aspx) 
method of the Membership class in System.Web.Security namespace. 

```csharp
public static string GeneratePassword(
    int length, 
    int numberOfNonAlphanumericCharacters 
)
```

The method is clearly super simple to use, taking in an overall length of 
password and count of non-alphanumeric characters to seed the password with.  
I am sure there are all sorts of pitfalls to using this; but frankly, for a 
fast solution to generating passwords for zip files... this fits the bill 
nicely. 