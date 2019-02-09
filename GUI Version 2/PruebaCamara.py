import picamera
from PIL import Image, ImageDraw
import time

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    # Set up the preview. Here we're using the return value of start_preview
    # but you can specify these values as arguments to start_preview too
    ##img = Image.new('RGB', (640, 480))
    img = Image.open('CIRCULO PRUEBA.png')
    ##d = ImageDraw.Draw(img)
    ##d.arc([(0, 0), (639, 479)],10,360, fill=None)
    
    preview = camera.start_preview()
    preview.fullscreen = False
    preview.window = (0, 0, 640, 480)
    #preview.alpha = 255
    # Set up the overlay. Again, you can specify arguments to add_overlay
    # or set attributes on the resulting renderer
    overlay = camera.add_overlay(img.tostring(), size=(640, 480))
    overlay.fullscreen = False
    overlay.window = (0, 0, 640, 480)
    overlay.alpha = 64
    overlay.layer = 4
    time.sleep(10)
