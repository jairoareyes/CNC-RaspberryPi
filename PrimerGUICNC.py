from tkinter import *
import tkinter.font
from MovMotores import *


## GUI DEFINITIONS
win = Tk()
win.geometry("500x700+0+0")
win.title("CNC Controller")
myFont = tkinter.font.Font(family = 'Arial', size = 12)
fuente2 = tkinter.font.Font(family = 'Times New Roman', size = 11)

##WIDGETS

#ledButton = Button(win, text = 'Turn LED on', font = myFont, command = ledToggle, bg = 'bisque2', height = 1, width = 24)
#ledButton.grid(row=0,column=1)
numPasos= ""
def funSB():
    global numPasos
    numPasos = sbAvMM.get()


#LabelFrames
lfCalibracion = LabelFrame(win, text="Calibración",bd=4,font=fuente2)
lfCalibracion.place(x=10,y=90, width=480, height=200)

#Labels
lbAvanzar = Label(win, text="Avanzar (mm)", font=fuente2)
lbAvanzar.place(x=30,y=110)

#Spinbox
sbAvMM = Spinbox(win, from_=0, to=50,format='%.1f',increment=0.1, command=funSB, font =fuente2)
sbAvMM.place(x=130, y=110,width=50)



#numPasos = sbAvMM.get()

def dirXPos1():
    global numPasos
    dirXPos(numPasos)
    
def dirXNeg1():
    global numPasos
    dirXNeg(numPasos)

def dirYPos1():
    global numPasos
    dirYPos(numPasos)

def dirYNeg1():
    global numPasos
    dirYNeg(numPasos)

def dirZPos1():
    global numPasos
    dirZPos(numPasos)

def dirZNeg1():
    global numPasos
    dirZNeg(numPasos)


 
# Eje X
btnDirXPos = Button(win, text = 'X+', font = myFont, command = dirXPos1, height = 1, width = 3)
btnDirXPos.place(x=300,y=150)

btnDirXNeg = Button(win, text = 'X-', font = myFont, command = dirXNeg1, height = 1, width = 3)
btnDirXNeg.place(x=170,y=150)

#Eje Y
btnDirYPos = Button(win, text = 'Y+', font = myFont, command = dirYPos1, height = 1, width = 3)
btnDirYPos.place(x=235,y=120)

btnDirYNeg = Button(win, text = 'Y-', font = myFont, command = dirYNeg1, height = 1, width = 3)
btnDirYNeg.place(x=235,y=180)

#Eje Z
btnDirZPos = Button(win, text = 'Z+', font = myFont, command = dirZPos1 ,height = 1, width = 3)
btnDirZPos.place(x=400,y=130)

btnDirZNeg = Button(win, text = 'Z-', font = myFont, command = dirZNeg1 ,height = 1, width = 3)
btnDirZNeg.place(x=400,y=170)



