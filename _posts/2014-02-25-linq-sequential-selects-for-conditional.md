---
layout: post
title: LINQ Sequential Selects for Conditional Joins
date: '2014-02-25T23:21:00.004-08:00'
author: William Berry
tags: 
modified_time: '2014-02-25T23:23:19.686-08:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-4061020750673606211
blogger_orig_url: http://www.lucidmotions.net/2014/02/linq-sequential-selects-for-conditional.html
---

I just finished a block of code that, while not ground breaking, is well worth 
recording.  The problem setup is: 

List&lt;Foo&gt; and List&lt;Bar&gt; conditionally joined to produce 
List&lt;T&gt; 

What data we join on, however, is conditional on a property x of Foo being in 
List&lt;Bar&gt;.  Let's get a bit more concrete with our example since I hate 
completely abstract examples. 

I have a List&lt;AppetizerItems&gt;, my wife has a List&lt;DinnerItems&gt;.  
So lets put together our List&lt;possibleMenu&gt; with a few caveats.  We 
would like to only go shopping at one store, be able to set the oven to one 
temperature and if the appetizer has has a wine, it would be nice if the 
dinner and appetizer shared the same color wine (i.e. red, white, rose, etc.). 

var menu = appetizerItems 
    .Where( appetizerItem =&gt; 
        dinnerItems.Any( 
            dinnerItems =&gt; 
                dinnerItems.Store == appetizerItem.Store 
                &amp;&amp; dinnerItems.OvenTemperature == 
appetizerItem.OvenTemperature 
        ) 
    .Select( appetizerItem =&gt; new 
    { 
        appetizerItem, 
        dinnerItem = ( 
            dinnerItems.Any(di =&gt; di.HasWine == appetizerItem.HasWine 
            ? dinerItems.First(di =&gt; 
                di.Store == appetizerItem.Store 
                &amp;&amp; di.OvenTemperature == appetizerItem.OvenTemperature 
                &amp;&amp; di.GrapeColor == appetizerItem.GrapeColor 
            ) 
            :  dinnerItems.First(di =&gt; 
                di.Store == appetizerItem.Store 
                &amp;&amp; di.OvenTemperature == appetizerItem.OvenTemperature 
    }) 
    .Select(possibleMenu =&gt;  new 
    { 
        possibleMenu.appetizerItem.AppetizerItems, 
        possibleMenu.dinnerItem.DinnerItems, 
        ... 
    }); 

As you can see, we have managed to do a conditional join via anonymous object 
composition and sequential selects. 