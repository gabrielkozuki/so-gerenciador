class Usuario:

    def __init__(self) -> None:
        pass

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

    def login_sucesso():
        sessao()

    def login_verificar():
        usuario1 = usuario_verificar.get()
        senha1 = senha_verificar.get()
        usuario_entrada.delete(0, END)
        senha_entrada.delete(0, END)
        
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