import os
import sys

from src.exception import CustomException
from src.logger import logging
from src.utils import read_mongodb

import pandas as pd
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered into the Data ingestion method')
        try:
            train_df = read_mongodb('user2023','test543', 'train_data')
            test_df = read_mongodb('user2023','test543', 'test_data')
            logging.info('Read Dataset from mongodb as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            train_df.to_csv(self.ingestion_config.train_data_path, header=True, index=False)
            test_df.to_csv(self.ingestion_config.test_data_path,header=True, index=False)
            logging.info('Ingestion of data is completed')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__== '__main__':
    obj = DataIngestion()
    obj.initiate_data_ingestion()








