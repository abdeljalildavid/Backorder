from src.train.configuration_provider import ConfigProvider
from src.train.components.data_ingestion.artifact_definition import DataIngestionArtifact
from src.train.components.data_ingestion.dataIngestion import DataIngestion
from src.train.components.data_validation.artifact_definition import DataValidationArtifact
from src.train.components.data_validation.dataValidation import DataValidation

from src.logger import logging
from src.exception import BackOrderException
import sys

class TrainingPipeline:

    def __init__(self, config_provider: ConfigProvider):
        self.pipeline_config: ConfigProvider = config_provider


    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion_config = self.pipeline_config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact

        except Exception as e:
            logging.error(BackOrderException(e, sys))
            return DataIngestionArtifact()
    


    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation_config = self.pipeline_config.get_data_validation_config()
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact

        except Exception as e:
            logging.error(BackOrderException(e, sys))
            #return DataValidationArtifact()
    



    def start(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
        except Exception as e:
            logging.error(BackOrderException(e, sys))

TrainingPipeline(ConfigProvider()).start()