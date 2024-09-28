from src.train.pipline.config_definition import TrainingPipelineConfig
from src.train.components.data_ingestion.config_definition import DataIngestionConfig
from src.train.components.data_ingestion.constants import *
from src.train.components.data_validation.config_definition import DataValidationConfig
from src.train.components.data_validation.constants import *

from datetime import datetime
from src.logger import logging
from src.exception import BackOrderException
from src.train.pipline.constants import PIPELINE_NAME,PIPELINE_ARTIFACT_DIR
import os,sys

class ConfigProvider:

    def __init__(self, pipeline_name=PIPELINE_NAME, timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")):

        self.timestamp = timestamp
        self.pipeline_name = pipeline_name
        self.pipeline_config = self.get_pipeline_config()

    def get_pipeline_config(self) -> TrainingPipelineConfig:
        """
        Provide pipeline config information


        returns > PipelineConfig = namedtuple("PipelineConfig", ["pipeline_name", "artifact_dir"])
        """
        try:
            logging.info("Prepare pipline configuration")

            artifact_dir = PIPELINE_ARTIFACT_DIR
            pipeline_config = TrainingPipelineConfig(pipeline_name=self.pipeline_name,
                                                     artifact_dir=artifact_dir)

            logging.info(f"Pipeline configuration: {pipeline_config}")

            return pipeline_config
        except Exception as e:
            logging.error(BackOrderException(e, sys))
            return TrainingPipelineConfig()
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:

        try:
            logging.info("Prepare data ingestion configuration")
            data_ingestion_master_dir = os.path.join(self.pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)

            # time based directory for each run
            data_ingestion_dir = os.path.join(data_ingestion_master_dir,self.timestamp)
            ingested_data_dir  = os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR)
            print()
            data_ingestion_config = DataIngestionConfig(
               data_ingestion_dir_path = data_ingestion_master_dir,
               ingested_data_dir       = ingested_data_dir,
               train_file_path         = os.path.join(ingested_data_dir,TRAIN_FILE_NAME),
               test_file_path          = os.path.join(ingested_data_dir,TEST_FILE_NAME),
               feature_store_dir       = os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR),
               feature_store_file_path = os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,DATA_INGESTION_FEATURE_STORE_FILE),
               train_test_split_ratio  = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO,
               table_name              =DATA_INGESTION_TABLE_NAME)
            logging.info(f"Data ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            logging.error(BackOrderException(e,sys))
            return DataIngestionConfig()

    def get_data_validation_config(self)->DataValidationConfig:
        try:
            logging.info("Prepare data validation configuration")
            data_validation_master_dir = os.path.join(self.pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)

            # time based directory for each run
            data_validation_dir = os.path.join(data_validation_master_dir,self.timestamp)
            valid_data_dir      = os.path.join(data_validation_dir,DATA_VALIDATION_VALID_DIR)
            invalid_data_dir    = os.path.join(data_validation_dir,DATA_VALIDATION_INVALID_DIR)
            report_dir          = os.path.join(data_validation_dir,DATA_VALIDATION_REPORT_DIR)
            drift_report_dir    = os.path.join(report_dir,DATA_VALIDATION_DRIFT_REPORT_DIR)

            
            data_validation_config = DataValidationConfig(
               data_validation_dir_path      = data_validation_master_dir,
               valid_data_dir                = valid_data_dir,
               invalid_data_dir              = invalid_data_dir,
               valid_train_file_path         = os.path.join(valid_data_dir, TRAIN_FILE_NAME),
               valid_test_file_path          = os.path.join(valid_data_dir, TEST_FILE_NAME),
               invalid_train_file_path       = os.path.join(invalid_data_dir, TRAIN_FILE_NAME),
               invalid_test_file_path        = os.path.join(invalid_data_dir, TEST_FILE_NAME),
               report_dir_path               = report_dir,
               drift_report_dir_path         = drift_report_dir,
               drift_report_yaml_file_path   = os.path.join(drift_report_dir,DATA_VALIDATION_DRIFT_REPORT_YAML_FILE),
               drift_report_html_file_path   = os.path.join(drift_report_dir,DATA_VALIDATION_DRIFT_REPORT_HTML_FILE),
               missing_columns_html_file_path= os.path.join(report_dir,DATA_VALIDATION_MISSING_COLUMNS_REPORT_HTML_FILE)

           )
            logging.info(f"Data validation config: {data_validation_config}")
            return data_validation_config
        except Exception as e:
            logging.error(BackOrderException(e,sys))
            return DataIngestionConfig()


ConfigProvider().get_data_validation_config()
