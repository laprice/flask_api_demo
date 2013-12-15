This repository is a cleaned up and sanitized version of a client
project from a 2012. It is made public only for purposes of evaluation
and education; you may not use it without permission. 

Copyright 2012-2013 Industrial Intellect LLC

It contains three separate components.

1. scrapy spiders and item definitions.
   
   We are currently using the latest version of Scrapy
   http://scrapy.readthedocs.org/en/0.15/index.html

   The spiders are not very sophisticated they all follow the strategy
   of trying to scrape as much as possible from multi page listings, it
   should in theory be easy to get the information, it's highly
   structured and regular data. But sometimes the HTML is poorly written.

2. adb/webd is the web interface api_server.py is the flask app see
   http://flask.pocoo.org/ for information about flask. We are using
   version 0.9 here. The current version of the app is only a step or
   two removed from hello world, it should be easy to extend. 
   db.py is the database interface library. It has a small library of
   useful queries. If you begin extending the data model in any
   significant way you'll probably want to step up to something like
   sqlalchemy or peewee orm to manage the SQL for you.

3. There are some lightweight management scripts for creating and destroying
   servers, starting crawls, backups, etc.  
   nightcrawler.sh is run from cron every night at midnight, it starts
   the crawl for each of the spiders.
   adb/webd/data_loader.py is the data management script, it has
   options for loading a given dataset, reloading a dataset per day
   etc. if run without arguments it will blindly load all data for all
   the spiders it knows about for the current day. This is executed
   from cron 6 hours after the crawls are started. This is not
   idempotent, running it more than once will result in multiple
   entries in the database.



