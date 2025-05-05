import cryptocode as crypt
from datetime import date,datetime
import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import webbrowser
import re
import psutil
class managerLicense():
    def __init__(self):
        self.janela = Tk()
        self.janela.title("Manager License - MICROBAN")
        self.new_text=""
        self.dt_validate=""
        self.mac_address=""
        self.body()
        self.txt_data.focus()
        self.centralizar()
        self.janela.wm_resizable(width=FALSE,height=FALSE)
        self.janela.mainloop()
    def centralizar(self):
        altura = 200
        largura = 400
        largura_screen = self.janela.winfo_screenwidth()
        altura_screen = self.janela.winfo_screenheight()
        posix = int(largura_screen/2 - largura/2)
        posiy = int(altura_screen/2 - altura/2)
        self.janela.geometry(f"{largura}x{altura}+{posix}+{posiy}")
    def data_valida(self,data):
        try:
            datetime.strptime(data, '%d/%m/%Y')
            return True
        except ValueError:
            return False
    def format_data(self,event = NONE):
        text = self.txt_data.get(1.0,END).replace("/", "").replace("-", "").replace("\n","")[:10]
        text = re.sub('<[a-zA-Z]>', '', text)

        if len(text)==9:
            self.txt_data.delete(1.0,END)
            self.txt_data.insert(1.0,self.new_text)
            return
        if event.keysym.lower() == "backspace": return
        
        for index in range(len(text)):
            if not text[index] in "0123456789": continue
            if len(text) == 8:
                self.new_text = f"{text[0:2]}/{text[2:4]}/{text[4:8]}"
                self.txt_data.delete(1.0,END)
                if(self.data_valida(self.new_text)):
                    self.txt_data.insert(1.0,self.new_text)
                    self.dt_validate = self.new_text
                    self.txt_mac.focus()
                else:
                    messagebox.showerror(title="Erro de Data",message="Favor Digitar uma data valida")
                return
            else:
                self.new_text = text
        
        self.txt_data.delete(1.0,END)
        self.txt_data.insert(1.0,self.new_text)
    
    def getMac(self):
        macs=[]
        for interface in psutil.net_if_addrs():
            # Check if the interface has a valid MAC address
            if psutil.net_if_addrs()[interface][0].address:
                # Print the MAC address for the interface
                mac=psutil.net_if_addrs()[interface][0].address
                if mac.find("-") > 0:
                    macs.append(mac)
        macs = tuple(macs)
        return macs
    
    def body(self):
        self.lbl_data = Label(self.janela,text="Data de validade:",anchor=W,justify=LEFT)
        self.lbl_data.place(x=5,y=5)
        self.txt_data = Text(self.janela,width=10,height=1)
        self.txt_data.place(x=115,y=5)
        self.txt_data.bind("<KeyRelease>", self.format_data)
        self.lbl_mac = Label(self.janela,text="Mac externo:",anchor=W,justify=LEFT)
        self.lbl_mac.place(x=5,y=30)
        self.txt_mac = Text(self.janela,width=15,height=1)
        self.txt_mac.place(x=115,y=30)
        self.clbl_mac = Label(self.janela,text="Mac da Maquina")
        self.clbl_mac.place(x=5,y=60)
        self.cmb_mac = ttk.Combobox(self.janela,values=self.getMac())
        self.cmb_mac.place(x=115,y=60)
        self.cmb_mac.bind('<<ComboboxSelected>>', self.choiceMac)
        self.btn_create = Button(self.janela,text="Gerar Chave",command=self.btnCreate)
        self.btn_create.place(x=170,y=90)
    
    def choiceMac(self,event):
        
        self.mc_selected=self.cmb_mac.get()
    
    def btnCreate(self):
        mac=""
        if self.cmb_mac.get() !="":
            mac =self.cmb_mac.get()
        else:
            if self.txt_mac.get(1.0,END).replace("\n","") !="":
                mac = self.txt_mac.get(1.0,END).replace("\n","")
            else:
                messagebox.showerror(title="Erro mac",message="Mac deve ser Preenchido ou escolhido")

        if mac !="" and self.dt_validate !="":    
            key = self.CreateLicenseKey(self.dt_validate,mac)
            
            self.gravar_arquivo(key)
        else:
            messagebox.showerror(title="Campos vazios",message="Todos os Campos devem ser preenchidos")
        
    def CreateLicenseKey(self,key,mac_address):
        self.mac_address=mac_address
        return crypt.encrypt(key,mac_address)
    def gravar_arquivo(self,key):
        data_hora = datetime.now()
        
        with open("license.txt", "w") as arquivo:
            arquivo.write("[    Gerado    ]\n")
            arquivo.write(f"{data_hora.strftime('%d/%m/%Y %H:%M')}\n")
            arquivo.write("[    Validade    ]\n")
            arquivo.write(f"{self.dt_validate}\n")
            arquivo.write("[    Mac Address ]\n")
            arquivo.write(f"{self.mac_address}\n")
            arquivo.write("[    Key     ]\n")
            arquivo.write(f"{key}\n")
        messagebox.showinfo(title="Key",message="Licença Gerada com sucesso")
        webbrowser.open("license.txt")

if __name__=="__main__":
    managerLicense()
