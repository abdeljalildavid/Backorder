from src.train.components import data_transformation
from src.train.configuration_provider import ConfigProvider
from src.train.components.data_ingestion.artifact_definition import DataIngestionArtifact
from src.train.components.data_ingestion.dataIngestion import DataIngestion
from src.train.components.data_validation.artifact_definition import DataValidationArtifact
from src.train.components.data_validation.dataValidation import DataValidation
from src.train.components.data_transformation.artifact_definition import DataTransformationArtifact
from src.train.components.data_transformation.dataTransformation import DataTransformation

from src.logger import logging
from src.exception import BackOrderException
import sys

class TrainingPipeline:

    def __init__(self, data_ingestion:DataIngestion,
                       data_validation:DataValidation,
                       data_transformation:DataTransformation):
        #self.pipeline_config: ConfigProvider = config_provider
        self.data_ingestion      = data_ingestion
        self.data_validation     = data_validation
        self.data_transformation = data_transformation

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            #data_ingestion_config = self.pipeline_config.get_data_ingestion_config()
            #data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact

        except Exception as e:
            logging.error(BackOrderException(e, sys)) # type: ignore
            raise BackOrderException(e,sys) # type: ignore
    


    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            #data_validation_config = self.pipeline_config.get_data_validation_config()
            #data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            data_validation_artifact = self.data_validation.initiate_data_validation(data_ingestion_artifact)
            return data_validation_artifact

        except Exception as e:
            logging.error(BackOrderException(e, sys)) # type: ignore
            raise BackOrderException(e,sys) # type: ignore


    def start_data_transormation(self,data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            #data_transformation_config = self.pipeline_config.get_data_transformation_config()
            #data_transformation = DataTransformation()
            data_transformation_artifact = self.data_transformation.initiate_data_transformation(data_validation_artifact)
            return data_transformation_artifact

        except Exception as e:
            logging.error(BackOrderException(e, sys)) # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore

    



    def start(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transormation(data_validation_artifact)
        except Exception as e:
            logging.error(BackOrderException(e, sys)) # type: ignore
