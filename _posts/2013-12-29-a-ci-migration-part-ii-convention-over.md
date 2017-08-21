---
layout: post
title: A CI Migration Part II - Convention Over Configuration
date: '2013-12-29T00:26:00.000-08:00'
author: William Berry
tags:
- Automation
- Kiln
- Build Pipeline
- Continuous Integration
- Jenkins
- DevOps
modified_time: '2013-12-30T00:11:55.114-08:00'
blogger_id: tag:blogger.com,1999:blog-4707687462195457004.post-6813295856311367397
blogger_orig_url: http://www.lucidmotions.net/2013/12/a-ci-migration-part-ii-convention-over.html
---

In this post I want to talk about template builds, stable builds and 
branch/feature builds for Jenkins. 

One of the first things I figured out with Jenkins is that configuration can 
be overwhelming.  Jenkins does a fabulous job of letting you tweak all the 
nobs throughout its infrastructure.  What that translates to however is the 
need to establish conventions early on in the set up process - if for no other 
reason than your sanity. 

The build and package process I am currently working in is probably similar to 
some .NET shops that are still working towards full Continuous Integration.  
The developer starts with a remote clone of stable in a Kiln repository group 
and then brings that clone locally (think long running single developer 
feature branch). The developer does their work to a satisfactory point and 
pushes changes to the remote repository. 

Once code is pushed to the remote repo, a code review request is made.  While 
the code review is underway, a build package is assembled and run, which will 
produce the final deployment artifacts.  With a combination of NAnt scripts 
and MSBuild, software is built and later packaged for deployment - where 
packaging forces a rebuild of the software regardless of the need to actually 
do so.  Once review is complete the deployed artifacts move along to QA for 
testing. 

Considering that this is not even the full picture - the million dollar 
question is where and how do you begin to insert Continuous Integration? 

Initial Goals: 
1. Dev should push and the push should automagically build and test the 
software. 
1. When packaging, software should not be rebuilt. 
1. Packaging should always refer to the latest built artifacts. 
1. The dev's effort in the build process should be limited to writing unit 
tests and pushing. 
<div>There are plenty of ways to approach this.  Given the above requirements, 
a Kiln SCM and Jenkins for CI tooling, I designed the following approach: 
1. Dev pushes to remote repository. 
1. Remote repository fires web hook to waiting Jenkins Management Service. 
1. Jenkins Management Service connects to Jenkins and configures a job for our 
build. 
1. Jenkins Management Service kicks off the build for our newly configured 
job, runs unit tests, etc. 
1. User receives notification via Chrome plugin as to the success or failure 
of the build job. 
1. Dev. prepares deployment package using latest compiled artifacts and sends 
to QA. 
1. Feature is released to Production after QA. 
1. Deployed code is merged to stable repository, rebuilt and unit tests 
re-run. 
<div>In order to achieve this workflow we need a chunk of middleware, the 
"Jenkins Management Service."  Though Kiln can fire a web hook directly at 
Jenkins to force a job build, we trade off the ability to make the build job 
creation automagical for the developer.  Depending on your set up, this direct 
coupling could be an option, assuming you do not need to have a new job for 
each feature branch.<div> 

To achieve our goal we will create two different Jenkins jobs per repository 
group.  The first, larger and more complex will be the build for stable. If 
your organization deploys stable, then you can lash this build job to extra 
processes such as performance tests, remote deploy to QA, remote deploy to 
integration test env, doc building, etc.  This build will be specific to the 
stable repository and should include all developers in the email notification 
chain so that everyone on the team can monitor what's going on. 

The second build will be a template build.  This job will be a lightweight 
build performing compilation, running just the most basic of unit tests and 
should run to completion in 1-2 minutes from the remote push. While we want 
the developer to take a break at this point, we also want to give them feed 
back as soon as possible. 

For our system I chose some common name formatting to keep everything in the 
Jenkins Management Service(JMS) scriptable an easy.  Repository Groups in Kiln 
are consistent with the product name; therefore in Jenkins, the stable build 
job is *RepositoryGroup_stable* and the template job is 
*RepositoryGroup_template*. 

The Jenkins Management Service, which is a simple python bottle cgi 
application running in IIS, receives a web hook from Kiln on its main route 
and plucks out the repository, repository group, pusher email, and kiln 
repository url from the payload.  It then turns to Jenkins and sucks down the 
list of all the available jobs and checks to see if a job with the name 
*RepositoryGroup_repository* exists.  If the job does not exist then the JMS 
retrieves the *RepositoryGroup_template* job, remaps various fields and 
submits the job to Jenkins.  If the job had existed, the JMS makes sure that 
all updated plugin sections are properly configured accruing to the template 
(you need to have your Chuck Norris plugin enabled after all) and if the 
pusher's email is not in the notification list, it is added. 

Once the job in Jenkins has been created/updated, the JMS then kicks off the 
build - this whole process is nearly instant.  Through this process we have 
confined the configurability to the stable and template build jobs and made 
the process nearly invisible to the developer.  If it fits your process, 
successful builds can fire off an email to the pushers with a link to the most 
recent archived artifacts, so they can deploy to their test servers. 

One last note about this process.  You will need to eventually remove the 
feature branch jobs; this can be done in a few ways.  Currently our process 
merges feature branches to stable after deployment.  This   requires 
developers to run a custom delete script that does some final 
checking/testing, removes the clone from Kiln and deletes the job.  This could 
in theory be completely automated by running a script that did the merge to 
stable, ran the stable build job and if all went well, cleaned up the Kiln 
repository and the Jenkins build job for that feature.  I am looking to 
experiment with this idea in January. 

Happy Automating in the New Year! 