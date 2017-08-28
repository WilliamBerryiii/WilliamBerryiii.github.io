---
layout: post
title: Using Azure IoT Hub and PowerBI to Visualize Plant Floor Data
date: '2017-01-04T15:25:00.001-08:00'
author: William Berry
tags:
- Azure
- IoT
- PowerBI
- Azure IoT Gateway SDK
modified_time: '2017-01-04T15:51:18.565-08:00'
thumbnail: https://1.bp.blogspot.com/-WahEkTixUxc/WG1NMXDmH-I/AAAAAAAAAi8/vBVdGDWO6tYv6pAygS0urddKD9Njww3PQCLcB/s72-c/iot_hub_create.PNG

---

[<img border="0" height="105" src="https://azure.microsoft.com/svghandler/iot-hub/?width=600&amp;height=315" width="200" />](https://azure.microsoft.com/svghandler/iot-hub/?width=600&amp;height=315)
In my [previous post on the Azure IoT Gateway SDK](http://www.lucidmotions.net/2016/12/fast-track-azure-gateway-sdk-w-powershell.html), 
we put together a Powershell quick start script for Modbus Gateway projects.  
In this post we'll continue the exploration by connecting a Modbus compatible 
Beckhoff BK9100 to Azure IoT Hub, shape our data with Azure Stream Analytics 
and then visualizing the current position of a Dynapar optical encoder with 
Power Bi. 

We'll begin by opening up the Azure Portal, click on the plus icon in the 
upper right corner and search for `IoT Hub`.  Once the resource is located, 
select `Create` in the lower left corner. 

[<img border="0" height="400" src="https://1.bp.blogspot.com/-WahEkTixUxc/WG1NMXDmH-I/AAAAAAAAAi8/vBVdGDWO6tYv6pAygS0urddKD9Njww3PQCLcB/s400/iot_hub_create.PNG" width="306" />](https://1.bp.blogspot.com/-WahEkTixUxc/WG1NMXDmH-I/AAAAAAAAAi8/vBVdGDWO6tYv6pAygS0urddKD9Njww3PQCLcB/s1600/iot_hub_create.PNG) 

Configure your IoT Hub with a unique name, select an appropriate scale tier, 
and make sure to put the hub into it's own resource group for easy clean-up 
later. 

[<img border="0" height="342" src="https://4.bp.blogspot.com/-PQHGyXoIgcg/WG1OI9u4UlI/AAAAAAAAAjA/LIWikFNbWzcVS-GkUHzJ26-BTohAB76nQCLcB/s400/iot_hub_create_2.PNG" width="400" />](https://4.bp.blogspot.com/-PQHGyXoIgcg/WG1OI9u4UlI/AAAAAAAAAjA/LIWikFNbWzcVS-GkUHzJ26-BTohAB76nQCLcB/s1600/iot_hub_create_2.PNG) 

Navigate to the `Shared access policies` tab of the IoT Hub and paste the 
`Primary key` of the `service` policy into a text file. 

[<img border="0" height="332" src="https://1.bp.blogspot.com/-B3996Waiht0/WG1aZW59GGI/AAAAAAAAAjc/6QblxSwZyJANgTfgAvvJoGGhnm27NcrcwCLcB/s400/service-policy.PNG" width="400" />](https://1.bp.blogspot.com/-B3996Waiht0/WG1aZW59GGI/AAAAAAAAAjc/6QblxSwZyJANgTfgAvvJoGGhnm27NcrcwCLcB/s1600/service-policy.PNG) 

Back in the Hub's primary blade, select the `Endpoints` tab under messaging. 
In the new blade select the `Events` entry under `Built-in endpoints`.  Once 
the new blade opens, copy the `Event Hub-compatible name` value and the first 
segment of the `Event Hub-compatible endpoint` value (e.g. 
`ihsuprodbyres043dednamespace`) into your text file.  We'll use these values 
in a moment to hook up our Azure Stream Analytics Job. 


[<img border="0" height="272" src="https://4.bp.blogspot.com/-2ERdeJpdEkQ/WG1b0aByl_I/AAAAAAAAAjk/pNOfZDrlzBYukcyrjMREQ1oiPjnYt2N1QCLcB/s400/endpoints.PNG" width="400" />](https://4.bp.blogspot.com/-2ERdeJpdEkQ/WG1b0aByl_I/AAAAAAAAAjk/pNOfZDrlzBYukcyrjMREQ1oiPjnYt2N1QCLcB/s1600/endpoints.PNG)<div> 

Next, we'll need an Azure Stream Analytics(ASA) Job to perform some data 
scaling on the path toward PowerBI.  While this operation could be performed 
in the gateway, ASA provides us an opportunity to sniff/validate our data and 
opens the door to easy persistence, should we so choose.  Again click the plus 
(+) icon in the upper left corner and search for `Stream Analytics`. Once the 
resource is located, select `Create` in the blade's lower left corner. 

[<img border="0" height="400" src="https://4.bp.blogspot.com/-_E_3DZpsXo4/WG1XrR_SmjI/AAAAAAAAAjQ/licXsye8pVkXmGXzgf6xIvHe9wlVLCNIwCEw/s400/asa.PNG" width="310" />](https://4.bp.blogspot.com/-_E_3DZpsXo4/WG1XrR_SmjI/AAAAAAAAAjQ/licXsye8pVkXmGXzgf6xIvHe9wlVLCNIwCEw/s1600/asa.PNG) 
 Configure the 
ASA job with a unique name and place it in the same resource group as the IoT 
Hub. 

[<img border="0" height="400" src="https://1.bp.blogspot.com/-OoVRsb93GAY/WG1XrU7bH3I/AAAAAAAAAjU/rveyKrhzkiIAyuGVtypmzWqY10RI0u2ygCEw/s400/asa-create.PNG" width="180" />](https://1.bp.blogspot.com/-OoVRsb93GAY/WG1XrU7bH3I/AAAAAAAAAjU/rveyKrhzkiIAyuGVtypmzWqY10RI0u2ygCEw/s1600/asa-create.PNG) 

We now need to patch the IoT Hub as the input for the ASA Job. In the overview 
pane, select the input section under `Job Topology`, and press add at the top 
of the new blade.  Enter an alias that will be used to reference the input in 
the ASA query.  Make sure that the `Source Type` is set to `Data Stream` and 
the `Source` is marked as `Event hub`.  Unfortunately, the Event Hub input 
blade will not automatically recognize the IoT Hub's Event Hub endpoints, so 
we'll need to set the `Subscription` field to `Provide event hub settings 
manually`.  Paste in the `Service bus namespace`, the 'Event hub name' and the 
`Event hub policy key` from your text file. Finish up by setting the `Event up 
policy name` to `service` and press `Create`.  There is no need to define a 
non-default consumer group and the data will be JSON formatted, encoded as 
UTF-8 

[<img border="0" height="400" src="https://3.bp.blogspot.com/-qumzzhxT-s8/WG1fmndoivI/AAAAAAAAAjw/h4JBw2VCcfk-k8vH-S-hOjnncFVXMDtEwCLcB/s400/asa-input2.PNG" width="376" />](https://3.bp.blogspot.com/-qumzzhxT-s8/WG1fmndoivI/AAAAAAAAAjw/h4JBw2VCcfk-k8vH-S-hOjnncFVXMDtEwCLcB/s1600/asa-input2.PNG) 

Before we define our ASA query we should set up the output hook to PowerBI.  
Back under the ASA Job's overview tab on the main blade, Select the `Output` 
section under `Job Topology` and press `Add` at the top.  Enter `power-bi` as 
your `Output alias`, set the `Sink` to `Power BI` and press authorize.  You'll 
be asked to enter your Power BI credentials at the login.  If you don't 
already have a Power BI account, you can sign up for one 
[here](https://powerbi.microsoft.com/en-us/get-started/).  Once the prompt 
completes login, enter in a `Dataset Name` and target `Table Name`. 

[<img border="0" height="268" src="https://2.bp.blogspot.com/-ZYGvf3-UZcQ/WG1j0yoIwFI/AAAAAAAAAj8/MQKmZn5azzADf43KApZINkfBWorFLSgmACLcB/s400/asa-powerbi-auth.PNG" width="400" />](https://2.bp.blogspot.com/-ZYGvf3-UZcQ/WG1j0yoIwFI/AAAAAAAAAj8/MQKmZn5azzADf43KApZINkfBWorFLSgmACLcB/s1600/asa-powerbi-auth.PNG) 

The last bit of ASA configuration we need to handle is setting up the query.  
For now, we'll build the query based on values that might end up being 
slightly different when you wire up your device. 

Navigate the the `Query` section under `Job Topology` and select it.  A new 
blade will open up that will list the Input and Output alias previously 
defined and a code editor to enter the ASA query.  We'll start by selecting 
the observation time stamp and the device type value.  As I noted earlier, we 
need to do some maths to range our encoder value to get the data in shape for 
PowerBI visualization.  To range the encoder value, cast the string to a 
float, devide by the ranges max count (in this case 65535) and multiply by 100 
to push to percentage. 


<script src="https://gist.github.com/WilliamBerryiii/c3d6e4e87d4507ffe02cb6327eb31ab3.js?file=query.sql"></script> 

Once the query is entered, select `Save` at the top and back on the ASA home 
blade, press `Start` to kick off the job. 

We can now turn our attention back to our Modbus device and complete the 
wiring of it to the gateway.  As I noted earlier, I'm using a Beckhoff BK9100, 
Modbus capable, bus coupler along with a pretty standard Dynapar 2 channel 
optical incremental encoder (no Z full rev. channel).  The Process Image for 
the coupler includes 8 channels of DIO in front of the mapping space for the 
encoder module, leaving our counter value located at the second word of the 
process image.  For the astute, the coupler is also confiugred for IPAddres 
assignment using BootP via Beckhoff's TCBootP application. 

[<img border="0" height="300" src="https://4.bp.blogspot.com/-S5T_SM_f_bo/WG1utD2Fw-I/AAAAAAAAAkQ/zPDZjSXhwTAxQzK3YQUMbd5oqRft8TFIwCLcB/s400/IMG_3692.JPG" width="400" />](https://4.bp.blogspot.com/-S5T_SM_f_bo/WG1utD2Fw-I/AAAAAAAAAkQ/zPDZjSXhwTAxQzK3YQUMbd5oqRft8TFIwCLcB/s1600/IMG_3692.JPG) 

The next step in the process is to register our device with the IoT Hub. While 
there are a number of ways to accomplish this, I suggest you check out our 
`iot-samples` repository on GitHub.  Begin by either cloning the repo, or just 
download the code directly.  Navigate to Device Management -&gt; csharp and 
open the solution file in Visual Studio (Note, you might also want to checkout 
my [Introduction to Azure IoT with Fsharp](http://www.lucidmotions.net/2016/11/introduction-to-azure-iot-with-fsharp.html) 
post too!).  With the solution open, set the `Create Device Identity` project 
as the startup project.  In the config folder, copy the `config.default.yaml` 
file to `config.yaml`.  Enter the Host Name for your IoT Hub, and the 
`iothubowner`'s primary key connection string, which can be found under the 
IoT Hub's `Shared Access policies` tab.   Finish up by modifying the 
`Nickname` and `DeviceId` values in the config file, they can be any value you 
want.  After you run the project, your device will be registered and a device 
key will be populated in the config file, we'll need that value shortly. 

Open the script from my [previous blog post](http://www.lucidmotions.net/2016/12/fast-track-azure-gateway-sdk-w-powershell.html) 
in an Administrative PowerShell ISE session.  You'll need to set at least the 
following values: 

1. rootProjectPath 
1. iotHubName 
1. deviceName - same as the "deviceId" you registered earlier 
1. deviceKey - the value from the config file in the Device Management Project 
1. deviceMac - the mac address of your modbus device 
1. modbusServerIp - the IP Address of your bus coupler/plc/IO device 
1. modbusPollingInterval - the number of milliseconds between device polls 
1. modbusDeviceType - this is the value that is plumbed to ASA 
1. modbus * - note in the sample script, I'm reading unit 0, with function 
code 4 (read input registers), reading starting at register 2 (1 based), and 
only reading 1 word of data ... you can see more about Modbus function codes 
on page 22 of [the protocol spec](http://modbus.org/docs/PI_MBUS_300.pdf). 

Once you fill out your data and run the script, navigate to {projectRootPath} 
-> azure-iot-gateway-sdk -> build -> samples -> modbus -> 
Debug.  Open the `modbus_win.json` file in a text editor and double check that 
the document looks well formed. 

You can now open a PowerShell command prompt in the same folder and issue the 
following command to begin reading from the device and sending data to Azure 
&gt; .\ modbus_sample.exe .\modbus_win.json 
You should see output similar to the following: 

[<img border="0" height="172" src="https://1.bp.blogspot.com/-v7lowFrKa0M/WG134K5Se-I/AAAAAAAAAkg/yZpAV1ltTkUNjBnG-_3nwp611K8up4uGACLcB/s640/gateway-run.PNG" width="640" />](https://1.bp.blogspot.com/-v7lowFrKa0M/WG134K5Se-I/AAAAAAAAAkg/yZpAV1ltTkUNjBnG-_3nwp611K8up4uGACLcB/s1600/gateway-run.PNG) 
Assuming you've set your polling to something reasonable, like 2000 (2 
seconds), you should be able to run the application for a few hours on a day's 
allowance for the IoT Hub free scaling tier. 

With data flowing to the IoT Hub and onto ASA, log in to Power BI.  Though it 
can take some time to finally show up, the ASA dataset should be visible in 
`Datasets` group. 

[<img border="0" height="320" src="https://4.bp.blogspot.com/-MpL0rG_D450/WG15EUj1DfI/AAAAAAAAAks/QtPMiV8rRNssETOzZGm8X1W9Efl_KI0EACLcB/s320/pbi-dataset.PNG" width="139" />](https://4.bp.blogspot.com/-MpL0rG_D450/WG15EUj1DfI/AAAAAAAAAks/QtPMiV8rRNssETOzZGm8X1W9Efl_KI0EACLcB/s1600/pbi-dataset.PNG) 

Select the Modbus dataset, and expand Visualization and Fields from the 
toggles on the right of the display. 

[<img border="0" height="288" src="https://4.bp.blogspot.com/-xo78fHYf-vA/WG15ueB7TzI/AAAAAAAAAkw/vBe0H3wRPaomO7hMZI6QMiaEeb6tzfoFACLcB/s640/pbi-dataset-start.PNG" width="640" />](https://4.bp.blogspot.com/-xo78fHYf-vA/WG15ueB7TzI/AAAAAAAAAkw/vBe0H3wRPaomO7hMZI6QMiaEeb6tzfoFACLcB/s1600/pbi-dataset-start.PNG) 
Add a `Line Chart` to the page and set the following values: 

1. Axis - datetimestamp 
1. Legend - device-type 
1. Values - cnt 

[<img border="0" height="400" src="https://3.bp.blogspot.com/-VFbsTrm9TeU/WG16gfYz12I/AAAAAAAAAk4/CmXHfQBuPKkIr40eJ2w7sj97FWIM8m6ZgCLcB/s400/graph-settings.PNG" width="185" />](https://3.bp.blogspot.com/-VFbsTrm9TeU/WG16gfYz12I/AAAAAAAAAk4/CmXHfQBuPKkIr40eJ2w7sj97FWIM8m6ZgCLcB/s1600/graph-settings.PNG

In the Filters menu for the chart, select the datetimestamp field and set 
the filter type to `Top N` and show the last 20 items.  This will produce a 
realtime graph of data streaming from the device.  The default polling 
interval should be around 3-4 seconds.  The resulting data will look like 
this!

[<img border="0" height="211" src="https://4.bp.blogspot.com/-C2MBM0RpndE/WG2ECXVDFYI/AAAAAAAAAlE/wHAIE-mB4YoKae1V7EoNGKs0oQe-eC9gwCLcB/s320/report.PNG" width="320" />](https://4.bp.blogspot.com/-C2MBM0RpndE/WG2ECXVDFYI/AAAAAAAAAlE/wHAIE-mB4YoKae1V7EoNGKs0oQe-eC9gwCLcB/s1600/report.PNG)<div> 

Happy Coding! 