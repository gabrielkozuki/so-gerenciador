from tkinter import *
import os

class Usuario:

    def __init__(self) -> None:
        pass

    def registrar_usuario(self, usuario, senha):
        print("usuario: " + usuario + str(type(usuario)))
        file=open(usuario, "w")
        file.write(usuario+ "\n")
        file.write(senha)
        file.close()

    def login_verificar(self, usuario, senha) -> str:
        lista_de_arquivos = os.listdir()

        if usuario in lista_de_arquivos:
            arquivo = open(usuario, "r")
            verificar = arquivo.read().splitlines()

            if senha in verificar:
                return 'dashboard'
            else:
                return 'err_pass'
        else:
            return 'err_user'