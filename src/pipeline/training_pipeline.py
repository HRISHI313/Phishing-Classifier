import os
import sys

from src.exception import CustomException
from src.logger import logging
from src.TrainingPrediction_components.data_ingestion import DataIngestion
from src.TrainingPrediction_components.DataTransformation import data_transformer
from src.TrainingPrediction_components.model_trainer import Model_Trainer


if __name__== '__main__':
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    data_transformation = data_transformer()
    train_arr,test_arr = data_transformation.initiate_data_transformer(train_data,test_data)

    model_trainer = Model_Trainer()
    model_trainer.initiate_model_trainer(train_arr,test_arr)