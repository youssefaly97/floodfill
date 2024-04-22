
def stackMerger(stacka,stackb):
    stackc = []
    a = 0
    b = 0
    for i in range(len(stacka)):
        for j in range(len(stackb)):
            if stacka[i] == stackb[j]:
                stackc.append(stacka[i])
                if (i - a) < (j - b):
                    for k in range(a,i):
                        stackc.append(stacka[k])
                else:
                    for k in range(b,j):
                        stackc.append(stackb[k])
                a = i
                b = j
    return stackc

def stackMerger2(stacka,stackb):
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

sA = [ 0, 1, 2, 3, 4, 5, 6, 7, 8,    9,13]
sB = [    1,10,11,    5,12,12,12,12, 9,14,14]

print(stackMerger2(sA,sB))