import RPi.GPIO as GPIO #Libreria GPIO
import time #Libreria de tiempo
GPIO.setmode(GPIO.BCM) #Se pone para que la numeracion de pines sea la del diagrama

## hardware
#led = LED(14)


StpX = 16
StpY = 20
StpZ = 21

DirX = 13
DirY = 19 
DirZ = 26

GPIO.setup(DirX, GPIO.OUT)
GPIO.setup(DirY, GPIO.OUT)
GPIO.setup(DirZ, GPIO.OUT)

GPIO.setup(StpX, GPIO.OUT) 
GPIO.setup(StpY, GPIO.OUT) 
GPIO.setup(StpZ, GPIO.OUT)

def dirXPos(valMM):
        GPIO.output(DirX,1)
        print("X Positivo"+valMM)
        PasosX(valMM)

def dirXNeg(valMM):
        GPIO.output(DirX,0)
        print("X Negativo"+valMM)
        PasosX(valMM)

def dirYPos(valMM):
        GPIO.output(DirY,1)
        print("Y Positivo"+valMM)
        PasosY(valMM)

def dirYNeg(valMM):
        GPIO.output(DirY,0)
        print("Y Negativo"+valMM)
        PasosY(valMM)

def dirZPos(valMM):
        GPIO.output(DirZ,1)
        print("Z Positivo"+valMM)
        PasosZ(valMM)

def dirZNeg(valMM):
        GPIO.output(DirZ,0)
        print("Z Negativo"+valMM)
        PasosZ(valMM)



def PasosX(val):
        valNum=float(val)
        valNum=valNum*50
        for i in range (int(valNum)):
                GPIO.output(StpX,1)
                time.sleep(0.001)
                GPIO.output(StpX,0)
                time.sleep(0.001)
        
def PasosY(val):
        valNum=float(val)
        valNum=valNum*50
        for i in range (int(valNum)):
                GPIO.output(StpY,1)
                time.sleep(0.001)
                GPIO.output(StpY,0)
                time.sleep(0.001)
        
def PasosZ(val):
        valNum=float(val)
        valNum=valNum*50
        for i in range (int(valNum)):
                GPIO.output(StpZ,1)
                time.sleep(0.001)
                GPIO.output(StpZ,0)
                time.sleep(0.001)
                

