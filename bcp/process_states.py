from enum import Enum

class ProcStates(Enum):
    READY = 0
    RUNNING = 1
    BLOCKED = 2 #i/o
    FINISHED = 3