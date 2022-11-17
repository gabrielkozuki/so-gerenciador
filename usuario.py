from tkinter import *
import os
import json

class Usuario:

    def __init__(self) -> None:
        json_data = self.load_data()
        self.uid = json_data['key']

    def load_data(self):
        with open('data.json') as f:
            return json.load(f)

    def save_data(self, json_data):
        with open('data.json', 'w') as f:
            json.dump(json_data, f, indent=4)

    def registrar_usuario(self, usuario, senha):
        json_data = self.load_data()

        for i in json_data["users"]:
            stored_usuario = json_data["users"][i]['usuario']
            if stored_usuario == usuario:
                return 'err_user'

        usuario = {
            'usuario': usuario,
            'senha': senha
        }
        
        json_data["users"][self.uid] = usuario 
        self.uid += 1
        json_data["key"] = self.uid 
        self.save_data(json_data)

    def login_verificar(self, usuario, senha) -> str:
        json_data = self.load_data()

        for k, v in json_data["users"].items():
            if v['usuario'] == usuario and v['senha'] == senha:
                return 'dashboard'
        
        return 'err_login'