from bcp.process_states import ProcStates
from bcp.instruction_enum import InstrEnum
import random

class Process:

    pid = 0
    
    def __init__(self, instrs =10, instrs_list = [] ) -> None:
        self.pid = Process.pid
        Process.pid += 1
        #self.prioridade = 0
        self.estado = ProcStates.READY
        self.pc = 0
        self.user_name = None
        self.program_name = None
        #self.tempo = 0 #time since creation
        #self.tempo_ucp = 0 
        self.cpu_count = 0
        self.frames = 5
        
        self.instrs = instrs
        self.isloop = False
        self.prev_estado = None
        self.io_queue = False

        self.instr_list = []
        if not instrs_list:
            self._random_instr()

    def example_instr(self):
        
        instr = InstrEnum.CPU
        self.instr_list.append(instr)

        if self.instrs > 2:

            for i in range(0, self.instrs - 2):
        
                if self.pid == 0:
                    instr = InstrEnum.IO
                else: instr = InstrEnum.CPU

                self.instr_list.append(instr)

            instr = InstrEnum.CPU
            self.instr_list.append(instr)

        else:
            for i in range(0, self.instrs - 1):
                instr = InstrEnum.CPU
                self.instr_list.append(instr)


    def _random_instr(self):
        
        instr = InstrEnum.CPU
        self.instr_list.append(instr)

        if self.instrs > 2:
            for i in range(0, self.instrs - 2):                        
                if random.randint(0, 1) == 0:
                    instr = InstrEnum.CPU
                else:
                    instr = InstrEnum.IO
                self.instr_list.append(instr)                
            instr = InstrEnum.CPU
            self.instr_list.append(instr)
        else:
            for i in range(0, self.instrs - 1):
                instr = InstrEnum.CPU
                self.instr_list.append(instr)

    def get_instruction(self):
        return self.instr_list[self.pc]
        #increase pc here

    def reset(self):
        
        self.estado = ProcStates.READY
        self.pc = 0
        self.tempo = 0 
        self.tempo_ucp = 0 
        self.frames = 5
        