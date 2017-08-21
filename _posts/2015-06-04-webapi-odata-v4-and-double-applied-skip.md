---
layout: post
title: WebAPI OData v.4 and A Double Applied $Skip
date: '2015-06-04T23:41:00.002-07:00'
author: William Berry
tags:
- OData
- Solr
- APIs
- WTF
- C#
- LINQ
- WebAPI
modified_time: '2015-06-04T23:41:42.909-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-2663850955249402343
blogger_orig_url: http://www.lucidmotions.net/2015/06/webapi-odata-v4-and-double-applied-skip.html
---

As I noted in my last 
[post](http://www.lucidmotions.net/2015/05/implementing-count-in-custom-linq.html), 
I have been struggling to implement a LINQ provider over a Solr index.  While 
the adventure has been trying at times, for the most part been, it has been 
quite successful.  My final hurdle, one that I had been struggling with for 
the last week or so, was quite confounding ... when the $skip option was used, 
it was seemingly double applied.  To fully understand this behavior, let's 
look at a few examples: 
<div>1. A query string of ~?$top=10&amp;$skip=10 over a set of 100 results 
yields 0 results. 
1. A query string of ~?$top=10&amp;$skip=8 over a set of 100 results yields 2 
results. 
<div>Before I explain the crazy, let's take a look at the Controller's Get: 
<div><style type="text/css">.csharpcode, .csharpcode pre {  font-size: 
13.3333px;  font-width: 400;  color: black;  font-family: "Courier New"; } 
.csharpcode pre { margin: 0px; } .csharpcode .comment { color: #008000; } 
.csharpcode .comment2 { color: #808080; } .csharpcode .type { color: #2B91AF; 
} .csharpcode .keyword { color: #0000FF; } .csharpcode .string { color: 
#A31515; } .csharpcode .preproc { color: #0000FF; } </style> 
<div class="csharpcode"><pre style="background: #f0f0f0; border: 1px dashed 
#CCCCCC; color: black; color: black; overflow-x: auto; overflow-y: hidden; 
padding: 0px; text-align: left; word-wrap: normal;">[EnableQuery( 
    AllowedQueryOptions = AllowedQueryOptions.Count 
                          | AllowedQueryOptions.<span class="type">Filter 
                          | AllowedQueryOptions.OrderBy 
                          | AllowedQueryOptions.Skip 
                          | AllowedQueryOptions.Top)] 
[ODataRoute] 
<span class="keyword">public <span class="type">PageResult&lt;<span 
class="type">Foo&gt; Get(<span class="type">ODataQueryOptions&lt;<span 
class="type">Foo&gt; queryOptions) 
{ 

    <span class="type">var bars = <span class="keyword">new <span 
class="type">QueryableData&lt;<span class="type">Foo&gt;(_provider); 

    <span class="type">var result = ((<span class="type">IQueryable&lt;<span 
class="type">Foo&gt;)<span class="type">queryOptions 
        .ApplyTo(bars, 
            <span class="keyword">new <span 
class="type">ODataQuerySettings(<span class="keyword">new <span 
class="type">ODataQuerySettings { EnableConstantParameterization = <span 
class="keyword">false, EnsureStableOrdering = <span class="keyword">false 
}))).ToList(); 
    <span class="type">var count = _provider.Count; 
    <span class="keyword">return <span class="keyword">new <span 
class="type">PageResult&lt;<span class="type">Foo&gt;(result, <span 
class="keyword">null, count); 
}<!--[if IE]> 

<![endif]--></pre> 
We start off with our Enable Query Attribute to set which Query Options we 
will allow.  In this case we'll use everything but $select and $expand, and 
follow that with our OData routing attribute.  The Get method will return a 
PageResult since we wand to handle the paging and counting and not delegate 
that responsibility to the framework(s), and lastly, we will also manually 
handle applying the ODataQueryOptions. 

While it is not required to use the overload here with the ODataQueryOptions, 
it can be a helpful for certain optimizations.  In the event that the count 
query option was applied the framework will pass the query expression to the 
queryable twice, once with a return type of 'long and then again with a return 
type of IQueryable&lt;T&gt;.  Since all Solr queries implicitly return with 
the num_results property, we can ignore the count expression query and pass 
the results count back through the query provider thereby saving either two 
calls to the database or having to implement futures. 

Now, back to our problem. 

The prudent developer, when challenged with unexpected results from a method 
call might drop a breakpoint on the return statement and see what values are 
being returned.  Doing this left me rather puzzled ... the query string 
?$top=10&amp;$skip=10 returned a PageResult&lt;Foo&gt;(Foo[10], null, null), 
exactly what was expected.  I flipped back over to chrome to find 'value:[ ]' 
on my screen. 

After a few <strike>hours</strike> days of trying different things I elected 
to load up the GitHub issues list for OData and came across this post: [OData 
PageResult method ignoring count parameter when using EnableQuery attribute 
#159](https://github.com/OData/WebApi/issues/159).  Reading through the issue 
I had the idea that maybe, just maybe, the EnableQuery attribute was 
re-applying the query options over the PageResult.  After commenting out the 
attribute, the method began to function as expected and I had a few fistfuls 
of hair to spare. 

Hope this helps someone! 

For internet linking purposes ... here is my stack overflow [question and 
answer](http://stackoverflow.com/questions/30608837/webapi-odata-skip-on-custom-iqueryable-double-applied/30626736#30626736). 