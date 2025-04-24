import logging
import time
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("cpy-errors.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) 

def connect_to_mysql(config, attempts=3, delay=2):
    attempt = 1
    
    while attempt < attempts + 1:
        try:
            return mysql.connector.connect(**config)
        except (mysql.connector.Error, IOError) as err:
            if (attempts is attempt):
            
                logger.info("Failed to connect, exiting without a connection: %s", err)
                return None
            logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err,
                attempt,
                attempts-1,
            )
            
            time.sleep(delay ** attempt)
            attempt += 1
    return None

user = os.getenv('DB_USER')
host = os.getenv('DB_HOST')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

config = {
    'user':user,
    'password':password,
    'host':host,
    'database':db_name,
    'raise_on_warnings':True,
}

cnx = connect_to_mysql(config)