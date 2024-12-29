'''data ingestion is to ingest the data from the source to the data pipeline
import data from the database or from the file'''

import os 
import sys
sys.path.append(os.path.abspath('/Users/anuhyasamudrala/Documents/Anu_uncc/mlproject/src'))
import pandas as pd
import logging
from exception import CustomException
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from components.data_transformation import DataTransformation
from components.data_transformation import DataTransformationConfig

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts','train.csv')  #create artifact folder and save the train.csv file
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','data.csv')
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info('Data Ingestion Started')
        
        try:
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('reading the dataset as dataframe')
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info('test and train split initiated')
            
            train_set , test_set = train_test_split(df,test_size=0.2,random_state=42) #split the data into train and test
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info('train and test data saved in the artifacts folder')  
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )          

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == '__main__':
    obj = DataIngestion()
    train_data , test_data = obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation()   #all the data validation help in this file like normalization and fit/fit_tranform data(columntranforer.fit_transfor)
    
    data_transformation.initiate_data_transformation(train_data, test_data)
    
    
    
        
            
            
    
    
    


