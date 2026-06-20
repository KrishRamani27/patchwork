from typing import TypedDict

class FixerState(TypedDict):
    task:str
    tests:str
    code:str
    result:str
    attempts:int