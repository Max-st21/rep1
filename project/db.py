import psycopg2
from psycopg2 import Error, pool
from db_config import db_name,user_name,passwd,host_name

try:
    postgresql_pool = psycopg2.pool.ThreadedConnectionPool(1,100,dbname=db_name, user=user_name, password=passwd, host=host_name, )

except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

def get_conn(postgresql_pool):
    conn = postgresql_pool.getconn()
    cur = conn.cursor()
    return cur, conn
