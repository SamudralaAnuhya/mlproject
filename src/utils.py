'''utils is used to handle the code for all modules'''

import numpy as np 
import pandas as pd 
import dill
import os
from src.exception import CustomException
import sys
sys.path.append(os.path.abspath('/Users/anuhyasamudrala/Documents/Anu_uncc/mlproject/src'))
import logging
from sklearn.metrics import  r2_score

def save_object(obj, file_path):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'wb') as f:
            dill.dump(obj, f) #create pickle file and save the object
            
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(X_train , y_train , X_test , y_test , models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            
            model.fit(X_train, y_train)  #training the model 
            y_train_pred = model.predict(X_train) #predicting the train data
            y_test_pred = model.predict(X_test) #predicting the test data
            
            train_model_score = r2_score(y_train, y_train_pred)  #r2 score for train data
            test_model_score = r2_score(y_test , y_test_pred)  #r2 score for test data
            
            report[list(models.keys())[i]] = test_model_score
            
            logging.info('model training is completed')  
        return report
    except Exception as e:
        raise CustomException(e,sys)