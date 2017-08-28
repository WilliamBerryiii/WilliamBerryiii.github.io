---
layout: post
title: Strata + Hadoop World 2015 - Conference or Trade Show?
date: '2015-02-22T15:40:00.001-08:00'
author: William Berry
tags:
- Big Data
- Hadoop
- Conference
modified_time: '2015-02-22T15:40:06.427-08:00'
---

Fresh off the plane from a few days at Strata + Hadoop World, I thought I'd 
draft a quick wrap up of the <strike>conference</strike> trade show.  This 
being my first attendance, expectations were quite high and I was 
unfortunately left frustrated and a bit disappointed. 

The event was held at the San Jose Convention Center and despite the buildings 
timid facade, the interior boasts a sprawling labyrinth of meeting rooms, 
public spaces and hidden hallways.  The organizers did well to provide plenty 
of workspace, conspicuous power and some of the best wifi I have experienced 
at a gathering of this size.  From a technical execution standpoint, the only 
blemish was sparse catering between scheduled breaks.  Finding a cup of coffee 
to prop yourself up during the extended afternoon sessions was an effort 
better fit for a scavenger hunt.  That said, the catering, when it was around, 
was on point with a fair diversity of offerings and a pleasant staff. 

Not unlike other gatherings of this size, the event pivoted around a sizable 
expo hall with plenty of variety on display.  During Wednesday's expo crawl, I 
found everything from two to three person startups to traditional enterprise 
integration firms to the multinationals; most all with polished pitches aimed 
at the myriad of personalities and business roles present. 

I zig-zagged my way through a sea of drones, "Bacon Scientist" t-shirts and 
overly caffeinated sales professionals and was struck by a rather horrifying 
realization - nearly every third vendor was brandishing demos about how their 
SQL/ACID transaction solution for Hadoop was "the fastest" or "the only".  
While many vendors are claiming that SQL will ultimately bring the masses to 
Hadoop, I worry that this very useful but still corner case capability for the 
platform has reached snake oil status.  More on this topic in my next post. 

The crawl ended at a modest 6:30pm leaving out-of-towners to fend for 
themselves that evening.  As is often the case on the road, Twitter saved a 
boring evening of hotel room email when Alistair Croll tipped me off to an 
event hosted by The Hive.  The meet and greet sandwiched a panel talk 
skillfully hosted by Alistair with Oscar Celma of Pandora, Jennifer Kennedy of 
SoundHound and Dr. Douglas Eck of Google's Play Music. 

As is often the case when listening to companies that have direct access to 
the emotional centers of our brains, I found myself completely enchanted with 
the possibilities and absolutely terrified for the future.  Perhaps the 
deepest and most unsettling settling insights came late in the evening as Dr. 
Eck explained the nuances of down voting a piece of music.  The overly eager 
group brandishing libations were lobed a doozie - "How can you tell if someone 
down voting every song on Coda hates Led Zeppelin or just the album?"  Blend 
the difficulty of that question with the threat of overplaying a beloved 
artist to a diehard fan and the complexities at hand become apparent.  As I 
stood there, Dr. Eck layered on the deep emotional connection we have to 
music, the difficulty of sustaining a listener's emotional state - positive or 
negative, and the goal of providing a rich and long lasting experience to 
expose the user to more advertising.  I closed out a rather late evening 
wondering how I would fair against two more days of thought provoking content. 

The following morning I found myself sitting in an overly dark room, amongst a 
sea of dimly lit laptops listening to the keynote addresses.  In turn - 
Cloudera, MemSql, SalesForce, MapR and IBM speakers leveraged identical 
formats to fill 10-15 minute slots with predictably bold statements about the 
future of "Big Data", each culminating with a terse and unashamed pitch for 
their various products.  On the tail of these presentations we encountered a 
meandering spiel by Dj Patil, the newly appointed US Chief Data Scientist, 
which included a short but warmly welcomed spot by President Obama.  Like 
papers strewn across a desk, the disjointed talk had clearly been disrupted by 
Mr. Patil's recent appointment and, unfortunately, it fell short of the 
momentum inducing spot it had been positioned for.  For those audience members 
seeking substance and had not yet walked out, two excellent talks punctuated 
the tail of the keynotes. The information dense, though poorly organized 
presentation from Solomon Hsiang on "Data-Driven Policy" brought to bear the 
complexities of interleaving data at global scale and the nervously delivered, 
but delightful and thought provoking talk from Poppy Crum of Dolby clearly 
illuminated our susceptibility to sensory augmentation through conflicting 
information sources.  In all, the balance in the keynotes would foreshadow the 
remainder of the content at Strata + Hadoop World. 

I kicked off the sessions with a talk on Apache Kafka which was about as 
informative as the project's homepage.  Kafka is exactly what you would expect 
to get from merging the clustering approaches of Hadoop, the WAL of a product 
like HBase or Cassandra and a message queue like RabbitMQ - all together very 
interesting stuff.  I would also say that behind mentions of Spark, it was the 
2nd most talked about project in the sessions.  Unfortunately in every 
OmniGraffle systems chart that was presented, replacing each occurrence of 
"Kafka" with "Tibco" and "Data Bus" with "Enterprise Message Bus" and it could 
easily have been 2005 all over again.  My point here is that the message bus 
in enterprise architecture has found its place and the considerations, such as 
asynchronicity, decoupling and message schema validation via middleware should 
be taken into account when building systems with Kafka.  If you are interested 
in getting a 10K foot overview, check out [this SE-Radio podcast](http://www.se-radio.net/2015/02/episode-219-apache-kafka-with-jun-rao/) 
on the project.  Last note of caution is that Kafka is not case hardened from 
a security perspective yet; those features and functionality are however on 
the roadmap. 

On the point of security, the Kafka session was followed up with an 
interesting presentation on the future of Hadoop security.  Core issues such 
as user proxying and restricting data access resonated with well with the 
audience.  Security after the fact on the platform is the current modus 
operandi and there were encouraging statements indicating that the trend may 
be reversing as common practices solidify.  I am not well informed on the 
topic, but my instinct says that we will see all the common RDBMS security 
controls ported or projected into the ecosystem very soon. 

The remainder of the early afternoon was filled with two sessions on data 
visualizations, both of which confirmed the immaturity of the field and the 
trail blazing that is being done daily by teams within the big data 
visualization space.  A quick post presentation chat with Etan Lightstone of 
New Relic re-introduced the work that Ernest Dichter did for Betty Crocker 
wherein adding an egg made housewives feel more involved in the process of 
baking; while relevant this is actually not true ([see here](http://www.bonappetit.com/entertaining-style/pop-culture/article/cake-mix-history)). 
 Either way, the chat did reignite concerns I have about giving users in data 
driven jobs just enough data to help them draw their own, albeit guided, 
conclusions. 

Around 5pm that evening I finally encountered the session I had been waiting 
for.  Scott Donaldson of FINRA gave a stunning architectural and 
implementation review of their fraud detection systems.  While the juicy 
details like cluster sizing were held back, he detailed an architecture which 
houses several petabytes of data and ingests a massive number of discretely 
schemed transactions per day.  Their solution is an interesting blend of bulk 
raw transaction data, data warehousing, network graphs to trace transaction 
flow between entities, data extraction into relational stores for deep 
analysis and an intense UI that enables investigators to exceed their prior 
investigational contexts. 

The following day picked up with an architectural patterns for Hadoop talk 
that while deeply interesting was for the most part a transposition of 
enterprise architectural patterns mixed with what has become standard data 
retention procedures of event sourcing systems.  On the back of that session, 
I had set high hopes for a deep dive into Elastic Search only to find a 
cursory review of [Kibana](http://www.elasticsearch.org/overview/kibana/) and 
its relationship to ElasticSearch.  Adding to the mediocre nature of the day 
was an introduction to using Parquet for ETL that landed in similar fashion to 
the prior day's Kafka talk.  We were presented with primarily a review of the 
internal structures of Parquet with little to any commentary as to its form 
and fit within an architecture.  The product itself is quite intriguing as a 
columnar data store that provides data packing for significant disk savings 
and increased search performance - for those in need of that feature set. 

In all, the conference was marginal at best.  Though it's obviously possible 
that I simply landed on a slew of sessions that missed reaching the potential 
of their abstracts, my instincts say that content like  FINRA will remain 
uncommon until implementors on the platform are willing to open up about what 
they are really doing behind closed doors.  So if you are just starting out 
with the platform, the conference as a trade show will introduce you to the 
big players in the field and provide enough orientation to sound informed 
during your first sales call.  Personally, should tickets fall into my lap 
next year and the ecosystem has see some significant changes then I might bear 
the cost of a flight and hotel room, otherwise I will be finding a different 
conference for my big data interests. 

Check back next week for a follow-up post on the state of big data post Strata & Hadoop World. 
