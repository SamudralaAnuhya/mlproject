import sys
import logging

def error_message_detail(error, error_details: sys):
    # Changed from error_details.exc_info() to sys.exc_info()
    _, _, exc_tb = sys.exc_info()  # Use sys.exc_info() directly
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = (
        "Error occurred in Python script name [{0}] at line number [{1}] with error message [{2}]"
        .format(file_name, exc_tb.tb_lineno, str(error))
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        # Pass sys module, not sys.exc_info()
        self.error_message = error_message_detail(error_message, error_details)
        
    def __str__(self):
        return self.error_message

