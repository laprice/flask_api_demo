#!/usr/bin/env python
import os
import sys
sys.path.append('/home/adb/adb/webd')
import db
import json
import datetime
import logging
import argparse
from pprint import pprint

DATA_DIR='/home/adb/data'

spiders = [
    "examplespider"
]

logging.basicConfig(filename='/home/adb/logs/db.log', filemode='a',level=logging.DEBUG)
logger = logging
logging.info('starting data loader')

def load_today(spider):
    day=datetime.date.today().isoformat()
    load_retailer(spider, day)

def load_retailer(spider, day):
    logger.debug('load_retailer: %s for day %s' % (spider, day))
    filename = "/".join([DATA_DIR,
                         spider,
                         day +'.json'])
    logger.debug(filename)
    content = open(filename,'r').readlines()
    for entry in content:
        d = json.loads(entry)
        d["acquired"] = day
        db.store_item(d ,logger)
        logger.debug(pprint(entry))
    print "done"

def delete_by_retailer(spider, day=None):
    if day:
        d = datetime.datetime.strptime(day,'%Y-%m-%d').date().isoformat()
    else:
        d = datetime.date.today().isoformat()
    db.delete_retailer_by_date({"retailer": spider, "day": d }, logger)
    return


def load_all():
    logger.info("load all files")
    for spider in spiders:
        load_today(spider)

def reload_date(**kwargs):
    logger.debug("reloading %s" % kwargs)
    delete_by_retailer(kwargs['spider'], day=kwargs['day'])
    load_retailer(kwargs['spider'], day=kwargs['day'])

def reload_spider(**kwargs):
    spider = kwargs['spider']
    delete_by_retailer(spider)
    load_today(spider)

    

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Load data sets')
    parser.add_argument('-s','--spider', metavar='spider')
    parser.add_argument('-r',action='store_true', help="reload a given spider,\ndeletes and reinserts")
    parser.add_argument('-d','--day', metavar='day')
    args = vars(parser.parse_args())
    logging.debug(pprint(args))
    if not args.keys():
        load_all()
    if args['spider']:
        if args['r']:
            if args.has_key('day'):
                if not args['day']:
                    args['day'] = datetime.date.today().isoformat()
                reload_date(**args)
            else:
                reload_spider(**args)
        else:
            load_today(args['spider'])
    else:
        load_all()
    
