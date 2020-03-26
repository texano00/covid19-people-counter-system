import psycopg2
import config
from configparser import ConfigParser 
from datetime import datetime
import os

def getCountByCode(code):
    """ insert a new data """
    conn = None
    results = []
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...', flush=True)
        conn = psycopg2.connect(host=os.getenv('POSTGRES_HOST'),database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'))
      
    except (Exception, psycopg2.DatabaseError) as error:
        print(error, flush=True)
    finally:
        if conn is not None:
            sql = "SELECT * FROM data.people P WHERE P.code='"+code+"' ORDER BY date desc LIMIT 20"
            try:
                # create a new cursor
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql)
                # commit the changes to the database
                results = cur.fetchall()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error, flush=True)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.', flush=True)
        else:
            print('Strange error', flush=True)

    return results