import os
import sys

from src.exception import CustomException
from src.logger import logging
from src.utils import read_mongodb
from src.TrainingPrediction_components.DataTransformation import data_transformer

from sklearn.model_selection import train_test_split

import pandas as pd
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered into the Data ingestion method')
        try:
            data1 = read_mongodb('banerjeeabishek999','mongodb', 'data')
            data2 = read_mongodb('banerjeeabishek999','mongodb', 'phishy_data')
            logging.info('Read Dataset from mongodb as dataframe')

            logging.info('Data concatenating and shuffling initiated')
            data = pd.concat([data1,data2],axis = 0)
            data.sample(frac = 1)
            data.drop('URL',axis = 1,inplace =True)
            logging.info('Data concatenating and shuffling finished')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            data.to_csv(self.ingestion_config.raw_data_path,index = False,header = True)

            logging.info("train test completed initiated")
            train_data,test_data = train_test_split(data,test_size = 0.3,random_state = 42)

            train_data.to_csv(self.ingestion_config.train_data_path,index = False,header = True)
            test_data.to_csv(self.ingestion_config.test_data_path,index = False,header = True)
            logging.info("train test split completed")

            logging.info("Data ingestion completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)










