

import pandas as pd
from scipy import sparse
import numpy as np
import os,sys
from sklearn.compose import ColumnTransformer
from src.exception import BackOrderException
from src.logger import logging
from src.utils import save_numpy_array_data, save_object

from src.train.components.data_transformation.artifact_definition import DataTransformationArtifact
from src.train.components.data_transformation.config_definition import DataTransformationConfig
from src.train.components.data_validation.artifact_definition import DataValidationArtifact
from src.train.components.data_transformation.transformers import Transformer,DatasetBalancer

class DataTransformation:
    
    def __init__(self, 
                 data_transformation_config:DataTransformationConfig,
                 transformations: list[Transformer],
                 datasetBalancer:DatasetBalancer
                 ):
        
        self.transformation_config = data_transformation_config
        self.transformers          = transformations
        self.datasetBalancer       = datasetBalancer
    

    def apply_columns_transformations(self,train_df:pd.DataFrame)-> ColumnTransformer:
        try:
            transformers = [trf.transformer for trf in self.transformers]
            ct = ColumnTransformer(transformers = transformers)
            return ct.fit(train_df)
        
        except Exception as e:
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore
    
    def balance_datasets(self,train_ds:np.ndarray)-> np.ndarray:

        try:
            
            return self.datasetBalancer.pipeline.fit_transform(train_ds[:-1],train_ds[-1])
            
        except Exception as e:
            logging.error(BackOrderException(e,sys))         # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore

    def initiate_data_transformation(self,data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            #read train and test dataframe from valid train and test data
            train_df                   = pd.read_csv(data_validation_artifact.valid_train_file_path)                    
            test_df                    = pd.read_csv(data_validation_artifact.valid_test_file_path)
            
            #transform data:

            #1. prepare transformations pipline and fitted to train data

            transformations_pipline    = self.apply_columns_transformations(train_df=train_df)
            
            #2. apply transormation to train and test data

            transformed_train_data      = transformations_pipline.transform(train_df)
            transformed_test_data       = transformations_pipline.transform(test_df)
            

            #3convert train and test data to numpy array

            if isinstance(transformed_train_data,sparse.csr_matrix):
                transformed_train_ds: np.ndarray = transformed_train_data.toarray()
            if isinstance(transformed_test_data,sparse.csr_matrix):
                transformed_test_ds:np.ndarray = transformed_test_data.toarray()
            

            #4. balance train data
            balanced_transormed_train_data   = self.balance_datasets(transformed_train_ds)


            #5. save train and test data
            save_numpy_array_data(
                self.transformation_config.transformed_train_data_file_path,
                balanced_transormed_train_data)
            save_numpy_array_data(
                self.transformation_config.transformed_test_data_file_path,
                transformed_test_ds)
            

            #6. save transformation pipeline object
            save_object(self.transformation_config.transfarmation_pipeline_object_file_path,
                        transformations_pipline)
            
            
            return DataTransformationArtifact(
                transformed_data_train_file_path=self.transformation_config.transformed_train_data_file_path,
                transormed_data_test_file_path= self.transformation_config.transformed_test_data_file_path,
                transformation_pipeline_file_path= self.transformation_config.transfarmation_pipeline_object_file_path
            ) 

        except Exception as e:
            logging.error(BackOrderException(e,sys))         # type: ignore
            raise(BackOrderException(e,sys)) # type: ignore


