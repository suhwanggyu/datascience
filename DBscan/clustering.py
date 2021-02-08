import sys
import math

# List for object
objectArr = []
# List for saving unvisited information
unvisited = []
# List for neighbor information
neighborList = {}
# Save each Cluster
clusterList = []
# parameter n, eps, minpts
n = 0
minpts = 0
eps = 0

## struct of datasample
class DataSample :
    def __init__(self, id, x, y):
      self.id = id
      self.xscore = x
      self.yscore = y


## function of read file
def readInputFile(filename):
    global unvisited
    global objectArr
    fp = open(filename, mode = "r", encoding = "utf-8")
    lines = fp.readlines()
    for tmp in lines :
        objecttmp = tmp.split()
        objectArr.append(DataSample(int(objecttmp[0]),float(objecttmp[1]),float(objecttmp[2])))
    # initialize unvisited List that include all object
    unvisited = [ obj.id for obj in objectArr ]
    fp.close()

## Calculate neighbor that distance is less than eps
def neighbor() :
    global objectArr
    global neighborList
    global eps
    print("Calculating neighbor distance : wait please")
    ## initialize neighborList
    for tmp in objectArr:
        neighborList[tmp.id] = []
    ## Calculate distance for find all neighbor of each object
    for idx,tmp1 in enumerate(objectArr):
        for i in range(idx+1,len(objectArr)):
            ## add cal easy
            tmp2 = objectArr[i]
            ## using Euclidean distance formula for calculating distance of two objects
            distance = math.sqrt(pow(tmp1.xscore - tmp2.xscore, 2) + pow(tmp1.yscore - tmp2.yscore, 2))
            if(eps >= distance) : 
                neighborList[tmp1.id].append(tmp2.id)
                neighborList[tmp2.id].append(tmp1.id)
    print("Calculating success")
    

## Check the object is core
def checkCorePoint(idx):
    global neighborList
    global minpts
    if(len(neighborList[idx]) >= minpts) :
        return True
    return False

## Function that execute DBscan
def clusterDBscan() :
    global unvisited
    global neighborList
    global objectArr
    global clusterList
    ## find neighbor of all cluster
    neighbor()
    inCluster = {}
    ## for checking object in any cluster. If a object is in any cluster, change it 0 to 1
    print("DBscanning")

    ## initialize information that object is already in cluster
    for tmp in objectArr :
        inCluster[tmp.id] = 0

    ## DBscan algorithm
    for idx, tmp in enumerate(unvisited) :
        ## 1. pick a object that is not visited
        newcluster = []
        del unvisited[idx]
        ## 2. check that object visited
        if(checkCorePoint(tmp)) :
            ## 3. if it is core point, the object's neighbor will be candidate set
            newcluster.append(tmp)
            candidate = neighborList[tmp]
            for i in candidate :
                ## 4. pick a candidate and check is it unvisited pointed
                if( i in unvisited ) :
                    ## 5. if it is core point, it's neighbors are included to candidateset
                    unvisited.remove(i)
                    if(checkCorePoint(i)) :
                        for j in neighborList[i] :
                            if(j not in candidate) :
                                candidate.append(j)
                ## 6. if candidate is not in any cluster, add to new cluster
                if(inCluster[i] == 0 and i not in newcluster) :
                    newcluster.append(i)
                    inCluster[i] = 1
        if(len(newcluster) != 0) :
            clusterList.append(newcluster)
    print("DBscanning success")

## write n cluster to output file 
def writeOut(filename, n):
    global clusterList
    print("Writing Output")
    for idx, tmp in enumerate(clusterList) :
        if(idx >= n) :
            break
        fp = open(filename[0:-4] + "_cluster_" + str(idx) + ".txt", "w")
        for i in tmp :
            fp.write(str(i) + "\n")
        fp.close()
    print("Write Output success")

## main function for DBscanning
if __name__ == "__main__" :
    n = int(sys.argv[2])
    eps = int(sys.argv[3])
    minpts = int(sys.argv[4])
    ## read input file
    readInputFile(sys.argv[1])
    ## DBscan
    clusterDBscan()
    ## sort for only writing n cluster
    sorted(clusterList, key=lambda tmp : -len(tmp))
    ## write output file
    writeOut(sys.argv[1], n)