from enum import Enum

class ProcStates(Enum):
    READY = 0
    RUNNING = 1
    BLOCKED = 2 #i/o
    FINISHED = 3

def translate(state):
    str_state = ""
    match state:
        case ProcStates.READY:
            str_state = "Pronto"
        case ProcStates.RUNNING:
            str_state = "Execução"
        case ProcStates.BLOCKED:
            str_state = "Espera"
        case ProcStates.FINISHED:
            str_state = "Concluído"
    
    return str_state


