import os
import pandas as pd
from src.logger import get_logger
from google.cloud import storage
from src.custom_exception import CustomException
from sklearn.model_selection import train_test_split
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)
CONFIG_PATH = "config/config.yaml"


class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config['bucket_name']
        self.file_name = self.config['bucket_file-name']
        self.train_test_ratio = self.config['train_ratio']

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info("Data Ingestion started with {self.bucket_name} and file is {self.file_name}")
    
    def download_csv_from_gcp(self):
        """
        Downloads a CSV file from Google Cloud Storage and saves it to the local raw directory.
        """
        try:
            client = storage.Client(project="vocal-tracker-466814-q0")
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"CSV File {self.file_name} successfully downloaded from GCP bucket {self.bucket_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error whle downloading CSV file from GCP")
            raise CustomException("Failed to download CSV file from GCP", e) # type: ignore
        
    def split_data(self):
        try:
            logger.info("Starting the splitting process")
            data = pd.read_csv(RAW_FILE_PATH)

            train_data, test_data = train_test_split(data, test_size = 1-self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info(f"Data split into train and test sets. Train data saved to {TRAIN_FILE_PATH}, Test data saved to {TEST_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error while splitting data")
            raise CustomException("Failed to split data into training and test sets", e) # type: ignore
        
    def run(self):
        try:
            logger.info("Starting the data ingestion process")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data ingestion process completed successfully")
        except CustomException as ce:
            logger.error(f"Custom Exception occurred: {str(ce)}")
            raise ce
        
        finally:
            logger.info("Data ingestion process finished")
            
if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()