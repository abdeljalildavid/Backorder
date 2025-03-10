
from typing import Protocol
from sklearn.metrics import get_scorer
from sklearn.base import BaseEstimator
from sklearn.model_selection import RandomizedSearchCV
from src.exception import BackOrderException
from src.logger import logging
import sys


class BaseModel(Protocol):
    def fit(self, X, y): ...
    def predict(self, X): ...
    def score(self, X, y, sample_weight=None): ...
    def set_params(self, **params): ...

class Model(Protocol):
    def fit(self, X, y)->BaseModel: ...
    def predict(self, X): ...
    def score(self, X, y, sample_weight=None): ...
    def set_metric(self,metric):...
    def set_params(self, **params): ...
    def tune(self,X_train,Y_train,cv,score)->dict:...


class SklearnModel:
    def __init__(self,base_model:BaseModel,estimator:BaseEstimator,parameters:dict):
        self.model = base_model
        self.estimator = estimator
        self.parameters = parameters
        self.metric = 'accuracy'

    def fit(self,X,Y)->object:
        try:
            self.model.fit(X,Y)
            return self
        except Exception as e:
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise BackOrderException(e,sys) # type: ignore
    
    def tune(self,X_train,Y_train,cv,score)->dict:
                         
        try:    
            grid_search = RandomizedSearchCV(
                                          estimator=self.estimator,
                                          param_distributions=self.parameters, 
                                          cv=cv, 
                                          scoring=score
                                         )
            grid_search.fit(X_train,Y_train)
            return grid_search.best_params_
            
        except Exception as e:
            logging.error(BackOrderException(e,sys)) # type: ignore
            raise BackOrderException(e,sys) # type: ignore


    def predict(self,X):
        return self.model.predict(X=X)
    
    def set_params(self,**params):
        self.model.set_params(**params)

    def set_metric(self, metric:str)->None:
        self.metric = metric

    def score(self,x,y)->float:
        scorer = get_scorer(self.metric)
        return scorer(self,x,y)