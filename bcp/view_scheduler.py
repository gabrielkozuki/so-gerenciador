from tkinter import *
from tkinter import ttk
from bcp.process_states import ProcStates
from bcp.process_states import translate
from enum import Enum



class ProcHeadings(Enum):
    PID = 0
    Estado = 1
    PC = 2    

class ViewSched:
    def __init__(self, main_tela, control) -> None:
        self.control = control
        self.window = Toplevel(main_tela)
        self.window.title("processos")

        self.window.protocol("WM_DELETE_WINDOW", self.control.view_sched_on_closing)
        
        self.b_frame = Frame(self.window)
        self.b_frame.grid(columnspan=3, row=0 ) 
      
        self.step_button = Button(self.b_frame, text="step", command=self.step_command)
        self.step_button.grid(rowspan=2, row=0, column=0, padx=5, sticky=NSEW)

        self.reset_button = Button(self.b_frame, text="reset", command=self.reset_command)
        self.reset_button.grid(rowspan=1, row=0, column=1, padx=5, sticky=NSEW)

        self.reset_button = Button(self.b_frame, text="run", command=self.run_command)
        self.reset_button.grid(rowspan=1, row=0, column=2, padx=5, sticky=NSEW)
        
        self.clock_label = Label(self.b_frame, text="Clock")
        self.clock_label.grid(rowspan=1, row=0, column=3, padx=5, sticky=NSEW)

        self.clock_data_label = Label(self.b_frame, text=str(self.control.get_clock_time()))
        self.clock_data_label.grid(rowspan=1, row=0, column=4, padx=2, sticky=NSEW)
        
        self.frame_p = LabelFrame(self.window, text="Pronto")
        self.frame_p.grid(row=1, column=0)

        self.frame_esq = LabelFrame(self.window, text="Fila Espera")
        self.frame_esq.grid(row=1, column=1)

        self.frame_e = LabelFrame(self.window, text="Execução")
        self.frame_e.grid(row=2, column=0)

        self.frame_es = LabelFrame(self.window, text="Espera")
        self.frame_es.grid(row=2, column=1)

        self.tables = {}
        self.idds = {}

        self.create_run_table(self.frame_p, ProcStates.READY)
        self.create_run_table(self.frame_e,ProcStates.RUNNING)
        self.create_run_table(self.frame_es,ProcStates.BLOCKED)
        self.create_run_table(self.frame_esq, "ioqueue")
    
    def create_run_table(self, frame, name):
        
        self.idds[name] = 0
        self.tables[name] = ttk.Treeview(frame, show='headings')
        self.tables[name]['columns'] = ("PID", "Estado", "PC")
               
        self.tables[name].column("#0", width=0, stretch=NO)
        self.tables[name].column("PID", width=70, anchor=W)
        self.tables[name].column("Estado", width=100, anchor=W)
        self.tables[name].column("PC", width=70, anchor=W)
        
        self.tables[name].heading("#0", text="", anchor=W)
        self.tables[name].heading("PID", text="PID", anchor=W)
        self.tables[name].heading("Estado", text="Estado", anchor=W)
        self.tables[name].heading("PC", text="PC", anchor=W)
        
        self.tables[name].pack(side="left", fill="both")

        verscrlbar = ttk.Scrollbar(frame, orient ="vertical", command = self.tables[name].yview)
        verscrlbar.pack(side ='right', fill ='both')
        self.tables[name].configure(yscrollcommand = verscrlbar.set)

    def load_process_list(self, process_list, list_name):
        for process in process_list:
            self.add_process(process, list_name)

    def add_process(self, new_process, list_name):
        value_list = [new_process.pid, translate(new_process.estado), new_process.pc]
        self.tables[list_name].insert(parent='', index='end', iid=self.idds[list_name], text="", values=tuple(value_list))
        self.idds[list_name] += 1
    
    def step_command(self):
        self.control.scheduler.running = False
        self.control.scheduler_step()

    def reset_command(self):
        self.control.scheduler_reset()
    
    def run_command(self):
        if self.control.scheduler.running:
            return
        self.control.scheduler.running = True
        self.control.scheduler_run()
        
    def update(self, process_moved, proc_list):
        #clock update
        self.clock_data_label.configure(text=str(self.control.get_clock_time()))
        
        for process in proc_list:
            if not process:
                continue
            if process.estado != process.prev_estado and process.estado != ProcStates.FINISHED:
                
                if process.prev_estado == ProcStates.READY:            
                    self.remove_entry_from_ready(process)
                elif process.prev_estado == ProcStates.RUNNING:            
                    self.remove_entry_from_exec(process)
                elif process.prev_estado == "ioqueue":            
                    self.remove_entry_from_block_queue(process)
                elif process.prev_estado == ProcStates.BLOCKED:            
                    self.remove_entry_from_block(process)

                if process.estado == ProcStates.RUNNING:
                    self.add_process(process, ProcStates.RUNNING)
                elif process.estado == ProcStates.BLOCKED and process.io_queue:            
                    self.add_process(process, "ioqueue")
                elif process.estado == ProcStates.BLOCKED:
                    self.add_process(process, ProcStates.BLOCKED)
                elif process.estado == ProcStates.READY:
                    self.add_process(process, ProcStates.READY)
        
        self.update_entries(proc_list)

    def update_entries(self, process_list):
        for process in process_list:
            if not process or process.prev_estado == ProcStates.FINISHED:
                continue

            state = process.estado
            if state == ProcStates.FINISHED:
                state = process.prev_estado
            elif state == ProcStates.BLOCKED and process.io_queue:
                state = "ioqueue"

            item = self.get_item_from_pid(process, state)
            if item:
                value_list = [process.pid, translate(process.estado) , process.pc]
                self.tables[state].item(item, values=tuple(value_list))

    def get_item_from_pid(self, process, list_name):
        for item in self.tables[list_name].get_children():
            if process.pid == self.tables[list_name].item(item)["values"][0]:
                return item

        return None

    def get_item_from_pid_t(self, process):
        for table in self.tables.value():
            for item in table.get_children():
                if process.pid == self.table.item(item)["values"][0]:
                    return item

        return None

    def remove_entry_from_ready(self, process):
        item = self.get_item_from_pid(process, ProcStates.READY)
        if item:
            self.tables[ProcStates.READY].delete(item)
        
    def remove_entry_from_exec(self, process):
        item = self.get_item_from_pid(process, ProcStates.RUNNING)
        if item:
            self.tables[ProcStates.RUNNING].delete(item)
            
    def remove_entry_from_block(self, process):
        item = self.get_item_from_pid(process, ProcStates.BLOCKED)
        if item:
            self.tables[ProcStates.BLOCKED].delete(item)
        
    def remove_entry_from_block_queue(self, process):
        item = self.get_item_from_pid(process, "ioqueue")
        if item:
            self.tables["ioqueue"].delete(item)
        
    def translate_header_enum(self, enum):
        match enum:
            case ProcHeadings.PID:
                return "pid"
    
    def clear(self):
        self.clock_data_label.configure(text=str(self.control.get_clock_time()))
        for table in self.tables.values():
            for item in table.get_children():
                table.delete(item)
