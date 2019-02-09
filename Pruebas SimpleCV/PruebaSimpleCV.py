import subprocess  
from SimpleCV import Image
import time  

call("raspistill -n -t 0 -o image.bmp", shell=True)

img = Image("image.bmp")

img.show()
time.sleep(5)
