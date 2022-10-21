from logging import warning
from mailbox import mbox
from msilib.schema import Icon
import os
from tkinter import *
import tkinter

def deletar2():
    tela3.destroy()
    
def deletar3():
    tela4.destroy()
    
def deletar4():
    tela5.destroy()

def logout(self):
    self.root.destroy()
    
def gerenciamento_de_memoria():
    tela9 = Toplevel(tela)
    tela9.title("Info")
    tela9.geometry("400x400")
    # Running the aforementioned command and saving its output
    output = os.popen('wmic process get description, processid').read()
 
    # Displaying the output
    print(output)
    
def sessao():
    tela8 = Toplevel(tela)
    tela8.title("Dashboard")
    tela8.geometry("400x400")
    Label(tela8, text = "Bem-vindo ao dashboard").pack()
    Button(tela8, text = "Verificar gerenciamente de memória", command = gerenciamento_de_memoria).pack()
    Button(tela8, text = "Sair", command= tela8.destroy).pack()
    
def login_sucesso():
    sessao()
    
def senha_nao_reconhecida():
    global tela4
    tela4 = Toplevel(tela)
    tela4.title("Sucesso")
    tela4.geometry("150x190")
    Label(tela4, text = "Erro na senha").pack()
    Button(tela4, text = "Ok", command= deletar3).pack()

def usuario_nao_encontrado():
    global tela5
    tela5 = Toplevel(tela)
    tela5.title("Sucesso")
    tela5.geometry("150x190")
    Label(tela5, text = "Erro na senha").pack()
    Button(tela5, text = "Ok", command= deletar4).pack()

def registrar_usuario():
    usuario_info = usuario.get()
    senha_info = senha.get()
    
    file=open(usuario_info,"w")
    file.write(usuario_info+"\n")
    file.write(senha_info)
    file.close()
    
    usuario_entrada.delete(0, END)
    senha_entrada.delete(0, END)
    
    Label(tela1, text = "Cadastro realizado com sucesso", fg = "green", font = ("calibri", 11)).pack()

def registrar():
    global tela1
    tela1 = Toplevel(tela)
    tela1.title("Registrar")
    tela1.geometry("300x250")

    global usuario
    global senha
    global usuario_entrada
    global senha_entrada
    usuario = StringVar()
    senha = StringVar()
    
    Label(tela1, text = "Entre com os detalhes abaixo").pack()
    Label(tela1, text= "").pack()
    Label(tela1, text = "Usuário * ").pack()
    usuario_entrada = Entry(tela1, textvariable = usuario)
    usuario_entrada.pack()
    Label(tela1, text= "Senha *").pack()
    senha_entrada = Entry(tela1, textvariable = senha, show='*')
    senha_entrada.pack()
    Label(tela1, text = "").pack()
    Button(tela1, text = "Registro", width = 10, height= 1, command = registrar_usuario).pack()

def login_verificar():
    
    usuario1 = usuario_verificar.get()
    senha1 = senha_verificar.get()
    usuario_entrada1.delete(0, END)
    senha_entrada1.delete(0, END)
    
    lista_de_arquivos = os.listdir()
    if usuario1 in lista_de_arquivos:
        arquivo1 = open(usuario1, "r")
        verificar = arquivo1.read().splitlines()
        if senha1 in verificar:
            login_sucesso()
        else:
            senha_nao_reconhecida()
    else:
        usuario_nao_encontrado()
        
def login():
    global tela2
    tela2 = Toplevel(tela)
    tela2.title("Login")
    tela2.geometry("300x250")
    Label(tela2, text = 'Por favor entre com as credenciais abaixo para logar').pack()
    Label(tela2, text = "").pack()
    
    global usuario_verificar
    global senha_verificar
    
    usuario_verificar = StringVar()
    senha_verificar = StringVar()
    
    global usuario_entrada1
    global senha_entrada1
        
    Label(tela2, text = "Usuário * ").pack()
    usuario_entrada1 = Entry(tela2, textvariable= usuario_verificar)
    usuario_entrada1.pack()
    Label(tela2, text= "").pack()
    Label(tela2, text = "Senha * ").pack()
    senha_entrada1 = Entry(tela2, textvariable= senha_verificar, show='*')
    senha_entrada1.pack()
    print("Login efetuado com sucesso!")
    Label(tela2, text= "").pack()
    Button(tela2, text = "Login", width= 10, height= 1, command= login_verificar).pack()    

def main_tela():
    global tela
    tela = Tk()
    tela.geometry("300x250")
    tela.title("Gerenciador de Tarefas")
    Label(text = "Gerenciador de tarefas", bg = "grey", width= "300", height = "2", font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Login", height = "2", width="30", command = login).pack()
    Label(text = "").pack()
    Button(text = "Registre-se", height = "2", width = "30", command = registrar).pack()
    
main_tela()