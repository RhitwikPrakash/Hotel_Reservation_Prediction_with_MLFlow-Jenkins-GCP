import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_details: Exception):  # Removed "sys" type annotation
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message)

    @staticmethod
    def get_detailed_error_message(error_message) -> str:
        _, _, exc_tb = traceback.sys.exc_info() # type: ignore
        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            return f"Error occurred in {file_name} at line number: {line_number} : {error_message}"
        else:
            return f"Error occurred: {error_message}"

    def __str__(self):
        return self.error_message