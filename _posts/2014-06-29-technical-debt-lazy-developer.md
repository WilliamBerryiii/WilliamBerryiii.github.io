---
layout: post
title: Technical Debt & the Lazy Developer
date: '2014-06-29T00:02:00.002-07:00'
author: William Berry
tags:
- Development
- Technical Debt
modified_time: '2014-06-29T21:49:36.883-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-9178844970113218702
blogger_orig_url: http://www.lucidmotions.net/2014/06/technical-debt-lazy-developer.html
---

I have been reflecting over the last few days, what it means to be a "lazy" 
developer, inclusive of both positive and negative connotations. 
<blockquote class="twitter-tweet" lang="en">I yearn for the day when developer 
laziness is not the root cause of 
[#TechnicalDebt](https://twitter.com/hashtag/TechnicalDebt?src=hash). 
— William Berry (@williamberryiii) [June 27, 
2014](https://twitter.com/williamberryiii/statuses/482377144048578560)</blockquote> 
<script async="" charset="utf-8" 
src="//platform.twitter.com/widgets.js"></script>Yup, that was me, and what I 
see is manifest in two distinct ways: 
1. Lazy Loading 
1. Misaligned priorities, unwillingness to contribute and apathy 
<div style="text-align: left;">Each or these points is directly resulting in 
the accumulation of technical debt.  These thoughts are by no means localized 
to software development, the industry just happens to be an easy vehicle of 
context. 

<div style="text-align: center;">***<div style="text-align: left;"> 
From my vantage point, lazy loading is that delightful form of efficient 
procrastination where I don't actually do something until it's needed.  I 
don't add interfaces until the testing requires it.  I don't leverage 
encapsulation until I am passing around List&lt;Tuple&lt;int, 
KeyValuePair&lt;string, string&gt;&gt;&gt;.  If the code can be simple, flat, 
clean and free of excess abstractions ... then I leave it that way. 

There is also the classic example of lazy loading ... ORMs; the perfect double 
edged sword.  The vast majority of the time, lazy loading works to your 
benefit; but, every now and again ... it totally screws you. 

Where I find myself most guilty of lazy development is the classic arenas: 
instrumentation, telemetry data collection, error handling, logging, 
performance optimization and documentation. 

The first four, instrumentation, telemetry data collection, error handling and 
logging, are all classic after thoughts.  Even the most well intentioned 
developer will persistently screw this up.  Why? Because you don't ***NEED*** 
these things to get a product up and functioning; except that maturity and 
experience will eventually teach you, through enough browbeating, that you do 
in fact ***NEED*** these things to get a product up and functioning. 

On the surface, it's clear how one can address this form of technical debt.  
You "should" have logging, you "should" be collecting telemetry data, and at 
some point you will address the debt and add the elements, simply because you 
are left with no other choice.  But, your debts from implementation after 
fact, will not net 0.  You will be left with a very subtle issue.  That, I 
posit, can cause nearly as much damage to a system/product. 

When rings like logging and error handling are addressed after the core of the 
application has been solidified, they are merely stapled on features.  They 
may have been woven into the fabric of the system, but they have not grown and 
matured with the core entities.  As such, they will never feel like a natural 
part of the development process and there will always be friction in the usage 
of them. 

I have experienced refactoring several existing projects, as well as building 
a few new ones, where I swore I would not lazy-load the instrumentation ... 
surprise, still haven't learned (and I bet I am not the only with this 
issue).<div style="text-align: left;"> 
On the flip side, by most accounts, early performance optimization is a waste 
of time.  Don't fix it, if it ain't broke, right?  What I don't think has been 
settled officially is when "early", is.  I suggest, that performance go hand 
in hand with instrumentation and collection of telemetry data.  By leaving 
performance optimization and the supporting framework for a time when you 
actually have the problems, you're open to the exact same issue noted above, 
only subtly worse. 

Not only will you be gluing your performance data collection to the side of 
your app, rather than making it integral, you have no historical data to help 
you key in on when things went gone wrong.  You could have had video of all 
the events leading up to and beyond the tragedy, instead, you are left in a 
room with no windows, no doors and no murder weapon.  While I will concede 
that early performance optimization can be a wasted effort, the establishment 
of a supporting architecture and integration of carefully selected tooling, is 
by no means a waste of time. 

There are two main things in flux here, with the first being tooling.  Adding 
instrumentation, data collection, logging, error handling and the like, is not 
easy; and, there are typically several non-trivial architectural decisions 
that must be made upfront for their inclusion to feel native, and therefore 
inspire usage.  Compound the complexity of tooling integrations with the 
maturity required to identify the situations upfront ... it's no wonder why we 
are lazy with the implementation of these components and why so many projects 
suffer from lazy loaded technical debt. 

<div style="text-align: center;">***<div style="text-align: center;"> 
<div><blockquote class="twitter-tweet" lang="en">Always endeavor to do the 
best you possibly can. Acknowledging delivery of anything less is a show of 
apathy. 
— William Berry (@williamberryiii) [June 27, 
2014](https://twitter.com/williamberryiii/statuses/482414563217113088)</blockquote> 
Most people easily envision the technical debt that is the byproduct of 
"common" laziness: poor design choices, deliberately evading standard 
approaches, partially implemented or hack solutions, etc.  These 
manifestations are actually pretty easy to clean up. 

If a piece of code is poorly factored or does not adhere to typical 
implementation strategies, then simply mix some refactoring with training and 
education, and more often than not, the problem goes away with little fanfare. 

Another easily identified negative manifestation of laziness is weak or 
missing documentation.  While its quite obvious that most all projects need 
documentation to capture both institutional knowledge and execution context, 
what is not always obvious is the emergence of technical debt outside of the 
software product. 

Poor documentation will directly impact marketing efforts and project 
reputation.  Unless the project is in it's infancy, this debt is not easily 
addressable by simple bolstering the amount/quality of the documentation.  
Often, trust of the end user or implementing developer has been lost or 
compromised, and interest payments here can be very costly. 

One technique for small teams to address documentation issues up front, is to 
communicate through formal specifications.  Though the [Agile 
Manifesto](http://agilemanifesto.org/) favors working software over 
comprehensive documentation, what we are really trying to capture here is 
execution context, design decisions, encapsulation of complexity, domain 
modeling and the development of a ubiquitous language. 

By codifying in documentation the initial project activities, you are setting 
a platform upon which to build later.  As the project begins to mature and 
ramp up, leave the hard documentation behind in favor of patterns and 
practices that will result in automatic document generation as the project 
moves forward. 

To give a hard example, let's say we were building a internal facing API over 
a data store.  We would start with a simple requirements or story document 
that laid out the 10,000 foot overview.  The document would include some goals 
for performance, usage patterns, etc.  Next we would generate the core 
resource endpoints and entity models, thereby distilling entity properties and 
furthering the development of our ubiquitous language.  Once the core 
resources have been loosely agreed up, the team simply begins development. 

That said, one of the first features/stories to be implemented is a management 
interface that auto-documents the API's entities and resource URLs.  Using 
this approach we have leveraged documentation to record foundational execution 
context and provided a mechanism to ensure the consumer's documentation is 
always up to date and accurate.  Additionally, we have mitigating the 
technical debt thrown off by weak documentation and through automation we have 
ensured that the product and its documentation can grow and mature in unison. 

The devil however, in all this laziness, is as manifest from apathy or 
misaligned values.  In both cases the technical debt is accruing in not just 
the team's current work product, but also in everything the team touches. 

Of the two, apathy is significantly easier to mitigate.  Though it can spread 
like a virus, the "I don't give a shit" attitude, 9 times out of 10, is easily 
course corrected when caught early or when isolated to a single team member.  
The technical debt accrual in the products, much like in the simple laziness 
example above, can almost alway be brought back into control, through an 
ernest refactoring effort. 

The complexity in dealing with apathy is addressing the team's underlaying 
issues.  Understanding the root cause of the behavioral shift is paramount.  
One technique that a manager can leverage is to actually join the tumult.  
Through participation, the instigator(s) and core issue(s) is often exposed. 

Having been both an instigator and a manager dealing with rampant apathy, I 
was often able to attribute it to long work hours, and poor training/tooling.  
The savvy team lead will leverage the apathy to unite the team around the core 
issue and then behind the scenes facilitate its resolution ... building team 
cohesion and course correcting all in one move. 

The final point of contention is to address the technical debt thrown off by 
laziness as it is manifest through misaligned values.  Though intention and 
commitment may be present, there may be an unwillingness to work with the 
values or towards the goals of the rest of the team; the result being a single 
product headed in multiple directions. 

The laziness associated with misaligned values is not the fault of the 
seemingly misdirected employee, but rather with the project lead or the 
instigator of change.  As is well documented in [Leading 
Change](http://www.amazon.com/Leading-Change-With-Preface-Author/dp/1422186431/ref=sr_1_1?ie=UTF8&amp;qid=1404005602&amp;sr=8-1&amp;keywords=leading+change+kotter) 
by Kotter - the project lead or change initiator is at fault here, simply 
because they have failed to instill a sufficient sense of urgency to inspire 
change.  Without reason or sufficient energy, all systems will remain in 
stasis. 

If misaligned values or divergent paths is at the core of your technical debt 
generation, then I highly recommend reading Leading Change. 

The approach to addressing the technical debt from misaligned values is 
complex.  Not only will you be leading a change effort to adjust team 
alignment, but you will need to wait to drive the refactorings until after the 
team has unified it's values.  Any significant addressing of technical debt 
before alignment, will result in continued divergence, albeit with a smaller 
delta. 
<div style="text-align: left;"> 
<div style="text-align: left;">Being cognizant of laziness within your 
organization and/or teams is the first stepping stone.  Understanding it's 
various manifestations and coping with or mitigating the side effects is the 
trump card.  Lastly, don't forget to turn the mirror on yourself.  Are you 
leading change effectively, setting the guidelines and goals and innovating by 
example ... if not, don't try to fix your team, before you have taken the time 
to fix yourself. 
I would appreciate comments and a conversation either here on twitter where 
you can reach me [@WilliamBerryiii](https://twitter.com/williamberryiii) 