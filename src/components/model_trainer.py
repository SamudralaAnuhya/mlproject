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
            logging.info(f'before evaluating model')
            X_train , y_train ,X_test , y_test = (
                train_array[:, :-1],   #all the rows and all the columns except the last column(target column)
                train_array[:,-1], #traget column in train
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            model = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                # "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            params={
                 "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                # "XGBRegressor":{
                #     'learning_rate':[.1,.01,.05,.001],
                #     'n_estimators': [8,16,32,64,128,256]
                # },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            
            model_report = evaluate_model(X_train = X_train,y_train = y_train,X_test= X_test, y_test =y_test, models = model , param = params)
            
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
        