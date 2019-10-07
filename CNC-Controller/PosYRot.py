
import numpy as np

x = 0
y = 0

corFidu = np.array([[],[]])
def rstZero():
    global x
    global y
    x=0
    y=0

def addX(_x):
    global x
    x+=_x

def addY(_y):
    global y
    y+=_y

def getX():
    global x
    return x

def getY():
    global y
    return y

def saveFidu(pos):
    global x
    global y
    global corFidu
    if pos==0:
        corFidu = ([[pos],[x,y]])    
    else:
        print("else")
        vec = np.array([[],[]])
        vec = ([[pos],[x,y]])
        corFidu=np.concatenate((corFidu, vec))
    print(corFidu)
