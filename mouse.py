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
    
    def move(self, cell):
        self.map[self.pos] = cell

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

        if self.dir == UP:
            self.pos = (self.pos[0], self.pos[1]-1)
        if self.dir == DOWN:
            self.pos = (self.pos[0], self.pos[1]+1)
        if self.dir == LEFT:
            self.pos = (self.pos[0]-1, self.pos[1])
        if self.dir == RIGHT:
            self.pos = (self.pos[0]+1, self.pos[1])

    def where(self, ppc=1):
        return self.pos #(self.x, self.y)


