import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import sys
import yaml

logger = get_logger(__name__)

def read_yaml(file_path):
    """
    Reads a YAML file and returns its content.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML file not found at {file_path}")
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read the YAML file")
            return config
        
    except Exception as e:
        logger.error(f"Error while reading YAML file")
        raise CustomException("Failed to read YAML file", e) # type: ignore

def load_data(path):
    try:
        logger.info(f"Loading data from {path}")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error while loading data {e}")
        raise CustomException(f"Failed to load data from {path}", e)
    