import pymongo
import pandas as pd
import json
from MUSHROOM.config import mongo_client


DATA_FILE_PATH = "/config/workspace/mushrooms.csv"
DATABASE_NAME = "mushroom"
COLLECTION_NAME = "mushroom_dataset"

if __name__ == '__main__':
    df = pd.read_csv(DATA_FILE_PATH)
    print(f'Rows and columns: {df.shape}')

    #Convert dataframe to json
    df.reset_index(drop=True,inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    #insert converted json record in mongodb
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)