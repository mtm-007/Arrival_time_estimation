import pandas as pd 
import datetime
import time
import random
import logging
import io 
import uuid
import pytz 
import psycopg


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]:%(message)s")
SEND_TIMEOUT = 10
rand = random.Random()


create_tabel_statement= """ 
DROP TABLE IF EXISTS dummy_metrics;
create table dummy_metrics(
    timestamp timestamp,
    value1 integer,
    value2 varchar,
    value3 float
)
"""


def preb_db():
    with psycopg.connect("host=localhost port=5432 user=postgres password=pass", autocommit=True) as conn:
        res =conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall())==0:
            conn.execute("create database test;")
        with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=pass") as conn:
            conn.execute(create_tabel_statement)

def calculate_dummy_metrics_with_postgresql(curr):
    value1 = rand.randint(0,1000)
    value2 = str(uuid.uuid4())
    value3 = rand.random()

    # curr.execute(
    #     "insert into dummy_metrics(timestamp, value1, value2, value3) values (%s,%s,%s,%s)",
    #     (datetime.datetime.now(pytz.timezone('America/Los_Angeles')), value1, value2, value3)
    # )
    try:
        curr.execute(
            "INSERT INTO dummy_metrics(timestamp, value1, value2, value3) VALUES (%s, %s, %s, %s)",
            (datetime.datetime.now(pytz.timezone('America/Los_Angeles')), value1, value2, value3)
        )
    except Exception as e:
        logging.error(f"Failed to insert data: {e}")

def main():
    preb_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=pass", autocommit=True) as conn:
        for i in range(0,100):
            with conn.cursor() as curr:
                calculate_dummy_metrics_with_postgresql(curr)
            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send = last_send + datetime.timedelta(seconds=10)
            logging.info("data sent")


if __name__=="__main__":
    main()



