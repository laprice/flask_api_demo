#!/bin/bash

#cron job to load data
#this could be done more cleanly and quickly in nightcrawler by spawing 
#a waitpid thread for each spider and loading it as it was done.
#or by having the spiders update the database directly.
#but like the man said; Done is better than perfect.


cd /home/adb/webd/
/usr/bin/python data_loader.py

