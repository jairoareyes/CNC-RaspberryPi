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
	txt=b''
	var='G21G91G00X'
	var+=valMM
	var+='1F200\r\n'
	ser.write(var.encode())
	addX(float(valMM)*1)
	time.sleep(0.2)
	readSerial()

def dirXNeg(valMM):
	txt=b''
	var='G21G91G00X-'
	var+=valMM
	var+='1F200\r\n'
	ser.write(var.encode())
	addX(float(valMM)*-1)
	time.sleep(0.2)
	readSerial()

def dirYPos(valMM):
	txt=b''
	var='G21G91G00Y'
	var+=valMM
	var+='1F200\r\n'
	ser.write(var.encode())
	addY(float(valMM)*1)
	time.sleep(0.1)       
	readSerial()

def dirYNeg(valMM):
	txt=b''
	var='G21G91G00Y-'
	var+=valMM
	var+='1F200\r\n'
	ser.write(var.encode())
	addY(float(valMM)*-1)
	time.sleep(0.1)
	readSerial()

def dirZPos(valMM):
	txt=b''
	var='G21G91G1Z'
	var+=valMM
	var+='1F300\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	readSerial()

def dirZNeg(valMM):
	txt=b''
	var='G21G91G1Z-'
	var+=valMM
	var+='1F300\r\n'
	ser.write(var.encode())
	time.sleep(0.01)
	readSerial()
		
def resetZero():
	txt=b''
	var='G92X0Y0Z0\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	rstZero() #reset cero en archivo pos
	print("reset cero")
	readSerial()
	
def resetZeroZ():
	txt=b''
	var='G92Z0\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	print("reset cero Z")
	readSerial()

def spindleOn():
	txt=b''
	var='M03\r\n'
	ser.write(var.encode())

def spindleOff():
	txt=b''
	var='M05\r\n'
	ser.write(var.encode())
	
def homeXY():
	txt=b''
	var='G90X0Y0\r\n'
	ser.write(var.encode())

def enviarGCode(valEnv):
	valEnv=valEnv.replace(" ","") #Quita espacios en blanco
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
		#print("No Recive!!!")
		time.sleep(0.1)
