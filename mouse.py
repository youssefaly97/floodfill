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
        self.map = np.zeros(size,dtype=int)
        self.dir = UP

        #prep the map for flood fill (distance to center)
        for i in range(0, int(size[0]/2)):
            for j in range(0, int(size[1]/2)):
                xd = abs((int(size[0]/2)-1 - i))
                yd = abs(int(size[1]/2)-1 - j)
                self.map[i,j] = xd + yd
                self.map[i, size[1]-j-1] = xd + yd
                self.map[size[0]-i-1, j] = xd + yd
                self.map[size[0]-i-1, size[1]-j-1] = xd + yd
    
    def move(self, cell):
        #self.map[self.pos] = cell

        '''
        self.dir = UP
        if (cell & 1) and self.dir == UP:
            self.dir = RIGHT
        if (cell & 8) and self.dir == RIGHT:
            self.dir = DOWN
        if (cell & 2) and self.dir == DOWN:
            self.dir = LEFT
        if cell & 4 and self.dir == LEFT:
            self.dir = STOPPED
            #quit cuz we're blocked
        '''

        if self.dir == self.getNextMove():
            self.moveOne()
        else:# self.canWeMove(self.getNextMove(), cell):
            self.dir = self.getNextMove()
        


    def where(self, ppc=1):
        return self.pos #(self.x, self.y)

    def getNextMove(self):
        if self.map[self.pos] > self.map[self.pos[0],self.pos[1]-1]: #move up
            return UP
        if self.map[self.pos] > self.map[self.pos[0],self.pos[1]+1]: #move down
            return DOWN
        if self.map[self.pos] > self.map[self.pos[0]-1,self.pos[1]]: #move left
            return LEFT
        if self.map[self.pos] > self.map[self.pos[0]+1,self.pos[1]]: #move right
            return RIGHT
        
    
    def moveOne(self):
        if self.dir == UP:
            self.pos = (self.pos[0], self.pos[1]-1)
        if self.dir == DOWN:
            self.pos = (self.pos[0], self.pos[1]+1)
        if self.dir == LEFT:
            self.pos = (self.pos[0]-1, self.pos[1])
        if self.dir == RIGHT:
            self.pos = (self.pos[0]+1, self.pos[1])

    def canWeMove(self, dir, cell):
        if (cell & 1) and dir == UP:
            return False
        if (cell & 8) and dir == RIGHT:
            return False
        if (cell & 2) and dir == DOWN:
            return False
        if cell & 4 and dir == LEFT:
            return False
        return True