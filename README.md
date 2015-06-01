CFX Job Scheduler
============

* Python based portable, scalable job scheduler with multiple priorities - for ANSYS CFX.
* Written with Python 2.7, using portable python, spyder, Notepad ++ and Sublime Text 3.
* This is a project in progress, with the goal of becoming a multi-platform job scheduler for ANSYS CFX that has a balance between sophistication and ease of deployment. Current job schedulers are relatively very sophisticated and complex to setup with several pre-requisites. As of now, this program is ideally suited for individuals and small teams, with 1-3 computing clusters working in tandem.

* See the [Wiki](https://github.com/shrysr/jobscheduler/wiki/) for the project goals, algorithm and other details.

* Issues and desired enhancements are listed


Setting up
=====================
* The program doesn't just work out of the box (for now). It needs some manual setting up. However, once setup - it should keep running without any problems.

* A zip file of the folder structure as it is, is provided. It should be downloaded and unzipped to the desired location where the simulations will run and be stored.

* System scheduler install is required, which will launch the python program every minute. This needs to be installed only on the master nodes.
