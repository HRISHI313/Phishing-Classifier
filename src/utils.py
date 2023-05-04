import pymongo
import pandas as pd
import dill
import os
from src.exception import CustomException

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




