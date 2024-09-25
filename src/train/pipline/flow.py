from src.train.configuration_provider import ConfigProvider
from src.train.components.data_ingestion.artifact_definition import DataIngestionArtifact
from src.train.components.data_ingestion.dataIngestion import DataIngestion
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
    
    def start(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            logging.error(BackOrderException(e, sys))

TrainingPipeline(ConfigProvider()).start()