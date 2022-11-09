from functools import partial
import os
import re
from tkinter import *
from tkinter import ttk
from bcp.pcb import ProcessTable

class View:
    
    def __init__(self, controller) -> None:
        self.controller = controller
        self.view_main()

    def logout(self):
        self.root.destroy()

    def msg_erro_senha(self):
        msg_senha_tela = Toplevel(self.main_tela)
        msg_senha_tela.title("Sucesso")
        msg_senha_tela.geometry("150x190")

        Label(msg_senha_tela, text = "Erro na senha").pack()
        Button(msg_senha_tela, text = "Ok", command= msg_senha_tela.destroy).pack()

    def msg_erro_usuario(self):
        msg_usuario_tela = Toplevel(self.main_tela)
        msg_usuario_tela.title("Sucesso")
        msg_usuario_tela.geometry("150x190")

        Label(msg_usuario_tela, text = "Erro na senha").pack()
        Button(msg_usuario_tela, text = "Ok", command= msg_usuario_tela.destroy).pack()

    def registrar_usuario_sucesso(self):
        self.usuario_entrada.delete(0, END)
        self.senha_entrada.delete(0, END)
        Label(self.registro_tela, text = "Cadastro realizado com sucesso", fg = "green", font = ("calibri", 11)).pack()

    def view_gerenciamento(self):
        gerenciamento_tela = Toplevel(self.main_tela)
        gerenciamento_tela.title("Info")
        #gerenciamento_tela.geometry("400x400")
        # Running the aforementioned command and saving its output
        output = os.popen('wmic process get description, processid, Name, Priority, WorkingSetSize').read()
        h_list = ["Description", "Name", "Priority", "ProcessId", "WorkingSetSize"]
        # Displaying the output
        print(output)
        
        self.lista_gerenciamento(gerenciamento_tela, h_list)
        splitoutput = [s for s in output.strip().splitlines(True) if s.strip()]
        splitoutput.pop(0)
        for line in splitoutput:
            word_list = re.split(r" {2,}", line)
            self.load_processes_data(word_list)

    
    def lista_gerenciamento(self, parent_w, h_list):

        self.idd = 0
        self.gtable_tree = ttk.Treeview(parent_w, show='headings')
        self.gtable_tree['columns'] = (h_list)
        
        self.gtable_tree.column("#0", width=0, stretch=NO)
        self.gtable_tree.heading("#0", text="", anchor=W)

        for heading in h_list:
            self.gtable_tree.column(heading, width=70, anchor=W)
            self.gtable_tree.heading(heading, text=heading, anchor=W)

        self.gtable_tree.pack(side="left", fill="both", expand=True)

        verscrlbar = ttk.Scrollbar(parent_w, orient ="vertical", command = self.gtable_tree.yview)
        verscrlbar.pack(side ='right', fill ='both')
        self.gtable_tree.configure(yscrollcommand = verscrlbar.set)

    def load_processes_data(self, line):
        self.gtable_tree.insert(parent='', index='end', iid=self.idd, text="", values=tuple(line))
        self.idd += 1

    def view_simulador_processos(self):
        self.simulador_tela = ProcessTable(self.main_tela)
            
    def view_dashboard(self):
        dashboard_tela = Toplevel(self.main_tela)
        dashboard_tela.title("Dashboard")
        dashboard_tela.geometry("400x400")
        Label(dashboard_tela, text = "Bem-vindo ao dashboard").pack()
        Button(dashboard_tela, text = "Verificar gerenciamente de memória", command = self.view_gerenciamento).pack()
        Button(dashboard_tela, text = "Simulador de processos", command = self.view_simulador_processos).pack()
        Button(dashboard_tela, text = "Sair", command= dashboard_tela.destroy).pack()

    def view_registrar(self):
        self.registro_tela = Toplevel(self.main_tela)
        self.registro_tela.title("Registrar")
        self.registro_tela.geometry("300x250")

        usuario = StringVar()
        senha = StringVar()
        
        Label(self.registro_tela, text = "Entre com os detalhes abaixo").pack()
        Label(self.registro_tela, text= "").pack()
        Label(self.registro_tela, text = "Usuário * ").pack()
        Label(self.registro_tela, text= "Senha *").pack()
        self.usuario_entrada = Entry(self.registro_tela, textvariable = usuario)
        self.usuario_entrada.pack()
        self.senha_entrada = Entry(self.registro_tela, textvariable = senha, show='*')
        self.senha_entrada.pack()
        Label(self.registro_tela, text = "").pack()
        Button(self.registro_tela, text = "Registro", width = 10, height= 1, command = lambda: self.controller.registrar_usuario(usuario.get(), senha.get())).pack()

    def view_login(self):
        login_tela = Toplevel(self.main_tela)
        login_tela.title("Login")
        login_tela.geometry("300x250")
        Label(login_tela, text = 'Por favor entre com as credenciais abaixo para logar').pack()
        Label(login_tela, text = "").pack()
        
        usuario_verificar = StringVar()
        senha_verificar = StringVar()

        Label(login_tela, text = "Usuário * ").pack()
        input_usuario = Entry(login_tela, textvariable= usuario_verificar)
        input_usuario.pack()
        Label(login_tela, text= "").pack()
        Label(login_tela, text = "Senha * ").pack()
        input_senha = Entry(login_tela, textvariable= senha_verificar, show='*')
        input_senha.pack()
        print("Login efetuado com sucesso!")
        Label(login_tela, text= "").pack()
        Button(login_tela, text = "Login", width= 10, height= 1, command= lambda: self.controller.login_verificar(usuario_verificar.get(), senha_verificar.get())).pack()  

    def view_main(self):
        self.main_tela = Tk()
        self.main_tela.geometry("300x250")
        self.main_tela.title("Gerenciador de Tarefas")

        Label(text = "Gerenciador de tarefas", bg = "grey", width= "300", height = "2", font = ("Calibri", 13)).pack()
        Label(text = "").pack()
        Button(text = "Login", height = "2", width="30", command = self.view_login).pack()
        Label(text = "").pack()
        Button(text = "Registre-se", height = "2", width = "30", command = self.view_registrar).pack()

    
    def mainloop(self):
        self.main_tela.mainloop()
