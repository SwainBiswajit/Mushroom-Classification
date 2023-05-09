from MUSHROOM.entity import config_entity,artifact_entity
from MUSHROOM import utils
from MUSHROOM.exception import MushroomException
from MUSHROOM.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os,sys


class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} DATA VALIDATION {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e :
            raise MushroomException(e, sys)

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report=dict()

            base_columns = base_df.columns
            current_columns = current_df.columns
            
            for base_column in base_columns:
                base_data,current_data = base_df[base_column],current_df[base_column]
                #Null hypothesis is that both column data drawn from same distribution
                logging.info(f"Hypothesis {base_column} : {base_data.dtype} , {current_data.dtype}")
                same_distribution = ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    #We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":same_distribution.pvalue,
                        "Same_distribution":True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":same_distribution.pvalue,
                        "Same_distribution":False
                    }
                    #Different distribution
            
            self.validation_error[report_key_name]=drift_report        

        except Exception as e :
            raise MushroomException(e, sys)


    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info('Reading base dataframe')
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            
            logging.info('Reading train dataframe')
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info('Reading test dataframe')
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            logging.info('Detecting data drift in train dataset')
            self.data_drift(base_df=base_df, current_df=train_df, report_key_name='Data_drift_train_dataset')
            logging.info('Detecting data drift in test dataset')
            self.data_drift(base_df=base_df, current_df=test_df, report_key_name='Data_drift_test_dataset')
            
            #Write the report
            logging.info('Write the report in yaml file')
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            logging.info(f'Data Validation artifact : {data_validation_artifact}')
            return data_validation_artifact
        except Exception as e :
            raise MushroomException(e, sys)        