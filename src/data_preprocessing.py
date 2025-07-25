import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


logger = get_logger(__name__)

class DataPreprocessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
  
    def preprocess_data(self, df):
        try:
            logger.info("Starting data preprocessing step")
            
            logger.info(f"Dropping the unnecessary columns and duplicates from the dataset")
            df.drop(columns=['Unnamed: 0','Booking_ID'], inplace=True)  # Drop all unnecessary columns
            df.drop_duplicates(inplace=True) # Drop duplicate rows

            cat_cols = self.config['data_processing']["categorical_columns"]
            num_cols = self.config['data_processing']["numerical_columns"]

            logger.info(f"Applying Label Encoding: {cat_cols}")

            label_encoder = LabelEncoder()
            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}   # type: ignore
            
            logger.info(f"Label Encoding completed with mappings: {mappings}")
            for col, mappings in mappings.items():
                logger.info(f"Column: {col}, Mappings: {mappings}")
            
            logger.info("Doing skewness handling")  # Apply skewness handling
            skew_threshold = self.config['data_processing']["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew()).sort_values(ascending=False)

            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column]) #  Apply log transformation to reduce skewness

            return df
        
        except Exception as e:
            logger.error(f"Error during data preprocessing: {e}")
            raise CustomException("Data preprocessing failed", e)
        
    def balance_data(self, df):
        try:
            logger.info("Handling imbalanced data using SMOTE")
            # Oversampling the minority class
            X = df.drop(columns=["booking_status"]) # type: ignore
            y = df["booking_status"] # type: ignore

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y) # type: ignore

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled  # type: ignore

            logger.info("Data balancing completed")
            return balanced_df
        except Exception as e:
            logger.error(f"Error during data balancing: {e}")
            raise CustomException("Data balancing failed", e)
        
    def select_features(self, df):
        try:
            logger.info("Starting our feature selection step")
            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': feature_importance
            })
            top_features = feature_importance_df.sort_values(by='importance', ascending=False)

            num_features_to_select = self.config['data_processing']["no_of_features"]
            top_10_features = top_features["feature"].head(num_features_to_select).values
            logger.info(f"Selected features: {top_10_features}")

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]
            logger.info(f"Feature selection completed successfully.")

            return top_10_df

        except Exception as e:
            logger.error(f"Error during feature selection: {e}")
            raise CustomException("Feature selection failed", e)
        
    def save_data(self, df, file_path):
        try:
            logger.info(f"Saving our data in processed folder")

            df.to_csv(file_path, index=False)
            logger.info(f"Data saved successfully at {file_path}")

        except Exception as e:
            logger.error(f"Error while saving data: {e}")
            raise CustomException("Failed to save data", e)
    
    def process(self):
        try:
            logger.info("Starting data preprocessing pipeline")
            
            # Load the data
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            # Preprocess the training data
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            # Balance the training and test data
            train_df = self.balance_data(train_df)  # type: ignore
            test_df = self.balance_data(test_df)  # type: ignore

            # Select features from the training data
            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]  # Ensure test data has the same columns as train data

            # Save the processed training data
            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data preprocessing pipeline completed successfully")

        except Exception as e:
            logger.error(f"Error in data preprocessing pipeline: {e}")
            raise CustomException("Data preprocessing pipeline failed", e)
        
if __name__ == "__main__":
    processor = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()




            