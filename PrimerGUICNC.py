from tkinter import *
import tkinter.font
import RPi.GPIO as GPIO #Libreria GPIO
import time #Libreria de tiempo
GPIO.setmode(GPIO.BCM) #Se pone para que la numeracion de pines sea la del diagrama

## hardware
#led = LED(14)

DirX = 16
DirY = 20
DirZ = 21

StpX = 13
StpY = 19 
StpZ = 26

GPIO.setup(DirX, GPIO.OUT)
GPIO.setup(DirY, GPIO.OUT)
GPIO.setup(DirZ, GPIO.OUT)

GPIO.setup(StpX, GPIO.OUT) 
GPIO.setup(StpY, GPIO.OUT) 
GPIO.setup(StpZ, GPIO.OUT)



## GUI DEFINITIONS
win = Tk()
win.title("CNC Controller")
myFont = tkinter.font.Font(family = 'Arial', size = 12, weight = "bold")

## EVENT FUNC

##def ledToggle():
##	if led.is_lit:
##		led.off()
##		ledButton["text"] = "Turn LED on"
##	else:
##		led.on()
##		ledButton["text"] = "Turn LED off"



def dirXPos():
        GPIO.output(DirX,1)
        time.sleep(0.1)
        GPIO.output(StpX,1)


##WIDGETS

#ledButton = Button(win, text = 'Turn LED on', font = myFont, command = ledToggle, bg = 'bisque2', height = 1, width = 24)
#ledButton.grid(row=0,column=1)

# Eje X
btnDirXPos = Button(win, text = 'X+', font = myFont,command = dirXPos , bg = 'grey', height = 1, width = 12)
btnDirXPos.grid(row=1,column=3)

btnDirXNeg = Button(win, text = 'X-', font = myFont, bg = 'grey', height = 1, width = 12)
btnDirXNeg.grid(row=1,column=1)

#Eje Y
btnDirYPos = Button(win, text = 'Y+', font = myFont, bg = 'grey', height = 1, width = 12)
btnDirYPos.grid(row=0,column=2)

btnDirYNeg = Button(win, text = 'Y-', font = myFont, bg = 'grey', height = 1, width = 12)
btnDirYNeg.grid(row=2,column=2)

#Eje Z
btnDirZPos = Button(win, text = 'Z+', font = myFont, bg = 'grey', height = 1, width = 12)
btnDirZPos.grid(row=0,column=5)

btnDirZNeg = Button(win, text = 'Z-', font = myFont, bg = 'grey', height = 1, width = 12)
btnDirZNeg.grid(row=2,column=5)

