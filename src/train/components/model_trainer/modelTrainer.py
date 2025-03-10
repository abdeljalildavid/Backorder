
from src.train.components.model_trainer.model import Model
from src.train.components.model_trainer.artifact__definition import ModelTrainerArtifact
from src.train.components.model_trainer.config_definition import ModelTrainerConfiguration
from src.train.components.data_transformation.artifact_definition import DataTransformationArtifact
from src.exception import BackOrderException
from src.logger import logging
from src.utils import load_numpy_array_data,save_object
import sys,os


class ModelTrainer:

    def __init__(self,
                 model_trainer_config : ModelTrainerConfiguration,
                 model                : Model      
                 ) -> None:
        
        self.model_trainer_config = model_trainer_config
        self.model                = model
    
    
    
    def initiate_model_trainer(self,data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
        #1. Read transformed train data and test data
            train_data = load_numpy_array_data(data_transformation_artifact.transformed_data_train_file_path)
            X_train = train_data[:,:-1]
            y_train = train_data[:,-1]

            test_data = load_numpy_array_data(data_transformation_artifact.transormed_data_test_file_path)
            X_test = test_data[:,:-1]
            y_test = test_data[:,-1]



        #2. Perform hyperpameter tuning
            best_params = self.model.tune(
                                           X_train=X_train,
                                           Y_train=y_train,
                                           cv=self.model_trainer_config.cross_validation_value,
                                           score=self.model_trainer_config.score
                                        )
            
        
        #3. Train the model with the best params
            self.model.set_params(**best_params)
            model = self.model.fit(X=X_train,y=y_train)
        
        #4. Get train score
            self.model.set_metric(self.model_trainer_config.score)
            train_score = self.model.score(X_train,y_train) 
        #5. Get test score
            test_score  = self.model.score(X_test,y_test)

        #6. Save the model
            os.makedirs(self.model_trainer_config.model_trainer_dir_path, exist_ok=True)
            save_object(self.model_trainer_config.model_object_file_path,model)

        #7. Prepare the artifact
            return ModelTrainerArtifact(
            trained_model_file_path= self.model_trainer_config.model_object_file_path,
            score_metric=self.model_trainer_config.score,
            train_score=train_score, # type: ignore
            test_score=test_score # type: ignore
            )
        except Exception as e:
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise BackOrderException(e,sys) # type: ignore


        

