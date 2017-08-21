---
layout: post
title: Implementing $Count in a Custom Linq Provider with WebAPI OData v4
date: '2015-05-24T17:43:00.004-07:00'
author: William Berry
tags:
- OData
- Solr
- C#
- C# NoSql
- LINQ
- WebAPI
modified_time: '2015-05-30T22:43:17.198-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-1465436280772497672
blogger_orig_url: http://www.lucidmotions.net/2015/05/implementing-count-in-custom-linq.html
---

Over the last week I have been working on implementing a custom Linq provider 
that wraps a Solr search query and returns a composite projection of the solr 
search results and some underlying Hbase data.  Just to add to the madness, 
the composite projection is a child element of a WebAPI endpoint and is made 
query-able via Odata. 

Before we can get to what this post is really about, implementing $count from 
the OData spec, we need to get familiar with all the moving pieces.  At the 
core, is the implementation of IQueryable or IOrderedQueryable if you need 
ordered results sets.  This queryable implementation takes a provider that 
consumes a context that handles all the parsing logic and mapping down to 
whatever service wrapper you are implementing for.  Throw in a few dozen 
classes to handle expression parsing, give yourself a week and boom you have a 
functioning IQueryable.  Then you turn on OData, wire up your controller and 
drop some code that looks like this: 

<pre style="background-color: white; margin: 0em; overflow: auto;"><code 
style="color: black; font-family: Consolas,&quot;Courier 
New&quot;,Courier,Monospace; font-size: 10pt;"><span style="color: blue;">var 
foo = <span style="color: blue;">new QueryableData&lt;Bar&gt;(_provider); 
<span style="color: blue;">var result = 
(IQueryable&lt;Bar&gt;)queryOptions.ApplyTo(foo); 

<span style="color: blue;">return <span style="color: blue;">new 
PageResult&lt;Bar&gt;(result.ToList(), <span style="color: blue;">null, 
_provider.Count);</code></pre> 
The provider is injected into the controller, passed to the QueryableData 
source, the OData QueryOptions are applied to the IQueryable and we return the 
result as a paged data set.  Boom. Slap some $count=true on the end of your 
urls and Done... 

Not so fast. 

I ran my code with a unit test to see what the $count was going to do.  
Unexpectedly, I encountered *'cannot convert IQueryable&lt;Bar&gt; to type 
long'* which had me a bit puzzled.  I had presumed that the count would turn 
out to be an expression that needed to be teased from the tree but in this 
case it appeared to be wrapping the entire tree - the debugger confirmed as 
much.  As a test, I reversed my logic of passing the count back as an 
accessory property up the chain to passing the queryable as the accessory and 
the count of results as the primary return type.  Running the unit test again 
resulted in yet another confusing error - *'cannot convert type long to 
IQueryable&lt;Bar&gt;'*. WTF? 

I reset my breakpoints and stepped through the code again finding a rather 
cleaver thing.  My expression parser was actually being called *twice*.  Once 
with the LongCout expression wrapper and then again without it.  A small 
change to my provider's execute method yielded the correct results: 

<pre style="background-color: white; margin: 0em; overflow: auto;"><code 
style="color: black; font-family: Consolas,&quot;Courier 
New&quot;,Courier,Monospace; font-size: 10pt;"><span style="color: blue;">if 
(Queryable == <span style="color: blue;">null) 
{ 
    <span style="color: blue;">var isEnumerable = (<span style="color: 
blue;">typeof(TResult).Name == <span style="color: #a31515;">"IEnumerable`1" 
|| <span style="color: blue;">typeof(TResult).Name == <span style="color: 
#a31515;">"Int64"); 
    <span style="color: blue;">var result = 
_serviceWrapperContext.Execute(expression, isEnumerable); 

    <span style="color: green;">// we dont have a count to contend with so 
just return the queryable 
    <span style="color: blue;">if (result.GetType() != <span style="color: 
blue;">typeof(QueryableCountWrapper)) 
        <span style="color: blue;">return (TResult)result; 

    <span style="color: blue;">var r = (QueryableCountWrapper)result; 
    <span style="color: green;">// Is our expression wrapped with a count 
query? 
    <span style="color: blue;">if (<span style="color: 
blue;">typeof(TResult).Name == <span style="color: #a31515;">"Int64") 
    { 
        Queryable = r.Queryable; 
        <span style="color: blue;">return (TResult)r.Count; 
    } 

    Count = Int64.Parse(r.Count.ToString()); 
} 
<span style="color: blue;">return (TResult)Queryable;</code></pre> 
Since the provider is an injected dependency of the controller with a per 
request life time, I am able to use it as a cache of sorts.  The first time 
through the execute method we will call our service wrapper context to have 
the query parsed, compiled and executed.  If we have a wrapping LongCount 
expression then the results will come back from the service wrapper bundled in 
a *QueryableCountWrapper*.  We can then unpack the *QueryableCountWrapper* 
into class properties, and with a bit of switching logic prevent a double 
execution of the service wrapper calls. 

Hope this saves someone some time in the future and happy coding. 