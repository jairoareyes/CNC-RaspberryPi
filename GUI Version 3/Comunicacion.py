import serial

arduino = serial.Serial('/dev/tty1', 9600)

print("Starting!")

while True:
      comando = input('Introduce un comando: ') #Input
      flagCharacter = 'k'
      arduino.write(flagCharacter.encode()) #Mandar un comando hacia Arduino
      if comando == 'H':
            print('LED ENCENDIDO')
      elif comando == 'L':
            print('LED APAGADO')

arduino.close() #Finalizamos la comunicacion
