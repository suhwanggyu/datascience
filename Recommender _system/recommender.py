# import numpy for speed up about matrix calculation
# if numpy is not install, put "pip install numpy" to shell and then can use it
import numpy as np
import math
# global variable
inputData = []
itemList = []
userList = []
testSet = []
ratingMatrix = np.array([0])
preuseMatrix = np.array([0])

def zeroInjection(theta) :
    tmp = np.ravel(preuseMatrix)
    tmp.sort()
    limits = tmp[theta]
    for i in range(0,len(ratingMatrix)) :
        for j in range(0,len(ratingMatrix[i])) :
            if preuseMatrix[i][j] <= limits :
                ratingMatrix[i][i] == 0


def matrixFactorization(k, m) :
    p = np.random.rand(m.shape[0],k)
    q = np.random.rand(k, m.shape[1])
    minp = np.array(([1]))
    minq = np.array(([1]))
    minerr = 10000000
    num = 0
    while num <  100:
        print(num)
        num += 1
        for idy, value in enumerate(m) :
            for idx, value in enumerate(m[idy]) :
                
                if m[idy][idx] >= 0 :
                    
                    err = error(idx,idy,m, p, q)
                    ## gradient descendent, assume alpha is 0.1
                    for i in range(0,k) :
                        p[idy][i] = p[idy][i] + 0.0001 *(2 * err * q[i][idx] - 0.02 * p[idy][i])
                        q[i][idx] = q[i][idx] + 0.0001 *(2 * err * p[idy][i] - 0.02 * q[i][idx])
        currentsum = lossfunction(m,p,q,k)
        print(currentsum)
        if minerr > currentsum :
            print("1. " + str(minerr))
            print("2. " + str(currentsum))
            minp = p.copy()
            minq = q.copy()
            if minerr - currentsum < 1 :
                break
            minerr = currentsum
            
        if minerr < 1 :
            break     
    return np.dot(minp,minq)

def error(i,j, R,p,q) :
    return R[j][i] - np.dot(p[j,:],q[:,i])

def lossfunction(R,p,q,k):
    sum = 0
    for i in range(R.shape[0]) :
        for j in range(R.shape[1]) :
            if R[i][j] >= 0 :
                sum += pow(R[i][j] - np.dot(p[i,:],q[:,j]),2)
                for t in range(0,k) :
                    sum +=  0.01 *(pow(p[i][t],2) + pow(q[t][j],2))
    return sum
# making initial matrix(rating Matrix, and pre-use preference matrix by using input data.
def makeratingMatrix() :
    global inputData
    global ratingMatrix
    global preuseMatrix
    ratingMatrix = np.full((len(userList),len(itemList)), -1)
    preuseMatrix = np.full((len(userList),len(itemList)), -1)
    for data in inputData :
        ratingMatrix[data[0]-1][data[1]-1] = data[2]
        preuseMatrix[data[0]-1][data[1]-1] = 1

# read Train file and save itemlist and userlist assuming id is not order, and it can be arbitrary
def readTrainFile(filename) :
    global inputData
    global userList
    global itemList
    f = open(filename, mode = "r")
    lines = f.readlines()
    tmpitem = set()
    tmpuser = set()
    for line in lines :
        tmp = line.split()
        inputData.append([int(tmp[0]),int(tmp[1]),int(tmp[2])])
        tmpuser.add(int(tmp[0]))
        tmpitem.add(int(tmp[1]))
    userList = list(tmpuser)
    itemList = list(tmpitem)
    userList.sort()
    itemList.sort()

# read test file and save itemlist and userlist assuming id is not order, and it can be arbitrary
def readTestFile(filename) :
    global userList
    global itemList
    global testSet
    f = open(filename, mode = "r")
    lines = f.readlines()
    for line in lines :
        tmp = line.split()
        testSet.append([int(tmp[0]),int(tmp[1])])
        if int(tmp[0]) not in userList :
            userList.append(int(tmp[0]))
        if int(tmp[1]) not in itemList :
            itemList.append(int(tmp[1]))
        userList.sort()
        itemList.sort()


def writeTestFile(filename) :
    global testSet
    global ratingMatrix
    global itemList
    global userList
    f = open("u1.base_prediction",mode = "w")
    for tmp in testSet:
        f.write(str(tmp[0]) + "\t" + str(tmp[1]) + "\t" + str(int(round(ratingMatrix[userList.index(tmp[0])][itemList.index(tmp[1])]))) + "\n")     
    f.close()
## main for recommender system
if __name__ == "__main__" :
    # read file
    readTrainFile('u1.base')
    readTestFile('u1.test')
    makeratingMatrix()
    preuseMatrix = matrixFactorization(3, preuseMatrix)
    zeroInjection(90)
    print(ratingMatrix)
    ratingMatrix = matrixFactorization(3, ratingMatrix)
    writeTestFile("aa")