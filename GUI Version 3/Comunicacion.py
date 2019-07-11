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
txt2=""
while True:
    txt=b''
    var = input("Introducir un Comando: ")
    var+='\r\n'
    ser.write(var.encode())
    time.sleep(0.2)
    while ser.inWaiting() > 0:
        txt += ser.read()
    if len(txt)>1:
        print(txt)
        #txt2="".join(map(chr,txt))
        #~ txt2=str(txt, 'utf-8')
        #~ print('txt2: '+txt2)
        #~ if(txt2.find("ok")!=-1):
            #~ print ('It´s OK!')
    
    
