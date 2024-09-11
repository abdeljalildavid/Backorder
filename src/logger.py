from datetime import datetime
import os
import logging

log_file        = f"{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.log"
log_folder_path = os.path.join(os.getcwd(),"log")
log_file_path   = os.path.join(log_folder_path,log_file)

os.makedirs(log_folder_path, exist_ok=True)

logging.basicConfig(
    filename = log_file_path,
    format   = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)



