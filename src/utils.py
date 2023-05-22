import pymongo
import pandas as pd
import dill
import os
import sys
import pickle
from src.exception import CustomException

from sklearn.metrics import accuracy_score

def read_mongodb(user,password,collection):
    client1 = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.numsybe.mongodb.net/?retryWrites=true&w=majority".format(user,password))
    db = client1['Phishing_classifier']
    cursor = db['{}'.format(collection)].find()
    dataframe = pd.DataFrame(list(cursor))
    dataframe.drop(columns=['_id'],axis=1,inplace=True)
    return dataframe

def save_object (file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)



def evaluate_model(x_train, y_train, x_test, y_test, models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            model.fit(x_train, y_train)

            y_test_pred = model.predict(x_test)

            test_model_score = accuracy_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_message = str(e)
            error_detail = f"{exc_type.__name__}: {exc_value}"
            raise CustomException(error_message, error_detail)










