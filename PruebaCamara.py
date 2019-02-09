import time
import picamera
with picamera.PiCamera() as picam:
    picam.resolution = (640, 420)
    picam.start_preview()
    time.sleep(5)
    picam.capture('imagenPru3.gif')
    picam.stop_preview()
    picam.close()
