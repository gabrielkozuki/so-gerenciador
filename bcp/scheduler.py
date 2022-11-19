from bcp.process_states import ProcStates
from bcp.instruction_enum import InstrEnum
from bcp.scheduler_policies import Policies

class Scheduler:
    def __init__(self) -> None:
        self.queue = [] #?
        self.io_queue = []
        self.clock = 0
        self.is_cpu_free = True
        self.is_io_free = True
        self.finished = False
        self.running = False
        
        self.prev_cpu = None
        self.prev_io = None
        self.cur_cpu = None
        self.cur_io = None
        self.changed_procs= []

        #prob delete this line
        self.process_moved = False

        self.policy = Policies.FIFO
        self.is_preemptive = False
        self.multiprogramming = True
        
        
    def load_queue_from_list(self, proc_list):
        self.queue.extend(proc_list)
        
    #run (FIFO)
    def process(self): 
        if self.cur_cpu:
            self.state(self.cur_cpu)
        elif self.cur_io:
            self.state(self.cur_io)

        elif not self.cur_cpu:
            self.load_process()
    
    def step(self):        
        if self.clock == 0:
            self.load_process()
            
        elif self.cur_cpu:
            self.state(self.cur_cpu)

        elif self.cur_io:
            self.state(self.cur_io)

        self.clock +=1

    #step with multiprog
    def step_mult(self):
        
        
        if self.cur_io:
            
            self.state(self.cur_io)
        elif self.io_queue:
            self.load_io_from_queue()

        if self.is_cpu_free and self.queue:
                self.load_process()
        
        elif self.cur_cpu:
            self.state(self.cur_cpu)       
                  
        self.clock +=1

    def load_process(self):
        
        if self.queue[0] in self.changed_procs:            
            return

        process = self.queue.pop(0)
        self.state(process)
        self.process_moved = True

    def load_io_from_queue(self):
        process = self.io_queue.pop(0)
        self.state(process)
               
    def state(self, process):
        #change state
        process.prev_estado = process.estado

        if process.estado == ProcStates.READY:
            if process.get_instruction() == InstrEnum.CPU:
                self.run(process)
            elif process.get_instruction() == InstrEnum.IO and process.pc != 0:
                self.block(process)

        elif process.estado == ProcStates.RUNNING:
            if process.get_instruction() == InstrEnum.CPU:
                self.run(process)
            elif process.get_instruction() == InstrEnum.IO:
                self.block(process)
                self.cur_cpu = None
                self.is_cpu_free = True

        elif process.estado == ProcStates.BLOCKED:
            if process.get_instruction() == InstrEnum.CPU:
                if self.multiprogramming:
                    self.ready(process)
                    self.cur_io = None
                    self.is_io_free = True
                    self.changed_procs.append(process)
                else:
                    self.run(process)
                    self.cur_io = None
                    self.is_io_free = True
            else:
                self.block(process)

        if process.prev_estado != process.estado and process.estado != ProcStates.FINISHED:
            self.process_moved = True

    def ready(self, process):
        process.estado = ProcStates.READY
        self.queue.append(process)
        self.is_io_free = True
        self.prev_io = self.cur_io
                
    def run(self, process):
        if process.prev_estado == ProcStates.BLOCKED:
            self.queue.append(process) 
            process.estado = ProcStates.READY
            return
        process.cpu_count += 1
        process.pc += 1
        self.is_cpu_free = False
        process.estado = ProcStates.RUNNING
        self.cur_cpu = process


    def block(self, process):
        if process.prev_estado == ProcStates.RUNNING:
            if not self.is_io_free or self.io_queue:
                self.io_queue.append(process)
                process.io_queue = True
                process.estado = ProcStates.BLOCKED
                self.prev_cpu = process
                return
        elif process.io_queue:
            process.prev_estado = "ioqueue"
            process.io_queue = False
            
        process.pc += 1 #?
        self.is_io_free = False
        process.estado = ProcStates.BLOCKED
        self.cur_io = process

    def finish(self, process):
        if process.estado == ProcStates.RUNNING:
            self.is_cpu_free = True
        elif process.estado == ProcStates.BLOCKED:
            self.is_io_free = True
        process.prev_estado = process.estado
        process.estado = ProcStates.FINISHED
    
    def check_finish(self, proc_list):
        for process in proc_list:
            if not process: continue
            elif process.pc == process.instrs:
                self.finish(process)
                return True
        return False
        
    def clear_prev(self):
        self.prev_cpu = None
        self.prev_io = None
        self.changed_procs.clear()

    def reset(self):
        self.queue.clear()
        self.io_queue.clear()
        self.clock = 0
        self.is_cpu_free = True
        self.is_io_free = True
        
        self.prev_cpu = None
        self.prev_io = None
        self.cur_cpu = None
        self.cur_io = None
