from usuario import Usuario
from view import View
from tkinter import *

class Controller:

    def __init__(self) -> None:
        self.usuario = Usuario()
        self.view = View(self)
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