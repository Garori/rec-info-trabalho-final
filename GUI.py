import sys
sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED
from tkinter import filedialog as fd
import os.path as path
import tkinter as tk
import datetime 
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from math import floor



class GUI( Frame ):
    def __init__( self ):
        self.show = False
        super().__init__()
        tk.Frame.__init__(self)
        self.pack()

        # configurando master
        self.master.title("Automação")
        self.master.tk_setPalette(background='gray95')
        self.master.columnconfigure(6)
        
        
        # containers
        self.inputsContainer = Frame(self.master)
        self.inputsContainer["pady"] = 10
        self.inputsContainer["padx"] = 10
        self.inputsContainer.pack(fill='both', expand=True)
        self.iniciarContainer = Frame(self.master)
        self.iniciarContainer["pady"] = 10
        self.iniciarContainer["padx"] = 10
        self.iniciarContainer.columnconfigure(6)
        # self.iniciarContainer["bg"] = "red"
        self.iniciarContainer.pack(expand=True)
        

        # fontes
        self.fonte_labels = ("Graphik", "12")

        # labels
        self.labelEmail = tk.Label(self.inputsContainer)
        self.labelEmail["text"] = "E-mail "
        self.labelEmail["font"] = self.fonte_labels
        self.labelEmail["padx"] = 5
        self.LabelPassword = tk.Label(self.inputsContainer)
        self.LabelPassword["text"] = "Senha"
        self.LabelPassword["font"] = self.fonte_labels
        self.LabelPassword["padx"] = 5
        self.labelArquivoDeConsolidacao = tk.Label(self.inputsContainer)
        self.labelArquivoDeConsolidacao["text"] = "Arquivo de consolidação"
        self.labelArquivoDeConsolidacao["font"] = self.fonte_labels
        self.labelArquivoDeConsolidacao["padx"] = 5
        self.labelCaminhoExcel = tk.Label(self.inputsContainer)
        self.labelCaminhoExcel["text"] = "Pasta para download dos arquivos a serem consolidados"
        self.labelCaminhoExcel["font"] = self.fonte_labels
        self.labelCaminhoExcel["padx"] = 5
        self.labelCaminhoPbix = tk.Label(self.inputsContainer)
        self.labelCaminhoPbix["text"] = "Dashboard a ser atualizado"
        self.labelCaminhoPbix["font"] = self.fonte_labels
        self.labelCaminhoPbix["padx"] = 5
        
        # inputs
        self.inputEmail = tk.Entry(self.inputsContainer)
        self.inputEmail["bg"] = "white"
        self.inputEmail["font"] = self.fonte_labels
        self.inputEmail["width"] = 30
        self.inputPassword = tk.Entry(self.inputsContainer, show="*")
        self.inputPassword["bg"] = "white"
        self.inputPassword["font"] = self.fonte_labels
        self.inputPassword["width"] = 30
        self.inputArquivoDeConsolidacao = tk.Entry(self.inputsContainer)
        self.inputArquivoDeConsolidacao["bg"] = "white"
        self.inputArquivoDeConsolidacao["font"] = self.fonte_labels
        self.inputArquivoDeConsolidacao["width"] = 30
        self.inputCaminhoExcel = tk.Entry(self.inputsContainer)
        self.inputCaminhoExcel["bg"] = "white"
        self.inputCaminhoExcel["font"] = self.fonte_labels
        self.inputCaminhoExcel["width"] = 30
        self.inputCaminhoPbix = tk.Entry(self.inputsContainer)
        self.inputCaminhoPbix["bg"] = "white"
        self.inputCaminhoPbix["font"] = self.fonte_labels
        self.inputCaminhoPbix["width"] = 30

        # buttons
        self.buttonPassword = tk.Button(self.inputsContainer)
        self.buttonPassword["text"] = "Mostrar"
        self.buttonPassword["font"] = self.fonte_labels
        self.buttonPassword["command"] = self.showPass
        self.buttonArquivoDeConsolidacao = tk.Button(self.inputsContainer)
        self.buttonArquivoDeConsolidacao["text"] = "Selecionar"
        self.buttonArquivoDeConsolidacao["font"] = self.fonte_labels
        self.buttonArquivoDeConsolidacao["command"] = lambda arg1= 0 : self.acharCaminho(arg1)
        self.buttonCaminhoExcel = tk.Button(self.inputsContainer)
        self.buttonCaminhoExcel["text"] = "Selecionar"
        self.buttonCaminhoExcel["font"] = self.fonte_labels
        self.buttonCaminhoExcel["command"] = lambda arg1= 1 : self.acharCaminho(arg1)
        self.buttonCaminhoPbix = tk.Button(self.inputsContainer)
        self.buttonCaminhoPbix["text"] = "Selecionar"
        self.buttonCaminhoPbix["font"] = self.fonte_labels
        self.buttonCaminhoPbix["command"] = lambda arg1= 2 : self.acharCaminho(arg1)
        self.buttonIniciar = tk.Button(self.iniciarContainer)
        self.buttonIniciar["text"] = "Iniciar!"
        self.buttonIniciar["font"] = self.fonte_labels
        self.buttonContinuar = tk.Button(self.iniciarContainer)
        self.buttonContinuar["text"] = "Continuar"
        self.buttonContinuar["font"] = self.fonte_labels
        self.defaultInputs()


    def showPass(self):
        if self.show:
            self.inputPassword.config(show="*")
            self.buttonPassword["text"] = "Mostrar"
        else:
            self.inputPassword.config(show="")
            self.buttonPassword["text"] = "Esconder"
        self.show = not self.show
            

    def defaultInputs(self):
        

        if not path.isfile("./saveFile.txt"):
            f = open("./saveFile.txt", "w")
            f.write(r" ") #production
            f.write("\n")
            f.write(r" ") #production
            f.write("\n")
            f.write(r" ") #production
            f.write("\n")
            f.write(" ") #production
            f.write("\n")
            f.write(" ") #production
            f.close()
            f.close()
        f = open("./saveFile.txt", "r")
        inputs = f.readlines()
        f.close()

        self.inputEmail.delete(0,END)
        # self.inputEmail.insert(0, r"gabriel.c.fonseca@accenture.com") #teste
        self.inputEmail.insert(0, inputs[0].replace("\n", ""))  # production
        self.inputArquivoDeConsolidacao.delete(0,END)
        # self.inputArquivoDeConsolidacao.insert(0, r"C:/Users/gabriel.c.fonseca/OneDrive - Accenture/Desktop/fabrica de automacoes/Automacao Tigre/dummy.pbix") #teste
        self.inputArquivoDeConsolidacao.insert(0, inputs[1].replace("\n","")) #production
        self.inputCaminhoExcel.delete(0,END)
        # self.inputCaminhoExcel.insert(0, r"C:/New Folder/NormalTaskReport.xlsx") #teste
        self.inputCaminhoExcel.insert(0, inputs[2].replace("\n", ""))  # production
        self.inputCaminhoPbix.delete(0, END)
        self.inputCaminhoPbix.insert(0,inputs[3].replace("\n",""))
        # self.inputPassword.delete(0, END)
        # self.inputPassword.insert(0, inputs[4].replace("\n", ""))


    def message(self, message):
        showinfo(message=message)

    def mainScreen(self):

        # print(self.shiftArq)
        # Shift

        self.labelEmail.grid(row=2, column=0, pady=10, padx=10, sticky=W)
        self.inputEmail.grid(row=2, column=1, sticky=EW, pady=10, padx=10)
        # self.buttonShiftAntigo.grid(row=3, column=3, pady=10, padx=10)

        self.LabelPassword.grid(row=3, column=0, pady=10, padx=10, sticky=W)
        self.inputPassword.grid(row=3, column=1, sticky=EW, pady=10, padx=10)
        self.buttonPassword.grid(row=3, column=3, pady=10, padx=10)

        self.labelArquivoDeConsolidacao.grid(row=4, column=0, pady=10, padx=10, sticky=W)
        self.inputArquivoDeConsolidacao.grid(row=4, column=1, sticky=EW, pady=10, padx=10)
        self.buttonArquivoDeConsolidacao.grid(row=4, column=3, pady=10, padx=10)

        self.labelCaminhoExcel.grid(row=5, column=0, pady=10, padx=10, sticky=W)
        self.inputCaminhoExcel.grid(row=5, column=1, sticky=EW, pady=10, padx=10)
        self.buttonCaminhoExcel.grid(row=5, column=3, pady=10, padx=10)

        self.labelCaminhoPbix.grid(row=6, column=0, pady=10, padx=10, sticky=W)
        self.inputCaminhoPbix.grid(row=6, column=1, sticky=EW, pady=10, padx=10)
        self.buttonCaminhoPbix.grid(row=6, column=3, pady=10, padx=10)

        # self.buttonPegarAuto.grid(row=1, column=3, pady=10, padx=10)
        self.buttonIniciar.grid(row=1, column=4, pady=10, padx=10)
        self.buttonContinuar.grid(row=1, column=5, pady=10, padx=10)

        
        
        self.master.mainloop()        


    def acharCaminho(self,num):
        if num==0:
            arq = fd.askopenfilename()
            self.inputArquivoDeConsolidacao.delete(0,END)
            self.inputArquivoDeConsolidacao.insert(0,arq)
        elif num == 1:
            arq = fd.askdirectory()
            self.inputCaminhoExcel.delete(0, END)
            self.inputCaminhoExcel.insert(0, arq)
        else:
            arq = fd.askopenfilename()
            self.inputCaminhoPbix.delete(0, END)
            self.inputCaminhoPbix.insert(0, arq)
    
    def updateSaveFile(self):
        f = open("./saveFile.txt", "w")
        f.write(self.inputEmail.get()) #production
        f.write("\n")
        f.write(self.inputArquivoDeConsolidacao.get()) #production
        f.write("\n")
        f.write(self.inputCaminhoExcel.get()) #production
        f.write("\n")
        f.write(self.inputCaminhoPbix.get()) #production
        # f.write("\n")
        # f.write(self.inputPassword.get()) #production
        f.close()
            

if __name__ == "__main__":
    tela = GUI()
    tela.mainScreen()
