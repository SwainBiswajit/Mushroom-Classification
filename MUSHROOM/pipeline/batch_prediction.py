from MUSHROOM.exception import MushroomException
from MUSHROOM.logger import logging
from MUSHROOM.predictor import ModelResolver
from MUSHROOM.utils import load_object
import numpy as np
import pandas as pd
from datetime import datetime
import os, sys

PREDICTION_DIR = "prediction"

def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info(f"Creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading file :{input_file_path}")
        df = pd.read_csv(input_file_path)
        
        logging.info(f"Loading label encoder to encode dataset")
        label_encoder = load_object(file_path=model_resolver.get_latest_label_encoder_path())
        for column in df.columns:
            df[column] = label_encoder.fit_transform(df[column])


        logging.info(f"Loading transformer to transform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
        input_feature_names =  list(transformer.feature_names_in_)
        input_arr = transformer.transform(df[input_feature_names])

        logging.info(f"Loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)
        
        prediction = prediction.astype('int')
        cat_prediction = label_encoder.inverse_transform(prediction)
        
        df["prediction"]=prediction
        df["cat_pred"]=cat_prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".data",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path
    except Exception as e:
        raise MushroomException(e, sys)