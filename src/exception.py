import sys
class BackOrderException(Exception):
    def __init__(self, error_message, error_detail:sys) -> None:
        super().__init__(error_message)
        self.error_message = f"Error occurred python script name {error_detail.exc_info()[2].tb_frame.f_code.co_filename} line number {error_detail.exc_info()[2].tb_frame.f_lineno} error message {error_message}"
    
    def __str__(self) -> str:
        return self.error_message