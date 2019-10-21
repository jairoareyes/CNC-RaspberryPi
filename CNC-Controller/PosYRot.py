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
        corFidu = ([[x,y]])    
    else:
        angle = 0
        dx = 0
        dy = 0
        vec = np.array([[]])
        vec = ([[x,y]])
        corFidu=np.concatenate((corFidu, vec))
        dx = corFidu[1,0]-corFidu[0,0]
        dy = corFidu[1,1]-corFidu[0,1]
        h = (dx**2+dy**2)**(1/2)
        angle = np.arcsin((dy/h))
        print("------- Angulo -------")
        print(np.degrees(angle))   
    print(corFidu)