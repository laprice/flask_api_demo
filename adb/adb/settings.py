# Scrapy settings for pde project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'adb' #this gets replaced with a function 
BOT_VERSION = '1.0'

SPIDER_MODULES = ['adb.spiders']
NEWSPIDER_MODULE = 'adb.spiders'
DEFAULT_ITEM_CLASS = 'adb.items.Product'
ITEM_PIPELINES = 'adb.pipelines.AdbPipeline'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

TELNETCONSOLE_HOST = '127.0.0.1' # defaults to 0.0.0.0 set so 
TELNETCONSOLE_PORT = '6073'      # only we can see it.
TELNETCONSOLE_ENABLED = False

WEBSERVICE_ENABLED = False

LOG_ENABLED = True
LOG_FILE = '/home/adb/logs/scrapy.log'

ROBOTSTXT_OBEY = False
ITEM_PIPELINES = [
    'adb.pipelines.AdbPipeline',
    ]

DATA_DIR = '/home/adb/data' #directory to store export files to.

DOWNLOAD_DELAY = 0.025
