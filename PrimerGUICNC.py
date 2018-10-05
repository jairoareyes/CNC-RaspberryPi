from tkinter import *
import tkinter.font
from MovMotores import *


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


##def dirXPos():
##        GPIO.output(DirX,1)
##        print("X Positivo")
##        PasosX()
##
##def dirXNeg():
##        GPIO.output(DirX,0)
##        print("X Negativo")
##        PasosX()
##
##def dirYPos():
##        GPIO.output(DirY,1)
##        print("Y Positivo")
##        PasosY()
##
##def dirYNeg():
##        GPIO.output(DirY,0)
##        print("Y Negativo")
##        PasosY()
##
##def dirZPos():
##        GPIO.output(DirZ,1)
##        print("Z Positivo")
##        PasosZ()
##
##def dirZNeg():
##        GPIO.output(DirZ,0)
##        print("Z Negativo")
##        PasosZ()
##
##
##
##def PasosX():
##        for i in range (100):
##                GPIO.output(StpX,1)
##                time.sleep(0.001)
##                GPIO.output(StpX,0)
##                time.sleep(0.001)
##        
##def PasosY():
##        for i in range (100):
##                GPIO.output(StpY,1)
##                time.sleep(0.001)
##                GPIO.output(StpY,0)
##                time.sleep(0.001)
##        
##def PasosZ():
##        for i in range (100):
##                GPIO.output(StpZ,1)
##                time.sleep(0.001)
##                GPIO.output(StpZ,0)
##                time.sleep(0.001)
        

##WIDGETS

#ledButton = Button(win, text = 'Turn LED on', font = myFont, command = ledToggle, bg = 'bisque2', height = 1, width = 24)
#ledButton.grid(row=0,column=1)

# Eje X
btnDirXPos = Button(win, text = 'X+', font = myFont, command = dirXPos , bg = 'grey', height = 1, width = 12)
btnDirXPos.grid(row=1,column=3)

btnDirXNeg = Button(win, text = 'X-', font = myFont, command = dirXNeg, bg = 'grey', height = 1, width = 12)
btnDirXNeg.grid(row=1,column=1)

#Eje Y
btnDirYPos = Button(win, text = 'Y+', font = myFont, command = dirYPos , bg = 'grey', height = 1, width = 12)
btnDirYPos.grid(row=0,column=2)

btnDirYNeg = Button(win, text = 'Y-', font = myFont, command = dirYNeg , bg = 'grey', height = 1, width = 12)
btnDirYNeg.grid(row=2,column=2)

#Eje Z
btnDirZPos = Button(win, text = 'Z+', font = myFont, command = dirZPos , bg = 'grey', height = 1, width = 12)
btnDirZPos.grid(row=0,column=5)

btnDirZNeg = Button(win, text = 'Z-', font = myFont, command = dirZNeg , bg = 'grey', height = 1, width = 12)
btnDirZNeg.grid(row=2,column=5)

