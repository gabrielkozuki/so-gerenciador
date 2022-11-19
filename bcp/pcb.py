from tkinter import *
from tkinter import ttk
import os.path
from bcp.process import Process
from bcp.process_states import ProcStates
from bcp.process_states import translate
from bcp.view_scheduler import ViewSched
import random

class ProcessTable:
    def __init__(self, main_tela, control) -> None:
        
        self.control = control
        self.process_list = []

        self.window = Toplevel(main_tela)
        self.window.title("Lista de processos")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.b_frame = Frame(self.window)
        self.b_frame.pack(anchor=CENTER)

        self.button_create = Button(self.b_frame, text="Criar processo", command=self.create_process)
        self.button_create.grid(rowspan=2, row=0, column=0, padx=5, sticky=NSEW)

        self.button_create = Button(self.b_frame, text="Run", command=self.control.criar_process_sim)
        self.button_create.grid(rowspan=2, row=0, column=2, padx=5, sticky=NSEW)
        
        self.priority_label = Label(self.b_frame, text="# instruções")
        self.priority_label.grid(row=0, column=1)
        
        self.current_value = StringVar(value=1)
        self.spinbox = ttk.Spinbox(self.b_frame, from_=1, to=50, textvariable=self.current_value, wrap=True, width=3)
        self.spinbox.grid(row=1, column=1)

        # self.priority_label = Label(self.b_frame, text="Prioridade")
        # self.priority_label.grid(row=0, column=1)
        
        # self.current_value = StringVar(value=0)
        # self.spinbox = ttk.Spinbox(self.b_frame, from_=0, to=10, textvariable=self.current_value, wrap=True, width=3)
        # self.spinbox.grid(row=1, column=1)
        
        self.frame = LabelFrame(self.window, text="Lista de processos")
        self.frame.pack(anchor=CENTER, fill="both")

        self.create_process_table()
    
    def create_process_table(self):

        self.idd = 0
        self.table_tree = ttk.Treeview(self.frame, show='headings')
        self.table_tree['columns'] = ("PID", "Estado", "PC", "Usuario", "Programa", "%CPU", "RAM")
               
        self.table_tree.column("#0", width=0, stretch=NO)
        self.table_tree.column("PID", width=70, anchor=W)
        self.table_tree.column("Estado", width=100, anchor=W)
        #self.table_tree.column("Prioridade", width=70, anchor=W)
        self.table_tree.column("PC", width=70, anchor=W)
        self.table_tree.column("Usuario", width=70, anchor=W)
        self.table_tree.column("Programa", width=70, anchor=W)
        self.table_tree.column("%CPU", width=70, anchor=W)
        self.table_tree.column("RAM", width=70, anchor=W)

        self.table_tree.heading("#0", text="", anchor=W)
        self.table_tree.heading("PID", text="PID", anchor=W)
        self.table_tree.heading("Estado", text="Estado", anchor=W)
        #self.table_tree.heading("Prioridade", text="Prioridade", anchor=W)
        self.table_tree.heading("PC", text="PC", anchor=W)
        self.table_tree.heading("Usuario", text="Usuario", anchor=W)
        self.table_tree.heading("Programa", text="Programa", anchor=W)
        self.table_tree.heading("%CPU", text="%CPU", anchor=W)
        self.table_tree.heading("RAM", text="RAM(pages)", anchor=W)

        self.table_tree.pack(side="left", fill="both")

        verscrlbar = ttk.Scrollbar(self.frame, orient ="vertical", command = self.table_tree.yview)
        verscrlbar.pack(side ='right', fill ='both')
        self.table_tree.configure(yscrollcommand = verscrlbar.set)

    def create_process_sim(self):
        view_sched = ViewSched(self.window)

    def create_process(self):
        numero_de_instr = int(self.spinbox.get())
        new_process = Process(instrs = numero_de_instr)
        new_process.user_name = self.control.get_current_user()
        new_process.program_name = self.give_random_name()
        
        self.add_process(new_process)

    def give_random_name(self):
        file = open(self.resourcePath("bcp\\fake_program_names"))
        name_list = file.read().splitlines()
        return random.choice(name_list)

    def add_process(self, new_process):
        self.process_list.append(new_process)

        value_list = list(new_process.__dict__.values())
        value_list[1] = translate(new_process.estado)
        
        self.table_tree.insert(parent='', index='end', iid=self.idd, text="", values=tuple(value_list))
        self.idd += 1

    def is_process_list_empty(self):
        if not self.process_list:
            return True
        else:
            return False

    def is_process_list_finished(self):
        for process in self.process_list:
            if process.estado != ProcStates.FINISHED:
                return False

        return True

    def update_process_list(self):
        for process in self.process_list:
            item = self.get_item_from_pid(process)
                    
            value_list = list(process.__dict__.values())
            value_list[1] = translate(process.estado)
            if self.control.get_clock_time():
                value_list[5] = int((process.cpu_count/self.control.get_clock_time()) * 100)
            else: value_list[5] = 0

            
            self.table_tree.item(item, values=tuple(value_list))

    def get_item_from_pid(self, process):
        for item in self.table_tree.get_children():
            if process.pid == self.table_tree.item(item)["values"][0]:
                return item

        return None

    def reset(self):
        for process in self.process_list:
            process.reset()

    def on_closing(self):
        Process.pid = 0
        self.control.processos_table = None
        self.window.destroy()

    def resourcePath(self, relativePath):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            basePath = sys._MEIPASS
        except Exception:
            basePath = os.path.abspath(".")

        return os.path.join(basePath, relativePath)