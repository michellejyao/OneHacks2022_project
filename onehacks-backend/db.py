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

conn = psycopg2.connect("postgresql://chantal:onehacks2022@free-tier6.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Donehacks-2022-2773")

def info(conn):
    with conn.cursor() as cur:
        cur.execute(
             "CREATE TABLE IF NOT EXISTS user_info (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), email VARCHAR, first_name VARCHAR, last_name VARCHAR, contact_number VARCHAR(15))")
      
        logging.debug("create_accounts(): status message: %s",
                      cur.statusmessage)
       
    
   
    conn.commit()  
info(conn)

def insert_activity(conn, info):
    with conn.cursor() as cur:
        cur.execute(
            f"UPSERT INTO activities (email, first_name, last_name, contact_number) VALUES ('{info['email']}','{info['first_name']}','{info['last_name']}',{info['contact_number']}')"
        )
        logging.debug("init_db(): status message: %s",
                      cur.statusmessage)
    conn.commit()

