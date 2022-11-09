from usuario import Usuario
from view import View
from tkinter import *

class Controller:

    def __init__(self) -> None:
        self.usuario = Usuario()
        self.view = View(self)
        self.view.mainloop()

    def registrar_usuario(self, usuario, senha):
        self.usuario.registrar_usuario(usuario, senha)
        self.view.registrar_usuario_sucesso()

    def login_verificar(self, usuario, senha):
        res = self.usuario.login_verificar(usuario=usuario, senha=senha)

        if res == 'dashboard':
            self.view.view_dashboard()
        elif res == 'err_user':
            self.view.msg_erro_usuario()
        elif res == 'err_pass':
            self.view.msg_erro_senha()