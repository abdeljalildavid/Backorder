import yaml
import sys
from src.logger import logging
from src.exception import BackOrderException
from typing import Optional, Dict, Any



def read_yaml(file_path:str)-> Optional[Dict[str,Any]]:
        """
        
        Reads a YAML file and returns the content as a Python dictionary.

        Returns:
            Optional[Dict[str, Any]]: Parsed YAML content as a dictionary or None if there's an error.
    
        """
        try:
            with open(file_path, 'r') as file:
                content = yaml.safe_load(file)  # Load YAML into Python dictionary
            return content
        except FileNotFoundError:
            logging(f"Error: File {file_path} not found.")
        except yaml.YAMLError as e:
            logging(f"Error while parsing YAML file: {BackOrderException(e,sys)}")
        except Exception as e:
            logging(f"An unexpected error occurred: {BackOrderException(e,sys)}")
        return None
    
if __name__ == "__main__":
    out = read_yaml('./data_schema.yaml')['drop_columns'][0]
    print(out)