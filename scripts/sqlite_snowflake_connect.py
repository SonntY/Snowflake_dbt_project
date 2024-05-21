import pandas as pd
import snowflake.connector
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os

# Create 3 data frames from CSV files

df_patients = pd.read_csv('patients.csv')
df_tests = pd.read_csv('tests.csv')
df_visit_info = pd.read_csv('visitinfo.csv')

conn = sqlite3.connect('patients.db')

# Load DataFrames into the SQLite database
df_patients.to_sql('patients', conn, if_exists='replace', index=False)
df_tests.to_sql('tests', conn, if_exists='replace', index=False)
df_visit_info.to_sql('visit_info', conn, if_exists='replace', index=False)

# Test if data was loaded
# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Execute a SELECT query to fetch data from the patients table
cur.execute("SELECT * FROM patients")

""""# Fetch and print the query results to see if everything got uploaded into the database
rows = cur.fetchall()
for row in rows:
    print(row)
"""

# Commit changes
conn.commit()

# SQLite connection settings
sqlite_db_file = 'patients.db'  # Path to your SQLite database file
sqlite_conn = sqlite3.connect(sqlite_db_file)
sqlite_cursor = sqlite_conn.cursor()

# Load the environment variables from the .env file
load_dotenv(dotenv_path='credentials.env')

# Connect to Snowflake
snowflake_conn = snowflake.connector.connect(
    user = os.getenv('snowflake_user'),
    password = os.getenv('snowflake_password'),
    account = os.getenv('snowflake_account'),
    warehouse = os.getenv('snowflake_warehouse'),
    database = os.getenv('snowflake_database'),
    schema = os.getenv('snowflake_schema')
)

snowflake_cursor = snowflake_conn.cursor()

# Fetch data from the "patients" table in SQLite
sqlite_cursor.execute('SELECT Name, Family, ID, birthdate, city, region FROM patients')
rows = sqlite_cursor.fetchall()

# Insert data into the "patients" table in Snowflake
for row in rows:
    # Construct the INSERT INTO statement with column names and values
    insert_statement = f"INSERT INTO patients (Name, Family, ID, birthdate, city, region) VALUES ('{row[0]}', '{row[1]}', {row[2]}, '{row[3]}', '{row[4]}', '{row[5]}')"
    snowflake_cursor.execute(insert_statement)

# Fetch data from the "tests" table in SQLite
sqlite_cursor.execute('SELECT sugar, Fe, whitcells, redcells, "date", id FROM tests')
rows = sqlite_cursor.fetchall()

# Insert data into the "tests" table in Snowflake
for row in rows:
    # Replace None values with NULL
    row_values = [value if value is not None else None for value in row]

    # Construct the INSERT INTO statement with parameterized query
    insert_statement = "INSERT INTO tests (sugar, Fe, whitecells, redcells, date, id) VALUES (%s, %s, %s, %s, %s, %s)"

    # Execute the INSERT statement
    snowflake_cursor.execute(insert_statement, row_values)

# Fetch data from the "visit_info" table in SQLite
sqlite_cursor = conn.cursor()
sqlite_cursor.execute('SELECT sick, active, medication, regilar, "date", id FROM visit_info')
rows = sqlite_cursor.fetchall()

# Insert data into the "visit_info" table in Snowflake
for row in rows:
    insert_statement = f"INSERT INTO visit_info (sick, active, medication, regular, date, id) VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}')"
    snowflake_cursor.execute(insert_statement)

snowflake_conn.commit()
snowflake_conn.close()
conn.close()
