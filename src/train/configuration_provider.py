from src.train.pipline.config_definition import TrainingPipelineConfig
from src.train.pipline.constants import *

from src.train.components.data_ingestion.config_definition import DataIngestionConfig
from src.train.components.data_ingestion.constants import *

from src.train.components.data_validation.config_definition import DataValidationConfig
from src.train.components.data_validation.constants import *

from src.train.components.data_transformation.config_definition import DataTransformationConfig
from src.train.components.data_transformation.constants import *

from src.train.components.model_trainer.config_definition import ModelTrainerConfiguration
from src.train.components.model_trainer.constants import *

from src.train.components.model_evaluator.config_definition import ModelEvaluatorConfiguration
from src.train.components.model_evaluator.constants import *


from datetime import datetime
from src.logger import logging
from src.exception import BackOrderException
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
            logging.error(BackOrderException(e, sys)) # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:

        try:
            logging.info("Prepare data ingestion configuration")
            data_ingestion_master_dir = os.path.join(self.pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)

            # time based directory for each run
            data_ingestion_dir = os.path.join(data_ingestion_master_dir,self.timestamp)
            ingested_data_dir  = os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR)

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
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore



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
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore

        
    def get_data_transformation_config(self) -> DataTransformationConfig:

        try:
            logging.info("Prepare data transformation configuration")
            data_transformation_master_dir = os.path.join(self.pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)

            # time based directory for each run
            data_transformation_dir = os.path.join(data_transformation_master_dir,self.timestamp)
            transformed_data_dir    = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR)
            pipeline_object_dir     = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_PIPELINE_OBJECT_DIR)
            
            data_transformation_config = DataTransformationConfig(
               data_transformation_dir_path = data_transformation_master_dir,
               transformed_data_dir_path       = transformed_data_dir,
               transformed_train_data_file_path         = os.path.join(transformed_data_dir,TRAIN_FILE_NAME),
               transformed_test_data_file_path          = os.path.join(transformed_data_dir, TEST_FILE_NAME ),
               transfarmation_pipeline_object_dir_path  = pipeline_object_dir,
               transfarmation_pipeline_object_file_path= os.path.join(pipeline_object_dir,DATA_TRANSFORMATION_PIPELINE_OBJECT_NAME)
               )
            
            logging.info(f"Data transformation config: {data_transformation_config}")
            return data_transformation_config
        except Exception as e:
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore



        
    def get_model_trainer_config(self) -> ModelTrainerConfiguration:

        try:
            logging.info("Prepare model trainer configuration")
            model_trainer_master_dir = os.path.join(self.pipeline_config.artifact_dir,MODEL_TRAINER_DIR_NAME)

            # time based directory for each run
            model_trainer_dir = os.path.join(model_trainer_master_dir,self.timestamp)
            
            model_trainer_config = ModelTrainerConfiguration(
                model_trainer_dir_path= model_trainer_dir,
                model_object_file_path= os.path.join(model_trainer_dir,MODEL_OBJECT_FILE),
                cross_validation_value=CROSS_VALIDATION,
                score=SCORE
                
               )
            
            logging.info(f"Model Trainer config: {model_trainer_config}")
            return model_trainer_config
        except Exception as e:
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore

    def get_model_evaluator_config(self) -> ModelEvaluatorConfiguration:

        try:
            logging.info("Prepare model evaluator configuration")
            model_evaluator_master_dir = os.path.join(self.pipeline_config.artifact_dir,MODEL_EVALUATOR_DIR_NAME)

            # time based directory for each run
            model_evaluator_dir = os.path.join(model_evaluator_master_dir,self.timestamp)
            
            model_evaluator_config = ModelEvaluatorConfiguration(
                model_evaluator_dir_path=model_evaluator_dir,
                model_report_file_path  = os.path.join(model_evaluator_dir,MODEL_REPORT_FILE),
                threshold = THREASHOLD
               )
            
            logging.info(f"Model Trainer config: {model_evaluator_config}")
            return model_evaluator_config
        except Exception as e:
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore






















ConfigProvider().get_data_transformation_config()
