---
layout: post
title: Inherent Complexity of Interface Specfication
date: '2016-01-20T00:08:00.001-08:00'
author: William Berry
tags:
- No Silver Bullet
- Brooks
- Specifications
- Interfaces
modified_time: '2016-01-20T10:46:50.675-08:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-3777398030264230064
blogger_orig_url: http://www.lucidmotions.net/2016/01/inherent-complexity-of-interface.html
---

In Brook's 'No Silver Bullet' paper he argues, impotently, that "much 
complexity [in software] comes from conformation to other interfaces".  The 
whole argument, which can be found in the "Conformity" section reduces to: 
<div>1. Software needs to interact with the world and the world is complex, 
therefore software is complex, and/or 
1. Software is easy to change and thus must be the element which changes, 
therefore software is still complex. 
<div>To phrase it another way ... water is wet.<div> 
<div>Throughout his paper Brooks paints a likable characterization of the 
software engineering process, one that plays to the ego, to the self-centered. 
 I fell for it.  I drank up the Koolaid like so many a hapless lead engineer 
or inexperienced manager.  It behooves us to.  We are compelled.  The argument 
makes us feel important. Unfortunately, the thought, which appears so 
palatable, is nominally vacuous.  A conversation of the complexity introduced 
by interfaces, encompassing Brooks' comment that re-engineering cannot 
eliminate the complexities of consuming interfaces, is implicit in the design 
process and is thus hardly worth mentioning in such isolated terms.  Brooks 
misses the underpinnings of interface complexity completely with his 
hand-waving.  Let me explain ...<div> 
<div>If we are to believe point one where the world's man made interfaces are 
muddy, fully captured devices born of human flaw then one would suppose that 
the natural driving instinct of all system architects would be to shutter 
protocols capturing volumes of complexity fast inside components.  This would 
have the immediate result of reducing the number, and likely complexity, of 
interfaces and necessitates the creation of a few large functional units where 
domain complexity is captured internally to those units.<div> 
<div>Running somewhere between completely counter and moderately orthogonal to 
Brooks' first point is his second.  For the sake of re-iteration - because 
software is easy to change, it must be the element to change and conforming to 
extrinsic pressure drives complexity.  Intuition says that Brooks is correct.  
We enhance the changeability of our software by increasing the the count, and 
possibly the complexity of, the interfaces of a system.  This concept may be 
exacted at different levels of abstraction, equally workable at the method 
level and all the way up to intra-system communications.<div> 
<div>In either case however, capturing the notion of complexity arising from 
conforming to or confirming an interface is unimportant, and I would go so far 
as to say that holds true even nestled in conversation of essential vs 
accidental complexity.  Let's enumerate again the design options that arise 
from Brooks' argument:<div>1. We make large functional units that aptly 
capture domain complexity but resist change 
1. We make small functional units which enhance change, capture domain 
complexity but bring additional protocol complexity to bear. 
<div>Each point makes assumptions, alluding to the presence of external 
motivators.  Point one subsumes that our software is in need of future change. 
Point two suggests that the addition of protocol complexity is somehow 
burdensome and therefore must be avoided.  What's missing in Brooks' argument, 
underpinning the entire conversation about interfaces, are financial 
considerations and enabling options for the future.  <div> 
<div>For point one where we assume that changeability is a requirement it 
means that we have not only good faith but predictive financial assessments 
dictating that: 1) the system will require future modification and 2) that 
optimizing for those costs is necessary burden that must be undertaken now.  
In the absence of either data point, the so called Majestic Monolith rises as 
a clear path forward.  Though future engineers and managers will likely damn 
the decision, it will have been made with the best of intentions, fully 
informed. <div> 
<div>For point two we must tackle the notion that the complexity wrought by a 
multitude of interfaces is, in fact, burdensome.  In this decision path the 
additional complexity is inherent, unavoidable in the requirements, the 
financial burden is therefore implicit.  The decision left on the table is to 
implement custom protocols or to leverage pre-established protocols to 
optimize the situation.  In some cases the financial burden of custom 
protocols will be warranted, in others that will be the case (that discussion 
is beyond the scope of this paper).      <div><div>In either case though, the 
complexity of capturing the domain persists and remains the core consideration 
of interface design, irrespective of the architectural/design choices made 
through implementation which are, for all intents and purposes, purely 
financial decisions, by products of requirements.  Furthermore, even in the 
consideration of  capturing someone else's poorly designed API through 
abstraction is a financial relief in terms of avoiding implementing the 
captured behavior yourself. <div> 
<div>Brooks rightly captured the dimensions of interface specification, though 
he was hardly the first.  Unfortunately he identifies merely the canopy of the 
conversation missing wholly the financial motivators and underpinnings of 
interface specification. 