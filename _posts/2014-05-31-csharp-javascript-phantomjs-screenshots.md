---
layout: post
title: Fun with C#, JavaScript & PhantomJS
date: '2014-05-31T14:40:00.001-07:00'
author: William Berry
tags:
- JavaScript
- C#
- PhantomJs
modified_time: '2014-06-01T13:25:13.862-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-6229064329590076049
blogger_orig_url: http://www.lucidmotions.net/2014/05/csharp-javascript-phantomjs-screenshots.html
---

I have a fun little project going on right now that involves taking a portion 
of a web page, loading it into PhantomJS, passing a lump of data to it, taking 
a picture of the page, and displaying that image in a RDLC report.  There are 
like a ba'gillion different ways to accomplish this, so the below is a 
hacker's proof of concept. 

<div><div style="text-align: center;">***<div> 
<div>First up, we are going to need is a very simple web page with the 
following elements: 
1. A form element with a hidden input "data" that will be used to move data 
from the primary application to the stub page. 
1. Two more inputs "height" and "width", which are used simply to show command 
line argument passing to Phantom. 
1. A button that can be used to trigger a JavaScript function that will in 
turn draw the page. 
<!-- HTML generated using hilite.me --> 
<div style="background: #ffffff; border-width: .1em .1em .1em .8em; border: 
solid gray; overflow: auto; padding: .2em .6em; width: auto;"><table><td><pre 
style="line-height: 125%; margin: 0;"> 1 
 2 
 3 
 4 
 5 
 6 
 7 
 8 
 9 
10 
11 
12 
13 
14 
15 
16 
17 
18 
19 
20 
21</pre><td><pre style="line-height: 125%; margin: 0;"><span style="color: 
#557799;">&lt;!DOCTYPE html&gt; 
<span style="color: #007700;">&lt;html <span style="color: 
#0000cc;">lang=<span style="background-color: #fff0f0;">"en" <span 
style="color: #0000cc;">xmlns=<span style="background-color: 
#fff0f0;">"http://www.w3.org/1999/xhtml"<span style="color: #007700;">&gt; 
    <span style="color: #007700;">&lt;head&gt; 
        <span style="color: #007700;">&lt;meta <span style="color: 
#0000cc;">charset=<span style="background-color: #fff0f0;">"utf-8" <span 
style="color: #007700;">/&gt; 
        <span style="color: #007700;">&lt;title&gt;This is my test page<span 
style="color: #007700;">&lt;/title&gt; 
        <span style="color: #007700;">&lt;script <span style="color: 
#0000cc;">src=<span style="background-color: #fff0f0;">"my.js"<span 
style="color: #007700;">&gt;&lt;/script&gt; 
    <span style="color: #007700;">&lt;/head&gt; 
    <span style="color: #007700;">&lt;body <span style="color: 
#0000cc;">style=<span style="background-color: #fff0f0;">"background-color: 
white; color: black; font-size: 1em;"<span style="color: #007700;">&gt; 
        <span style="color: #007700;">&lt;form&gt; 
            <span style="color: #007700;">&lt;input <span style="color: 
#0000cc;">id=<span style="background-color: #fff0f0;">"data" <span 
style="color: #0000cc;">type=<span style="background-color: #fff0f0;">"hidden" 
<span style="color: #0000cc;">name=<span style="background-color: 
#fff0f0;">"data" <span style="color: #0000cc;">value=<span 
style="background-color: #fff0f0;">""<span style="color: #007700;">&gt; 
            <span style="color: #007700;">&lt;input <span style="color: 
#0000cc;">id=<span style="background-color: #fff0f0;">"height" <span 
style="color: #0000cc;">type=<span style="background-color: #fff0f0;">"hidden" 
<span style="color: #0000cc;">name=<span style="background-color: 
#fff0f0;">"height" <span style="color: #0000cc;">value=<span 
style="background-color: #fff0f0;">""<span style="color: #007700;">&gt; 
            <span style="color: #007700;">&lt;input <span style="color: 
#0000cc;">id=<span style="background-color: #fff0f0;">"width" <span 
style="color: #0000cc;">type=<span style="background-color: #fff0f0;">"hidden" 
<span style="color: #0000cc;">name=<span style="background-color: 
#fff0f0;">"width" <span style="color: #0000cc;">value=<span 
style="background-color: #fff0f0;">""<span style="color: #007700;">&gt; 
            <span style="color: #007700;">&lt;button <span style="color: 
#0000cc;">id=<span style="background-color: #fff0f0;">"buildFoo" <span 
style="color: #0000cc;">name=<span style="background-color: 
#fff0f0;">"buildFoo" 
             <span style="color: #0000cc;">type=<span style="background-color: 
#fff0f0;">"button" <span style="color: #0000cc;">value=<span 
style="background-color: #fff0f0;">"Submit" 
             <span style="color: #0000cc;">onclick=<span 
style="background-color: #fff0f0;">" init() " <span style="color: 
#0000cc;">style=<span style="background-color: #fff0f0;">"visibility: 
hidden;"<span style="color: #007700;">&gt; 
      <span style="color: #007700;">&lt;/button&gt; 
        <span style="color: #007700;">&lt;/form&gt; 
        <span style="color: #007700;">&lt;div <span style="color: 
#0000cc;">class=<span style="background-color: #fff0f0;">"container"<span 
style="color: #007700;">&gt; 
        <span style="color: #007700;">&lt;/div&gt; 
    <span style="color: #007700;">&lt;/body&gt; 
<span style="color: #007700;">&lt;/html&gt; 
</pre><div> 
Hopefully it's obvious that our Javascript method init() in my.js, will simply 
plunk everything in the "container" div for display. 

<div style="text-align: center;">*** 
The next element we need, moving up the stack, is our Javascript runner that 
we will pass to Phantom, kicking this whole process off.  Make note of the 
filesystem call for *stumpage.html*; this could be passed in; but, I figured 
showing a filesystem call might be useful to someone. 

<div><!-- HTML generated using hilite.me --> 
<div style="background: #ffffff; border-width: .1em .1em .1em .8em; border: 
solid gray; overflow: auto; padding: .2em .6em; width: auto;"><table><td><pre 
style="line-height: 125%; margin: 0;"> 1 
 2 
 3 
 4 
 5 
 6 
 7 
 8 
 9 
10 
11 
12 
13 
14 
15 
16 
17 
18 
19 
20 
21 
22 
23 
24 
25 
26 
27 
28 
29 
30 
31 
32 
33 
34 
35 
36 
37 
38 
39 
40 
41 
42 
43 
44 
45 
46 
47 
48 
49 
50 
51 
52 
53 
54 
55 
56 
57 
58 
59 
60 
61 
62 
63 
64 
65 
66 
67 
68 
69 
70 
71 
72 
73 
74 
75 
76 
77 
78 
79 
80 
81 
82 
83</pre><td><pre style="line-height: 125%; margin: 0;"><span style="color: 
#008800; font-weight: bold;">var system <span style="color: #333333;">= 
require(<span style="background-color: #fff0f0;">'system'); 
<span style="color: #008800; font-weight: bold;">var args <span style="color: 
#333333;">= require(<span style="background-color: #fff0f0;">'system').args; 
<span style="color: #008800; font-weight: bold;">var fs <span style="color: 
#333333;">= require(<span style="background-color: #fff0f0;">'fs'); 
<span style="color: #008800; font-weight: bold;">var page <span style="color: 
#333333;">= require(<span style="background-color: 
#fff0f0;">'webpage').create(); 

<span style="color: #888888;">//args[0] is this javascript file. 
<span style="color: #008800; font-weight: bold;">var height <span 
style="color: #333333;">= args[<span style="color: #0000dd; font-weight: 
bold;">1]; 
<span style="color: #008800; font-weight: bold;">var width <span style="color: 
#333333;">= args[<span style="color: #0000dd; font-weight: bold;">2]; 

<span style="color: #008800; font-weight: bold;">var address <span 
style="color: #333333;">= <span style="background-color: #fff0f0;">"file:///" 
<span style="color: #333333;">+ fs.workingDirectory <span style="color: 
#333333;">+ <span style="background-color: #fff0f0;">"/stubpage.html"; 
<span style="color: #008800; font-weight: bold;">var data <span style="color: 
#333333;">= system.stdin.readLine(); 

page.open(address, <span style="color: #008800; font-weight: bold;">function() 
{ 

 page.zoomFactor <span style="color: #333333;">= <span style="color: #0000dd; 
font-weight: bold;">1; 
 page.viewportSize <span style="color: #333333;">= { 
  width<span style="color: #333333;">: width, 
  height<span style="color: #333333;">: height 
 }; 
 page.evaluate(<span style="color: #008800; font-weight: bold;">function(data, 
height, width) { 
  <span style="color: #888888;">//add the "data" to our page 
  <span style="color: #008800; font-weight: bold;">var d <span style="color: 
#333333;">= <span style="color: #007020;">document.getElementById(<span 
style="background-color: #fff0f0;">'data'); 
  d.value <span style="color: #333333;">= data; 
  <span style="color: #888888;">//set the height input 
  <span style="color: #008800; font-weight: bold;">var h <span style="color: 
#333333;">= <span style="color: #007020;">document.getElementById(<span 
style="background-color: #fff0f0;">'height'); 
  h.value <span style="color: #333333;">= height; 
  <span style="color: #888888;">//set the width input 
  <span style="color: #008800; font-weight: bold;">var w <span style="color: 
#333333;">= <span style="color: #007020;">document.getElementById(<span 
style="background-color: #fff0f0;">'width'); 
  w.value <span style="color: #333333;">= width; 
  <span style="color: #888888;">//click the button to fire the page's JS 
  <span style="color: #008800; font-weight: bold;">var b <span style="color: 
#333333;">= <span style="color: #007020;">document.getElementById(<span 
style="background-color: #fff0f0;">"buildFoo"); 
  b.click(); 
 }, data, height, width); 

 waitFor(<span style="color: #008800; font-weight: bold;">function() { 
  <span style="color: #888888;">//something to wait on ... 
  <span style="color: #008800; font-weight: bold;">return page.evaluate(<span 
style="color: #008800; font-weight: bold;">function() { 
   <span style="color: #888888;">//do we ahve a foo element on the page yet? 
   <span style="color: #008800; font-weight: bold;">if (<span style="color: 
#007020;">document.getElementById(<span style="background-color: 
#fff0f0;">'foo')) { 
    <span style="color: #008800; font-weight: bold;">return <span 
style="color: #008800; font-weight: bold;">true; 
   } <span style="color: #008800; font-weight: bold;">else { 
    <span style="color: #008800; font-weight: bold;">return <span 
style="color: #008800; font-weight: bold;">false; 
   } 
  }); 
 }, <span style="color: #008800; font-weight: bold;">function() { 
  <span style="color: #888888;">//take a picture, it lasts longer 
  <span style="color: #008800; font-weight: bold;">var base64Image <span 
style="color: #333333;">= page.renderBase64(<span style="background-color: 
#fff0f0;">'PNG'); 
  <span style="color: #888888;">//write the image to stdout 
  system.stdout.write(base64Image); 
  <span style="color: #007020;">window.phantom.exit(); 
 }); 
}); 

<span style="color: #008800; font-weight: bold;">function waitFor(testFx, 
onReady, timeOutMillis) { 
 <span style="color: #888888;">// timeout after 10 sec. 
 <span style="color: #008800; font-weight: bold;">var maxtimeOutMillis <span 
style="color: #333333;">= timeOutMillis <span style="color: #333333;">? 
timeOutMillis <span style="color: #333333;">: <span style="color: #0000dd; 
font-weight: bold;">10000, 
  start <span style="color: #333333;">= <span style="color: #008800; 
font-weight: bold;">new <span style="color: #007020;">Date().getTime(), 
  condition <span style="color: #333333;">= <span style="color: #008800; 
font-weight: bold;">false, 
  interval <span style="color: #333333;">= setInterval(<span style="color: 
#008800; font-weight: bold;">function() { 
   <span style="color: #008800; font-weight: bold;">if ((<span style="color: 
#008800; font-weight: bold;">new <span style="color: 
#007020;">Date().getTime() <span style="color: #333333;">- start <span 
style="color: #333333;">&lt; maxtimeOutMillis) 
    <span style="color: #333333;">&amp;&amp; <span style="color: 
#333333;">!condition) { 
    <span style="color: #888888;">// If not time-out yet 
    <span style="color: #888888;">// and condition not yet fulfilled 
    condition <span style="color: #333333;">= (<span style="color: #008800; 
font-weight: bold;">typeof(testFx) <span style="color: #333333;">=== <span 
style="background-color: #fff0f0;">"string" 
     <span style="color: #333333;">? <span style="color: 
#007020;">eval(testFx) 
     <span style="color: #333333;">: testFx()); 
   } <span style="color: #008800; font-weight: bold;">else { 
    <span style="color: #008800; font-weight: bold;">if (<span style="color: 
#333333;">!condition) { 
     <span style="color: #888888;">// If condition still not fulfilled 
     <span style="color: #888888;">//(timeout but condition is 'false') 
     phantom.exit(<span style="color: #0000dd; font-weight: bold;">1); 
    } <span style="color: #008800; font-weight: bold;">else { 
     <span style="color: #888888;">// Condition fulfilled 
     <span style="color: #888888;">//(timeout and/or condition is 'true') 
     <span style="color: #008800; font-weight: bold;">typeof(onReady) <span 
style="color: #333333;">=== <span style="background-color: #fff0f0;">"string" 
     <span style="color: #333333;">? <span style="color: 
#007020;">eval(onReady) 
     <span style="color: #333333;">: onReady(); 
     <span style="color: #888888;">//&lt; Stop this interval 
     clearInterval(interval); 
    } 
   } 
  }, <span style="color: #0000dd; font-weight: bold;">250); <span 
style="color: #888888;">// repeat check every 250ms 
}; 
</pre> 
There are quite a few things to note in this file: 

First, lines 7 &amp; 8 are pulling out command line args from the Phantom 
process startup, you will see the supplying of those args from C# in the next 
section.  Then take note of the code on line 11 which reads out data blob off 
the stdin pipe (be sure to see the warning in the C# section below). 

The meat of the script is the 
[page.open](http://phantomjs.org/api/webpage/method/open.html) call where 
Phantom will load up our html page.  In this function we will set page 
attributes through the zoom factor and viewport properties.  We then leverage 
the [page.evaluate](http://phantomjs.org/api/webpage/method/evaluate.html) 
function to get our data, height and width values into the hidden inputs in 
our html page.  And finally we find the hidden button and click it which will 
begin the process of drawing our page. 

Since the page drawing (rendering of an SVG image or the map) takes time, we 
must set up a polling routine that will wait until the page has been rendered 
before taking a screenshot.  To set up the loop we are using a very nice 
little example from the Phantom codebase over at GitHub which can be found 
[here](https://github.com/ariya/phantomjs/blob/master/examples/waitfor.js).  
The loop simply waits for a "foo" element to be present on the page then 
continues on to take the screen shot, write the bytes to stdout and then exit. 

<div style="text-align: center;">*** 
The last piece of the puzzle is starting Phantom in a process and getting our 
data across stdin to our JS runner above. 

<div><!-- HTML generated using hilite.me --> 
<div style="background: #ffffff; border-width: .1em .1em .1em .8em; border: 
solid gray; overflow: auto; padding: .2em .6em; width: auto;"><table><td><pre 
style="line-height: 125%; margin: 0;"> 1 
 2 
 3 
 4 
 5 
 6 
 7 
 8 
 9 
10 
11 
12 
13 
14 
15 
16 
17 
18 
19 
20 
21 
22 
23 
24 
25 
26 
27 
28 
29 
30 
31 
32 
33</pre><td><pre style="line-height: 125%; margin: 0;"><span style="color: 
#008800; font-weight: bold;">public <span style="color: #008800; font-weight: 
bold;">static <span style="color: #333399; font-weight: bold;">byte[] <span 
style="color: #0066bb; font-weight: bold;">GetImage( 
                         IEnumerable&lt;Datum&gt; data, 
                         <span style="color: #333399; font-weight: 
bold;">string jsFile 
                     ) 
{ 
<span style="color: #888888;">//Path to PhantomJS install, you can add to 
path, etc. 
<span style="color: #008800; font-weight: bold;">const <span style="color: 
#333399; font-weight: bold;">string path = <span style="background-color: 
#fff0f0;">@"C:\Program Files\phantomjs-1.9.7\phantomjs.exe"; 
<span style="color: #888888;">//build command line args, Phantom Runner and 
height/width args 
<span style="color: #333399; font-weight: bold;">var args = <span 
style="color: #008800; font-weight: bold;">new <span style="color: #333399; 
font-weight: bold;">object[] { jsFile, <span style="color: #6600ee; 
font-weight: bold;">800, <span style="color: #6600ee; font-weight: bold;">650 
}; 
<span style="color: #888888;">//startup environment for Phantom 
<span style="color: #333399; font-weight: bold;">var info = <span 
style="color: #008800; font-weight: bold;">new ProcessStartInfo(path, <span 
style="color: #333399; font-weight: bold;">string.Join(<span 
style="background-color: #fff0f0;">" ", args)) 
{ 
    RedirectStandardInput = <span style="color: #008800; font-weight: 
bold;">true, 
    RedirectStandardOutput = <span style="color: #008800; font-weight: 
bold;">true, 
    RedirectStandardError = <span style="color: #008800; font-weight: 
bold;">true, 
    UseShellExecute = <span style="color: #008800; font-weight: bold;">false, 
    CreateNoWindow = <span style="color: #008800; font-weight: bold;">true 
}; 
<span style="color: #333399; font-weight: bold;">var p = Process.Start(info); 
p.Start(); 

<span style="color: #888888;">//open stream, write serialized data, close 
<span style="color: #333399; font-weight: bold;">var streamwriter = 
p.StandardInput; 
streamwriter.WriteLine(JsonConvert.SerializeObject(data.ToList())); 
streamwriter.Close(); 

<span style="color: #888888;">//listen on standard out and read until process 
exits. 
<span style="color: #333399; font-weight: bold;">var stdout = 
p.StandardOutput.ReadToEnd(); 
p.WaitForExit(); 

<span style="color: #888888;">//return byte[] of image 
<span style="color: #008800; font-weight: bold;">return 
Convert.FromBase64String(stdout); 
} 
</pre> 
We begin our C# method by setting up the path to Phantom (note: you could add 
Phantom to your path, pass it in so there are no magic consts, etc.).  Next we 
need to set up the command line arguments for Phantom: 

1. The relative path to our JavaScript runner file from above. 
1. The page height. 
1. The page width. 

Continue by setting up a process environment for Phantom by redirecting 
Standard In, Out &amp; Error which will enable interaction with Phantom.  The 
final two process settings are to prevent a window at process launch and the 
disabling of Shell Execution (see MSDN docs for details on [Shell 
Execution](http://msdn.microsoft.com/en-us/library/system.diagnostics.processstartinfo.useshellexecute.aspx)) 

With Phantom up and running we can take a reference to the redirected standard 
input stream, serialize our data over to our Phantom process.  Closing of the 
input stream will trigger page evaluation over in Phantom. 

## *WARNING* it should be noted that a read of stdin as of Phantom 1.9.7 is a 
blocking call.  However, there is a feature request for 2.0 that will make 
this async by default.  If you are utilizing this technique you will want to 
defensively block on the stdin read in the event that things change in the 
future. 

The final step is to snag the bytes from stdout making sure to call to 
WaitForExit method of the process happens after you take a reference to the 
stdout.  The ordering will ensure that you read off all the contents of 
stdout.  Lastly, convert the string to a byte array and return. 

<div style="text-align: center;">***<div style="text-align: center;"> 
<div style="text-align: left;">As I noted in the introduction, you could add 
your byte array to a dataset, then map an Image element of an RDLC to the 
dataset, giving you dynamic image content for reports.  You could potentially 
use this technique in integration tests to ensure that the positions of 
elements on the page have not moved.  Or even as a simple archiving technique 
to scrape and save the state of a website.  <div style="text-align: left;"> 
<div style="text-align: left;">Happy Hacking! 