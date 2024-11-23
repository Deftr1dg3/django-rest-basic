#!/usr/bin/env python
import os 
import csv
import sys
import argparse
import psycopg2

import dotenv

# Load env variables from FILE ------------------------
dotenv.load_dotenv('./postgres_env')

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file', type=str, help='Path to the *.csv file', required=True)
parser.add_argument('-t', '--table', type=str, help='Table name', required=True)

args = parser.parse_args()

file_path = args.file 
table_name = args.table

if not os.path.exists(file_path):
    raise FileNotFoundError(f'File "{file_path}" does not exist.')


USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE = os.getenv('POSTGRES_DB')

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

try:
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
except Exception as ex:
    print(f'An Exception occured while connecting to database.\n{ex}')
    sys.exit(1)

cursor = conn.cursor()

with open(file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    
    headers = next(reader)
    # print(f'{headers = }')

    insert_query = f"""
    INSERT INTO {table_name} ({', '.join(headers)}) VALUES({', '.join('%s' for _ in headers)})
    """
    
    rows = [row for row in reader]
    # print(f'{rows[0] = }')
    
    try:
        print(f'Inserting {len(rows)} rows into the "{table_name}" in DB: "{DATABASE}".')
        cursor.executemany(insert_query, rows)
    except psycopg2.errors.UndefinedTable:
        raise ValueError(f'An Exception occured:\nTable with provided name -> "{table_name}" does not exist.')
    
    # Commit changes -------
    conn.commit()
    
cursor.close()
conn.close()

print(f'{len(rows)} rows have been inserted into the "{table_name}" successfully.')
