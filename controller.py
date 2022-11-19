from usuario import Usuario
from view import View
from bcp.scheduler import Scheduler
from bcp.view_scheduler import ViewSched
from bcp.pcb import ProcessTable
from tkinter import *
from tkinter import messagebox
from bcp.process_states import ProcStates
from bcp.process_states import translate

class Controller:

    def __init__(self) -> None:
        self.usuario = Usuario()
        self.view = View(self)
        self.scheduler = None
        self.view_sched = None
        self.processos_table = None

        self.view.mainloop()

    def registrar_usuario(self, usuario, senha):
        msg = self.usuario.registrar_usuario(usuario, senha)
        if msg == 'err_user':
            self.view.popupMensagem("Este nome de usuário já existe.")
        else:
            self.view.usuario_entrada.delete(0, END)
            self.view.senha_entrada.delete(0, END)
            self.view.popupMensagem("Cadastro efetuado com sucesso.")


    def login_verificar(self, usuario, senha):
        res = self.usuario.login_verificar(usuario=usuario, senha=senha)

        if res == 'dashboard':
            self.view.login_tela.destroy()
            self.view.view_dashboard()
        elif res == 'err_login':
            self.view.popupMensagem("Credenciais incorretas.")            
        
    def criar_tela_processos(self):
        if not self.processos_table:
            self.processos_table = ProcessTable(self.view.main_tela, self)

    def criar_process_sim(self):

        if self.processos_table.is_process_list_empty():
            messagebox.showwarning(title=None, message="Lista de processos vazia. Necessário ao menos um processo")
            return

        self.scheduler = Scheduler()
        self.scheduler.load_queue_from_list(self.processos_table.process_list)

        self.criar_sched_view()
        self.view_sched.window.grab_set() 

    def criar_sched_view(self):
        self.view_sched = ViewSched(self.view.main_tela, self)
        self.view_sched.load_process_list(self.scheduler.queue, ProcStates.READY)

    def scheduler_step(self):
        
        if self.processos_table.is_process_list_finished():
            self.scheduler.finished = True
            messagebox.showinfo(title=None, message="Processos concluídos")
            return
        self.scheduler.step_mult()

        proc_list = [self.scheduler.cur_cpu, self.scheduler.cur_io, self.scheduler.prev_cpu, self.scheduler.prev_io]

        self.view_sched.update(self.scheduler.process_moved , proc_list)
        if self.scheduler.process_moved:
            self.scheduler.process_moved = False

        self.check_finish(proc_list)

        self.processos_table.update_process_list()

        self.scheduler.clear_prev()

    def check_finish(self, proc_list):
        
        if self.scheduler.check_finish(proc_list):
            proc_list = [p for p in proc_list if p if p.estado == ProcStates.FINISHED]                    
            self.view_sched.update(self.scheduler.process_moved , proc_list)
            if self.scheduler.process_moved:
                self.scheduler.process_moved = False

    def scheduler_reset(self):
        
        self.processos_table.reset()
        self.scheduler.reset()
        self.scheduler.finished = False
        self.scheduler.running = False
        self.view_sched.clear()
        self.processos_table.update_process_list()

        self.scheduler.load_queue_from_list(self.processos_table.process_list)
        self.view_sched.load_process_list(self.scheduler.queue, ProcStates.READY)

    def scheduler_run(self):
                
        self.scheduler_step()
        
        if not self.scheduler.finished and self.scheduler.running:
            self.view.main_tela.after(500, self.scheduler_run )
        
    def get_clock_time(self):
        return self.scheduler.clock

    def get_current_user(self):
        return self.usuario.get_username()

    def view_sched_on_closing(self):
        self.scheduler_reset()
        self.view_sched.window.destroy()

    



