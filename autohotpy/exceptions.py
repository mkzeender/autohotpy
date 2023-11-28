class AhkError(Exception):
    pass

class AhkRuntimeError(AhkError):
    def __init__(self, err, *args: object) -> None:
        super().__init__(*args)
        
    
class ExitApp(SystemExit):
    def __init__(self, reason:str, code:int, *args: object) -> None:
        super().__init__(code, *args)
        self.reason = reason

    def __str__(self) -> str:
        return f'Exit Code: {self.code}, Reason: {self.reason}'