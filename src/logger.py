'''any excution happens it should colelct the logs and store it in the file'''

import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"  # log file for each second
logs_path = os.path.join(os.getcwd(), "logs" , LOG_FILE)  # path to store logs
os.makedirs(logs_path, exist_ok=True)  # create logs directory if not exists

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)  # path to store logs
logging.basicConfig(filename=LOG_FILE_PATH, 
                    format  = "[ %(asctime)s ]  %(lineno)d  %(filename)s  -  %(levelname)s -  %(message)s ", 
                    level=logging.INFO
                    )  # logging configuration

