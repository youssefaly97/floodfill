import numpy as np

FLOODFILL = 0
DFS = 1
BFS = 2

STOPPED = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

class mouse():
    def __init__(self, size, start, ):
        #take start position
        #self.x = start[0]
        #self.y = start[1]
        self.pos = start
        self.size = size
        self.wallMap = np.zeros(size,dtype=int)
        self.floodMap = np.zeros(size,dtype=int)
        self.dir = UP
    
    def move(self, cell):
        self.wallMap[self.pos] = cell
        print("running flood")
        self.flood()

        # self.dir = UP
        # if (cell & 1) and self.dir == UP:
        #     self.dir = RIGHT
        # if (cell & 8) and self.dir == RIGHT:
        #     self.dir = DOWN
        # if (cell & 2) and self.dir == DOWN:
        #     self.dir = LEFT
        # if cell & 4 and self.dir == LEFT:
        #     self.dir = STOPPED
        #     #quit cuz we're blocked

        # if self.dir == UP:
        #     self.pos = (self.pos[0], self.pos[1]-1)
        # if self.dir == DOWN:
        #     self.pos = (self.pos[0], self.pos[1]+1)
        # if self.dir == LEFT:
        #     self.pos = (self.pos[0]-1, self.pos[1])
        # if self.dir == RIGHT:
        #     self.pos = (self.pos[0]+1, self.pos[1])

    def where(self, ppc=1):
        return self.pos #(self.x, self.y)
    
    def flood(self):
        queue = []
        queue.append((int(self.size[0]/2), int(self.size[1]/2)))
        queue.append((int((self.size[0]/2)), int((self.size[1]/2)-1)))
        queue.append((int((self.size[0]/2)-1), int((self.size[1]/2)-1)))
        queue.append((int((self.size[0]/2)-1), int((self.size[1]/2))))
        self.vistedMap=np.zeros(self.size,dtype=int)

        self.vistedMap[(int(self.size[0]/2), int(self.size[1]/2))]=1
        self.vistedMap[(int(self.size[0]/2), int(self.size[1]/2))]=1
        self.vistedMap[(int(self.size[0]/2), int(self.size[1]/2))]=1
        self.vistedMap[(int(self.size[0]/2), int(self.size[1]/2))]=1

        self.floodHelper(self.vistedMap, queue, 0)



    def floodHelper(self, vistedMap, queue, iteration):
        self.holding = queue.pop(0)
        self.floodMap[self.holding]=iteration

        holding=(self.holding[0]-1,self.holding[1])
        if(self.wallMap[holding] & 1 and vistedMap[holding] == 1):#check if up is visited or blocked
            queue.append((self.holding[0]-1,self.holding[1]))
            vistedMap[(self.holding[0]-1,self.holding[1])]=1

        holding=(self.holding[0]+1,self.holding[1])
        if(self.wallMap[holding] & 2 and vistedMap[holding] == 1):#check if down is visited or blocked
            queue.append(holding)
            vistedMap[holding]=1

        holding=(self.holding[0],self.holding[1]-1)
        if(self.wallMap[holding] & 4 and vistedMap[holding] == 1):#check if left is visited or blocked
            queue.append(holding)
            vistedMap[holding]=1

        holding=(self.holding[0],self.holding[1]+1)
        if(self.wallMap[holding] & 8 and vistedMap[holding] == 1):#check if right is visited or blocked
            queue.append(holding)
            vistedMap[holding]=1

        if(queue != None):
            print(iteration)
            self.floodHelper(vistedMap, queue, iteration+1)
             

        


        