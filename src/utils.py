
import yaml
import json
import sys,os
import numpy as np
import dill
from src.logger import logging
from src.exception import BackOrderException
from typing import Dict



def read_yaml(file_path:str)-> Dict:
        """
        
        Reads a YAML file and returns the content as a Python dictionary.

        Returns:
            Optional[Dict[str, Any]]: Parsed YAML content as a dictionary or None if there's an error.
    
        """
        try:
            with open(file_path, 'r') as file:
                content = yaml.safe_load(file)  # Load YAML into Python dictionary
            return content
    
        except Exception as e:
            logging.error(f"An unexpected error occurred: {BackOrderException(e,sys)}")
            raise(BackOrderException(e,sys))
        




def write_to_json(file_path:str, content:dict)-> None:
        
    
        with open(file_path, "w") as file:
            if content is not None:
                json.dump(content, file,)
    

def save_numpy_array_data(file_path: str, array: np.ndarray)-> None:
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: numpy array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        
        raise BackOrderException(e, sys)


def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise BackOrderException(e, sys)


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise BackOrderException(e, sys) from e


def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise BackOrderException(e, sys) from e
     
    
