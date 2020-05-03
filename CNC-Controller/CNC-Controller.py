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
GPIO.setup(23, GPIO.IN)

## GUI DEFINITIONS
win = Tk()
win.geometry("910x700+0+0")
win.title("CNC Controller")
myFont = tkinter.font.Font(family = 'Piboto', size = 12)
fuente2 = tkinter.font.Font(family = 'Piboto', size = 11)

#resetZero() # Toma como cero la pocicion de encendido

#Valirables
numPasos= StringVar(win)
GCode = StringVar(win)
nFidu = IntVar(win)
nFidu = 0
layer = IntVar(win)
profundidad = StringVar(win)
maxCordNum = IntVar(win)
maxCordNum = 0

isCameraOn = False
isSendingGCode = False
isSpindleOn = False
isStopSending = True
isRecog = False
contCirRec = 0

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

 #Grafica
lfGrafica = LabelFrame(win, text="Gráfica",bd=4,font=fuente2)
lfGrafica.place(x=500,y=10, width=400, height=280)

#Labels
lbAvanzar = Label(win, text="Avanzar (mm)", font=fuente2)
lbAvanzar.place(x=30,y=30)

lbCapa = Label(win, text="Capa:", font=fuente2)
lbCapa.place(x=30,y=250)

lbProgress = Label(win, text="Progreso : --/--", font=fuente2)
lbProgress.place(x=150, y=305)

lbProfundidad = Label(win, text="Prof. Z", font=fuente2)
lbProfundidad.place(x=225, y=250)

lbVideo = Label(win)
lbVideo.place(x=540,y=330)
img = PhotoImage(file='ImagenFondo.png')
lbVideo.configure(image=img)

#ListBox
listbox = Listbox(win)
listbox.pack()
listbox.place(x=30, y=350, width=440, height=250)
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

sbProfundidad = Spinbox(win, from_=0, to=100,increment=40 , textvariable=profundidad, font =fuente2)
sbProfundidad.place(x=280, y=250,width=50)

def ComboSelect(event):
    global layer
    global nFidu
    layer = combo.current() 
    btnCargarArchivo['state'] = 'normal'
    if layer == 2:
        nFidu=0
        btnFiducial['state'] = 'normal'
        btnFiducial['text'] = 'Fidu. 1'
        btnActivarCamara ['state'] = 'normal'

#ComboBox
combo = ttk.Combobox(win)
combo.place(x=75, y=255)

combo["values"] = ["Drill", "Top Layer", "Bottom Layer"]
combo["width"] = ["11"]
combo.bind("<<ComboboxSelected>>", ComboSelect)

#Canvas
canv = Canvas(win, width=350, height=230,bg='white')
canv.place(x=520,y=40)
canv.create_line(30,210,30,10,fill='black',width=3)
canv.create_line(30,210,345,210,fill='black',width=3)
canv.create_text(340,220,text='X')
canv.create_text(15,15,text='Y')

def dirXPos1():
    global numPasos
    pasos = ''
    pasos = numPasos.get()
    if not '.' in pasos:
        pasos=pasos+'.0'
    dirXPos(pasos)
    
def dirXNeg1():
    global numPasos
    pasos = ''
    pasos = numPasos.get()
    if not '.' in pasos:
        pasos=pasos+'.0'
    dirXNeg(pasos)

def dirYPos1():
    global numPasos
    pasos = ''
    pasos = numPasos.get()
    if not '.' in pasos:
        pasos=pasos+'.0'
    dirYPos(pasos)

def dirYNeg1():
    global numPasos
    pasos = ''
    pasos = numPasos.get()
    if not '.' in pasos:
        pasos=pasos+'.0'
    dirYNeg(pasos)

def dirZPos1():
    global numPasos
    pasos = ''
    pasos = numPasos.get()
    if not '.' in pasos:
        pasos=pasos+'.0'
    dirZPos(pasos)

def dirZNeg1():
    global numPasos
    pasos = ''
    pasos = numPasos.get()
    if not '.' in pasos:
        pasos=pasos+'.0'
    dirZNeg(pasos)

def ResetCero():
    global nFidu
    resetZero()
    nFidu=0
    btnFiducial['state'] = 'normal'
    btnFiducial['text'] = 'Fidu. 1'

def ResetCeroZ():
    global nFidu
    resetZeroZ()

def HomeXY():
    homeXY()

def SpindleOn():
    global isSpindleOn
    if isSpindleOn:
        btnActivarSpindle['text'] = 'Activar Spindle'
        spindleOff()
        isSpindleOn=False
    else:
        btnActivarSpindle['text'] = 'Desac. Spindle'
        spindleOn()
        isSpindleOn=True
    
def autoCalibrar():
    messagebox.showinfo("Autocalibrar", "¡Coloque los electrodos, por favor!")
    while not GPIO.input(23):
        dirZNeg("0.04")
    ResetCeroZ()
    dirZPos("3.0")
    messagebox.showinfo("Finalizada", "¡Calibración finalizada, remueva el electrodo, por favor!")

def CargarArchivo():
    listbox.delete(0, END)
    NombreArchivo = askopenfilename(filetypes=(("all files","*.*"),("NC Files","*.nc"),("Txt","*.txt")))
    if NombreArchivo:
        try:
            global GCode
            global layer
            Archivo = open (NombreArchivo,'r')
            GCode = Archivo.read()
            Archivo.close()
            time.sleep(0.1)
            btnEnviarArchivo['state'] = 'normal'
            lbProgress.config(text=str("Progreso: 0/" + str(len(GCode.splitlines())) + " | 0%"  ))
            getVectorCord(NombreArchivo, GCode) # Obtiene las coordenas de archivo en tipo float
            graficar() # Grafica el GCode Cargado
            if layer == 2:
                GCode = getGcodeRotated()
                Archivo = open ('GcodeRotado.nc','r')
                for line in Archivo:
                    listbox.insert(END, line)
                Archivo.close()
                time.sleep(0.1)
                Archivo = open ('GcodeRotado.nc','r')
                GCode = Archivo.read()
                Archivo.close()
                time.sleep(0.1)
            else:
                Archivo = open (NombreArchivo,'r')
                for line in Archivo:
                    listbox.insert(END, line)
                Archivo.close()
        except: 
            showerror("Open Source File", "Failed to read file")
        return

def sendingGCode():
    global GCode
    nLine = 0
    global isSendingGCode
    global isStopSending
    global profundidad
    print("Enviar Archivo")
    linea=GCode.splitlines() #Convierte el String en Array
    btnCargarArchivo['state'] = 'disable'
    btnActivarCamara['state'] = 'disable'
    btnActivarSpindle['state'] = 'disable'
    btnAutoCalibracion['state'] = 'disable'
    btnDirXNeg['state'] = 'disable'
    btnDirXPos['state'] = 'disable'
    btnDirYNeg['state'] = 'disable'
    btnDirYPos['state'] = 'disable'
    btnDirZNeg['state'] = 'disable'
    btnDirZPos['state'] = 'disable'
    btnRstCero['state'] = 'disable'
    btnHomeXY['state']='disable'
    btnDetenerEnvio['state'] = 'normal'
    while isSendingGCode:
        if not isStopSending:
            enviarGCode(linea[nLine],str(int(profundidad.get())/1000))
            nLine=nLine+1
            lbProgress.config(text=str("Progreso: " + str(nLine) + "/" + str(len(linea)) + " | " + str(int(nLine/len(linea)*100))+ "%"))
            if nLine==len(linea):
                isSendingGCode=False
                isStopSending=True
                nLine=0
                messagebox.showinfo("Finalizado", "¡Envío de código G finalizado!")
                btnActivarCamara['state'] = 'normal'
                btnActivarSpindle['state'] = 'normal'
                btnAutoCalibracion['state'] = 'normal'
                btnDirXNeg['state'] = 'normal'
                btnDirXPos['state'] = 'normal'
                btnDirYNeg['state'] = 'normal'
                btnDirYPos['state'] = 'normal'
                btnDirZNeg['state'] = 'normal'
                btnDirZPos['state'] = 'normal'
                btnRstCero['state']='normal'
                btnHomeXY['state']='normal'
                btnEnviarArchivo['state']='disable'
                btnEnviarArchivo['text'] = 'Enviar Archivo'
                btnDetenerEnvio['state'] = 'disable'

def EnviarArchivo():
    global isStopSending
    global isSendingGCode

    if isSendingGCode and not isStopSending: #Entra cuando se pausa el envio
        isStopSending = True
        btnEnviarArchivo['text'] = 'Seguir Enviando'
    elif not isSendingGCode and isStopSending: #Entra cuando se va a empezar a enviar
        btnEnviarArchivo['text'] = 'Pausar Envío'
        #Define Hilo del envio de GCode
        hiloGCode = threading.Thread(target=sendingGCode)
        isSendingGCode=True
        isStopSending=False
        hiloGCode.start()
    else: #Entra cuando se está enviando
        btnEnviarArchivo['text'] = 'Pausar Envío'
        isStopSending=False
    
def DetenerEnvio():
    global isSendingGCode
    global isStopSending
    global nLine
    isSendingGCode=False    
    isStopSending=True
    time.sleep(0.2)
    spindleOff()
    dirZPos("3.0")
    nLine=0
    messagebox.showinfo("Detenido", "¡Envío de código G detenido!")
    homeXY()
    btnActivarCamara['state'] = 'normal'
    btnActivarSpindle['state'] = 'normal'
    btnAutoCalibracion['state'] = 'normal'
    btnDirXNeg['state'] = 'normal'
    btnDirXPos['state'] = 'normal'
    btnDirYNeg['state'] = 'normal'
    btnDirYPos['state'] = 'normal'
    btnDirZNeg['state'] = 'normal'
    btnDirZPos['state'] = 'normal'
    btnRstCero['state']='normal'
    btnHomeXY['state']='normal'
    btnEnviarArchivo['state']='normal'
    btnEnviarArchivo['text'] = 'Enviar Archivo'
    btnDetenerEnvio['state'] = 'disable'

def startReco():
    global isCameraOn
    global isRecog
    if isCameraOn and isRecog:
        isCameraOn = False
        isRecog = False
        btnEmpezarRec['text'] = 'Empezar Reco.'
        btnActivarCamara['text'] = 'Activar Camara'
        btnActivarCamara ['state'] = 'normal'
        btnEmpezarRec ['state'] = 'disable'
    else:
        isCameraOn = True
        isRecog = True
        time.sleep(0.5)
        btnEmpezarRec['text'] = 'Detener Reco.'
        btnActivarCamara ['state'] = 'disable'
        #Define Hilo de la camara
        hiloCam = threading.Thread(target=scCam)
        hiloCam.start()
        
def scCam():
    centro = []
    global isCameraOn
    global isRecog
    cap=cv2.VideoCapture(0)
    time.sleep(0.1)
    while isCameraOn and isRecog:
        _, frame = cap.read()
        frame = cv2.rotate(frame,cv2.ROTATE_180)
        vector = cv2.resize(frame, (320,240))
        cv2image = cv2.cvtColor(vector, cv2.COLOR_BGR2RGBA)
        grayImage=cv2.cvtColor(cv2image,cv2.COLOR_BGR2GRAY)
        circles=cv2.HoughCircles(grayImage,cv2.HOUGH_GRADIENT,2,400, # Encuentra los circulos
        param1=80,param2=40,
        minRadius=30,maxRadius=45)
        try:
            circles=np.uint16(np.around(circles))
            centro=[circles[0][0][0],circles[0][0][1]] # Guarda las cordenadas del centro del circulo
            print(str(centro[0]) + " , " + str(centro[1]))
            cv2.circle(cv2image,(centro[0],centro[1]),circles[0][0][2],(0,255,0),2) #Dibuja el circulo
            cv2.circle(cv2image,(circles[0][0][0],circles[0][0][1]),2,(0,0,255),3) #Dibuja un punto el centro
            autoSearchCenter(centro[0],centro[1])
        except:
            print("No Circles")
        cv2.rectangle(cv2image, (120, 80), (200, 160), (252, 255, 0), 1,1) #Dibuja un rectangulo   
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lbVideo.imgtk = imgtk
        lbVideo.configure(image=imgtk)
        time.sleep(0.1)
    cap.release()
    cv2.destroyAllWindows()
    time.sleep(0.2)
    img = PhotoImage(file='ImagenFondo.png')
    lbVideo.configure(image=img)

def autoSearchCenter(x,y):
    global isCameraOn
    global contCirRec
    global isRecog
    if x>120 and x<200 and y>80 and y<160:
        if x>161:
            contCirRec = 0
            dirXPos("0.04")
        elif x<159:
            contCirRec = 0
            dirXNeg("0.04")
        elif x>=159 and x<=161:
            print("X Centered")
        if y<119:
            contCirRec = 0
            dirYPos("0.04")
        elif y>121:
            contCirRec = 0
            dirYNeg("0.04")
        elif  y>=119 and y<=121:
            print("Y Centered")
            if x>=159 and x<=161:
                contCirRec = contCirRec + 1
                print("Centrados ambos :) " + str(contCirRec))
            else:
                contCirRec = 0
    if contCirRec == 3:
        messagebox.showinfo("Finalizada", "¿Fiducial reconocido?")
        isCameraOn = False
        isRecog = False
        contCirRec = 0
        btnEmpezarRec['text'] = 'Empezar Reco.'
        btnEmpezarRec['state'] = 'disable'
        btnActivarCamara['state'] = 'normal'
        btnActivarCamara['text'] = 'Activar Camara'
  
def CameraOn():
    global isCameraOn
    
    if isCameraOn:
        isCameraOn = False
        btnActivarCamara['text'] = 'Activar Camara'
        btnEmpezarRec ['state'] = 'disable'
    else:
        isCameraOn = True
        btnEmpezarRec ['state'] = 'normal'
        btnActivarCamara['text'] = 'Desac. Camara'
        #Define Hilo de la camara
        hiloCam2 = threading.Thread(target=camOnTr)
        hiloCam2.start()

def camOnTr():
    global isCameraOn
    global isRecog
    cap=cv2.VideoCapture(0)
    time.sleep(0.1)
    while isCameraOn and not isRecog:
        _, frame = cap.read()
        frame = cv2.rotate(frame,cv2.ROTATE_180)
        vector = cv2.resize(frame, (320,240))
        cv2image = cv2.cvtColor(vector, cv2.COLOR_BGR2RGBA)
        try:
            cv2.rectangle(cv2image, (120, 80), (200, 160), (252, 255, 0), 1,1) #Dibuja un rectangulo   
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lbVideo.imgtk = imgtk
            lbVideo.configure(image=imgtk)
        except:
            print("No Circles")
        time.sleep(0.1)
    cap.release()
    cv2.destroyAllWindows()
    time.sleep(0.1)
    img = PhotoImage(file='ImagenFondo.png')
    lbVideo.configure(image=img)

# def cordActual():
#     print("X: " + str(getX()) + " | Y: " + str(getY()))

def fiducials():
    global nFidu
    if nFidu == 0:
        dirXPos("0.8")
        dirYPos("47.12")
        resetZero() 
        btnFiducial['text'] = 'Fidu. 2'
        saveFidu(nFidu)
        nFidu = nFidu + 1
    elif nFidu == 1:
        dirXPos("0.8")
        dirYPos("47.12")
        saveFidu(nFidu)
        nFidu = 0
        btnFiducial['state'] = 'disable'

def graficar():
    global layer
    global maxCordNum
    vecG01 = np.array([[]])
    vecG00 = np.array([[]])
    indG0 = np.array([[]])
    vec0 = np.array([[]])
    vec1 = np.array([[]])
    maxCord = []
    colorLinea = ''

    if layer==0:
        colorLinea='green'
    elif layer==1:
        colorLinea='red'
    elif layer==2:
        colorLinea='blue'
    (vecG01,vecG00, indG0)=getMatrizG01()
    if maxCordNum == 0:
        if layer == 1 or layer == 2:
            maxCord.append(np.amax(vecG00)) 
            maxCord.append(np.amax(vecG01))
            maxCordNum = np.amax(maxCord)
            maxCordNum = 200/maxCordNum
        else:
            maxCord.append(np.amax(vecG00)) 
            maxCordNum = np.amax(maxCord)
            maxCordNum = 180/maxCordNum
    print ("normalizado: "+str(maxCordNum))
    par = 0
    print("*********************************")
    nG00=0
    i=-1
    if layer == 1 or layer == 2:
        for coor in vecG01:
            i = i + 1
            if indG0[nG00]-8-2*nG00-nG00 == i: # Si es una linea siguiente a un G00
                vec1=vecG00[nG00]
                vec0=coor
                if layer == 1 or layer == 2:
                    canv.create_line(vec1[0]*maxCordNum+30,((vec1[1]*-1)+200/maxCordNum)*maxCordNum + 15,vec0[0]*maxCordNum+30,((vec0[1]*-1)+200/maxCordNum)*maxCordNum + 15,fill=colorLinea)
                nG00 = nG00 + 1
                par=0
            else:
                if par==0: # si la linea es impar
                    vec1=coor   
                    par = par +1
                    if layer == 1 or layer == 2:
                        canv.create_line(vec0[0]*maxCordNum+30,((vec0[1]*-1)+200/maxCordNum)*maxCordNum + 15 ,vec1[0]*maxCordNum+30,((vec1[1]*-1)+200/maxCordNum)*maxCordNum + 15,fill=colorLinea)
                else: # Si es par
                    vec0=coor
                    if layer == 1 or layer == 2:
                        canv.create_line(vec1[0]*maxCordNum+30,((vec1[1]*-1)+200/maxCordNum)*maxCordNum + 15 ,vec0[0]*maxCordNum+30,((vec0[1]*-1)+200/maxCordNum)*maxCordNum + 15,fill=colorLinea)
                    par=0
    else:
        for coorActual in vecG00:
            if coorActual[0] == 0.0:
                continue
            else:
                print(coorActual[0])
                canv.create_oval((coorActual[0])*maxCordNum + 30,((coorActual[1]*-1)+180/maxCordNum)*maxCordNum + 15,(coorActual[0])*maxCordNum+32,((coorActual[1]*-1)+180/maxCordNum)*maxCordNum+17,fill=colorLinea,width=3)

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

#HOME
btnHomeXY = Button(win, text = 'Home XY', font = fuente2, command = HomeXY ,height = 1, width = 8)
btnHomeXY.place(x=350,y=150)

#Cargar Archivo
btnCargarArchivo = Button(win, text = 'Cargar Archivo', font = fuente2, command = CargarArchivo,height = 1, width = 10, state='disable')
btnCargarArchivo.place(x=30,y=300)

#Enviar Archivo
btnEnviarArchivo = Button(win, text = 'Enviar Archivo', font = fuente2, command = EnviarArchivo,height = 1, width = 10, state='disable')
btnEnviarArchivo.place(x=350,y=300)

#Detener envío
btnDetenerEnvio = Button(win, text = 'Detener Envío', font = fuente2, command = DetenerEnvio,height = 1, width = 10, state='disable')
btnDetenerEnvio.place(x=350,y=250)

#Activar Camara
btnActivarCamara = Button(win, text = 'Activar Camara', font = fuente2, command = CameraOn,height = 1, width = 12, state='disable')
btnActivarCamara.place(x=645,y=580)

#Empezar Rerconocimiento
btnEmpezarRec = Button(win, text = 'Empezar Reco.', font = fuente2, command = startReco,height = 1, width = 11, state='disable')
btnEmpezarRec.place(x=520,y=580)

#Activar Spindle
btnActivarSpindle = Button(win, text = 'Activar Spindle', font = fuente2, command = SpindleOn,height = 1, width = 15)
btnActivarSpindle.place(x=30,y=120)

#AutoCalibracion
btnAutoCalibracion= Button(win, text = 'Autocalibrar', font = fuente2, command = autoCalibrar,height = 1, width = 15)
btnAutoCalibracion.place(x=30,y=170)

#Fiducials
btnFiducial = Button(win, text = 'Fidu. 1', font = fuente2, command = fiducials,height = 1, width = 8, state='disable')
btnFiducial.place(x=780,y=580)

# # #Cordenada actual
# btnCordenadaActual = Button(win, text = 'Cord. Actual', font = fuente2, command = cordActual,height = 1, width = 15)
# btnCordenadaActual.place(x=200,y=620)

# #Graficar
# btnGraficar = Button(win, text = 'Graficar', font = fuente2, command = graficar,height = 1, width = 15)
# btnGraficar.place(x=400,y=620)

win.mainloop()

