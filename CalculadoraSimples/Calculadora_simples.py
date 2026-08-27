# Projeto de calculadora simples em Python feito por KaelxDev (KaelxDev@gmail.com)

import tkinter as tk

# ==========================
# CORES
# ==========================

FUNDO = "#1E1E1E"
VISOR = "#2B2B2B"

COR_NUM = "#333333"
COR_OP = "#717171"
COR_AC = "#FF3B30"
COR_IGUAL = "#34C759"

TEXTO = "white"

OPERADORES = "+-*/%"


class Calculadora:

    def __init__(self):

        self.historico = []

        self.janela = tk.Tk()
        self.janela.title("Calculadora - KaelxDev")
        self.janela.geometry("380x600")
        self.janela.configure(bg=FUNDO)
        self.janela.resizable(False, False)

        self.criar_interface()

        self.janela.bind("<Key>", self.tecla)

        self.janela.mainloop()

    # ======================
    # Interface
    # ======================

    def criar_interface(self):

        self.visor = tk.Entry(
            self.janela,
            font=("Segoe UI", 30, "bold"),
            justify="right",
            bg=VISOR,
            fg="white",
            bd=0,
            insertbackground="white"
        )

        self.visor.pack(
            fill="x",
            padx=20,
            pady=20,
            ipady=18
        )

        frame = tk.Frame(self.janela, bg=FUNDO)
        frame.pack(expand=True, fill="both", padx=15, pady=10)

        for i in range(4):
            frame.columnconfigure(i, weight=1)

        for i in range(6):
            frame.rowconfigure(i, weight=1)

        botoes = [

            ("Hist",0,0,FUNDO,self.mostrar_historico),
            ("AC",0,1,COR_AC,self.limpar),
            ("⌫",0,2,COR_OP,self.apagar),
            ("/",0,3,COR_OP,lambda:self.inserir("/")),

            ("7",1,0,COR_NUM,lambda:self.inserir("7")),
            ("8",1,1,COR_NUM,lambda:self.inserir("8")),
            ("9",1,2,COR_NUM,lambda:self.inserir("9")),
            ("×",1,3,COR_OP,lambda:self.inserir("*")),

            ("4",2,0,COR_NUM,lambda:self.inserir("4")),
            ("5",2,1,COR_NUM,lambda:self.inserir("5")),
            ("6",2,2,COR_NUM,lambda:self.inserir("6")),
            ("-",2,3,COR_OP,lambda:self.inserir("-")),

            ("1",3,0,COR_NUM,lambda:self.inserir("1")),
            ("2",3,1,COR_NUM,lambda:self.inserir("2")),
            ("3",3,2,COR_NUM,lambda:self.inserir("3")),
            ("+",3,3,COR_OP,lambda:self.inserir("+")),

            ("%",4,0,COR_NUM,lambda:self.inserir("%")),
            ("0",4,1,COR_NUM,lambda:self.inserir("0")),
            (",",4,2,COR_NUM,lambda:self.inserir(".")),
            ("=",4,3,COR_IGUAL,self.calcular)

        ]

        for texto, linha, coluna, cor, comando in botoes:

            tk.Button(
                frame,
                text=texto,
                font=("Segoe UI",18,"bold"),
                bg=cor,
                fg=TEXTO,
                bd=0,
                activebackground="#555555",
                command=comando
            ).grid(
                row=linha,
                column=coluna,
                sticky="nsew",
                padx=5,
                pady=5
            )

    # ======================
    # Entrada
    # ======================

    def inserir(self, valor):

        texto = self.visor.get()

        if valor in OPERADORES:

            if not texto:
                return

            if texto[-1] in OPERADORES:
                return

        if valor == ".":

            ultimo = texto

            for op in OPERADORES:
                ultimo = ultimo.split(op)[-1]

            if "." in ultimo:
                return

        self.visor.insert(tk.END, valor)

    # ======================
    # Cálculo
    # ======================

    def calcular(self):

        expressao = self.visor.get()

        if not expressao:
            return

        try:

            resultado = eval(expressao, {"__builtins__": None}, {})

            if isinstance(resultado, float):
                resultado = round(resultado, 10)

                if resultado.is_integer():
                    resultado = int(resultado)

            self.historico.append(
                f"{expressao} = {resultado}"
            )

            self.visor.delete(0, tk.END)
            self.visor.insert(0, resultado)

        except ZeroDivisionError:

            self.visor.delete(0, tk.END)
            self.visor.insert(0, "Erro")

        except:

            self.visor.delete(0, tk.END)
            self.visor.insert(0, "Inválido")

    # ======================
    # Utilidades
    # ======================

    def limpar(self):

        self.visor.delete(0, tk.END)

    def apagar(self):

        texto = self.visor.get()

        if texto:
            self.visor.delete(len(texto)-1, tk.END)

    # ======================
    # Histórico
    # ======================

    def mostrar_historico(self):

        janela = tk.Toplevel(self.janela)
        janela.title("Histórico")
        janela.geometry("350x400")
        janela.configure(bg=FUNDO)

        texto = tk.Text(
            janela,
            bg=VISOR,
            fg="white",
            font=("Consolas",12),
            bd=0
        )

        texto.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        if not self.historico:

            texto.insert(tk.END, "Nenhum cálculo realizado.")

        else:

            for item in self.historico:
                texto.insert(tk.END, item + "\n")

        texto.config(state="disabled")

    # ======================
    # Teclado
    # ======================

    def tecla(self, event):

        if event.keysym == "Return":
            self.calcular()

        elif event.keysym == "BackSpace":
            self.apagar()

        elif event.keysym == "Escape":
            self.limpar()

        elif event.char in "0123456789+-*/%.":
            self.inserir(event.char)


# ==========================
# Executar
# ==========================

Calculadora()