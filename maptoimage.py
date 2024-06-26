import cv2 as cv
import numpy as np
import pandas as pd
from mouse import mouse as mouse
from queue import Queue 

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
    GRAY = np.array([100, 100, 100])/255
    LIGHT = np.array([50, 50, 50])/255
    h,w = map.shape #gets the map size
    blank = np.zeros((h*ppc, w*ppc, 3)) #creates an empty rgb image with the map size in pixels

    for i in range(0, h):
        for j in range(0, w):
            if map[i,j] & 64: blank[i*ppc:i*ppc+ppc,j*ppc:j*ppc+ppc] = LIGHT

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

def drawMouse(mouse, img, prevpos=[], drawMouseMap=False, ppc=30):
    pos = mouse.where()
    pixPos = (pos[0]*ppc + int(ppc/2), pos[1]*ppc + int(ppc/2))

    img_ = img
    if drawMouseMap:
        map = mouse.getFloodMap()
        for i in range(0, map.shape[0]):
            for j in range(0, map.shape[1]):
                img_ = cv.putText(img_, str(map[i,j]), (j*ppc + int(ppc/2) - 12, i*ppc + int(ppc/2) + 12), cv.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)

    for posI in prevpos:
        img_ = cv.circle(img_, (posI[0]*ppc+ int(ppc/2), posI[1]*ppc+ int(ppc/2)), 4, [0.5, 0, 0.5], -1)

    return cv.circle(img_, pixPos, 4, [200, 0, 200], -1)

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

def stackCleaner(stack, pos):
    tempStack=[]
    while(len(stack)!=0):
        tempHold=stack.pop()
        if(tempHold==pos):
            tempStack.clear()
        tempStack.append(tempHold)
    while(len(tempStack)):
        stack.append(tempStack.pop())
    return stack

def stackMerger(stacka,stackb_,reverse=True):
    stackb = []
    if reverse:
        for k in range(len(stackb_)-1,-1,-1):
            stackb.append(stackb_[k])
    else:
        for k in range(0,len(stackb_)):
            stackb.append(stackb_[k])
        
    a = 0 #last common point index of stack a
    b = 0
    stackc = []
    for i in range(len(stacka)):
        for j in range(len(stackb)):
            if stacka[i] == stackb[j]: #if we reach a common point, append the shorter segment
                if (i-a)<(j-b):
                    for k in range(a,i):
                        stackc.append(stacka[k])
                else:
                    for k in range(b,j):
                        stackc.append(stackb[k])
                a = i #store common point to check next segment
                b = j
    #check remaining length of both stacks & take the shorter
    if (len(stacka) - a)<(len(stackb) - b): 
        for k in range(a,len(stacka)):
            stackc.append(stacka[k])
    else:
        for k in range(b,len(stackb)):
            stackc.append(stackb[k])
    return stackc

map1 = loadMap("./example maps/maze_93apec.csv")
map1[(15,0)] += 16

#print(map1.shape)
#print(map1)

steve = mouse((16,16),(0,15))
print("Steve is here")
print(steve.where())

img = drawMouse(steve, drawMap(map1, ppc=30), drawMouseMap=False)
cv.imshow("Maze", drawMouse(steve, img))

stackToCenter = []
#img = drawMap(map1,ppc=30)
for i in range(0,5000) :#search to center Flood fill
    cv.waitKey(1)
    pos = steve.where()
    #print(map1[pos[1], pos[0]])
    stackToCenter = stackCleaner(stackToCenter,pos)
    img = drawMouse(steve, drawMap(steve.knownWalls(),ppc=30), stackToCenter, drawMouseMap=True)
    cv.imshow("Flood fill search", img)
    stackToCenter.append(steve.move(map1[pos[1], pos[0]],"Goal"))
    
    #img = drawMouseMap(steve,drawMouse(steve, img))
    
    if cv.waitKey(0) == 27: break
    if(steve.isDone("Goal")):#when center found exit for loop
        print("Flood fill start to goal moves: " + str(i))
        stackToCenter.append(steve.where())
        break

stackToStart = []
for i in range(0,5000) :#search to start Flood fill
    cv.waitKey(1)
    img = drawMouse(steve, drawMap(steve.knownWalls(),ppc=30), stackToStart, drawMouseMap=True)
    cv.imshow("Flood fill search",drawMouse(steve, img))
    pos = steve.where()
    #print(map1[pos[1], pos[0]])
    stackToStart.append(steve.move(map1[pos[1], pos[0]],"Start"))
    stackToStart = stackCleaner(stackToStart,pos)
    
    if cv.waitKey(0) == 27: break
    if(steve.isDone("Start")):#when center found exit for loop
        print("Flood fill goal to start moves: " + str(i))
        stackToCenter.append(steve.where())
        break


'''
visitedMap = np.zeros(steve.getSize(),dtype=int)
pos = steve.where()
print(stackToCenter)
print("\n\n")
print(stackToStart)
print("\n\n")
'''
shortestStack=stackMerger(stackToCenter,stackToStart)
#print(shortestStack)

finalStack = []
for i in range(0,250) :
    img = drawMouse(steve, drawMap(steve.knownWalls(),ppc=30), finalStack, drawMouseMap=False)
    cv.imshow("Flood fill search",drawMouse(steve, img))
    finalStack.append(steve.moveHere(shortestStack.pop(0)))
    if cv.waitKey(0) == 27: break
    if(steve.isDone("Goal")):#when center found exit for loop
        img = drawMouse(steve, drawMap(steve.knownWalls(),ppc=30), finalStack, drawMouseMap=False)
        cv.imshow("Flood fill search",drawMouse(steve, img))
        print("Flood fill optimal path moves: " + str(i))
        break


# ............................................................ start of breadth search
# max = mouse((16,16),(0,15))
# img = drawMouse(max, drawMap(map1, ppc=30), drawMouseMap=False)
# cv.imshow("Maze", drawMouse(max, img))




# print("max is here")
# print(max.where())
# #create stack
# for i in range(0,25):
#     img = drawMouse(max, drawMap(max.knownWalls(),ppc=30), drawMouseMap=False)
#     cv.imshow("Breathe search",drawMouse(max, img))
#     pos = max.where()
#     max.breatheOfSearch(map1[pos[1], pos[0]],"Goal")
#     #tempStack=stack from current position to current target
#     #loop till tempStack is empty
#         #max.breadthMoveHere(tempStack)
#         #img = drawMouse(max, drawMap(max.knownWalls(),ppc=30), drawMouseMap=False)
#         #cv.imshow("Breadth search",drawMouse(max, img))
#     #add all new branches to stack

#     if cv.waitKey(0) == 27: break
#     if(max.isDone("Goal")):#when center found exit for loop
#         img = drawMouse(max, drawMap(max.knownWalls(),ppc=30), drawMouseMap=False)
#         cv.imshow("Breathe search",drawMouse(max, img))
#         break

#............................................................ start of depth search
    
sam = mouse((16,16),(0,15))
img = drawMouse(sam, drawMap(map1, ppc=30), drawMouseMap=False)
cv.imshow("Maze", drawMouse(sam, img))




print("sam is here")
print(sam.where())
#create stack
for i in range(0,500):
    img = drawMouse(sam, drawMap(sam.knownWalls(),ppc=30), drawMouseMap=False)
    cv.imshow("Depth search",drawMouse(sam, img))
    pos = sam.where()
    sam.depthOfSearch(map1[pos[1], pos[0]],"Goal")


    if cv.waitKey(0) == 27: break
    if(sam.isDone("Goal")):#when center found exit for loop
        pos = sam.where()
        sam.depthOfSearch(map1[pos[1], pos[0]],"Goal")
        img = drawMouse(sam, drawMap(sam.knownWalls(),ppc=30), drawMouseMap=False)
        cv.imshow("Depth search",drawMouse(sam, img))
        print("DFS start to goal moves: " + str(i))
        break



for i in range(0,500):
    img = drawMouse(sam, drawMap(sam.knownWalls(),ppc=30), drawMouseMap=False)
    cv.imshow("Depth search",drawMouse(sam, img))
    pos = sam.where()
    sam.depthOfSearch(map1[pos[1], pos[0]],"Start")

    if cv.waitKey(0) == 27: break
    if(sam.isDone("Start")):#when center found exit for loop
        img = drawMouse(sam, drawMap(sam.knownWalls(),ppc=30), drawMouseMap=False)
        cv.imshow("Depth search",drawMouse(sam, img))
        print("DFS goal to start moves: " + str(i))
        break

finalStack=[]
stackOfPositions=[]
stackOfPositions=sam.getStackOfPositions()
#print("stackOfPositions")
#print(stackOfPositions)
#img = drawMouse(steve, drawMap(steve.knownWalls(),ppc=30), finalStack, drawMouseMap=False)
for i in range(0,500):
    temp=sam.moveHere(stackOfPositions.pop())
    img = drawMouse(sam, drawMap(sam.knownWalls(),ppc=30), finalStack,drawMouseMap=False)
    cv.imshow("Depth search",drawMouse(sam, img))
    finalStack.append(temp)
    pos = sam.where()
    if cv.waitKey(0) == 27: break
    if(sam.isDone("Goal")):#when center found exit for loop
        img = drawMouse(sam, drawMap(sam.knownWalls(),ppc=30), finalStack, drawMouseMap=False)
        cv.imshow("Depth search",drawMouse(sam, img))
        print("DFS best path moves: " + str(i))
        break

cv.waitKey(0)
cv.destroyAllWindows()       

