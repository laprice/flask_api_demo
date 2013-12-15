from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
import logging
from flask import jsonify
import db
import json

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"available_methods" : 
                       { "search" : ("string","list"),
                         "product": ("string", "dictionary"),
                         "brand": ("string", "list"),
                         "retailers": (None, "list"),
                         "report_quantities": (None, "list"),
                         }
                       })


@app.route('/search/<query>')
def search(query):
    return (json.dumps(db.lookup(query, logger)),
            200, {"Content-Type": "application/json"})
            

@app.route('/retailers/')
def retailers():
    return (json.dumps(db.get_retailers(logger)),
            200, {"Content-Type": "application/json"})

@app.route('/report_quantities/')
def report_quantities():
    return (json.dumps(db.get_retailer_quantity_by_day(logger)),
            200, {"Content-Type": "application/json"})

app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_pyfile('settings.py')
logger = app.logger
logging.basicConfig(filename=app.config['LOG_FILE'])
if __name__=='__main__':
    app.run()

