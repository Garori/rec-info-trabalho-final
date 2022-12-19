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
        self.master.title("Nostalgia Crawler")
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
        self.labelQuery = tk.Label(self.inputsContainer)
        self.labelQuery["text"] = "Query:"
        self.labelQuery["font"] = self.fonte_labels
        self.labelQuery["padx"] = 5
        self.labelDownload = tk.Label(self.inputsContainer)
        self.labelDownload["text"] = "Pasta para download dos arquivos "
        self.labelDownload["font"] = self.fonte_labels
        self.labelDownload["padx"] = 5
        self.labelAnoInicio = tk.Label(self.inputsContainer)
        self.labelAnoInicio["text"] = "Ano de início(opcional):"
        self.labelAnoInicio["font"] = self.fonte_labels
        self.labelAnoInicio["padx"] = 5
        self.labelAnoFim = tk.Label(self.inputsContainer)
        self.labelAnoFim["text"] = "Ano de fim (opcional):"
        self.labelAnoFim["font"] = self.fonte_labels
        self.labelAnoFim["padx"] = 5
        self.labelMaxSize = tk.Label(self.inputsContainer)
        self.labelMaxSize["text"] = "Tamanho máximo por arquivo em MB"
        self.labelMaxSize["font"] = self.fonte_labels
        self.labelMaxSize["padx"] = 5
        self.labelNumDownloads = tk.Label(self.inputsContainer)
        self.labelNumDownloads["text"] = "Número máximo de downloads por domínio:"
        self.labelNumDownloads["font"] = self.fonte_labels
        self.labelNumDownloads["padx"] = 5
        self.labelUrlsExtras = tk.Label(self.inputsContainer)
        self.labelUrlsExtras["text"] = "Urls adicionais (separadas por espaço) (OPCIONAL):"
        self.labelUrlsExtras["font"] = self.fonte_labels
        self.labelUrlsExtras["padx"] = 5
        self.labelOnlyExtra = tk.Label(self.inputsContainer)
        self.labelOnlyExtra["text"] = "Utilizar apenas urls adicionais? (1/0)"
        self.labelOnlyExtra["font"] = self.fonte_labels
        self.labelOnlyExtra["padx"] = 5
        self.labelSearchKeywords = tk.Label(self.inputsContainer)
        self.labelSearchKeywords["text"] = "Procurar por keywords nos domínios encontrados? (1/0)"
        self.labelSearchKeywords["font"] = self.fonte_labels
        self.labelSearchKeywords["padx"] = 5

        
        # inputs
        self.inputQuery = tk.Entry(self.inputsContainer)
        self.inputQuery["bg"] = "white"
        self.inputQuery["font"] = self.fonte_labels
        self.inputQuery["width"] = 30
        self.inputUrlsExtras = tk.Entry(self.inputsContainer)
        self.inputUrlsExtras["bg"] = "white"
        self.inputUrlsExtras["font"] = self.fonte_labels
        self.inputUrlsExtras["width"] = 30
        self.inputAnoInicio = tk.Entry(self.inputsContainer)
        self.inputAnoInicio["bg"] = "white"
        self.inputAnoInicio["font"] = self.fonte_labels
        self.inputAnoInicio["width"] = 30
        self.inputDownload = tk.Entry(self.inputsContainer)
        self.inputDownload["bg"] = "white"
        self.inputDownload["font"] = self.fonte_labels
        self.inputDownload["width"] = 30
        self.inputAnoFim = tk.Entry(self.inputsContainer)
        self.inputAnoFim["bg"] = "white"
        self.inputAnoFim["font"] = self.fonte_labels
        self.inputAnoFim["width"] = 30
        self.inputUrlsExtras = tk.Entry(self.inputsContainer)
        self.inputUrlsExtras["bg"] = "white"
        self.inputUrlsExtras["font"] = self.fonte_labels
        self.inputUrlsExtras["width"] = 30
        self.inputAnoFim = tk.Entry(self.inputsContainer)
        self.inputAnoFim["bg"] = "white"
        self.inputAnoFim["font"] = self.fonte_labels
        self.inputAnoFim["width"] = 30
        self.inputMaxSize = tk.Entry(self.inputsContainer)
        self.inputMaxSize["bg"] = "white"
        self.inputMaxSize["font"] = self.fonte_labels
        self.inputMaxSize["width"] = 30
        self.inputNumDownloads = tk.Entry(self.inputsContainer)
        self.inputNumDownloads["bg"] = "white"
        self.inputNumDownloads["font"] = self.fonte_labels
        self.inputNumDownloads["width"] = 30
        self.inputOnlyExtra = tk.Entry(self.inputsContainer)
        self.inputOnlyExtra["bg"] = "white"
        self.inputOnlyExtra["font"] = self.fonte_labels
        self.inputOnlyExtra["width"] = 30
        self.inputSearchKeywords = tk.Entry(self.inputsContainer)
        self.inputSearchKeywords["bg"] = "white"
        self.inputSearchKeywords["font"] = self.fonte_labels
        self.inputSearchKeywords["width"] = 30

        # buttons
        
        self.buttonDownload = tk.Button(self.inputsContainer)
        self.buttonDownload["text"] = "Selecionar"
        self.buttonDownload["font"] = self.fonte_labels
        self.buttonDownload["command"] = self.acharCaminho
        self.buttonIniciar = tk.Button(self.iniciarContainer)
        self.buttonIniciar["text"] = "Iniciar!"
        self.buttonIniciar["font"] = self.fonte_labels
        self.defaultInputs()


    def showPass(self):
        if self.show:
            self.inputUrlsExtras.config(show="*")
            self.buttonUrlsExtras["text"] = "Mostrar"
        else:
            self.inputUrlsExtras.config(show="")
            self.buttonUrlsExtras["text"] = "Esconder"
        self.show = not self.show
            

    def defaultInputs(self):
        

        if not path.isfile("./saveFile.txt"):
            f = open("./saveFile.txt", "w")
            f.write("ragnarok online") #production
            f.write("\n")
            f.write("2002") #production
            f.write("\n")
            f.write("C:/") #production
            f.write("\n")
            f.write("2022") #production
            f.write("\n")
            f.write("50") #production
            f.write("\n")
            f.write("100")  # production
            f.write("\n")
            f.write("levelupgames.com.br") #production
            f.write("\n")
            f.write("0") #production
            f.write("\n")
            f.write("1") #production
            f.close()
        f = open("./saveFile.txt", "r")
        inputs = f.readlines()
        f.close()

        self.inputQuery.delete(0,END)
        self.inputQuery.insert(0, inputs[0].replace("\n", ""))  # production
        self.inputAnoInicio.delete(0,END)
        self.inputAnoInicio.insert(0, inputs[1].replace("\n","")) #production
        self.inputDownload.delete(0,END)
        self.inputDownload.insert(0, inputs[2].replace("\n", ""))  # production
        self.inputAnoFim.delete(0, END)
        self.inputAnoFim.insert(0,inputs[3].replace("\n",""))
        self.inputMaxSize.delete(0, END)
        self.inputMaxSize.insert(0, inputs[4].replace("\n", ""))
        self.inputNumDownloads.delete(0, END)
        self.inputNumDownloads.insert(0, inputs[5].replace("\n", ""))
        self.inputUrlsExtras.delete(0, END)
        self.inputUrlsExtras.insert(0, inputs[6].replace("\n", ""))
        self.inputOnlyExtra.delete(0, END)
        self.inputOnlyExtra.insert(0, inputs[7].replace("\n", ""))
        self.inputSearchKeywords.delete(0, END)
        self.inputSearchKeywords.insert(0, inputs[8].replace("\n", ""))


    def message(self, message):
        showinfo(message=message)

    def mainScreen(self):

        # print(self.shiftArq)
        # Shift

        self.labelQuery.grid(row=0, column=0, pady=10, padx=10, sticky=W)
        self.inputQuery.grid(row=0, column=1, sticky=EW, pady=10, padx=10)

        self.labelDownload.grid(row=1, column=0, pady=10, padx=10, sticky=W)
        self.inputDownload.grid(row=1, column=1, sticky=EW, pady=10, padx=10)
        self.buttonDownload.grid(row=1, column=3, pady=10, padx=10)
        
        self.labelAnoInicio.grid(row=2, column=0, pady=10, padx=10, sticky=W)
        self.inputAnoInicio.grid(row=2, column=1, sticky=EW, pady=10, padx=10)

        self.labelAnoFim.grid(row=3, column=0, pady=10, padx=10, sticky=W)
        self.inputAnoFim.grid(row=3, column=1, sticky=EW, pady=10, padx=10)

        self.labelNumDownloads.grid(row=4, column=0, pady=10, padx=10, sticky=W)
        self.inputNumDownloads.grid(row=4, column=1, sticky=EW, pady=10, padx=10)

        self.labelMaxSize.grid(row=5, column=0, pady=10, padx=10, sticky=W)
        self.inputMaxSize.grid(row=5, column=1, sticky=EW, pady=10, padx=10)

        self.labelUrlsExtras.grid(row=6, column=0, pady=10, padx=10, sticky=W)
        self.inputUrlsExtras.grid(row=6, column=1, sticky=EW, pady=10, padx=10)


        self.labelOnlyExtra.grid(row=7, column=0, pady=10, padx=10, sticky=W)
        self.inputOnlyExtra.grid(row=7, column=1, sticky=EW, pady=10, padx=10)

        self.labelSearchKeywords.grid(row=8, column=0, pady=10, padx=10, sticky=W)
        self.inputSearchKeywords.grid(row=8, column=1, sticky=EW, pady=10, padx=10)


        # self.buttonPegarAuto.grid(row=1, column=3, pady=10, padx=10)
        self.buttonIniciar.grid(row=1, column=4, pady=10, padx=10)
        # self.buttonContinuar.grid(row=1, column=5, pady=10, padx=10)

        
        
        self.master.mainloop()        


    def acharCaminho(self):
        arq = fd.askdirectory()
        self.inputDownload.delete(0, END)
        self.inputDownload.insert(0, arq)
    
    def updateSaveFile(self):
        f = open("./saveFile.txt", "w")
        f.write(self.inputQuery.get()) #production
        f.write("\n")
        f.write(self.inputAnoInicio.get()) #production
        f.write("\n")
        f.write(self.inputDownload.get()) #production
        f.write("\n")
        f.write(self.inputAnoFim.get()) #production
        f.write("\n")
        f.write(self.inputMaxSize.get()) #production
        f.write("\n")
        f.write(self.inputNumDownloads.get()) #production
        f.write("\n")
        f.write(self.inputUrlsExtras.get()) #production
        f.write("\n")
        f.write(self.inputOnlyExtra.get()) #production
        f.write("\n")
        f.write(self.inputSearchKeywords.get())  # production
        # f.write("\n")
        # f.write(self.inputUrlsExtras.get()) #production
        f.close()
            

if __name__ == "__main__":
    tela = GUI()
    tela.mainScreen()
