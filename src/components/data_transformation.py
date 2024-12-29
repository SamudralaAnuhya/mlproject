''' data transformation is to transform the data from the raw data to the data that can be used for the model training ]
one _hot_encoding is to convert the categorical data to numerical data
normalize is to normalize the data to make the data in the same scale'''


import sys
import os
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer   #handle missing values 
# sys.path.append(os.path.abspath('/Users/anuhyasamudrala/Documents/Anu_uncc/mlproject/src'))
from src.exception import CustomException
import logging

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str=os.path.join('artifacts','preprocessor.pkl')  #pickle file to save the preprocessor object

class DataTransformation:
    def __init__(self):
        logging.info('Data Transformation Started')
        self.transformation_config = DataTransformationConfig()
    
    def get_transformer_object(self):   #handilind data normalization and one hot encoding and missing values
        try:
            numeric_features = ['reading_score','writing_score']
            categorical_features = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']
            
            numeric_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),  #fill the missing numerical values with median
                    ('scaler',StandardScaler(with_mean=False))  #standardize the data
                ])
            logging.info('numeric transformer created')
            categorical_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),  #fill the missing categorical values with most_frequent(mode vales)
                    ('One_hot_encoder',OneHotEncoder()) , #change the categorical data to numerical data
                    ('scaler',StandardScaler(with_mean=False))  #standardize the data (normalize as mean  and std 1 )      
                ])
            logging.info('categorical transformer created')
            preprocessor  = ColumnTransformer(
                [
                   ('numeric',numeric_pipeline,numeric_features),
                   ('categorical',categorical_pipeline,categorical_features)
                ])
            logging.info('preprocessor object created')
        
            return preprocessor  
        
        except Exception as e:
            raise CustomException(e,sys)
        
        
        
    def initiate_data_transformation(self , train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            preprocessor_obj = self.get_transformer_object()
            
            target_column_name = 'math_score'
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis =1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name],axis =1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info('appliying preproser on the train data')
            input_feature_train = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test = preprocessor_obj.transform(input_feature_test_df)
            
            train_array = np.c_[input_feature_train,np.array(target_feature_train_df)]
            test_array = np.c_[input_feature_test,np.array(target_feature_test_df)]
            
            logging.info('saved preprocessor object')
            
            save_object(
                file_path = self.transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
            
            return(
                train_array,
                test_array,
                self.transformation_config.preprocessor_obj_file_path
            )
  
        except Exception as e:
            raise CustomException(e,sys)