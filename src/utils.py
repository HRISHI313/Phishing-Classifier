import pymongo
import pandas as pd

def read_mongodb(user,password,collection):
    client1 = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.k5pminz.mongodb.net/?retryWrites=true&w=majority".format(user,password))
    db = client1['phishing_classification']
    cursor = db['{}'.format(collection)].find()
    dataframe = pd.DataFrame(list(cursor))
    dataframe.drop(columns=['_id'],axis=1,inplace=True)
    return dataframe