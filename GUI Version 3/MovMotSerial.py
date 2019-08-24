import time 
import serial
    
           
ser = serial.Serial(            
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
 )

#txt = b''
#~ txt2=""
#~ while True:
    #~ txt=b''
    #~ var = input("Introducir un Comando: ")
    #~ var+='\r\n'
    #~ ser.write(var.encode())
    #~ time.sleep(0.2)
    #~ while ser.inWaiting() > 0:
        #~ txt += ser.read()
    #~ if len(txt)>1:
        #~ print(txt)
#txt=b''

def dirXPos(valMM):
	txt=b''
	var='G21G91G1X'
	var+=valMM
	var+='1F100\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	print("X Positivo "+var)
	readSerial()

def dirXNeg(valMM):
	txt=b''
	var='G21G91G1X-'
	var+=valMM
	var+='1F100\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	print("X Negativo "+var)
	readSerial()

def dirYPos(valMM):
	txt=b''
	var='G21G91G1Y'
	var+=valMM
	var+='1F100\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	print("Y Positivo "+var)        
	readSerial()


def dirYNeg(valMM):
	txt=b''
	var='G21G91G1Y-'
	var+=valMM
	var+='1F100\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	print("Y Negativo "+var)
	readSerial()

def dirZPos(valMM):
	txt=b''
	var='G21G91G1Z'
	var+=valMM
	var+='1F100\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	print("Z Positivo "+var)
	readSerial()

def dirZNeg(valMM):
	txt=b''
	var='G21G91G1Z-'
	var+=valMM
	var+='1F100\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	print("Z Negativo "+var) 
	readSerial()
		
def resetZero():
	txt=b''
	var='G92X0Y0Z0\r\n'
	ser.write(var.encode())
	time.sleep(0.2)
	print("Reset Zero") 
	readSerial()
	
def enviarGCode(valEnv):
	#txt=b''
	#~ var='G21G91G1Z-'
	#~ var+=valMM
	#~ var+='1F100\r\n'
	valEnv=valEnv.replace(" ","") #Quita espacios en blanco
	print('valor enviado: '+valEnv)
	valEnv+='\r\n'
	ser.write(valEnv.encode())
	time.sleep(0.1)
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
