'''utils is used to handle the code for all modules'''

import numpy as np 
import pandas as pd 
import dill
import os
from exception import CustomException

def save_object(obj, file_path):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'wb') as f:
            dill.dump(obj, f) #create pickle file and save the object
            
    except Exception as e:
        pass