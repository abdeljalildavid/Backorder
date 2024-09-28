from src.train.components.data_validation.config_definition import DataValidationConfig
from src.train.components.data_validation.artifact_definition import DataValidationArtifact
from src.train.components.data_ingestion.artifact_definition import DataIngestionArtifact
from src.train.pipline.constants import DATA_SCHEMA_FILE_PATH
from src.train.components.data_validation.custom_checker import ColumnsExistCheck
from deepchecks.tabular.checks import FeatureDrift
from src.logger import logging
from deepchecks.tabular import Dataset
from src.exception import BackOrderException
from src.utils import read_yaml,write_to_yaml
import pandas as pd
import os, sys

class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact:DataIngestionArtifact) -> None:
        self.data_ingestion_artifact   = data_ingestion_artifact
        self.data_validation_config    = data_validation_config
        self.columns                   = read_yaml(DATA_SCHEMA_FILE_PATH)['columns']
        self.target                    = read_yaml(DATA_SCHEMA_FILE_PATH)['target'][0]
        self.categorical_features      = read_yaml(DATA_SCHEMA_FILE_PATH)['categorical_features']



    def is_all_columns_exist(self,train_dataframe:pd.DataFrame, test_dataframe:pd.DataFrame)->None:
        try:
           
           logging.info("Verifying if all columns exist...")
           result = ColumnsExistCheck(self.columns).\
            run(Dataset(train_dataframe,label=self.target,cat_features=self.categorical_features ),
                Dataset(test_dataframe, label=self.target, cat_features=self.categorical_features))
           logging.info(f"Verification completed. Result: {result}")
           logging.info("Save missing columns report as html... ")
        
           os.makedirs(self.data_validation_config.report_dir_path, exist_ok=True)
  
           result.save_as_html(self.data_validation_config.missing_columns_html_file_path)
           print("result: ", result.value["status"])
           
           if result.value["status"]:
              os.makedirs(self.data_validation_config.invalid_data_dir, exist_ok=True)
              train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path, index=False, header=True)
              test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path, index=False, header=True)
              logging.error(f"Error: Missing columns : {result}")
  

           else:
              os.makedirs(self.data_validation_config.valid_data_dir, exist_ok=True)
              train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
              test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

        except Exception as e:
            logging.error(BackOrderException(e,sys))

     


    def train_test_drift(self,train_dataframe:pd.DataFrame, test_dataframe:pd.DataFrame)->None:
        try:
           
           logging.info("Start train test drift check...")
           result = FeatureDrift().\
            add_condition_drift_score_less_than(max_allowed_categorical_score=0.2,
                                                max_allowed_numeric_score=0.1).\
            run(Dataset(train_dataframe,label=self.target,cat_features=self.categorical_features ),
                Dataset(test_dataframe, label=self.target, cat_features=self.categorical_features))
           logging.info(f"Check completed. Result: {dict(result.value)}")
           logging.info("Save drift report as html and yaml... ")
        
           os.makedirs(self.data_validation_config.drift_report_dir_path, exist_ok=True)
  
           result.save_as_html(self.data_validation_config.drift_report_html_file_path)
           write_to_yaml(self.data_validation_config.drift_report_yaml_file_path,content=dict(result.value))
        except Exception as e:
            logging.error(BackOrderException(e,sys))
   


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.trained_file_path ,index_col=None)
            test_df  = pd.read_csv(self.data_ingestion_artifact.test_file_path, index_col=None)

            self.is_all_columns_exist(train_dataframe=train_df,test_dataframe=test_df)
            self.train_test_drift(train_dataframe=train_df,test_dataframe=test_df)

            return DataValidationArtifact(
                valid_train_file_path        = self.data_validation_config.valid_train_file_path,
                 valid_test_file_path        =self.data_validation_config.valid_test_file_path,
                 invalid_train_file_path     =self.data_validation_config.invalid_train_file_path,
                 invalid_test_file_path      =self.data_validation_config.invalid_test_file_path,
                 drift_report_yaml_file_path = self.data_validation_config.drift_report_yaml_file_path
                 )
        except Exception as e:
            logging.error(BackOrderException(e,sys))