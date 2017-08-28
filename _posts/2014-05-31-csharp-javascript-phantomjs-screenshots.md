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
---

I have a fun little project going on right now that involves taking a portion 
of a web page, loading it into PhantomJS, passing a lump of data to it, taking 
a picture of the page, and displaying that image in a RDLC report.  There are 
like a ba'gillion different ways to accomplish this, so the below is a 
hacker's proof of concept. 

First up, we are going to need is a very simple web page with the 
following elements: 
1. A form element with a hidden input "data" that will be used to move data 
from the primary application to the stub page. 
1. Two more inputs "height" and "width", which are used simply to show command 
line argument passing to Phantom. 
1. A button that can be used to trigger a JavaScript function that will in 
turn draw the page. 

```html
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta charset="utf-8" />
        <title>This is my test page</title>
        <script src="my.js"></script>
    </head>
    <body style="background-color: white; color: black; font-size: 1em;">
        <form>
            <input id="data" type="hidden" name="data" value="">
            <input id="height" type="hidden" name="height" value="">
            <input id="width" type="hidden" name="width" value="">
            <button id="buildFoo" name="buildFoo" 
             type="button" value="Submit" 
             onclick=" init() " style="visibility: hidden;">
      </button>
        </form>
        <div class="container">
        </div>
    </body>
</html>
```

Hopefully it's obvious that our Javascript method init() in my.js, will simply 
plunk everything in the "container" div for display. 

The next element we need, moving up the stack, is our Javascript runner that 
we will pass to Phantom, kicking this whole process off.  Make note of the 
filesystem call for *stumpage.html*; this could be passed in; but, I figured 
showing a filesystem call might be useful to someone. 

```javascript
var system = require('system');
var args = require('system').args;
var fs = require('fs');
var page = require('webpage').create();

//args[0] is this javascript file.
var height = args[1];
var width = args[2];

var address = "file:///" + fs.workingDirectory + "/stubpage.html";
var data = system.stdin.readLine();

page.open(address, function() {

 page.zoomFactor = 1;
 page.viewportSize = {
  width: width,
  height: height
 };
 page.evaluate(function(data, height, width) {
  //add the "data" to our page
  var d = document.getElementById('data');
  d.value = data;
  //set the height input
  var h = document.getElementById('height');
  h.value = height;
  //set the width input
  var w = document.getElementById('width');
  w.value = width;
  //click the button to fire the page's JS
  var b = document.getElementById("buildFoo");
  b.click();
 }, data, height, width);

 waitFor(function() {
  //something to wait on ...
  return page.evaluate(function() {
   //do we ahve a foo element on the page yet?
   if (document.getElementById('foo')) {
    return true;
   } else {
    return false;
   }
  });
 }, function() {
  //take a picture, it lasts longer
  var base64Image = page.renderBase64('PNG');
  //write the image to stdout
  system.stdout.write(base64Image);
  window.phantom.exit();
 });
});

function waitFor(testFx, onReady, timeOutMillis) {
 // timeout after 10 sec.
 var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 10000,
  start = new Date().getTime(),
  condition = false,
  interval = setInterval(function() {
   if ((new Date().getTime() - start < maxtimeOutMillis) 
    && !condition) {
    // If not time-out yet
    // and condition not yet fulfilled
    condition = (typeof(testFx) === "string" 
     ? eval(testFx) 
     : testFx());
   } else {
    if (!condition) {
     // If condition still not fulfilled 
     //(timeout but condition is 'false')
     phantom.exit(1);
    } else {
     // Condition fulfilled 
     //(timeout and/or condition is 'true')
     typeof(onReady) === "string" 
     ? eval(onReady) 
     : onReady();
     //< Stop this interval
     clearInterval(interval); 
    }
   }
  }, 250); // repeat check every 250ms
};
```
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


The last piece of the puzzle is starting Phantom in a process and getting our 
data across stdin to our JS runner above. 
```csharp
public static byte[] GetImage(
                         IEnumerable<Datum> data,
                         string jsFile
                     )
{
//Path to PhantomJS install, you can add to path, etc.
const string path = @"C:\Program Files\phantomjs-1.9.7\phantomjs.exe";
//build command line args, Phantom Runner and height/width args
var args = new object[] { jsFile, 800, 650 };
//startup environment for Phantom
var info = new ProcessStartInfo(path, string.Join(" ", args))
{
    RedirectStandardInput = true,
    RedirectStandardOutput = true,
    RedirectStandardError = true,
    UseShellExecute = false,
    CreateNoWindow = true
};
var p = Process.Start(info);
p.Start();

//open stream, write serialized data, close
var streamwriter = p.StandardInput;
streamwriter.WriteLine(JsonConvert.SerializeObject(data.ToList()));
streamwriter.Close();

//listen on standard out and read until process exits.
var stdout = p.StandardOutput.ReadToEnd();
p.WaitForExit();

//return byte[] of image
return Convert.FromBase64String(stdout);
} 
```

We begin our C# method by setting up the path to Phantom (note: you could add 
Phantom to your path, pass it in so there are no magic consts, etc.).  Next we 
need to set up the command line arguments for Phantom: 

1. The relative path to our JavaScript runner file from above. 
1. The page height. 
1. The page width. 

Continue by setting up a process environment for Phantom by redirecting 
Standard In, Out &amp; Error which will enable interaction with Phantom.  The 
final two process settings are to prevent a window at process launch and the 
disabling of Shell Execution (see MSDN docs for details on [Shell Execution](http://msdn.microsoft.com/en-us/library/system.diagnostics.processstartinfo.useshellexecute.aspx)) 

With Phantom up and running we can take a reference to the redirected standard 
input stream, serialize our data over to our Phantom process.  Closing of the 
input stream will trigger page evaluation over in Phantom. 

## *WARNING* 
It should be noted that a read of stdin as of Phantom 1.9.7 is a 
blocking call.  However, there is a feature request for 2.0 that will make 
this async by default.  If you are utilizing this technique you will want to 
defensively block on the stdin read in the event that things change in the 
future. 

The final step is to snag the bytes from stdout making sure to call to 
WaitForExit method of the process happens after you take a reference to the 
stdout.  The ordering will ensure that you read off all the contents of 
stdout.  Lastly, convert the string to a byte array and return. 

As I noted in the introduction, you could add 
your byte array to a dataset, then map an Image element of an RDLC to the 
dataset, giving you dynamic image content for reports.  You could potentially 
use this technique in integration tests to ensure that the positions of 
elements on the page have not moved.  Or even as a simple archiving technique 
to scrape and save the state of a website.  

Happy Hacking! 