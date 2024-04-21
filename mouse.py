import time
import numpy as np
from queue import Queue 

FLOODFILL = 0
DFS = 1
BFS = 2

STOPPED = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

class mouse():
    def __init__(self, size, start ):
        #take start position
        #self.x = start[0]
        #self.y = start[1]
        self.pos = start
        self.size = size

        self.wallMap = np.zeros(size,dtype=int)
        self.wallMap[(int(size[0]/2), int(size[1]/2))]+=32# sets target
        self.wallMap[(int(size[0]/2), int(size[1]/2-1))]+=32# sets target
        self.wallMap[(int(size[0]/2-1), int(size[1]/2-1))]+=32# sets target
        self.wallMap[(int(size[0]/2-1), int(size[1]/2))]+=32# sets target

        self.floodMap = np.zeros(size,dtype=int)
        self.dir = STOPPED
    
    def move(self, cell):
        self.wallMap[(self.pos[1],self.pos[0])] = cell
        print("running flood")
        self.flood()
        print("current floodMap")
        print(self.floodMap) 
        print("current wallMap")
        print(self.wallMap) 

        self.dir = STOPPED
        if   ((not (cell & 1)) and (self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1]-1,self.pos[0]]) and (self.pos[1]-1) >=0):#check up
            self.dir = UP
            print("going Up")
        elif not (cell & 2) and (self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1]+1,self.pos[0]]) and (self.pos[1]+1) <self.size[1]:#check down
            self.dir = DOWN
            print("going Down")
        elif not (cell & 8) and (self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1],self.pos[0]+1]) and (self.pos[0]+1) >=0:#check right
            self.dir = RIGHT
            print("going Right")
        elif not (cell & 4) and (self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1],self.pos[0]-1]) and (self.pos[0]-1) <self.size[0]:#check left
            self.dir = LEFT
            print("going Left")
        
        
        
            

        if self.dir == UP:
            self.pos = (self.pos[0], self.pos[1]-1)
        elif self.dir == DOWN:
            self.pos = (self.pos[0], self.pos[1]+1)
        elif self.dir == LEFT:
            self.pos = (self.pos[0]-1, self.pos[1])
        elif self.dir == RIGHT:
            self.pos = (self.pos[0]+1, self.pos[1])

    def where(self, ppc=1):
        return self.pos #(self.x, self.y)
    
    def isDone(self):
        if(self.pos==(int(self.size[0]/2), int(self.size[1]/2)) or self.pos==(int(self.size[0]/2), int(self.size[1]/2-1)) or self.pos==(int(self.size[0]/2-1), int(self.size[1]/2-1)) or self.pos==(int(self.size[0]/2-1), int(self.size[1]/2))) :
            return True
        else :
            return False






    def flood(self):
        queue = Queue()
        queue.put((int(self.size[0]/2), int(self.size[1]/2)))
        queue.put((int((self.size[0]/2)), int((self.size[1]/2)-1)))
        queue.put((int((self.size[0]/2)-1), int((self.size[1]/2)-1)))
        queue.put((int((self.size[0]/2)-1), int((self.size[1]/2))))
        iteration = Queue()
        iteration.put(0)
        iteration.put(0)
        iteration.put(0)
        iteration.put(0)
        self.vistedMap=np.zeros(self.size,dtype=int)

        self.vistedMap[(int(self.size[0]/2), int(self.size[1]/2))]=1
        self.vistedMap[(int(self.size[0]/2), int(self.size[1]/2-1))]=1
        self.vistedMap[(int(self.size[0]/2-1), int(self.size[1]/2-1))]=1
        self.vistedMap[(int(self.size[0]/2-1), int(self.size[1]/2))]=1

        # print(self.vistedMap)
        self.floodHelper(self.vistedMap, queue, iteration)


        
        



    def floodHelper(self, vistedMap, queue, iteration):
        holding = queue.get()
        
        thisiteration= iteration.get()
        self.floodMap[holding]=thisiteration
        cell=self.wallMap[holding]
        

        holding2=(holding[0]-1,holding[1])
        if (holding2[0]< self.size[0] and holding2[0]>= 0 and holding2[1]< self.size[1] and holding2[1]>= 0):
            cell2=self.wallMap[holding2]
            if((not(cell & 1) and not(cell2 & 2)) and vistedMap[holding2] == 0):#check if up is visited or blocked
                queue.put(holding2)
                vistedMap[holding2]=1
                iteration.put(thisiteration+1)


        holding2=(holding[0]+1,holding[1])
        if (holding2[0]< self.size[0] and holding2[0]>= 0 and holding2[1]< self.size[1] and holding2[1]>= 0):
            cell2=self.wallMap[holding2]
            if((not(cell & 2) and not(cell2 & 1)) and vistedMap[holding2] == 0):#check if down is visited or blocked
                queue.put(holding2)
                vistedMap[holding2]=1
                iteration.put(thisiteration+1)

        holding2=(holding[0],holding[1]+1)
        if (holding2[0]< self.size[0] and holding2[0]>= 0 and holding2[1]< self.size[1] and holding2[1]>= 0):
            cell2=self.wallMap[holding2]
            if((not(cell & 8) and not(cell2 & 4)) and vistedMap[holding2] == 0):#check if left is visited or blocked
                queue.put(holding2)
                vistedMap[holding2]=1
                iteration.put(thisiteration+1)

        holding2=(holding[0],holding[1]-1)
        if (holding2[0]< self.size[0] and holding2[0]>= 0 and holding2[1]< self.size[1] and holding2[1]>= 0):
            cell2=self.wallMap[holding2]
            if((not(cell & 4) and not(cell2 & 8)) and vistedMap[holding2] == 0):#check if right is visited or blocked
                queue.put(holding2)
                vistedMap[holding2]=1
                iteration.put(thisiteration+1)



        if(not queue.empty()):
            self.floodHelper(vistedMap, queue, iteration)
             

        


        