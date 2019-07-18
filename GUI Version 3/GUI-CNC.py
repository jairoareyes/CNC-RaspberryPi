from tkinter import *
import tkinter.font
from MovMotSerial import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import time
import os, sys

# import picamera

# camera = picamera.PiCamera()

## GUI DEFINITIONS
win = Tk()
win.geometry("500x700+400+0")
win.title("CNC Controller")
myFont = tkinter.font.Font(family = 'Arial', size = 12)
fuente2 = tkinter.font.Font(family = 'Times New Roman', size = 11)
#~ scrollbar=Scrollbar(win)
#~ scrollbar.pack(side=RIGHT, fill=Y)

#Valirables
numPasos= StringVar(win)
GCode = StringVar(win)
nLine = IntVar(win)
nLine=0

## LabelFrames ##

#Calibracion
lfCalibracion = LabelFrame(win, text="Calibración",bd=4,font=fuente2)
lfCalibracion.place(x=10,y=10, width=480, height=200)

#Cargar Archivo
lfCargarArchivo = LabelFrame(win, text="Cargar Archivo",bd=4,font=fuente2)
lfCargarArchivo.place(x=10,y=220, width=480, height=400)

#Labels
lbAvanzar = Label(win, text="Avanzar (mm)", font=fuente2)
lbAvanzar.place(x=30,y=30)

#ListBox
listbox = Listbox(win)
listbox.pack()

#Scrollbar
vscroll = Scrollbar(listbox, orient=VERTICAL, command=listbox.yview)
listbox['yscroll'] = vscroll.set

vscroll.pack(side="right", fill="y")

#Spinbox
sbAvMM = Spinbox(win, from_=0.1, to=50,format='%.1f',increment=0.1 , textvariable=numPasos, font =fuente2)
sbAvMM.place(x=130, y=30,width=50)

def dirXPos1():
    global numPasos
    dirXPos(numPasos.get())
    
def dirXNeg1():
    global numPasos
    dirXNeg(numPasos.get())

def dirYPos1():
    global numPasos
    dirYPos(numPasos.get())

def dirYNeg1():
    global numPasos
    dirYNeg(numPasos.get())

def dirZPos1():
    global numPasos
    dirZPos(numPasos.get())

def dirZNeg1():
    global numPasos
    dirZNeg(numPasos.get())

def ResetCero():
    print("Reset Cero")


def CargarArchivo():
    NombreArchivo = askopenfilename(filetypes=(("all files","*.*"),("NC Files","*.nc"),("Txt","*.txt")))
    if NombreArchivo:
        try:
            global GCode
            listbox.place(x=30, y=300, width=440, height=300)
            Archivo = open (NombreArchivo,'r')
            GCode = Archivo.read()
            Archivo.close()
            time.sleep(0.1);
            Archivo = open (NombreArchivo,'r')
            for line in Archivo:
                listbox.insert(END, line)
            Archivo.close()
            btnEnviarArchivo['state'] = 'normal'
        except: 
            showerror("Open Source File", "Failed to read file")
        return

def EnviarArchivo():
    global GCode
    global nLine
    print("Enviar Archivo")
    linea=GCode.splitlines() #Convierte el String en Array
    for line in linea:
        print(linea[nLine])
        enviarGCode(linea[nLine])
        nLine=nLine+1
        time.sleep(0.5)

# def CameraOn():
#     global camera
#     camera.preview_fullscreen=False
#     camera.preview_window=(90,100, 320, 240)
#     camera.resolution=(640,480)
#     camera.start_preview()

# def CameraOff():
#     camera.stop_preview()
#     camera.close()

# def TakePhoto():
#     camera.capture('imagenPru3.gif')
    
## Botones ##

# Eje X
btnDirXPos = Button(win, text = 'X+', font = myFont, command = dirXPos1, height = 1, width = 3)
btnDirXPos.place(x=300,y=70)

btnDirXNeg = Button(win, text = 'X-', font = myFont, command = dirXNeg1, height = 1, width = 3)
btnDirXNeg.place(x=170,y=70)

#Eje Y
btnDirYPos = Button(win, text = 'Y+', font = myFont, command = dirYPos1, height = 1, width = 3)
btnDirYPos.place(x=235,y=40)

btnDirYNeg = Button(win, text = 'Y-', font = myFont, command = dirYNeg1, height = 1, width = 3)
btnDirYNeg.place(x=235,y=100)

#Eje Z
btnDirZPos = Button(win, text = 'Z+', font = myFont, command = dirZPos1 ,height = 1, width = 3)
btnDirZPos.place(x=400,y=50)

btnDirZNeg = Button(win, text = 'Z-', font = myFont, command = dirZNeg1 ,height = 1, width = 3)
btnDirZNeg.place(x=400,y=90)

#Reset Cero
btnRstCero = Button(win, text = 'Reset Cero', font = fuente2, command = ResetCero ,height = 1, width = 6)
btnRstCero.place(x=220,y=150)

#Cargar Archivo
btnCargarArchivo = Button(win, text = 'Cargar Archivo', font = fuente2, command = CargarArchivo,height = 1, width = 10)
btnCargarArchivo.place(x=30,y=250)

#Enviar Archivo
btnEnviarArchivo = Button(win, text = 'Enviar Archivo', font = fuente2, command = EnviarArchivo,height = 1, width = 10, state='disable')
btnEnviarArchivo.place(x=350,y=250)

win.mainloop()

