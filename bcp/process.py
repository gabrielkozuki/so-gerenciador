from bcp.process_states import ProcStates

class Process:

    pid = 0

    def __init__(self) -> None:
        self.pid = Process.pid
        Process.pid += 1
        self.prioridade = 0
        self.estado = ProcStates.READY
        self.pc = 0
        self.tempo = 0
        self.tempo_ucp = 0
        self.frames = 5