##from SimpleCV import Camera, Image
##import time
##
##cam = Camera(prop_set={"width":320, "height":240})
### Snap a Picture
##img = cam.getImage()
##
### Save picture
##img.save("images/foto.jpg")
##
##


from SimpleCV import Image
import time

img = Image('lenna')
binlena = img.binarize()
binlena.save("/home/pi/Desktop/Tesis/binlena.jpg")

time.sleep(3)

edgelena = img.edges()
edgelena.save("/home/pi/Desktop/Tesis/edgelena.jpg")
