from MUSHROOM import utils
from MUSHROOM.entity import config_entity
from MUSHROOM.entity import artifact_entity
from MUSHROOM.exception import MushroomException
from MUSHROOM.logger import logging
import os, sys
import pandas as pd
from sklearn.model_selection import train_test_split


class DataIngestion:

    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} DATA INGESTION {'>>'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e :
            raise MushroomException(e, sys)    

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info("Exporting collection as pandas dataframe")
            #Exporting collection data as pandas dataframe
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name)

            logging.info("Create feature store folder if not exist")
            #Create feature store folder if not exist
            feature_store_dir = os.path.dirname(self.data_ingestion_config.features_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            logging.info("Save df to feature store folder")
            #Save df to fearture store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.features_store_file_path,index=False,header=True)

            logging.info("Splitting the dataset into train and test set")
            #Split dataset into train and test set
            train_df , test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size ,random_state=42)

            logging.info("Create dataset directory if not available")
            #Create dataset directory if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)

            logging.info("Save train and test dataset into feature store folder")    
            #Save df to feature store folder
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            #Prepare artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                features_store_file_path=self.data_ingestion_config.features_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
                )

            logging.info(f"DATA INGESTION ARTIFACT: {data_ingestion_artifact}")
            return data_ingestion_artifact    

        except Exception as e :
            raise MushroomException(e, sys)        