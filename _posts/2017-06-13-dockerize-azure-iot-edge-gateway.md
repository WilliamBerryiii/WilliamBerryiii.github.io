---
layout: post
title: Dockerize the Azure IoT-Edge Gateway
date: '2017-06-13T16:59:00.002-07:00'
author: William Berry
tags:
- Azure Iot Hub
- Containers
- Docker
- IoT-Edge
- Azure IoT Gateway SDK
modified_time: '2017-06-13T16:59:26.953-07:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-6933621790343635894
blogger_orig_url: http://www.lucidmotions.net/2017/06/dockerize-azure-iot-edge-gateway.html
---

Like most developers in the IoT space, I write code that is typically destined 
for Linux run-times; but I spend my days typing away on a Surface Book running 
Windows.  In days past, when I needed to do some hacking, I'd fire up a 
Raspberry PI or jump over onto one of a few Ubuntu VMs running HyperV sucking 
up disk space, processor time and RAM.  Thankfully, technology has progressed 
and these days, with Docker being all the rage, I just spin up a container and 
get to work. 

One of my common tasks has been developing workflow modules for Azure 
IoT-Edge, our open source IoT gateway.  These modules provide functionality 
like data compression, aggregation, protocol translation, etc.  Easily 
spinning up a consistent development environment has been critical to 
accelerating this work, so I figured I'd share the love and show you how to 
get the gateway up and running in a Linux container on your Windows box using 
Docker. 

Step one is installing Docker on your Windows 10 (Anniversary edition or 
higher).  Docker provides great [setup 
instructions](https://docs.docker.com/docker-for-windows/install/) that will 
walk you through that whole process.  Though you can switch to using "Windows 
Containers" in the Docker settings, let's leave it with the default "Linux 
Container" setting.  With Docker installed, check and make sure everything is 
working properly by issuing: 

`docker version` 

in an elevated Powershell prompt.  This command should return data for both 
the client and server.  If it doesn't ... there are a copious number of fixes 
blogged about across the web.  I've also found that just selecting "Restore 
Docker" from the Docker Settings pane to be a useful nuke option. 

Head over to the Azure Portal and set up a "Free" tier IoT Hub.  Use the 
integrated device manager to add two test devices, select 'Symetric Keys' and 
have them auto-generated.  Record the device names and primary keys for use in 
our dockerfile. 

Now create a folder that we can put a dockerfile into:  
```powershell
mkdir iot-edge-container
``` 

`cd` into the directory and create a text file called `dockerfile.txt`. 

The first step with our dockerfile will be to declare the base OS we want to 
use for the image.  In this case we'll do Ubuntu: 

```dockerfile
FROM ubuntu
``` 

Boy that was super hard; glad we got it out of the way. 

Next we'll need to add some environment variables to the image.  There are a 
thousand secure ways to do this other than putting our secretes into our 
dockerfile; but time is of the essence, and that was a disclaimer to encourage 
you to do the right thing.  Please [see here 
](https://blog.docker.com/2017/02/docker-secrets-management/)for detailed 
options from Docker.  So onto those env vars: 

```Dockerfile
# ENV vars for setup 
ENV IoTHubName {iot_hub_name} 
ENV IoTHubSuffix azure-devices.net 
ENV device1 {device1_name} 
ENV device1key {device1_key} 
ENV device2 {device2_name} 
ENV device2key {device2_key} 
``` 

With the environment variables set up, we need to now make sure that the base 
image is up-to-date and all the IoT-Edge project dependencies are installed.  
Apt-Get will be our friend ... 

```Dockerfile
# Update image 
RUN apt-get update 
RUN apt-get --assume-yes install curl build-essential libcurl4-openssl-dev git cmake pkg-config libssl-dev uuid-dev valgrind jq libglib2.0-dev libtool autoconf autogen vim 
``` 

Please take note that I've intentionally started a flame war by installing vim 
... I have a hard enough time exiting vim, so emacs is off the table 
completely.  Also note that we are installing `jq` - this will be used to 
dynamically populate the Gateway's simulator JSON config file. 

With the image all updated, we can turn our attention to cloning the IoT-Edge 
repository and kicking off the build: 

```Dockerfile
# Checkout code 
WORKDIR /usr/src/app 
RUN git clone https://github.com/Azure/iot-edge.git 

# Build 
WORKDIR /usr/src/app/iot-edge/tools 
RUN ./build.sh --disable-native-remote-modules 
``` 

Take note of the flag on the build script, this may or may not be necessary 
depending on the base OS you are using.  Since we are running on Ubuntu, this 
flag will keep libuv from blowing up during the build. 

Finally, we can turn our attention to getting the container run-time commands 
all ready.  The following big block of code will get us into the right 
directory to modify the json config file, echo the config to the console to 
make sure it's all correct and then kick off the Gateway.  The `ENTRYPOINT` 
command will ensure that the container does not exit immediately after 
starting.  Also note the last two `jq` commands which will set the loop time 
for the simulated devices ... 2 second intervals will chew through your 8K 
free messages quickly when you can't figure out how to kill your container 
:-). 

```Dockerfile
# RUN 
WORKDIR /usr/src/app/iot-edge/build 

## cat config file into env var 
ENTRYPOINT J_FILE=$(cat 
/usr/src/app/iot-edge/samples/simulated_device_cloud_upload/src/simulated_device_cloud_upload_lin.json) 
\ 

    # cd into sample dir 
    &amp;&amp; cd 
/usr/src/app/iot-edge/samples/simulated_device_cloud_upload/src/ \ 

    # update settings based on env vars 
    &amp;&amp; echo "$J_FILE" \ 
    #configure iot hub 
    | jq '.modules[0].args.IoTHubName="'$IoTHubName'"' \ 
    | jq '.modules[0].args.IoTHubSuffix="'$IoTHubSuffix'"' \ 
    | jq '.modules[0].args.Transport="AMQP"' \ 
    # configure device 1 
    | jq '.modules[1].args[0].deviceId="'$device1'"' \ 
    | jq '.modules[1].args[0].deviceKey="'$device1key'"' \ 
    # configure device 2 
    | jq '.modules[1].args[1].deviceId="'$device2'"' \ 
    | jq '.modules[1].args[1].deviceKey="'$device2key'"' \ 
    # set device 1 message period 
    | jq '.modules[2].args.messagePeriod=10000' \ 
    # set device 2 message period 
    | jq '.modules[3].args.messagePeriod=10000' \ 
    &gt; replaced.json \ 

    # print updates 
    &amp;&amp; cat replaced.json \ 

    # cd back up to build dir 
    &amp;&amp; cd /usr/src/app/iot-edge/build/ \ 

    # run gateway 
    &amp;&amp; 
./samples/simulated_device_cloud_upload/simulated_device_cloud_upload_sample 
../samples/simulated_device_cloud_upload/src/replaced.json 
<div> 
``` 

With the dockerfile scripted out, we can now create our complete image.  From 
the previously opened elevated Powershell prompt issue the following command: 

```powershell
Get-Content .\Dockerfile.txt | docker build -t iot-edge -
``` 

This will read the dockerfile in and pass it to the Docker build command.  
Also not that the image will be tagged with 'iot-edge' for easy 
identification.  This command will take about 10-15 to run initially, but 
subsequent runs should leveraging caching and be much faster. 

Now for the pièces de résistance! 

```powershell
docker run -ti iot-edge
``` 

The container will fire up, print out the json config file and begin sending 
telemetry data to Azure!  Wait a few min and refresh the portal to see your 
simulated data arriving in IoT Hub from your fancy containerized IoT-Edge 
Gateway! 

The complete docker file can be found at [this 
gist](https://gist.github.com/WilliamBerryiii/ee31a154d99130f9bbe472a320d49655). 

Happy Coding! 