import psycopg2
import config
from configparser import ConfigParser 
from datetime import datetime
import os

def insertData(count, code):
    """ insert a new data """
    conn = None
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...', flush=True)
        conn = psycopg2.connect(host=os.getenv('POSTGRES_HOST'),database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'))
      
    except (Exception, psycopg2.DatabaseError) as error:
        print(error, flush=True)
    finally:
        if conn is not None:
            sql = """INSERT INTO data.people(count, code, date)
                    VALUES(%s,%s,%s);"""
            timestamp = datetime.now()
            try:
                # create a new cursor
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (count,code,timestamp,))
                # commit the changes to the database
                conn.commit()
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
    return