from tkinter import *
import tkinter.font
from MovMotores import *


## GUI DEFINITIONS
win = Tk()
win.geometry("800x500+0+0")
win.title("CNC Controller")
myFont = tkinter.font.Font(family = 'Arial', size = 12)


##WIDGETS

#ledButton = Button(win, text = 'Turn LED on', font = myFont, command = ledToggle, bg = 'bisque2', height = 1, width = 24)
#ledButton.grid(row=0,column=1)

# Eje X
btnDirXPos = Button(win, text = 'X+', font = myFont, command = dirXPos , height = 1, width = 3)
btnDirXPos.place(x=200,y=50)

btnDirXNeg = Button(win, text = 'X-', font = myFont, command = dirXNeg, bg = 'grey', height = 1, width = 6)
btnDirXNeg.place(x=50,y=50)

#Eje Y
btnDirYPos = Button(win, text = 'Y+', font = myFont, command = dirYPos , bg = 'grey', height = 1, width = 6)
btnDirYPos.place(x=125,y=10)

btnDirYNeg = Button(win, text = 'Y-', font = myFont, command = dirYNeg , bg = 'grey', height = 1, width = 6)
btnDirYNeg.place(x=125,y=90)

#Eje Z
btnDirZPos = Button(win, text = 'Z+', font = myFont, command = dirZPos , bg = 'grey', height = 1, width = 6)
btnDirZPos.place(x=350,y=10)

btnDirZNeg = Button(win, text = 'Z-', font = myFont, command = dirZNeg , bg = 'grey', height = 1, width = 6)
btnDirZNeg.place(x=350,y=90)

