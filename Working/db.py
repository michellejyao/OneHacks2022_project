#!/usr/bin/env python3
"""
Test psycopg with CockroachDB.
"""
from collections import defaultdict

import json
import time
import random
import logging
import os
from argparse import ArgumentParser, RawTextHelpFormatter
import logging

import psycopg2
from psycopg2.errors import SerializationFailure

conn = psycopg2.connect("postgresql://chantal:onehacks2022@free-tier6.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Donehacks-backend-2776")

def info(conn):
    with conn.cursor() as cur:
        cur.execute(
             "CREATE TABLE IF NOT EXISTS user_info (email varchar(319), password VARCHAR)")
      
        logging.debug("create_accounts(): status message: %s",
                      cur.statusmessage)
       
    
    conn.commit()  


info(conn)

def insert_activity(conn, email, password):
    with conn.cursor() as cur:
        cur.execute(
            f"UPSERT INTO user_info (email, password) VALUES ('{email}', '{password}')"
        )
        logging.debug("init_db(): status message: %s",
                      cur.statusmessage)
    conn.commit()


# insert_activity(conn, email='hi', password='pass')