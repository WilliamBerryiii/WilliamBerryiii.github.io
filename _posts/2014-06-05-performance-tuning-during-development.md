---
layout: post
title: Performance Tuning During Development
date: '2014-06-05T22:41:00.001-07:00'
author: William Berry
tags:
- APIs
- Data Structures
- C#
- Performance Tuning
modified_time: '2014-06-06T00:46:27.550-07:00'
---

The day (and lately, night) job has been focused on a data api backing a new 
business insights tool.  Despite concerted efforts by nefarious interests, we 
have managed to keep the API resource centric, only leaking behavior where 
absolutely necessary.  We are starting the process of putting internal 
customers in front of the tool, and as such, I have become increasingly aware 
of the performance issues, of which there are quite a few. 

The API provides an abstraction over two different 
persistence store technologies (Sql Server &amp; HBase) and the domain models 
are built from data that resides in both stores.  No one particular resource 
channel is slow, but in the aggregate it *could* be more performant.  We have 
been working hard over the last few days to weave instrumentation into the 
application using Semantic Logging, and I figured, while I was down in bowels, 
I could investigate what I perceived to be performance problems.  

I started with the usual Visual Studio performance tooling ... 
fire up Performance Analyzer and run all of the stock wizard tests one by one 
(except for the contention test - I am not convinced it ever really gives 
useful information).  These tests should be focused and limited in scope.  
Running the analyzer for 20 min and exploring every corner of your API is for 
another time.  Here we are just trying to keep tabs on sticky or overly 
complex code blocks and you really just need to scout for a few key data 
points:
1. What methods in your stack or in the core libs are called most 
often? What is their percentage of total calls? 
1. What blocks of code are flagged in the hotlines graph? 
1. Where is most of the processing time spent? 
1. What spends the most time waiting for other methods to finish? 

Don't spend more than a few min just skimming the reports, remembering 
that you are here purely to simplify data structures, make your code cleaner 
and maybe a bit faster.  

Below is a classic example of 
scaffolded code that I started a new algorithm off with.  It was filled in 
with business logic, and then became a blight on the 
system.

First the scaffold code:

```csharp
var dedupedEdges = new List<Tuple<string, string>>(); 
foreach (var edge in edgeGroups.SelectMany(x => x.EdgeList))
    // Make sure both points are not "green" 
    // Tuple is not in list as (item1, item2) 
    // Tuple is not in list as (item2, item1) 
    { 
    dedupedEdges.Add(new Tuple<string, string>("","")); 
    }
```

After writing a few failing tests we have a naive implementation ... that works perfect over the small data set we are unit testing against. 

The code as first implemented:

```csharp
var dedupedEdges = new List<Tuple<string, string>>(); 
foreach (var edge in edgeGroups.SelectMany(x => x.EdgeList)
    .Where(x => !x.Item1.IsGreen() || !x.Item2.IsGreen()) 
    .Where(edge => !dedupedEdges 
        .Contains(new Tuple<string, string>(edge.Item1, edge.Item2))) 
    .Where(edge => !dedupedEdges 
        .Contains(new Tuple<string, string>(edge.Item2, edge.Item1)))) 
    { 
    dedupedEdges.Add(new Tuple<string, string>(edge.Item1, edge.Item2)); 
    }
```

Now I am not proud of this code; it's repetitive and poorly designed.  But, it's also done, working and passing 
all the tests.  *Don't fool yourself, if you write enough code, day in and day 
out ... a non-neglible percentage is pure drivel like this. *

So I am merrily flipping through the reports only to find that I am making 1.25 
million ... yes I said MILLION calls to Tuple.Item1 and another 1.25 million 
calls to Tuple.Item2 during one very large API call.  So following the 
hotlines graph, I am kindly directed by Visual Studio to the crap starting on 
line 2.  Knowing better than to just start hacking away at it, as my instincts 
directed, I put in some code to help me understand the severity of the problem 
first.  *"If it ain't Baroque don't fix it"* 

Stopwatch() ... as the 
guys on DotNetRocks say "*know it, learn it, love it.*"  I dropped one around 
this  block with a handy little *Debug.Print(Stopwatch.EllapsedMiliseconds)* 
and found my 2.5 million calls to Tuple.Item* were taking 1753ms, over an 
average of 10 runs across this code.  First, the .Net framework can clearly 
make very, very bad code run not so badly.  Second, I clearly have a 
demonstrable problem here.

When I <strike>wrote</strike> phoned in this 
code, I was focused on the bigger algorithm at hand ... "pass the tests and 
move on."  But now, armed with metrics, I have justifiable cause to go 
a'hacking. 

There are a number of things that need to be fixed, but 
let's first take a look at what this code is supposed to do.
1. The usage of *SelectMany* indicates in this context that we are iterating a child list 
of multiple *EdgeGroups*. 
1. An *Edge* is a *Tuple*&lt;*string* &amp; *string&gt;.* 
1. The first predicate filter makes sure both elements are not "*green*" 
(whatever *green* means). 
1. We then check the *dedupedEdges* *List* to make sure a new version of the 
*Tuple* is not already in the list. 
1. We next check the *dedupedEdges* *List* to make sure the reversed *Tuple* 
is not in the list. 
1. Finally take the Tuple, decompose it, rebuild a new tuple and finally add 
it to the *dedupedEdges* *List*. 

What, pray tell, could possibly be wrong here?  Let's go through each 
step and see if we can't make this better, shall we?

Well the first step is to not use a crappy data structure.  What we need here is a Set, 
someplace where we can only stick 1 of an item and not end up with any 
duplicates.  Additionally, we need to do fast lookups into the data structure 
to make sure the reversed tuple is not present.  Hello, 
[HashSet](http://msdn.microsoft.com/en-us/library/bb397727(v=vs.110).aspx).  
Let's see what this code looks like after a refactor:

```csharp 
var dedupedEdges = new HashSet<Tuple<string, string>>(); 
foreach (var edge in edgeGroups.SelectMany(x => x.EdgeList)
    .Where(x => !x.Item1.IsGreen() || !x.Item2.IsGreen()) 
    .Where(edge => !idIncludedEdges.Contains( 
        new Tuple<string, string>(edge.Item2, edge.Item1)))) 
    { 
    dedupedEdges.Add(edge); 
    }
```

The loop still does the original predicate on green-ness; but now, we are doing do a highly 
performant lookup on the reverse tuple construct and finish by blindly tossing 
the filtered items at the HashSet which will ensure uniqueness for us. 

Is this perfect?  *Nope*. 
Could it be better?  *Sure*. 
Do I care? *Nope*. 

I get paid to write code ... hopefully, a lot of code.  If I can 
produce that code quickly great!  If that code is quick itself, greater sill!  
If someone else can understand my quickly generated, quick code - I can stop 
for the day, as I have succeeded.

So, the totally unscientific 
performance boost from this refactor ... 1753ms ... to an average of 5ms over 
10 iterations. 

Core Takeaway:
1. You can do "some" performance 
work during development without hindering forward progress. 
1. If you chose to do performance during active development, keep your efforts 
reasonable. 
1. Deep dives while you are still developing an algorithm are distracting. 
1. Often you can make huge performance gains without changing the shape of the 
code. 
1. You will write crappy code and 90% of the time ... thats OK. 
1. Know that you write crappy code, own it, hunt for it, fix it. 
