from src.data_acess.cassandra_connection_manager import CassandraConnectionManager

def import_data_as_csv():
        # Get the singleton instance of the connection manager
        cassandra_manager      = CassandraConnectionManager()

        # Connect to Cassandra
        cassandra_manager.connect()
    
        query = "SELECT * FROM backorder_dataset"
        df = cassandra_manager.execute_query(query)
        print(len(df))

        cassandra_manager.close()
        

import_data_as_csv()