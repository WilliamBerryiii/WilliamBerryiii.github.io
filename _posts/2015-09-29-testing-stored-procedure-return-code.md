---
layout: post
title: Testing Stored Procedure Return Code Control Flow in C# with Moq
date: '2015-09-29T00:23:00.000-07:00'
author: William Berry
tags:
- Moq
- Testing
modified_time: '2015-09-29T00:23:00.906-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-5074276985536072095
blogger_orig_url: http://www.lucidmotions.net/2015/09/testing-stored-procedure-return-code.html
---

When modifying legacy code, one of our bigger challenges can be getting tests 
and test harness worked into the existing structures.  As I noted in my last 
post on [Timing Method Execution in 
C#](http://www.lucidmotions.net/2015/09/timing-method-execution-in-csharp.html), 
I've been spending quite a bit of time in our repository layer, and part of 
that work has been adding unit tests to old sections of the code base in 
preparation for some upcoming refactoring.  Obviously, or maybe not so 
obviously, there is an art to adding unit tests to code that was not 
originally designed to be tested, and the older portions of our repository 
layer are no exception. 

Think what you will of the approach, our data access is done nearly 100% 
through stored procedure calls, yielding two distinct challenges when 
attempting to test the code. 

<u>**Challenge 1 **</u> 
The repository makes heavy use of return codes from the stored procedures to 
drive control flow after a database call.  The return codes are occasionally 
passed back in ancillary tables, but more often than not they come back as 
output parameters supplied with the original call to the database, meaning 
setting the return code value to put post database call control flow under 
test is difficult at best. 

<u>**Challenge 2**</u> 
Again, and not unsurprisingly, the parameter lists for the stored procedure 
calls are built within the methods that need to be tested.  Each method 
includes logic to determine whether or not to include a parameter, if so what 
should the value be, etc., etc.  This is not as challenging as the return code 
issue, but it's not insignificant in and of itself. 

Enter [Moq](https://github.com/Moq). 

Moq is a wonderful testing framework for .Net that makes both mocking and 
stubbing a breeze.  The library does have a steep initial learning curve and 
will likely be frustrating to those who are less familiar with lambdas, funcs 
and actions; but it's power and ubiquity is worth the time investment to 
learn.  The framework has been essential in helping me get my repository code 
under test without having to modify the original code base.  So let's look at 
a simple example: 

<script 
src="https://gist.github.com/WilliamBerryiii/3c1eb22fc963cffe6cbf.js"></script> 
Starting off the test are a few local consts that will be helpful to have as a 
single point of change, a dictionary to store our parameter list and our mock 
executor defined against the ISqlExecutor interface.  Note that the 
ISqlExecutor interface simply does some lite wrapping of the SqlHelper Data 
Block from Microsoft to make things more consistent and simpler. 

After mocking the interface we encounter a call to Setup for our mock sql 
executor.  The setup method will provide a basic implementation of the 
interface method that is to be mocked, in this case the ExecuteNonQuery 
method.  What we are basically doing here is registering a method, on our mock 
object called ExecuteNonQuery and telling the Moq framework that the method 
will be called with 3 parameters - two strings and a dictionary.  For a lot of 
typical testing needs, particularly where you are just checking if a method 
was called, you would stop here appending only the Verifyable() method after 
the call to Setup; but in our case we need some more functionality. 

Following the Setup method is a call to Callback, the block of code in this 
method is an Action() that can be taken when the mock method is called.  
You'll notice that the delegate signature mirrors that of the mock method and 
in this case we'll use it to suck out the parameter list and store it locally 
for our following asserts, covering our needs in 'Challenge 2'.  Additionally, 
after copying out the parameter list from the call, we can inject a return 
code into the parameter dictionary allowing us to further test our post call 
control flow, exceptions and such from 'Challenge 1'. 

With the Setup and Callback put together we can then call the method under 
test and begin our stack of assertions - like the final line where we check 
that the return code meets expectations. 

Lastly, this whole approach could also be mixed with the [NUnit 
TestCase](http://www.nunit.org/index.php?p=testCase&amp;r=2.5) feature to put 
the method through its paces, exceptions and all. 

Happy Coding! 