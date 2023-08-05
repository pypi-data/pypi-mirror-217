import inspect

class GeneratedNameError(Exception):
    def __init__(self):
        frame = inspect.currentframe().f_back
        line_number = frame.f_lineno
        filename = frame.f_code.co_filename
        line = inspect.getframeinfo(frame).code_context[0].strip()
        super().__init__(f"Error occurred at line {line_number}, line {line_number}: {line}")
        super().__init__(f"")