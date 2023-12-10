import tkinter as tk
from tkinter import messagebox

class ContaBancaria:
    def __init__(self, usuario, saldo_inicial=5000):
        self.usuario = usuario
        if usuario == 'Tio Patinhas':
            self.saldo = 25000
        elif usuario == 'Ali-Baba':
            self.saldo = -15000
        elif usuario == 'Usuario':
            self.saldo = saldo_inicial

        self.transacoes = []

    def deposito(self, valor):
        if self.usuario == 'Tio Patinhas':
            self.saldo += valor + 500  # Bônus de 500 para 'Tio Patinhas'
        elif self.usuario == 'Ali-Baba':
            self.saldo += valor -  400  # Penalidade de 400 para 'Ali-Baba'
        elif self.usuario == 'Usuario':
            self.saldo += valor
            self.transacoes.append(f'Depósito: +{valor}, Saldo: {self.saldo}')


    def saque(self, valor):
        if self.usuario == 'Tio Patinhas':
            self.saldo -= valor - 100  # Bônus de 100 para 'Tio Patinhas' ao realizar saque
        elif self.usuario == 'Ali-Baba':
            self.saldo -= valor + 400 # Penalidade de 400 para 'Ali-Baba' ao realizar saque
        elif self.usuario == 'Usuario':
            self.saldo -= valor
            self.transacoes.append(f'Saque: -{valor}, Saldo: {self.saldo}')

    def extrato(self):
        extrato = '\nExtrato:'
        for transacao in self.transacoes:
            extrato += '\n' + transacao
        extrato += f'\nSaldo atual: {self.saldo}'
        return extrato



class PaginaLogin:
    def __init__(self, master, banco_app):
        self.master = master
        self.banco_app = banco_app

        self.label_usuario = tk.Label(master, text="Usuário:")
        self.label_usuario.pack()

        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.pack()

        self.label_senha = tk.Label(master, text="Senha:")
        self.label_senha.pack()

        self.entry_senha = tk.Entry(master, show="*")
        self.entry_senha.pack()

        self.botao_login = tk.Button(master, text="Login", command=self.verificar_login)
        self.botao_login.pack()

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if self.banco_app.verificar_credenciais(usuario, senha):
            self.master.destroy()
            self.banco_app.iniciar_operacoes(usuario)
        else:
            messagebox.showerror("Erro de Login", "Credenciais inválidas. Tente novamente.")

class BancoApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Sistema Bancário')

        self.usuario_autenticado = False

        self.conta = None

        self.label_saldo = tk.Label(master, text='')
        self.label_saldo.pack()

        self.label_resultado = tk.Label(master, text='')
        self.label_resultado.pack()

        self.entry_valor = tk.Entry(master)
        self.entry_valor.pack()

        self.botao_deposito = tk.Button(master, text='Depósito', command=self.realizar_deposito, state=tk.DISABLED)
        self.botao_deposito.pack()

        self.botao_saque = tk.Button(master, text='Saque', command=self.realizar_saque, state=tk.DISABLED)
        self.botao_saque.pack()

        self.botao_extrato = tk.Button(master, text='Extrato', command=self.exibir_extrato, state=tk.DISABLED)
        self.botao_extrato.pack()

        self.botao_sair = tk.Button(master, text='Sair', command=master.destroy)
        self.botao_sair.pack()

        # Exibir a página de login
        self.exibir_pagina_login()

    def exibir_pagina_login(self):
        self.pagina_login = PaginaLogin(tk.Toplevel(self.master), self)

    def verificar_credenciais(self, usuario, senha):
        # Implemente a lógica de verificação de credenciais aqui
        # Por exemplo, você pode ter um dicionário de usuários e senhas
        usuarios_senhas = {'Tio Patinhas': 'HZL1947', 'Ali-Baba': 'Abre-te Sésamo', 'Usuario': 'senha123'}
        return usuario in usuarios_senhas and usuarios_senhas[usuario] == senha

    def iniciar_operacoes(self, usuario):
        self.usuario_autenticado = True
        self.conta = ContaBancaria(usuario)
        self.botao_deposito['state'] = tk.NORMAL
        self.botao_saque['state'] = tk.NORMAL
        self.botao_extrato['state'] = tk.NORMAL
        self.atualizar_interface()

    def realizar_deposito(self):
        valor = float(self.entry_valor.get())
        self.conta.deposito(valor)
        self.atualizar_interface()

    def realizar_saque(self):
        valor = float(self.entry_valor.get())
        resultado = self.conta.saque(valor)
        if resultado:
            self.label_resultado['text'] = resultado
        else:
            self.atualizar_interface()

    def exibir_extrato(self):
        resultado = self.conta.extrato()
        self.label_resultado['text'] = resultado

    def atualizar_interface(self):
        self.label_saldo['text'] = f'Saldo atual: {self.conta.saldo}'
        self.label_resultado['text'] = ''

if __name__ == "__main__":
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()
