

import sys
from src.logger import logging
import pandas as pd

from src.exception import BackOrderException
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from cassandra.auth import PlainTextAuthProvider
from src.data_acess.cassandra_db_config import ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET, ASTRA_DB_SECURE_BUNDLE_PATH, KEYSPACE


class CassandraConnectionManager:
    _instance = None  # Singleton instance of the class
    _session = None   # Singleton instance of the session

    def __new__(cls):
        """Control instance creation to enforce singleton behavior"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        """Initialize the Cassandra session if it doesn't exist"""
        if self._session is None:
            try:
                cloud_config = {'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH}
                auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
                cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
                self._session = cluster.connect(KEYSPACE)
                logging.info("Successfully connected to Cassandra.")
            except Exception as e:
                logging.error(f"Failed to connect to Cassandra. {BackOrderException(e,sys)}")
        else:
            logging.info("Reusing the existing Cassandra session.")

    def close(self):
        """Shutdown the session and cluster if it exists"""
        if self._session:
            try:
                self._session.shutdown()
                self._session = None
                logging.info("Cassandra session closed.")
            except Exception as e:
                logging.error(f"Error closing the session. {BackOrderException(e,sys)}")
        else:
            logging.warning("No active session to close.")

    @classmethod
    def get_session(cls):
        """Return the Cassandra session instance"""
        if cls._session is None:
            logging.warning("Session is not initialized. Call connect() first.")
        return cls._session

    def execute_query(self, query:str)-> pd.DataFrame:
        """Execute a given CQL query and return results"""
        if self._session is None:
            logging.error("Session is not initialized. Call connect() first.")
            return None

        try:
            statement = self._session.prepare(query)
            statement.fetch_size = 100000
            result_set = self._session.execute(statement)
            
            all_rows = []
            while result_set.has_more_pages:
                rows = result_set.current_rows
                all_rows.extend(rows)  # Append the current page of results
                result_set.fetch_next_page()  # Fetch the next page of results
                print(len(all_rows))

            # Don't forget to append the last set of rows
            all_rows.extend(result_set.current_rows)

            # Convert all rows to a DataFrame
            df = pd.DataFrame(all_rows)
            print(df.shape)
            return df
            
        except Exception as e:
            logging.error(f"Error executing query. {BackOrderException(e,sys)}")
            return pd.DataFrame()
        
#####################################################################################################        

def main():
    # Get the singleton instance of the connection manager
    cassandra_manager = CassandraConnectionManager()


    # Connect to Cassandra
    cassandra_manager.connect()
    

    # Example: Query some data
    query = "SELECT * FROM backorder_dataset LIMIT 1;"
    result = cassandra_manager.execute_query(query)

    # Print the results
    if result:
        for row in result:
            print(row)

    # Close the session
    cassandra_manager.close()

if __name__ == "__main__":
    main()

