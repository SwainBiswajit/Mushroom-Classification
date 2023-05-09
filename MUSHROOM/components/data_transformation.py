from MUSHROOM.entity import config_entity,artifact_entity
from MUSHROOM import utils
from MUSHROOM.exception import MushroomException
from MUSHROOM.logger import logging
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import os,sys


class DataTransformation:

    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
            try:
                logging.info(f"{'>>'*20} DATA TRANSFORMATION {'<<'*20}")
                self.data_transformation_config = data_transformation_config
                self.data_ingestion_artifact = data_ingestion_artifact
            except Exception as e:
                raise MushroomException(e, sys)
                
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            standard_scaler = StandardScaler()
            pipeline = Pipeline(steps=[
                        ('StandardScaler', standard_scaler)
                        ])
            return pipeline            
        except Exception as e :
            raise MushroomException(e , sys)     


    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        try:
            #Readind training and testing file
            logging.info("Readind training and testing file")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

             #Encoding the input feature
            logging.info("Encoding the input feature")
            label_encoder = LabelEncoder()
            for column in train_df.columns:
                label_encoder.fit(train_df[column])
                train_df[column] = label_encoder.transform(train_df[column])
                test_df[column] = label_encoder.transform(test_df[column])


            #Selecting input features for train and test dataframe
            logging.info("Selecting input features for train and test dataframe")
            input_feature_train_arr = train_df.drop(train_df.iloc[:,:1], axis=1)
            input_feature_test_arr = test_df.drop(test_df.iloc[:,:1], axis=1)

            #Selecting target feature for train and test dataframe
            logging.info("Selecting target feature for train and test dataframe")
            target_feature_train_arr = train_df.iloc[:,:1]
            target_feature_test_arr = test_df.iloc[:,:1]


            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_arr)

            #Transforming input feature
            logging.info("Transforming input feature")
            input_feature_train_array = transformation_pipeline.transform(input_feature_train_arr)
            input_feature_test_array = transformation_pipeline.transform(input_feature_test_arr)


            train_arr = np.c_[input_feature_train_array, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_array, target_feature_test_arr]


            #Save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                           array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                           array=test_arr)

            utils.save_object(file_path=self.data_transformation_config.transform_object_path, 
                                           obj=transformation_pipeline)                   
  

            utils.save_object(file_path=self.data_transformation_config.label_encoder_path, 
                                           obj=label_encoder)


            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                label_encoder_path=self.data_transformation_config.label_encoder_path,
                )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact                            
        except Exception as e :
            raise MushroomException(e, sys)               