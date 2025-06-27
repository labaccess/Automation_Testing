# custom_exceptions.py

class StepFailedError(Exception):
    """Raised when a step fails in Robot Framework"""
    def __init__(self, step_name, message="Step failed"):
        self.step_name = step_name
        self.message = f"{message}: {step_name}"
        super().__init__(self.message)

class LoginTimeoutError(Exception):
    """Raised when login takes too long"""
    pass

