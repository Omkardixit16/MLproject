import sys
import os
import json
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
from src.db_config import get_db_connection


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join("artifacts","preprocessor.pkl")
            print("Before Loading" )
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            self.save_predictions_to_db(features, preds)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)

    def save_predictions_to_db(self, features, predictions):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            for feature, pred in zip(features.values, predictions):
                feature_json = json.dumps(feature.tolist())
                cursor.execute(
                    "INSERT INTO predictions (features, prediction_value) VALUES (%s, %s)",
                    (feature_json, pred)
                )
            conn.commit()
            cursor.close()
            conn.close()
        
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(  self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender

        self.race_ethnicity = race_ethnicity

        self.parental_level_of_education = parental_level_of_education

        self.lunch = lunch

        self.test_preparation_course = test_preparation_course

        self.reading_score = reading_score

        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)