''' model trainer is a class that trains a model on a dataset and saves the model to a file '''

import os 
import sys
from dataclasses import dataclass
import numpy as np 

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor , GradientBoostingRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object , evaluate_model


@dataclass
class ModelTrainerconfig:
    trained_model_file:str = os.path.join('artifacts','trained_model.pkl')  #pickle file to save the trained model
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerconfig()
        
        
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info('splitting training and testing data')
            # train_array = np.array(train_array)
            # test_array = np.array(test_array)
            
            # logging.info(f'train_array type: {type(train_array)}, shape: {train_array.shape}')
            # logging.info(f'test_array type: {type(test_array)}, shape: {test_array.shape}')

            logging.info(f'before evaluating model')
            X_train , y_train ,X_test , y_test = (
                train_array[:, :-1],   #all the rows and all the columns except the last column(target column)
                train_array[:,-1], #traget column in train
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            model = {
                'LinearRegression':LinearRegression(),
                'RandomForestRegressor':RandomForestRegressor(),
                'GradientBoostingRegressor':GradientBoostingRegressor(),
                'AdaBoostRegressor':AdaBoostRegressor(),
                'DecisionTreeRegressor':DecisionTreeRegressor(),
                'KNeighborsRegressor':KNeighborsRegressor(),
                'CatBoostRegressor':CatBoostRegressor(verbose=False),
                'XGBClassifier':XGBRegressor()
            }
            
            model_report = evaluate_model(X_train = X_train,y_train = y_train,X_test= X_test, y_test =y_test, models = model)
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = model[best_model_name]
            
            if best_model_score < 0.7:
                logging.info('no model found')
            logging.info('best model selected on training and test')
            
            save_object(
                file_path = self.model_trainer_config.trained_model_file,
                obj = best_model
            )
            
            prediction = best_model.predict(X_test)
            r2_square = r2_score(y_test,prediction)
            logging.info(f'r2 score of the model is {r2_square}')
            return r2_square
        
        
                
        except Exception as e:
            raise CustomException(e, sys)
        