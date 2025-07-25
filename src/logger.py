import logging      # Used for logging purposes
import os           # Used for file path operations, creating directories, etc.
from datetime import datetime   # Used for getting the current date and time

LOGS_DIR = "logs"                     # Directory where log files will be stored
os.makedirs(LOGS_DIR, exist_ok=True)  # Create the logs directory if it doesn't exist

LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")  # Log file path

logging.basicConfig(
    filename=LOG_FILE,  # Log file to write logs to
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format of the log messages
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format for the log messages
)

def get_logger(name):
    """
    Function to get a logger with the specified name.
    
    Args:
        name (str): Name of the logger.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)  # Get a logger with the specified name
    logger.setLevel(logging.INFO)  # Set the logging level to INFO for this logger
    return logger  # Return the configured logger instance