import cv2
import numpy as np
import time

cap=cv2.VideoCapture(0)


def captura():
	_,frame=cap.read()
	grayImage=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	circles=cv2.HoughCircles(grayImage,cv2.HOUGH_GRADIENT,2,400,
	param1=40,param2=40,
	minRadius=10,maxRadius=100)
	try:
		cirles=np.uint16(np.around(circles))
		for circuloActual in circles[0,:]:
			centroX=circuloActual[0]
			centroY=circuloActual[1]
			radio=circuloActual[2]
			cv2.circle(frame,(centroX,centroY),radio,(0,255,0),2)
			cv2.circle(frame,(circles[0][0][0],circles[0][0][1]),2,(0,0,255),3) #Dibuja un punto el centro
			print(str(centroX) + " , " + str(centroY) + " , " + str(radio))
	except:
		print("No Circles")
	cv2.imshow('Video',frame)
	k=cv2.waitKey(30) & 0xff
	if k==27:
		cap.release()
		cv2.destroyAllWindows()	
	

while True:
    captura()
    time.sleep(0.1)
