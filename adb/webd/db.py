import psycopg2
import datetime

dsn = {
    'host': 'localhost',
    'port': 5432,
    'user': 'adb',
    'database': 'adb',
    'password': 'apasswd',
    }

# keeping the DSN in code like this is not best practice
# we may want to move it to a config file.

try:
    dbx = psycopg2.connect(**dsn)
except psycopg2.Error, e:
    logger.error(e.pgerror)

def convert(row):
    d = dict(zip(["product", "retailer", "acquired", "url", "price", "weight"],
              row))
    d["acquired"] = d["acquired"].date().isoformat()
    d["price"] = str(d["price"])
    d["weight"] = str(d["weight"])
    return d

def lookup(query, logger):
    search_str = "%%%s%%" % query
    try:
        cnx = dbx.cursor()
        cnx.execute("select product,retailer, acquired, url, price, weight from product where product ilike %s and acquired = ( select acquired from latest) order by product, retailer;",
                    [search_str])
    except psycopg2.Error, e:
        logger.error(e.pgerror)
    if cnx.rowcount >= 1:
        result = [convert(row) for row in cnx]
    else:
        result = None
    cnx.close()
    return result

def store_item(item, logger):
    cnx = dbx.cursor()
    query = """
INSERT INTO PRODUCT ( product, retailer, acquired, url, price, weight )
VALUES (%(product)s, %(retailer)s, %(acquired)s, %(url)s, %(price)s, %(weight)s);
"""
    try:
        logger.debug(cnx.mogrify(query, item))
        cnx.execute(query, item)
        dbx.commit()
    except psycopg2.Error, e:
        logger.log(e.pgerror)
    
def delete_retailer_by_date(item, logger):
    #warning does exactly what it says.
    cnx = dbx.cursor()
    query = """
DELETE FROM PRODUCT where retailer = %(retailer)s and acquired = %(day)s;
"""
    try:
        logger.debug(cnx.mogrify(query, item))
        cnx.execute(query, item)
        dbx.commit()
    except psycopg2.Error, e:
        logger.error(e.pgerror)


def get_retailers(logger):
    cnx = dbx.cursor()
    query = """
select distinct retailer from product;
"""
    try:
        logger.debug(cnx.mogrify(query))
        cnx.execute(query)
        return [r[0] for r in cnx.fetchall()]
    except psycopg2.Error, e:
        logger.error(e.pgerror)

def get_retailer_quantity_by_day(logger):
    cnx = dbx.cursor()
    query = """
select retailer, acquired, count(*) from product where retailer is not null group by retailer, acquired order by retailer, acquired;
"""
    try:
        logger.debug(cnx.mogrify(query))
        cnx.execute(query)
        result = cnx.fetchall()
        labels = [ 'retailer','acquired','quantity' ]
        dicts = [ dict(zip(labels, r)) for r in result]
        for d in dicts:
            d['acquired'] = d['acquired'].date().isoformat()
        return dicts
    except psycopg2.Error, e:
        logger.error(e.pgerror)










# def generic_query(item, logger):

#     cnx = dbx.cursor()
#     query = """

# """
#     try:
#         logger.debug(cnx.mogrify(query, item))
#         cnx.execute(query, item)
#         dbx.commit()
#     except psycopg2.Error, e:
#         logger.log(e.pgerror)


