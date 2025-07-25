"""
Why do we perform Custom Exception Handling?
Custom exceptions allow us to handle errors in a more controlled and informative way, providing detailed context about
the error, such as the file name and line number where it occurred. This is particularly useful in larger applications where 
understanding the source of an error quickly can save time and effort in debugging.

Also we don't get issues in the terminal. We get all the information in the log file itself.

Logging and CustomException handling are crucial for maintaining rhe record of errors, their time and when the programmer fixed them.
"""

from src.logger import get_logger  
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide_numbers(num1, num2):
    try:
        result = num1 / num2
        logger.info(f"Division of 2 numbers")
        return result
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise CustomException("Custom Zero Error", sys) # type: ignore

if __name__ == "__main__":
    try:
        logger.info("Starting the main program")
        divide_numbers(10,2)
    except CustomException as ce:
        logger.error(str(ce))

