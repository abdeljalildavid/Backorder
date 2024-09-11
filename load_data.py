
#gdown https://drive.google.com/uc?id=1GweUxUAZJhhUVgKHnhL0Hwd6qGZ25BCe
#gdown https://drive.google.com/uc?id=1HOSsnY0tUWlCjvIoxZPXkgx3J1tI_vgD
import os
import pandas as pd
from cassandra.cluster import Cluster, BatchStatement
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.ERROR)


# Load environment variables from .env file
load_dotenv()


# Set up connection parameters using environment variables
client_id = os.getenv('ASTRA_DB_CLIENT_ID')
client_secret = os.getenv('ASTRA_DB_CLIENT_SECRET')
secure_bundle_path = os.getenv('ASTRA_DB_BUNDLE_PATH')

# Verify that environment variables are loaded correctly
if not all([client_id, client_secret, secure_bundle_path]):
    raise ValueError("Missing Astra DB connection details in environment variables.")

# Create a Cassandra connection using the secure connect bundle
auth_provider = PlainTextAuthProvider(client_id, client_secret)
cluster = Cluster(cloud={'secure_connect_bundle': secure_bundle_path}, auth_provider=auth_provider)

# Connect to the session
session = cluster.connect()

# Set keyspace (replace with your keyspace name)
session.set_keyspace('backorder')

# CQL to drop the table
drop_table_query = "DROP TABLE IF EXISTS backorder_dataset;"

# Execute the query
session.execute(drop_table_query)


create_table_query = """
CREATE TABLE IF NOT EXISTS backorder_dataset (
    sku TEXT PRIMARY KEY,
    national_inv FLOAT,              
    lead_time FLOAT,                 
    in_transit_qty FLOAT,            
    forecast_3_month FLOAT,        
    forecast_6_month FLOAT,          
    forecast_9_month FLOAT,          
    sales_1_month FLOAT,             
    sales_3_month FLOAT,             
    sales_6_month FLOAT,             
    sales_9_month FLOAT,             
    min_bank FLOAT,                  
    potential_issue TEXT,            
    pieces_past_due FLOAT,           
    perf_6_month_avg FLOAT,
    perf_12_month_avg FLOAT,
    local_bo_qty FLOAT,              
    deck_risk TEXT,                  
    oe_constraint TEXT,              
    ppap_risk TEXT,                  
    stop_auto_buy TEXT,              
    rev_stop TEXT,                   
    went_on_backorder TEXT           
);

"""


session.execute(create_table_query)

# Prepare the INSERT query
insert_data_query = """
INSERT INTO backorder_dataset (sku, national_inv, lead_time, in_transit_qty, forecast_3_month, forecast_6_month, forecast_9_month, sales_1_month, sales_3_month, sales_6_month, sales_9_month, min_bank, potential_issue, pieces_past_due, perf_6_month_avg, perf_12_month_avg, local_bo_qty, deck_risk, oe_constraint, ppap_risk, stop_auto_buy, rev_stop, went_on_backorder)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
prepared_statement = session.prepare(insert_data_query)

# Read CSV file
df = pd.read_csv('Kaggle_Training_Dataset_v2.csv')

# Handle missing values (leave them as None for Cassandra to insert as NULL)
df = df.where(pd.notnull(df), None)

# Create a batch statement
batch = BatchStatement()

# Loop over rows in the DataFrame and add to batch
for i, row in df.iterrows():
    if i == 90 : print()
    
    batch.add(prepared_statement, (
        repr(row['sku']).encode('utf-8'),
        row['national_inv'],         # Missing values will be None, inserted as NULL in Cassandra
        row['lead_time'],
        row['in_transit_qty'],
        row['forecast_3_month'],
        row['forecast_6_month'],
        row['forecast_9_month'],
        row['sales_1_month'],
        row['sales_3_month'],
        row['sales_6_month'],
        row['sales_9_month'],
        row['min_bank'],
        repr(row['potential_issue']).encode('utf-8'),       # Missing booleans will be None, inserted as NULL
        row['pieces_past_due'],
        row['perf_6_month_avg'],
        row['perf_12_month_avg'],
        row['local_bo_qty'],
        repr(row['deck_risk']).encode('utf-8'),
        repr(row['oe_constraint']).encode('utf-8'),
        repr(row['ppap_risk']).encode('utf-8'),
        repr(row['stop_auto_buy']).encode('utf-8'),
        repr(row['rev_stop']).encode('utf-8'),
        repr(row['went_on_backorder']).encode('utf-8')
    ))

    # Execute batch after every 100 rows
    if (i + 1) % 100 == 0:
        print(i)
        session.execute(batch)
        batch = BatchStatement()  # Reset the batch for the next 100 rows

# Insert any remaining rows (if less than 100 rows)
if len(batch) > 0:
    session.execute(batch)


session.shutdown()
cluster.shutdown()
