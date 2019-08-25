# Falta Rotar los archivos que comienzan con G00

from tkinter import *
import tkinter.font
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import numpy as np
import time

## GUI DEFINITIONS
win = Tk()
win.geometry("500x700+50+0")
win.title("CNC Controller")
myFont = tkinter.font.Font(family = 'Arial', size = 12)
fuente2 = tkinter.font.Font(family = 'Times New Roman', size = 11)

#Valirables
GCode = StringVar(win)
matriz = []

#Cargar Archivo
lfCargarArchivo = LabelFrame(win, text="Cargar Archivo",bd=4,font=fuente2)
lfCargarArchivo.place(x=10,y=220, width=480, height=400)

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

def calculateRotation():
	global matriz
	global GCode
	GCode2=[]
	subStrX=''
	subStrY=''
	strRotated=[]
	n=0
	theta = np.radians(30) # Define el angulo de rotación
	# Calcula la matriz de rotación
	r = np.array(( (np.cos(theta), -np.sin(theta)), 
				   (np.sin(theta),  np.cos(theta)) ))
	print('***************************')
	print('rotation matrix:')
	print(r)
	print('***************************')
	for vec in matriz: # Convierte el punto vectorizado a GCode
		vec = r.dot(vec)
		subStrX = str(vec[0:1])
		subStrY = str(vec[1:])
		subStrX = 'X' + subStrX[1:subStrX.find(".")+5] # Convierte el valor cauculado a Str con 4 decimales
		subStrY = 'Y' + subStrY[1:subStrY.find(".")+5]
		#strRotated = 'G01 '+subStrX + subStrY
		strRotated.append('G01 '+subStrX + subStrY)
	print (strRotated)
	print('***************************')
	lineas=GCode.splitlines() # Codifica el String
	for line in lineas:
		if 'G01 X' in line:
			line = line.replace(line,strRotated[n])
			n=n+1
		GCode2.append(line)
	print(GCode2)
	
	f = open ('GcodeRotado.nc','w')
	for line2 in GCode2:
		f.write(str(line2))
		f.write("\n")
	f.close()

def CargarArchivo():
	v = np.array((0,0))
	listbox.delete(0, END)
	NombreArchivo = askopenfilename(filetypes=(("all files","*.*"),("NC Files","*.nc"),("Txt","*.txt")))
	if NombreArchivo:
		try:
			global GCode
			global matriz
			Archivo = open (NombreArchivo,'r')
			GCode = Archivo.read()
			Archivo.close()
			time.sleep(0.1)
			Archivo = open (NombreArchivo,'r')
			for line in Archivo:
				if 'G01 X' in line: # Convierte el string de las cordenadas a float
					v=(float(line[line.find("X")+1:line.find("Y"):]),float(line[line.find("Y")+1:]))
					matriz.append(v) # Añade cada vector a una matriz
				listbox.insert(END, line)
			Archivo.close()
			print(matriz)
		except:
			showerror("Open Source File", "Failed to read file")
		return
		
#Cargar Archivo
btnCargarArchivo = Button(win, text = 'Cargar Archivo', font = fuente2, command = CargarArchivo,height = 1, width = 10)
btnCargarArchivo.place(x=30,y=250)

#Cargar Archivo
btnMakeRotation = Button(win, text = 'Make Rotation', font = fuente2, command = calculateRotation,height = 1, width = 10)
btnMakeRotation.place(x=200,y=250)

win.mainloop()
