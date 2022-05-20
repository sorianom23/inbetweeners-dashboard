
from decouple import config
from opensea import OpenseaAPI
import psycopg2 as ps2
import requests

api = OpenseaAPI(apikey=config('API_KEY_OS'))

# get data
def get_info():
    data = api.collection_stats(collection_slug="inbetweeners")
    return data['stats']['floor_price'], data['stats']['total_volume'], data['stats']['total_sales']


# SQL
def database(floor_price, total_volume, total_sales):
    conn=ps2.connect(config('psql_url'))
    cur=conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS test1(floor_price FLOAT, total_volume FLOAT, total_sales INT, date_time TIMESTAMP DEFAULT NOW())
    ''')

    cur.execute('''
    INSERT INTO test(floor_price, total_volume, total_sales) VALUES(%s,%s, %s)
    ''',(floor_price, total_volume, total_sales)) 

    conn.commit()
    cur.close()
    conn.close()


# main function
def main():
    floor_price, total_volume, total_sales = get_info()
    database(floor_price, total_volume, total_sales)


if __name__ == '__main__':
    main()