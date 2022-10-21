from logging import warning
from mailbox import mbox
from msilib.schema import Icon
import os
from tkinter import *
import tkinter

class View:
    
    def __init__(self) -> None:
        pass

    def logout(self):
        self.root.destroy()

    def msg_erro_senha():
        global msg_senha_tela

        msg_senha_tela = Toplevel(main_tela)
        msg_senha_tela.title("Sucesso")
        msg_senha_tela.geometry("150x190")

        Label(msg_senha_tela, text = "Erro na senha").pack()
        Button(msg_senha_tela, text = "Ok", command= msg_senha_tela.destroy).pack()

    def msg_erro_usuario():
        global msg_usuario_tela

        msg_usuario_tela = Toplevel(main_tela)
        msg_usuario_tela.title("Sucesso")
        msg_usuario_tela.geometry("150x190")

        Label(msg_usuario_tela, text = "Erro na senha").pack()
        Button(msg_usuario_tela, text = "Ok", command= msg_usuario_tela.destroy).pack()

    def view_gerenciamento():
        gerenciamento_tela = Toplevel(main_tela)
        gerenciamento_tela.title("Info")
        gerenciamento_tela.geometry("400x400")
        # Running the aforementioned command and saving its output
        output = os.popen('wmic process get description, processid').read()
    
        # Displaying the output
        print(output)
    
    def view_dashboard(self):
        dashboard_tela = Toplevel(main_tela)
        dashboard_tela.title("Dashboard")
        dashboard_tela.geometry("400x400")
        Label(dashboard_tela, text = "Bem-vindo ao dashboard").pack()
        Button(dashboard_tela, text = "Verificar gerenciamente de memória", command = self.view_gerenciamento).pack()
        Button(dashboard_tela, text = "Sair", command= dashboard_tela.destroy).pack()

    def view_registrar():
        global registro_tela
        registro_tela = Toplevel(main_tela)
        registro_tela.title("Registrar")
        registro_tela.geometry("300x250")

        global usuario
        global senha
        global usuario_entrada
        global senha_entrada
        usuario = StringVar()
        senha = StringVar()
        
        Label(registro_tela, text = "Entre com os detalhes abaixo").pack()
        Label(registro_tela, text= "").pack()
        Label(registro_tela, text = "Usuário * ").pack()
        usuario_entrada = Entry(registro_tela, textvariable = usuario)
        usuario_entrada.pack()
        Label(registro_tela, text= "Senha *").pack()
        senha_entrada = Entry(registro_tela, textvariable = senha, show='*')
        senha_entrada.pack()
        Label(registro_tela, text = "").pack()
        Button(registro_tela, text = "Registro", width = 10, height= 1, command = registrar_usuario).pack()

    def view_login():
        global login_tela

        login_tela = Toplevel(main_tela)
        login_tela.title("Login")
        login_tela.geometry("300x250")
        Label(login_tela, text = 'Por favor entre com as credenciais abaixo para logar').pack()
        Label(login_tela, text = "").pack()
        
        global usuario_verificar
        global senha_verificar
        
        usuario_verificar = StringVar()
        senha_verificar = StringVar()
        
        global input_usuario
        global input_senha
            
        Label(login_tela, text = "Usuário * ").pack()
        input_usuario = Entry(login_tela, textvariable= usuario_verificar)
        input_usuario.pack()
        Label(login_tela, text= "").pack()
        Label(login_tela, text = "Senha * ").pack()
        input_senha = Entry(login_tela, textvariable= senha_verificar, show='*')
        input_senha.pack()
        print("Login efetuado com sucesso!")
        Label(login_tela, text= "").pack()
        Button(login_tela, text = "Login", width= 10, height= 1, command= login_verificar).pack()  

    def view_main(self):
        global main_tela

        main_tela = Tk()
        main_tela.geometry("300x250")
        main_tela.title("Gerenciador de Tarefas")

        Label(text = "Gerenciador de tarefas", bg = "grey", width= "300", height = "2", font = ("Calibri", 13)).pack()
        Label(text = "").pack()
        Button(text = "Login", height = "2", width="30", command = self.view_login).pack()
        Label(text = "").pack()
        Button(text = "Registre-se", height = "2", width = "30", command = self.view_registrar).pack()
