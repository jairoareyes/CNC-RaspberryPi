# Rotacion de instrucciones G00 y G01 

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
matrizG01 = []
matrizG00 = []

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
	global matrizG01
	global matrizG00
	global GCode
	GCode2 = []
	subStrX = ''
	subStrY = ''
	strRotatedG01 = []
	strRotatedG00 = []
	n=0
	m=0
	theta = np.radians(-30) # Define el angulo de rotación
	# Calcula la matriz de rotación
	r = np.array(( (np.cos(theta), -np.sin(theta)), 
				   (np.sin(theta),  np.cos(theta)) ))
	print('***************************')
	print('rotation matrix:')
	print(r)
	print('***************************')
	for vec01 in matrizG01: # Rota cada coordenada G01
 
		vec01 = r.dot(vec01)
		subStrX = str(vec01[0:1])
		subStrY = str(vec01[1:])
		subStrX = 'X' + subStrX[1:subStrX.find(".")+5] # Convierte el valor cauculado a Str con 4 decimales
		subStrY = 'Y' + subStrY[1:subStrY.find(".")+5]
		strRotatedG01.append('G01 '+subStrX + subStrY)
	print (strRotatedG01)
	print('***************************')
	
	for vec00 in matrizG00: # Rota cada coordenada G00
		vec00 = r.dot(vec00)
		subStrX = str(vec00[0:1])
		subStrY = str(vec00[1:])
		subStrX = 'X' + subStrX[1:subStrX.find(".")+5] # Convierte el valor cauculado a Str con 4 decimales
		subStrY = 'Y' + subStrY[1:subStrY.find(".")+5]
		strRotatedG00.append('G00 '+subStrX + subStrY)
	print (strRotatedG00)
	print('***************************')
	
	lineas=GCode.splitlines() # Codifica el String
	for line in lineas: # Reemplaza las coordenadas rotadas en el GCode
		if 'G01 X' in line:
			line = line.replace(line,strRotatedG01[n])
			n=n+1
		elif 'G00 X' in line:
			line = line.replace(line,strRotatedG00[m])
			m=m+1
		GCode2.append(line)
	
	f = open ('GcodeRotado.nc','w')
	for line2 in GCode2:
		f.write(str(line2))
		f.write("\n")
	f.close()

def CargarArchivo():
	v1 = np.array((0,0))
	v2 = np.array((0,0))
	listbox.delete(0, END)
	NombreArchivo = askopenfilename(filetypes=(("all files","*.*"),("NC Files","*.nc"),("Txt","*.txt")))
	if NombreArchivo:
		try:
			global GCode
			global matrizG01
			Archivo = open (NombreArchivo,'r')
			GCode = Archivo.read()
			Archivo.close()
			time.sleep(0.1)
			Archivo = open (NombreArchivo,'r')
			for line in Archivo:
				if 'G01 X' in line: # Convierte el string de las cordenadas a float
					v1=(float(line[line.find("X")+1:line.find("Y"):]),float(line[line.find("Y")+1:]))
					matrizG01.append(v1) # Añade cada vector a una matriz
				elif 'G00 X' in line: 
					v2=(float(line[line.find("X")+1:line.find("Y"):]),float(line[line.find("Y")+1:]))
					matrizG00.append(v2) # Añade cada vector a una matriz
				
				listbox.insert(END, line) # Inserta la linea leida al ListBox
			Archivo.close()
			print("Matriz G01")
			print(matrizG01)
			print("Matriz G00")
			print(matrizG00)
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
