import numpy as np
from os import remove

x = 0
y = 0
angle = 0
matrizG01 = []
matrizG00 = []
GCode = ""
GCode2 = []
nG0=[]

corFidu = np.array([[],[]])
def rstZero():
    global x
    global y
    x=0
    y=0

def addX(_x):
    global x
    x+=_x

def addY(_y):
    global y
    y+=_y

def getX():
    global x
    return x

def getY():
    global y
    return y

def saveFidu(pos):
    global x
    global y
    global corFidu
    global angle
    if pos==0:
        corFidu = ([[x,y]])    
    else:
        dx = 0
        dy = 0
        vec = np.array([[]])
        vec = ([[x,y]])
        corFidu=np.concatenate((corFidu, vec))
        dx = corFidu[1,0]-corFidu[0,0]
        dy = corFidu[1,1]-corFidu[0,1]
        h = (dx**2+dy**2)**(1/2)
        angle = np.arcsin((dy/h))
        angle = np.degrees(angle)
        print("------- Angulo -------")
        print(angle)   
        #calculateRotation(np.degrees(angle))
    print(corFidu)

def calculateRotation(angle):
    global matrizG01
    global matrizG00
    global GCode
    global GCode2
    subStrX = ''
    subStrY = ''
    strRotatedG01 = []
    strRotatedG00 = []
    n=0
    m=0
    print("------- Angulo 2 -------")
    print(angle)   
    theta = np.radians(angle) # Define el angulo de rotación
    # Calcula la matriz de rotación
    r = np.array(( (np.cos(theta), -np.sin(theta)), 
                    (np.sin(theta),  np.cos(theta)) ))

    for vec01 in matrizG01: # Rota cada coordenada G01
        vec01 = r.dot(vec01)
        subStrX = str(vec01[0:1]*-1) # Invierte el signo del eje X
        subStrY = str(vec01[1:])
        if subStrX.find("]") < 8:
            subStrX = 'X' + subStrX[1:subStrX.find("]")-0] # Convierte el valor cauculado a Str con n decimales
        else:
            subStrX = 'X' + subStrX[1:subStrX.find(".")+5] # Convierte el valor cauculado a Str con 4 decimales
        if subStrY.find("]") < 8:
            subStrY = 'Y' + subStrY[1:subStrY.find("]")-0] # Convierte el valor cauculado a Str con n decimales
        else:
            subStrY = 'Y' + subStrY[1:subStrY.find(".")+5] # Convierte el valor cauculado a Str con 4 decimales
        strRotatedG01.append('G01 '+subStrX + subStrY)

    for vec00 in matrizG00: # Rota cada coordenada G00
        vec00 = r.dot(vec00)
        subStrX = str(vec00[0:1]*-1) # Invierte el signo del eje X
        subStrY = str(vec00[1:])
        if subStrX.find("]") < 8:
            subStrX = 'X' + subStrX[1:subStrX.find("]")-0] # Convierte el valor cauculado a Str con n decimales
        else:
            subStrX = 'X' + subStrX[1:subStrX.find(".")+5] # Convierte el valor cauculado a Str con 4 decimales
        if subStrY.find("]") < 8:
            subStrY = 'Y' + subStrY[1:subStrY.find("]")-0] # Convierte el valor cauculado a Str con n decimales
        else:
            subStrY = 'Y' + subStrY[1:subStrY.find(".")+5] # Convierte el valor cauculado a Str con 4 decimales
        strRotatedG00.append('G00 '+subStrX + subStrY)

    lineas=GCode.splitlines() # Codifica el String
    for line in lineas: # Reemplaza las coordenadas rotadas en el GCode
        if 'G01 X' in line:
            line = line.replace(line,strRotatedG01[n])
            line=line.replace("]","") #Quita los corchetes
            n=n+1
        elif 'G00 X' in line:
            line = line.replace(line,strRotatedG00[m])
            line=line.replace("]","") #Quita los corchetes
            m=m+1
        GCode2.append(line)

    try:
        remove("GcodeRotado.nc")
    except:
        print('Archivo GCode Rotado no encontrado')
    
    f = open ('GcodeRotado.nc','w')
    for line2 in GCode2:
        f.write(str(line2))
        f.write("\n")
    f.close()

def getGcodeRotated():
    global GCode2
    global angle
    calculateRotation(angle)
    return GCode2

def getMatrizG01():
    global matrizG01
    global matrizG00
    global nG0
    return (matrizG01,matrizG00,nG0)

def getVectorCord(NombreArchivo, _gCode):
    global GCode
    GCode = _gCode
    v1 = np.array((0,0))
    v2 = np.array((0,0))
    global matrizG01
    global matrizG00
    global nG0
    matrizG00 = []
    matrizG01 = []
    nG0 = []
    nG0line = 0
    if NombreArchivo:
        try:
            Archivo = open (NombreArchivo,'r')
            for line in Archivo:
                if 'G01 X' in line: # Convierte el string de las cordenadas a float
                    v1=(float(line[line.find("X")+1:line.find("Y"):]),float(line[line.find("Y")+1:]))
                    matrizG01.append(v1) # Añade cada vector a una matriz
                elif 'G00 X' in line: 
                    v2=(float(line[line.find("X")+1:line.find("Y"):]),float(line[line.find("Y")+1:]))
                    matrizG00.append(v2) # Añade cada vector a una matriz
                    nG0.append(nG0line)
                nG0line = nG0line + 1
            Archivo.close()            
        except:
            showerror("Open Source File", "Failed to read file 2")
        return
