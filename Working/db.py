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
             "CREATE TABLE IF NOT EXISTS user_info (email VARCHAR(319), password VARCHAR(50), username VARCHAR(50), counter INT DEFAULT 0)")
      
        logging.debug("create_accounts(): status message: %s",
                      cur.statusmessage)
       
    
    conn.commit()  


info(conn)

def insert_user(conn, email, password, username):
    with conn.cursor() as cur:
        cur.execute(
            f"UPSERT INTO user_info (email , password, username) VALUES ('{email}', '{password}', '{username}')"
        )
        logging.debug("init_db(): status message: %s",
                      cur.statusmessage)
    conn.commit()

def validate_login(conn, email, password):
   
    with conn.cursor() as cur:
        
        cur.execute(
            f"SELECT username FROM user_info WHERE email='{email}' AND password='{password}'"
        )
        result = cur.fetchone()
        conn.commit()
        print(result)

def insertCounter(conn, username, counter):
     with conn.cursor() as cur:
        
        cur.execute(
            f"UPDATE user_info SET counter = counter + {counter} WHERE username='{username}'"
        )
        
        conn.commit()
        
    



insert_user(conn, email='hi@gmail.com', password='pass', username='chalory')
validate_login(conn, email='hi@gmail.com', password='pass')
insertCounter(conn, username='chalory', counter=1)
