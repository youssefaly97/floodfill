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
        self.knownMap = np.zeros(size,dtype=bool)
        self.floodMap = np.zeros(size,dtype=int)
        self.dir = STOPPED
        self.targets=[(0,0)]
    
        self.wallMap[(int(size[0]/2), int(size[1]/2))]+=32# sets target
        self.wallMap[(int(size[0]/2), int(size[1]/2-1))]+=32# sets target
        self.wallMap[(int(size[0]/2-1), int(size[1]/2-1))]+=32# sets target
        self.wallMap[(int(size[0]/2-1), int(size[1]/2))]+=32# sets target
        self.wallMap[start] += 16

        
    
    

       
    

#         self.map = np.zeros(size,dtype=int)           #redundant and incompatible code with recursive flood fill
        

#         #prep the map for flood fill (distance to center)
#         for i in range(0, int(size[0]/2)):
#             for j in range(0, int(size[1]/2)):
#                 xd = abs((int(size[0]/2)-1 - i))
#                 yd = abs(int(size[1]/2)-1 - j)
#                 self.map[i,j] = xd + yd
#                 self.map[i, size[1]-j-1] = xd + yd
#                 self.map[size[0]-i-1, j] = xd + yd
#                 self.map[size[0]-i-1, size[1]-j-1] = xd + yd

    def findpath(self, visitedMap, pos, method):
        self.pos=pos
        self.wallMap[(self.pos[1],self.pos[0])]=self.wallMap[(pos[1],pos[0])]
        queue= Queue()
        if method=="Flood search" :# flood fill method
            print("searching for best path")#debug prints
            # print("current wallMap")
            # print(self.wallMap) 
            # print("current floodMap")
            # print(self.floodMap)
            # print("current knownMap")
            # print(self.floodMap)
            
            holding=(pos)
            if(holding[1]-1>=0):
                if( visitedMap[holding[0],holding[1]-1] != True and self.knownMap[holding[0],holding[1]-1] == True and (not (self.wallMap[(pos)] & 1))) :#check up
                    queue.put((holding[0],holding[1]-1))
                    print("going up")

            if((holding[0]+1)<16):
                if( visitedMap[holding[0]+1,holding[1]] != True and self.knownMap[holding[0]+1,holding[1]] == True and (not (self.wallMap[(pos)] & 8))) :#check right
                    queue.put((holding[0]+1,holding[1]))
                    print("going right")

            if(holding[1]+1<16):
                if(visitedMap[holding[0],holding[1]+1] != True and self.knownMap[holding[0],holding[1]+1] == True and (not (self.wallMap[(pos)] & 2))) :#check down
                    queue.put((holding[0],holding[1]+1))
                    print("going down")

            if((holding[0]-1)>=0):
                if(visitedMap[holding[0]-1,holding[1]] != True and self.knownMap[holding[0]-1,holding[1]] == True and (not (self.wallMap[(pos)] & 4))) :#check left
                    queue.put((holding[0]-1,holding[1]))
                    print("going left")

            
            return queue

        


            


    def move(self, cell, target):
        self.wallMap[(self.pos[1],self.pos[0])] = cell
        # print("running flood")
        self.flood(target)# calls recursive flood fill

        # print("current floodMap")#debug prints
        # print(self.floodMap) 
        # print("current wallMap")
        # print(self.wallMap) 
        
        '''
        self.dir = STOPPED# if left unchange by end of if chain then no valid path
        #if self.floodMap[self.pos[1], self.pos[0]] <= self.getForwardCell() or (self.canWeMove(self.dir, self.getForwardCell()) == False):
        if   ((not (cell & 1)) and (self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1]-1,self.pos[0]]) and (self.pos[1]-1) >=0):#check if up valid
            self.dir = UP
            print("going Up")
        if not (cell & 8) and (self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1],self.pos[0]+1]) and (self.pos[0]+1) >=0:#check if right is valid
            self.dir = RIGHT
            print("going Right")
        if not (cell & 2) and (self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1]+1,self.pos[0]]) and (self.pos[1]+1) <self.size[1]:#check if down is valid
            self.dir = DOWN
            print("going Down")
        if not (cell & 4) and (self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1],self.pos[0]-1]) and (self.pos[0]-1) <self.size[0]:#check if left is valid
            self.dir = LEFT
            print("going Left")
        '''
        self.dir = self.getMinimumDir(cell)

        # if self.map[self.pos] > self.map[self.pos[0],self.pos[1]-1]: #move up
        #     return UP
        # if self.map[self.pos] > self.map[self.pos[0],self.pos[1]+1]: #move down
        #     return DOWN
        # if self.map[self.pos] > self.map[self.pos[0]-1,self.pos[1]]: #move left
        #     return LEFT
        # if self.map[self.pos] > self.map[self.pos[0]+1,self.pos[1]]: #move right
        #     return RIGHT



        #if self.dir == self.getNextMove():
        temp=self.pos 
        self.moveOne()
        return temp
        #else:# self.canWeMove(self.getNextMove(), cell):
        #    self.dir = self.getNextMove()
        

    def getMinimumDir(self, cell):
        d = self.dir
        x = 1e12
        
        if self.pos[1]-1 >= 0            and not(cell & 1) and self.dir == UP and self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1]-1,self.pos[0]]:
            x2 = abs(self.floodMap[self.pos[1],self.pos[0]] - self.floodMap[self.pos[1]-1,self.pos[0]])
            if x2 < x:
                x = x2
                d = UP
        if self.pos[1]+1 <= self.size[1] and not(cell & 2) and self.dir == DOWN and self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1]+1,self.pos[0]]:
            x2 = abs(self.floodMap[self.pos[1],self.pos[0]] - self.floodMap[self.pos[1]+1,self.pos[0]])
            if x2 < x:
                x = x2
                d = DOWN
        if self.pos[0]-1 >= 0            and not(cell & 4) and self.dir == LEFT and self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1],self.pos[0]-1]:
            x2 = abs(self.floodMap[self.pos[1],self.pos[0]] - self.floodMap[self.pos[1],self.pos[0]-1])
            if x2 < x:
                x = x2
                d = LEFT
        if self.pos[0]+1 <= self.size[0] and not(cell & 8) and self.dir == RIGHT and self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1],self.pos[0]+1]:
            x2 = abs(self.floodMap[self.pos[1],self.pos[0]] - self.floodMap[self.pos[1],self.pos[0]+1])
            if x2 < x:
                x = x2
                d = RIGHT
        
        if self.pos[1]-1 >= 0            and not(cell & 1) and self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1]-1,self.pos[0]]:
            x2 = abs(self.floodMap[self.pos[1],self.pos[0]] - self.floodMap[self.pos[1]-1,self.pos[0]])
            if x2 < x:
                x = x2
                d = UP
        if self.pos[1]+1 <= self.size[1] and not(cell & 2) and self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1]+1,self.pos[0]]:
            x2 = abs(self.floodMap[self.pos[1],self.pos[0]] - self.floodMap[self.pos[1]+1,self.pos[0]])
            if x2 < x:
                x = x2
                d = DOWN
        if self.pos[0]-1 >= 0            and not(cell & 4) and self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1],self.pos[0]-1]:
            x2 = abs(self.floodMap[self.pos[1],self.pos[0]] - self.floodMap[self.pos[1],self.pos[0]-1])
            if x2 < x:
                x = x2
                d = LEFT
        if self.pos[0]+1 <= self.size[0] and not(cell & 8) and self.floodMap[self.pos[1],self.pos[0]] > self.floodMap[self.pos[1],self.pos[0]+1]:
            x2 = abs(self.floodMap[self.pos[1],self.pos[0]] - self.floodMap[self.pos[1],self.pos[0]+1])
            if x2 < x:
                x = x2
                d = RIGHT
        return d

    def where(self):
        return self.pos #(self.x, self.y)
    
    def getSize(self):
        return self.size
    
    def knownWalls(self):
        return self.wallMap
    
    def knownTiles(self):
        return self.knownMap
    
    def knownWalls(self):
        return self.wallMap


    def getNextMove(self):  #currently incompatible with recursive flood fill
        if self.map[self.pos] > self.map[self.pos[0],self.pos[1]-1]: #move up
            return UP
        if self.map[self.pos] > self.map[self.pos[0],self.pos[1]+1]: #move down
            return DOWN
        if self.map[self.pos] > self.map[self.pos[0]-1,self.pos[1]]: #move left
            return LEFT
        if self.map[self.pos] > self.map[self.pos[0]+1,self.pos[1]]: #move right
            return RIGHT
        
    
    def moveOne(self):#moves mouse to next position
        if self.dir == UP:
            self.pos = (self.pos[0], self.pos[1]-1)
            self.knownMap[self.pos] = True
        elif self.dir == DOWN:
            self.pos = (self.pos[0], self.pos[1]+1)
            self.knownMap[self.pos] = True
        elif self.dir == LEFT:
            self.pos = (self.pos[0]-1, self.pos[1])
            self.knownMap[self.pos] = True
        elif self.dir == RIGHT:
            self.pos = (self.pos[0]+1, self.pos[1])
            self.knownMap[self.pos] = True
        else :
            print("no move found")

    def moveHere(self, pos):
        self.pos=pos

    def where(self, ppc=1):
        return self.pos #(self.x, self.y)
    
    def isDone(self, target):#checks to see if mouse is at the center of the maze
        if target=="Goal" :
            if(self.pos==(int(self.size[0]/2), int(self.size[1]/2)) or self.pos==(int(self.size[0]/2), int(self.size[1]/2-1)) or self.pos==(int(self.size[0]/2-1), int(self.size[1]/2-1)) or self.pos==(int(self.size[0]/2-1), int(self.size[1]/2))) :
                return True #mouse is at goal
        if target=="Start" :
            if self.pos==(0,15) :
                return True #mouse is at start
        return False #mouse is not at goal or start



    def canWeMove(self, dir, cell): #currently incompatible with recursive flood fill
        if (cell & 1) and dir == UP:
            return False
        if (cell & 8) and dir == RIGHT:
            return False
        if (cell & 2) and dir == DOWN:
            return False
        if cell & 4 and dir == LEFT:
            return False
        return True








    def flood(self, target):#setup for flood fill
        queue = Queue()#what tile to fill next
        iteration = Queue()# the depth of the tile
        
        self.vistedMap=np.zeros(self.size,dtype=int)#remembers what tiles is/was in queue
        if (target=="Goal"):
            queue.put((int(self.size[0]/2), int(self.size[1]/2)))## puts center in queue
            queue.put((int((self.size[0]/2)), int((self.size[1]/2)-1)))
            queue.put((int((self.size[0]/2)-1), int((self.size[1]/2)-1)))
            queue.put((int((self.size[0]/2)-1), int((self.size[1]/2))))

            iteration.put(0)
            iteration.put(0)
            iteration.put(0)
            iteration.put(0)

            self.vistedMap[(int(self.size[0]/2), int(self.size[1]/2))]=1# set center as visited
            self.vistedMap[(int(self.size[0]/2), int(self.size[1]/2-1))]=1
            self.vistedMap[(int(self.size[0]/2-1), int(self.size[1]/2-1))]=1
            self.vistedMap[(int(self.size[0]/2-1), int(self.size[1]/2))]=1
        elif (target=="Start") :
            queue.put((15,0))
            iteration.put(0)
            self.vistedMap[(15,0)]=1

        # print(self.vistedMap)
        self.floodHelper(self.vistedMap, queue, iteration)#enter recursive section of flood()





    def floodHelper(self, vistedMap, queue, iteration):#main segment of flood()
        holding = queue.get()#retirve position of current tile in maze
        
        thisiteration= iteration.get()#retrive depth from queue
        self.floodMap[holding]=thisiteration# update current tile
        cell=self.wallMap[holding]#remember walls of current tile
        

        holding2=(holding[0]-1,holding[1])#retirve position of next tile in maze
        if (holding2[0]< self.size[0] and holding2[0]>= 0 and holding2[1]< self.size[1] and holding2[1]>= 0):#check if legal tile
            cell2=self.wallMap[holding2]#check walls of upward tile
            if((not(cell & 1) and not(cell2 & 2)) and vistedMap[holding2] == 0):#check if up is visited or blocked
                queue.put(holding2)#add tile to queue
                vistedMap[holding2]=1
                iteration.put(thisiteration+1)


        holding2=(holding[0]+1,holding[1])#retirve position of next tile in maze
        if (holding2[0]< self.size[0] and holding2[0]>= 0 and holding2[1]< self.size[1] and holding2[1]>= 0):#check if legal tile
            cell2=self.wallMap[holding2]#check walls of downward tile
            if((not(cell & 2) and not(cell2 & 1)) and vistedMap[holding2] == 0):#check if down is visited or blocked
                queue.put(holding2)#add tile to queue
                vistedMap[holding2]=1
                iteration.put(thisiteration+1)

        holding2=(holding[0],holding[1]+1)#retirve position of next tile in maze
        if (holding2[0]< self.size[0] and holding2[0]>= 0 and holding2[1]< self.size[1] and holding2[1]>= 0):#check if legal tile
            cell2=self.wallMap[holding2]#check walls of left tile
            if((not(cell & 8) and not(cell2 & 4)) and vistedMap[holding2] == 0):#check if left is visited or blocked
                queue.put(holding2)#add tile to queue
                vistedMap[holding2]=1
                iteration.put(thisiteration+1)

        holding2=(holding[0],holding[1]-1)#retirve position of next tile in maze
        if (holding2[0]< self.size[0] and holding2[0]>= 0 and holding2[1]< self.size[1] and holding2[1]>= 0):#check if legal tile
            cell2=self.wallMap[holding2]#check walls of right tile
            if((not(cell & 4) and not(cell2 & 8)) and vistedMap[holding2] == 0):#check if right is visited or blocked
                queue.put(holding2)#add tile to queue
                vistedMap[holding2]=1
                iteration.put(thisiteration+1)



        if(not queue.empty()):#is queue empty, if not continue recursion
            self.floodHelper(vistedMap, queue, iteration)

    def getFloodMap(self):
        return self.floodMap
