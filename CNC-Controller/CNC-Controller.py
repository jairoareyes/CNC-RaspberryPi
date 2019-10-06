from tkinter import *
import tkinter.font
from MovMotSerial import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import messagebox
from tkinter import ttk
import cv2
import numpy as np
import PIL
from PIL import Image, ImageTk
import time
import os, sys
import sched, time
import threading
import RPi.GPIO as GPIO

# Puerto para la Autoalibración 
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)

## GUI DEFINITIONS
win = Tk()
win.geometry("910x700+50+0")
win.title("CNC Controller")
myFont = tkinter.font.Font(family = 'Arial', size = 12)
fuente2 = tkinter.font.Font(family = 'Times New Roman', size = 11)

#Valirables
numPasos= StringVar(win)
GCode = StringVar(win)

isCameraOn = False
isSendingGCode=False
isSpindleOn = False
## LabelFrames ##

#Calibracion
lfCalibracion = LabelFrame(win, text="Calibración",bd=4,font=fuente2)
lfCalibracion.place(x=10,y=10, width=480, height=200)

#Cargar Archivo
lfCargarArchivo = LabelFrame(win, text="Cargar Archivo",bd=4,font=fuente2)
lfCargarArchivo.place(x=10,y=220, width=480, height=400)

#Camara
lfCamara = LabelFrame(win, text="Cámara",bd=4,font=fuente2)
lfCamara.place(x=500,y=300, width=400, height=320)

#Labels
lbAvanzar = Label(win, text="Avanzar (mm)", font=fuente2)
lbAvanzar.place(x=30,y=30)

lbProgress = Label(win, text="Progreso : --/--", font=fuente2)
lbProgress.place(x=150, y=255)

lbVideo = Label(win)
lbVideo.place(x=540,y=330)
img = PhotoImage(file='ImagenFondo.png')
lbVideo.configure(image=img)

#ListBox
listbox = Listbox(win)
listbox.pack()
listbox.place(x=30, y=300, width=440, height=300)
#Scrollbar
vscroll = Scrollbar(listbox, orient=VERTICAL, command=listbox.yview)

listbox['yscroll'] = vscroll.set
vscroll.pack(side="right", fill="y")

varListbox = 0
#Llena el listBox con 10 espacios en blanco
while varListbox<10:
    listbox.insert(END, "")
    varListbox=varListbox+1

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
    resetZero()
    print("Reset Cero")

def SpindleOn():
    global isSpindleOn
    if isSpindleOn:
        btnActivarSpindle['text'] = 'Activar Spindle'
        spindleOff()
        isSpindleOn=False
    else:
        btnActivarSpindle['text'] = 'Desactivar Spindle'
        spindleOn()
        isSpindleOn=True
    
def autoCalibrar():
    while not GPIO.input(22):
        dirZNeg("0.1")
        time.sleep(0.1)
    ResetCero()
    dirZPos("3.0")
    #stButton=GPIO.input(22)
    print("Calibracion Finalizada!")

def CargarArchivo():
    listbox.delete(0, END)
    NombreArchivo = askopenfilename(filetypes=(("all files","*.*"),("NC Files","*.nc"),("Txt","*.txt")))
    if NombreArchivo:
        try:
            global GCode
            Archivo = open (NombreArchivo,'r')
            GCode = Archivo.read()
            Archivo.close()
            time.sleep(0.1)
            Archivo = open (NombreArchivo,'r')
            for line in Archivo:
                listbox.insert(END, line)
            Archivo.close()
            btnEnviarArchivo['state'] = 'normal'
        except: 
            showerror("Open Source File", "Failed to read file")
        return

def sendingGCode():
    global GCode
    nLine = 0
    global isSendingGCode
    print("Enviar Archivo")
    linea=GCode.splitlines() #Convierte el String en Array
    while isSendingGCode:
        enviarGCode(linea[nLine])
        nLine=nLine+1
        lbProgress.config(text=str("Progreso: " + str(nLine) + "/" + str(len(linea)) + " | " + str(int(nLine/len(linea)*100))+ "%"))
        if nLine==len(linea):
            isSendingGCode=False
            nLine=0
            messagebox.showinfo("Finalizado", "¡Envío de código G finalizado!")

def EnviarArchivo():
    #Define Hilo del envio de GCode
    hiloGCode = threading.Thread(target=sendingGCode)
    global isSendingGCode
    isSendingGCode=True
    hiloGCode.start()

def scCam():
    global isCameraOn
    cap=cv2.VideoCapture(0)
    time.sleep(0.1)
    while isCameraOn:
        _, frame = cap.read()
        vector = cv2.resize(frame, (320,240))
        cv2image = cv2.cvtColor(vector, cv2.COLOR_BGR2RGBA)
        grayImage=cv2.cvtColor(cv2image,cv2.COLOR_BGR2GRAY)
        circles=cv2.HoughCircles(grayImage,cv2.HOUGH_GRADIENT,2,400, # Encuentra los circulos
        param1=50,param2=30,
        minRadius=30,maxRadius=100)
        cirles=np.uint16(np.around(circles))
        cv2.circle(cv2image,(circles[0][0][0],circles[0][0][1]),circles[0][0][2],(0,255,0),2) #Dibuja el circulo
        cv2.circle(cv2image,(circles[0][0][0],circles[0][0][1]),2,(0,0,255),3) #Dibuja un punto el centro
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lbVideo.imgtk = imgtk
        lbVideo.configure(image=imgtk)
        time.sleep(0.2)
    cap.release()
    cv2.destroyAllWindows()
    img = PhotoImage(file='ImagenFondo.png')
    lbVideo.configure(image=img)

        
def CameraOn():
    global isCameraOn
    
    if isCameraOn:
        isCameraOn = False
        btnActivarCamara['text'] = 'Activar Camara'
    else:
        isCameraOn = True
        btnActivarCamara['text'] = 'Desactivar Camara'
        #Define Hilo de la camara
        hiloCam = threading.Thread(target=scCam)
        hiloCam.start()

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
btnRstCero = Button(win, text = 'Reset Cero', font = fuente2, command = ResetCero ,height = 1, width = 8)
btnRstCero.place(x=220,y=150)

#Cargar Archivo
btnCargarArchivo = Button(win, text = 'Cargar Archivo', font = fuente2, command = CargarArchivo,height = 1, width = 10)
btnCargarArchivo.place(x=30,y=250)

#Enviar Archivo
btnEnviarArchivo = Button(win, text = 'Enviar Archivo', font = fuente2, command = EnviarArchivo,height = 1, width = 10, state='disable')
btnEnviarArchivo.place(x=350,y=250)

#Activar Camara
btnActivarCamara = Button(win, text = 'Activar Camara', font = fuente2, command = CameraOn,height = 1, width = 15)
btnActivarCamara.place(x=630,y=580)

#Activar Spindle
btnActivarSpindle = Button(win, text = 'Activar Spindle', font = fuente2, command = SpindleOn,height = 1, width = 15)
btnActivarSpindle.place(x=30,y=120)

#AutoCalibracion
btnAutoCalibracion= Button(win, text = 'Autocalibrar', font = fuente2, command = autoCalibrar,height = 1, width = 15)
btnAutoCalibracion.place(x=30,y=170)

win.mainloop()

