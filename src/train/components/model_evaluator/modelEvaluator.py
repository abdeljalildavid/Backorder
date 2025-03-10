
from typing import Union
from src.train.components.model_evaluator.config_definition import ModelEvaluatorConfiguration
from src.train.components.model_trainer.model import Model
from src.train.components.model_trainer.artifact__definition import ModelTrainerArtifact
from src.train.components.data_transformation.artifact_definition import DataTransformationArtifact
from src.train.components.model_evaluator.artifact_definition import ModelEvaluatorArtifact
from src.exception import BackOrderException
from src.logger import logging
from src.utils import load_numpy_array_data
import sys


class modelEvaluator:

    def __init__(self,model_evaluator_config:ModelEvaluatorConfiguration,current_best_model:Union[Model,None] = None) -> None:
        self.model_evaluator_config = model_evaluator_config
        self.current_best_model     = current_best_model
        

    
    
    
    def initiate_model_evaluator(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_artifact:ModelTrainerArtifact) -> ModelEvaluatorArtifact:
        try:
            if self.current_best_model:
            #1. Read transformed test data

                test_data = load_numpy_array_data(data_transformation_artifact.transormed_data_test_file_path)
                X_test = test_data[:,:-1]
                y_test = test_data[:,-1]
    
                self.current_best_model.set_metric(model_trainer_artifact.score_metric)
            
            #2. Get current best model score
                current_best_model_score  = self.current_best_model.score(X_test,y_test)
                new_model_score = model_trainer_artifact.test_score
            #3.Compare current best model with our new model
                score_difference    = new_model_score - current_best_model_score # type: ignore
                new_model_is_better = score_difference > self.model_evaluator_config.threshold
            #4. Prepare the artifact
                return ModelEvaluatorArtifact(
                       trained_model_file_path= model_trainer_artifact.trained_model_file_path,
                       new_model_is_better = new_model_is_better,
                       score_improves_by = score_difference, 
                        
            )
            else:
                return ModelEvaluatorArtifact(
                       trained_model_file_path= model_trainer_artifact.trained_model_file_path,
                       new_model_is_better = True,
                       score_improves_by = 0, 
                )

        except Exception as e:
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise BackOrderException(e,sys) # type: ignore

