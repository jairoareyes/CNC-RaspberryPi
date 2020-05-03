import time 
import serial
from PosYRot import *  
           
ser = serial.Serial(            
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
 )

def dirXPos(valMM):
	var='G21G91G00X'
	var+=valMM
	var+='F200\r\n'
	ser.write(var.encode())
	addX(float(valMM)*1)
	time.sleep(0.02)
	readSerial()

def dirXNeg(valMM):
	var='G21G91G00X-'
	var+=valMM
	var+='F200\r\n'
	ser.write(var.encode())
	addX(float(valMM)*-1)
	time.sleep(0.02)
	readSerial()

def dirYPos(valMM):
	var='G21G91G00Y'
	var+=valMM
	var+='1F200\r\n'
	ser.write(var.encode())
	addY(float(valMM)*1)
	time.sleep(0.02)       
	readSerial()

def dirYNeg(valMM):
	var='G21G91G00Y-'
	var+=valMM
	var+='F200\r\n'
	ser.write(var.encode())
	addY(float(valMM)*-1)
	time.sleep(0.02)
	readSerial()

def dirZPos(valMM):
	var='G21G91G1Z'
	var+=valMM
	var+='F300\r\n'
	ser.write(var.encode())
	time.sleep(0.02)
	readSerial()

def dirZNeg(valMM):
	var='G21G91G1Z-'
	var+=valMM
	var+='F300\r\n'
	ser.write(var.encode())
	time.sleep(0.02)
	readSerial()
		
def resetZero():
	var='G92X0Y0F100\r\n'
	ser.write(var.encode())
	time.sleep(0.02)
	rstZero() #reset cero en archivo pos
	print("reset cero")
	readSerial()
	
def resetZeroZ():
	var='G92Z0\r\n'
	ser.write(var.encode())
	time.sleep(0.02)
	readSerial()

def spindleOn():
	var='M03\r\n'
	ser.write(var.encode())

def spindleOff():
	var='M05\r\n'
	ser.write(var.encode())
	
def homeXY():
	var='G90G01X0F250\r\n'
	ser.write(var.encode())
	time.sleep(0.1)
	var='G90G01Y0F250\r\n'
	ser.write(var.encode())

def enviarGCode(valEnv,profundidad):
	if "G01 Z" in valEnv:
		profActual = 0.0
		profActual = float(valEnv[valEnv.find("Z")+1:])
		profActual = profActual - float(profundidad)
		valEnv="G01 Z" + str(profActual) #Adiciona el valor de profundidad
		valEnv = valEnv[0:valEnv.find(".")+5] # Convierte el valor cauculado a Str con 4 decimales
	elif "G00 X0Y0" in valEnv:
		spindleOff()
	elif "G00 X0.Y0." in valEnv:
		spindleOff()
	elif "G00 X-0.Y0." in valEnv:
		spindleOff()
			
					
	valEnv=valEnv.replace(" ","") #Quita espacios en blanco
	valEnv=valEnv.replace("G00","G01") #Quita Expresiones G00
	print('valor enviado: '+valEnv)
	valEnv+='\r\n'
	ser.write(valEnv.encode())
	readSerial()

def readSerial():
	txt=b''
	recive=False
	while not recive:
		while ser.inWaiting() > 0:
			txt += ser.read()
		if len(txt)>1:
			print(txt)
			recive = True
		time.sleep(0.1)
