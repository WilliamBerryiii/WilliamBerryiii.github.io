---
layout: post
title: LINQ Sequential Selects for Conditional Joins
date: '2014-02-25T23:21:00.004-08:00'
author: William Berry
tags: 
modified_time: '2014-02-25T23:23:19.686-08:00'

---

I just finished a block of code that, while not ground breaking, is well worth 
recording.  The problem setup is: 

List&lt;Foo> and List&lt;Bar> conditionally joined to produce 
List&lt;T> 

What data we join on, however, is conditional on a property x of Foo being in 
List&lt;Bar>.  Let's get a bit more concrete with our example since I hate 
completely abstract examples. 

I have a List&lt;AppetizerItems>, my wife has a List&lt;DinnerItems>.  
So lets put together our List&lt;possibleMenu> with a few caveats.  We 
would like to only go shopping at one store, be able to set the oven to one 
temperature and if the appetizer has has a wine, it would be nice if the 
dinner and appetizer shared the same color wine (i.e. red, white, rose, etc.). 

```csharp
var menu = appetizerItems 
    .Where( appetizerItem => 
        dinnerItems.Any( 
            dinnerItems => 
                dinnerItems.Store == appetizerItem.Store 
                && dinnerItems.OvenTemperature == 
appetizerItem.OvenTemperature 
        ) 
    .Select( appetizerItem => new 
    { 
        appetizerItem, 
        dinnerItem = ( 
            dinnerItems.Any(di => di.HasWine == appetizerItem.HasWine 
            ? dinerItems.First(di => 
                di.Store == appetizerItem.Store 
                && di.OvenTemperature == appetizerItem.OvenTemperature 
                && di.GrapeColor == appetizerItem.GrapeColor 
            ) 
            :  dinnerItems.First(di => 
                di.Store == appetizerItem.Store 
                && di.OvenTemperature == appetizerItem.OvenTemperature 
    }) 
    .Select(possibleMenu =>  new 
    { 
        possibleMenu.appetizerItem.AppetizerItems, 
        possibleMenu.dinnerItem.DinnerItems, 
        ... 
    }); 
```

As you can see, we have managed to do a conditional join via anonymous object 
composition and sequential selects. 