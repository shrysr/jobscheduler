jobscheduler
============

Python scripts for portable, scalable job scheduler with multiple priorities - for ANSYS CFX.

This code was originally developed for my R&D Center  @ *Wilo SE*. A modified (and more generic) version of the same is available here. It is simply meant to fire away simulations, triggered by a scheduler software. (Tested with the free version of *System Scheduler*).

The program basically loops through pre designated folders and lists .def files based on the *last modified* date available in Windows. The system interaction is via BASH scripts created via the Python code.

This is a project in progress, with the goal of becoming a multi-platform job scheduler for ANSYS CFX that has a balance between sophistication and ease of deployment. Current job schedulers are relatively very sophisticated and complex to setup with several pre-requisites. As of now, this program is ideally suited for individuals and small teams, with 1-3 computing clusters working in tandem.

See the Wiki for the project goals, algorithm and other details.