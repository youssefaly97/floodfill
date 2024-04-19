import cv2 as cv
import numpy as np

h = 16
w = 16
map = np.zeros((h,w),dtype=int)
map[-1,0] |= 16
map[int(h/2)-1:int(h/2)+1,int(w/2)-1:int(w/2)+1] |= 32

img = cv.imread("./example maps/maze_92lon.png", cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

ret, th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
rgb = cv.cvtColor(th1, cv.COLOR_GRAY2RGB)

s = th1.shape
h_ = int(th1.shape[0]/(h*2))
w_ = int(th1.shape[1]/(w*2))

#row scanning first
for j in range(0,h):
    h1 = int(th1.shape[0]/(h*2))*(j*2+1) # index of the row center, iterates accross the maze rows
    w1 = int(th1.shape[1]/(w*2)) # index of the column center

    m = np.where(th1[h1]>127,1,0) #get a binary array of the row in question form the thresholded image
    b = th1[int(h1-(h_*0.8)):int(h1+(h_*0.8)),:] #take a band of 80% around the row in question
    v = np.var(b,axis=0) #calculate the variance column wise in the band
    mv = np.max(v) #max to normalize the variance
    v /= mv #normalized variance
    k = np.where(v>0,0,1) #mask to delete columns with non-zero variance (which have text)
    r = np.multiply(k,m) #multiple element wise with mask to delete non-zero variance columns (text), r is text free row

    for i in range(0,w):
        if np.mean(r[w1*2*i+w1:min(w1*2*i+w1*3,r.size)])>0: map[j,i] |= 8 #column-wise-mean centered about the wall index (w1) (between maze columns), assigns right walls
        if np.mean(r[max(w1*2*i-w1,0):w1*2*i+w1])>0: map[j,i] |= 4 # assigns left walls

#draws a red line through the row in question, changes to blue at a wall
for i in range(0,th1.shape[1]):
    c = [0,0,255] if r[i] == 0 else [255,0,0]
    rgb[h1,i] = c

#colum scanning
for j in range(0,w):
    h1 = int(th1.shape[0]/(h*2))
    w1 = int(th1.shape[1]/(w*2))*(j*2+1)

    m = np.where(th1[:,w1]>127,1,0)
    b = th1[:,int(w1-(w_*0.8)):int(w1+(w_*0.8))]
    v = np.var(b,axis=1)
    mv = np.max(v)
    v /= mv
    k = np.where(v>0,0,1)
    r = np.multiply(k,m)

    #print(r)

    for i in range(0,h):
        if np.mean(r[h1*2*i+h1:min(h1*2*i+h1*3,r.size)])>0: map[i,j] |= 2
        if np.mean(r[max(h1*2*i-h1,0):h1*2*i+h1])>0: map[i,j] |= 1

#map is ready
print(map)
    
#draw red line at the center of the row, blue at the walls
for i in range(0,th1.shape[0]):
    c = [0,0,255] if r[i] == 0 else [255,0,0]
    rgb[i,w1] = c

#save map to csv file
def saveMap(map, filename):
    f = open(filename, "w")
    for i in range(0,map.shape[0]):
        for j in range(0,map.shape[1]):
            f.write(str(map[i,j]))
            if(j != map.shape[1]-1): f.write(",")
        f.write("\n")

saveMap(map, "map1.csv")

#draw map in a window
cv.imshow("maze", rgb)
cv.waitKey(0)
cv.destroyAllWindows()