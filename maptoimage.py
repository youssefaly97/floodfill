import cv2 as cv
import numpy as np
import pandas as pd
from mouse import mouse as mouse
import time

'''
hh=16
ww=16
map = np.random.randint(0,16,(hh,ww))*0

#set map boundary walls
for i in range(0,ww):
    map[0, i] |= 1
    map[hh-1, i] |= 2
for i in range(0,hh):
    map[i,0] |= 4
    map[i,ww-1] |= 8

#set top left to be start
map[0,0] |= 16
map[1,0] &= ~1
map[0,1] &= ~4

#set center 4 to be end
map[int(hh/2) - 1:int(hh/2)+1, int(ww/2) - 1:int(ww/2)+1] |= 32
'''

def walls(z):
    #0 no walls, 1 top, 2 bottom, 4 left, 8 right, 16 start, 32 end
    start = 0
    end = 0
    top = 0
    bottom = 0
    left = 0
    right = 0
    no_wall = 0

    if z & 1: top = 1
    if z & 2: bottom = 1
    if z & 4: left = 1
    if z & 8: right = 1
    if z & 16: start = 1
    if z & 32: end = 1
    if z == 0: no_wall = 1

    return top, bottom, left, right, start, end, no_wall

def drawWalls(img, map, x, y, ppc, t=1):
    RED = [0, 0, 255]
    GREEN = [0, 255, 0]
    BLUE = [255, 0, 0]
    z = map[x, y] #note the image to array coordinates are transposed
    top, bottom, left, right, start, end, no_wall = walls(z)
    
    #swap coordinates for drawing
    x += y
    y = x - y
    x -= y

    COLOR = RED

    if z & 16: COLOR = BLUE
    if z & 32: COLOR = GREEN

    if z & 1:
        x1 = x*ppc
        x2 = x*ppc+ppc-1
        y1 = y*ppc
        y2 = y1
        img = cv.line(img, (x1, y1), (x2, y2), COLOR, t)
    
    if z & 2:
        x1 = x*ppc
        x2 = x*ppc+ppc-1
        y1 = y*ppc+ppc
        y2 = y1
        img = cv.line(img, (x1, y1), (x2, y2), COLOR, t)

    if z & 4:
        x1 = x*ppc
        x2 = x1
        y1 = y*ppc
        y2 = y*ppc+ppc-1
        img = cv.line(img, (x1, y1), (x2, y2), COLOR, t)

    if z & 8:
        x1 = x*ppc+ppc
        x2 = x1
        y1 = y*ppc
        y2 = y*ppc+ppc-1
        img = cv.line(img, (x1, y1), (x2, y2), COLOR, t)
    
    return img

def drawMap(map,ppc=30): #ppc: pixel per cell
    GRAY = [10, 10, 10]
    h,w = map.shape #gets the map size
    blank = np.zeros((h*ppc, w*ppc, 3)) #creates an empty rgb image with the map size in pixels

    #draw grid lines
    for i in range(1, h):
        for j in range(0, w*ppc, 4):
            blank[i*ppc,j,:] = GRAY
    for i in range(0, h*ppc, 4):
        for j in range(1, w):
            blank[i,j*ppc,:] = GRAY

    for i in range(0,h):
        for j in range(0,w):
            blank = drawWalls(blank, map, i, j, ppc, 2)
    return blank

def drawMouse(mouse, img, ppc=30):
    pos = mouse.where()
    pixPos = (pos[0]*ppc + int(ppc/2), pos[1]*ppc + int(ppc/2))
    return cv.circle(img, pixPos, 4, [200, 0, 200], -1)

def loadMap(filename):
    try:
        return np.array(pd.read_csv(filename, header=None))
    except Exception as e:
        print(e)

def saveMap(map, filename):
    f = open(filename, "w")
    for i in range(0,map.shape[0]):
        for j in range(0,map.shape[1]):
            f.write(str(map[i,j]))
            if(j != map.shape[1]-1): f.write(",")
        f.write("\n")

#saveMap(map, "map1.csv")
map1 = loadMap("./example maps/maze_92lon.csv")

print(map1.shape)
print(map1)

steve = mouse((16,16),(0,15))

print("steve is here")
print(steve.where())

cv.imshow("blank",drawMouse(steve, drawMap(map1,ppc=30)))
cv.waitKey(333)

for i in range(0,500):

    cv.waitKey(1)
    pos = steve.where()
    print(map1[pos[1], pos[0]])
    steve.move(map1[pos[1], pos[0]])
    cv.imshow("blank",drawMouse(steve, drawMap(map1,ppc=30)))
    cv.waitKey(222)
    if(steve.isDone()):
        break

cv.waitKey(0)
cv.destroyAllWindows()