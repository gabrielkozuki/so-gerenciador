from tkinter import *
from tkinter import ttk
from bcp.process import Process
from bcp.process_states import ProcStates

class ProcessTable:
    def __init__(self, main_tela) -> None:
        self.window = Toplevel(main_tela)
        self.window.title("Lista de processos")

        self.b_frame = Frame(self.window)
        self.b_frame.pack(anchor=CENTER)

        self.button_create = Button(self.b_frame, text="Criar processo", command=self.create_process)
        self.button_create.grid(rowspan=2, row=0, column=0, padx=5, sticky=NSEW)
        
        self.priority_label = Label(self.b_frame, text="Prioridade")
        self.priority_label.grid(row=0, column=1)
        
        self.current_value = StringVar(value=0)
        self.spinbox = ttk.Spinbox(self.b_frame, from_=0, to=10, textvariable=self.current_value, wrap=True, width=3)
        self.spinbox.grid(row=1, column=1)
        
        self.frame = LabelFrame(self.window, text="Lista de processos")
        self.frame.pack(anchor=CENTER, fill="both")

        self.create_process_table()
    
    def create_process_table(self):

        self.idd = 0
        self.table_tree = ttk.Treeview(self.frame, show='headings')
        self.table_tree['columns'] = ("PID", "Prioridade", "Estado", "PC", "Tempo", "Tempo UCP", "Frames")
               
        self.table_tree.column("#0", width=0, stretch=NO)
        self.table_tree.column("PID", width=70, anchor=W)
        self.table_tree.column("Estado", width=100, anchor=W)
        self.table_tree.column("Prioridade", width=70, anchor=W)
        self.table_tree.column("PC", width=70, anchor=W)
        self.table_tree.column("Tempo", width=70, anchor=W)
        self.table_tree.column("Tempo UCP", width=70, anchor=W)
        self.table_tree.column("Frames", width=70, anchor=W)

        self.table_tree.heading("#0", text="", anchor=W)
        self.table_tree.heading("PID", text="PID", anchor=W)
        self.table_tree.heading("Estado", text="Estado", anchor=W)
        self.table_tree.heading("Prioridade", text="Prioridade", anchor=W)
        self.table_tree.heading("PC", text="PC", anchor=W)
        self.table_tree.heading("Tempo", text="Tempo", anchor=W)
        self.table_tree.heading("Tempo UCP", text="Tempo UCP", anchor=W)
        self.table_tree.heading("Frames", text="Frames", anchor=W)

        self.table_tree.pack(side="left", fill="both")

        verscrlbar = ttk.Scrollbar(self.frame, orient ="vertical", command = self.table_tree.yview)
        verscrlbar.pack(side ='right', fill ='both')
        self.table_tree.configure(xscrollcommand = verscrlbar.set)

    def create_process(self):
        new_process = Process()
        new_process.prioridade = self.spinbox.get()
        
        
        self.add_process(new_process)

    def add_process(self, new_process):
        value_list = list(new_process.__dict__.values())
        value_list[2] = self.translate_state(new_process.estado)

        self.table_tree.insert(parent='', index='end', iid=self.idd, text="", values=tuple(value_list))
        self.idd += 1

    def translate_state(self, state):
        str_state = ""
        match state:
            case ProcStates.READY:
                str_state = "ready"
            case ProcStates.RUNNING:
                str_state = "running"
            case ProcStates.BLOCKED:
                str_state = "blocked"
            case ProcStates.FINISHED:
                str_state = "finished"
        
        return str_state