from src.train.components.data_ingestion.config_definition import DataIngestionConfig
from src.train.components.data_ingestion.artifact_definition import DataIngestionArtifact
from src.train.pipline.constants import DATA_SCHEMA_FILE_PATH
from src.data_acess.cassandra_connection_manager import CassandraConnectionManager
from src.logger import logging
from src.exception import BackOrderException
from src.utils import read_yaml
from sklearn.model_selection import train_test_split
import pandas as pd
import os, sys

class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig) -> None:
        self.data_ingestion_config     = data_ingestion_config
        self.columns_to_drop           = read_yaml(DATA_SCHEMA_FILE_PATH)['drop_columns']
        
    def import_data_from_db(self)-> pd.DataFrame:
        """
        Import data from Cassandra db, and store the imported 
        data as csv.
        Returns:

           pd.DataFrame

        """

        try:
                    
    
            # Get the singleton instance of the connect
            cassandra_manager   = CassandraConnectionManager()

            # Connect to Cassandra
            cassandra_manager.connect()
            # import data from cassandra db
            query               = f"SELECT * FROM {self.data_ingestion_config.table_name} LIMIT 120000;"
            df                  = cassandra_manager.execute_query(query)
            
            # Save the dataframe as csv in the given path
            print(self.data_ingestion_config.feature_store_dir)

            dir_path = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            logging.info(f"Create feature store directory {dir_path}")

            os.makedirs(dir_path, exist_ok=True)

            
            df.to_csv(self.data_ingestion_config.feature_store_file_path)
            cassandra_manager.close()
            return df
        
        except Exception as e:
            logging.error(BackOrderException(e,sys))
    
    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        """
        Feature store dataset will be split into train and test file
        """

        try:
            # Split data into train and test
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            logging.info(f"Create ingested directory {dir_path}")
            # Create the directory where we store train and test data
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test data to file path.")
            
            # Save train data as csv 
            train_set.to_csv(
                self.data_ingestion_config.train_file_path, index=False, header=True
                )
            
            # Save test data as csv 
            test_set.to_csv(
                self.data_ingestion_config.test_file_path, index=False, header=True
            )

            logging.info(f" Done.")
        except Exception as e:
            logging.error(BackOrderException(e,sys))
        


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Start data ingestion...")
            dataframe = self.import_data_from_db()
            dataframe = dataframe.drop(self.columns_to_drop,axis=1)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.train_file_path,
                                                           test_file_path=self.data_ingestion_config.test_file_path)
            logging.info("Terminater")
            return data_ingestion_artifact
        except Exception as e:
            logging.error(BackOrderException(e,sys))
            return DataIngestionArtifact()