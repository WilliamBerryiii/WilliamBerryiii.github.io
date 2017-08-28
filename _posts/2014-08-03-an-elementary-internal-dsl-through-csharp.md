---
layout: post
title: An Elementary Internal Domain Specific Language (DSL) Using C# Extension Methods
date: '2014-08-03T15:51:00.002-07:00'
author: William Berry
tags:
- Domain Specific Language
- Option Types
- C#
- Extension Methods
- DSL
modified_time: '2014-08-03T17:21:51.286-07:00'

---

A few weeks ago I had the opportunity to execute a small business rules engine 
for a client feature request that was done as an internal Domain Specific 
Language (DSL).  The novel aspect of the project for me was not the harnessing 
of extension methods; that, while not elementary, was trivial compared to the 
application of functional design/programing, specifically compositional 
concepts.  The resulting product was a terse, highly readable module that 
demonstrated the ability to fold functional approaches into an object oriented 
language and architecture.  Most importantly however, this project marked my 
first real "Ah Ha" moment with functional programing &amp; design approaches. 

*** 

From the applications perspective the interface into the rules engine was 
simple ... hand over the rules, hand over the things to run through the rules 
and then get back one or more applicable rules as the result.  Each rule 
consisted of several operations that needed to be validated to see if the rule 
applied.  For instance: start date, end date, minimum and maximum count, 
object selector.  By all accounts, a clearer case for an internal DSL could 
not be found. 

The first question I asked myself was what do I want this DSL to look like?  
Since, C# provides extension methods, which can be an enabler of building 
fluent internal DSLs, they seemed like a likely candidate; a few rounds of 
pseudo-coding later, I had something like this: 

```
var rule in rules){ 
    foreach(var obj in objects){ 
    return rule.HasTargetId(obj.id) 
            .AfterStartDate(obj.date) 
            .BeforeEndDate(obj.date) 
            .LessThanMax(obj.count) 
            .GreaterThanMin(obj.count) != null 
            ? rule 
            : null; 
    } 
} 
```

Readable, terse and easily extended notion - UNLOCKED. 

With pseudo-code in hand, I began to work on the component architecture.  
Since one of the core tenants of FP is to segregate data and behavior, I 
framed out a few classes: the rules engine, a static class to house all the 
rule operations, and a few data type classes to model rules and the objects to 
pass through the rules. 

The design of the rules engine class is very simple with only one constructor 
and one method.  The constructor takes in a set of rules as a dependency, 
building a readonly enumerable to hold the rules.  The single method, takes in 
a set of objects, pushes those into the local projection, and runs the rules 
returning a list of matched rule. 

The extension methods, housed in the static class, encapsulate the behavior on 
our data, and are equally as simple and the rules engine.  Let's take a look 
at one of them: 

```
public static Rule LessThanMax(this Rule rule, int objectCount){ 
    if(policy == null) return null; 
    return objectCount < rule.MaxCount ? rule : null; 
} 
```

The basic premise here is, if we pass in a null rule then the extension method 
simply returns null to the next method in the chain.  If the rule is not null 
then we check the rule and object arguments, either passing the rule or null 
along to the next method. 

While all these nulls floating around is not very pretty, it does get the job 
done; given that though, it may be preferable to create default instances of 
your rule(s) with sane values and pass that through in place of the nulls. 

And that's it ... a simple internal DSL that leverages extension methods, 
composition, segregation of data and behavior to facilitate an easy to reason 
about rules engine.  Most importantly ... no nasty nested "if" statements! 

For further study, I would highly suggest watching [Scott Wlaschin](https://twitter.com/ScottWlaschin)'s 
[Railway Oriented Programming](http://vimeo.com/97344498) talk to get some ideas about how you 
could weave in error handling; or checkout [Tomas Petricek](https://twitter.com/tomaspetricek) & [Jon Skeet](https://twitter.com/jonskeet)'s [Real World Functional 
Programming](http://www.manning.com/petricek/) book ... in chapter 5 they 
cover an implementation of Option Types in C# which would dramatically enhance 
the naive implementation above. 

As always, I would appreciate comments, corrections or feedback! 
