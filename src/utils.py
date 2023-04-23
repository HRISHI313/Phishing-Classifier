import pymongo
import pandas as pd

def read_mongodb(collection):
    client1 = pymongo.MongoClient("mongodb+srv://banerjeeabishek999:mongodb@clutter1.njaa4j8.mongodb.net/?retryWrites=true&w=majority")
    db = client1['phishing_classifier']
    cursor = db[collection].find()
    dataframe = pd.DataFrame(list(cursor))
    dataframe.drop(columns=['_id'],axis=1,inplace=True)
    return dataframe
