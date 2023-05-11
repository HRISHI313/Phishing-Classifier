import os
import sys

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
from src.utils import evaluate_model

import pandas as pd
import numpy as np
from dataclasses import dataclass

# Modelling
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
import warnings
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


@dataclass
class ModelTrainConfig:
    model_trainer_file_path = os.path.join('artifacts','model.pkl')

class Model_Trainer:
    def __init__(self):
        self.Model_Trainer_Config = ModelTrainConfig()

    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info('Splitting the Dependentand Independent Columns')
            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "XGBoost": XGBClassifier(),
                "CatBoost": CatBoostClassifier(verbose=False),
                "Ada boost":AdaBoostClassifier(),
                "SVC":SVC(),
                "K-nearest classifier":KNeighborsClassifier()
            }

            model_report = evaluate_model(x_train, y_train, x_test, y_test, models)
            print(model_report)
            print('\n===========================================================================================')
            logging.info(f'Model Report: {model_report}')

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            print(f'Best Model Found , Model name : {best_model_name} , Accuracy Score : {best_model_score}')
            print('\n============================================================================================')
            logging.info(f'Best Model found, Model Name : {best_model_name} , Accuracy Score : {best_model_score}')

            save_object(
                file_path=self.Model_Trainer_Config.model_trainer_file_path,
                obj = best_model
            )

        except Exception as e:
            raise CustomException (e,sys)


