from src.train.components.data_validation.config_definition import DataValidationConfig
from src.train.components.data_validation.artifact_definition import DataValidationArtifact
from src.train.components.data_ingestion.artifact_definition import DataIngestionArtifact
from src.train.pipline.constants import DATA_SCHEMA_FILE_PATH
from src.logger import logging
from src.exception import BackOrderException
from src.utils import read_yaml
import pandas as pd
import os, sys

class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact:DataIngestionArtifact) -> None:
        self.data_ingestion_artifact   = data_ingestion_artifact
        self.data_validation_config    = data_validation_config
        self.columns_to_drop           = read_yaml(DATA_SCHEMA_FILE_PATH)['columns']
        
    