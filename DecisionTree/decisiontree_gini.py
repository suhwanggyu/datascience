import sys
import copy
import math
db = []
attributelist = ()
valuelist = {}
splitlist = []
testdb = []

class Node :
    def __init__(self, result, candidateSet, parent) :
        self.rightchild = -1
        self.leftchild = -1
        self.splitnum = -1
        self.result = result
        self.candidateSet = candidateSet
        self.parent = parent



def calculate(node) :
    global valuelist
    global db
    global attributelist
    count = [0] * len(valuelist[attributelist[-1]])
    for idx, value in enumerate(valuelist[attributelist[-1]]) :
        for cand in node.candidateSet :
            if db[cand][-1] == value :
                count[idx] = count[idx] + 1

    tmp = [i for i,x in enumerate(count) if x == max(count)]
    return tmp[-1]


def choose(node, splitcandidate, depth) :
    global splitlist
    global attributelist
    global db
    if len(node.candidateSet) == 0 :
        node.result = calculate(node.parent)
        return;
    if depth ==  10 :
        print('aa')
        node.result = calculate(node)
        return;

    initial = -100000 #threshold
    maxdeltagini = initial
    minleftcandidate = []
    minrightcandidate = []
    for splitnumber in splitcandidate :
        leftcandidate = []
        rightcandidate = []
        for idx in node.candidateSet :
            cnt = 0
            for check in splitlist[splitnumber][1] :
                if db[idx][attributelist.index(splitlist[splitnumber][0])] == check :
                    cnt = 1
                    leftcandidate.append(idx)
            if cnt == 0 :
                rightcandidate.append(idx)
        deltagini = gini_index(node.candidateSet) - calculate_giniA(node.candidateSet, leftcandidate, rightcandidate)
        if deltagini != 0 and len(leftcandidate) != 0 and len(rightcandidate) != 0 and maxdeltagini < deltagini :
            maxdeltagini = deltagini
            newleftnode = Node(-1, leftcandidate, node)
            newrightnode = Node(-1, rightcandidate, node)
            node.splitnum = splitnumber
            node.leftchild = newleftnode
            node.rightchild = newrightnode
            node.result = -1
    if maxdeltagini != initial :
        nextsplitcandidate = copy.deepcopy(splitcandidate)
        nextsplitcandidate.remove(node.splitnum)
        
        choose(node.leftchild, nextsplitcandidate, depth+1)

        nextsplitcandidate = copy.deepcopy(splitcandidate)
        nextsplitcandidate.remove(node.splitnum)
        choose(node.rightchild, nextsplitcandidate, depth+1)

    if node.leftchild == -1 or node.rightchild == -1 :
        node.result = calculate(node)



def calculate_giniA(candidateSet, leftcandidate, rightcandidate) :
    if len(candidateSet) == 0 :
        return 0
    return (len(leftcandidate)/len(candidateSet))*gini_index(leftcandidate) + (len(rightcandidate)/len(candidateSet))*gini_index(rightcandidate)


def gini_index(candidateSet) :
    global valuelist
    global db
    global attributelist
    if len(candidateSet) == 0 :
        return 0
    count = [0] * len(valuelist[attributelist[-1]])
    for idx, value in enumerate(valuelist[attributelist[-1]]) :
        for cand in candidateSet :
            if db[cand][-1] == value :
                count[idx] = count[idx] + 1
    currentgini = 1
    for cnt in count :
        prob = cnt/len(candidateSet)
        if cnt != 0 :    
            currentgini = currentgini - (prob * prob)
    return currentgini

def make_ginisplit() :
    global attributelist

    for i in range (0, len(attributelist) - 1) :
        split([], [], i, 0 )
        split([], [], i, 0 )
        
def split(left, right, nattr, nval ) :
    global splitlist
    global attributelist
    global valuelist
    inlist = copy.deepcopy(left)
    waitlist = copy.deepcopy(right)
    if nval >= len(valuelist[attributelist[nattr]]) :
        if len(inlist) != 0 and len(waitlist) != 0 :
            splitlist.append([attributelist[nattr],inlist,waitlist])
        nval = 0
        return
    
    inlist.append(valuelist[attributelist[nattr]][nval])
    split(inlist,waitlist, nattr, nval+1)
    split(waitlist, inlist, nattr, nval+1)




def make_DecisionTree() :
    global db
    global attributelist
    global splitlist
    initialSample = list(range(0,len(db)))
    make_ginisplit()
    node = Node(-1, initialSample, -1)
    choose(node,list(range(0,len(splitlist))),0)
    return node

 

def testFileHandler(lines) :
    global testdb
    del lines[0]
    for temp in lines :
        testdb.append(temp.split())

def trainFileHandler(lines) :
    global attributelist
    global valuelist
    global db

    attributelist = lines[0].split()
    del lines[0]
    for temp in lines :
        db.append(temp.split())

def make_valuelist() :
    global db
    global testdb
    global attributelist
    global valuelist
    for att in attributelist :
        for record in db :
            if att not in valuelist :
                valuelist[att] = list()
                valuelist[att].append(record[attributelist.index(att)])
            else :
                if record[attributelist.index(att)] not in valuelist[att] :
                    valuelist[att].append(record[attributelist.index(att)])
        if attributelist.index(att) != len(attributelist) - 1 :
            for record in testdb :
                if att not in valuelist :
                    valuelist[att] = list()
                    valuelist[att].append(record[attributelist.index(att)])
                else :
                    if record[attributelist.index(att)] not in valuelist[att] :
                        valuelist[att].append(record[attributelist.index(att)])



def readFile(filename, mode):
    r = open(filename, mode = 'rt', encoding = 'utf-8')
    lines = r.readlines()
    if mode == 'train' :
        trainFileHandler(lines)
    elif mode == 'test' :
        testFileHandler(lines)
    else :
        return -1
    r.close()

def test(sample, node) :
    global valuelist
    global attributelist
    global splitlist
    while node.result == -1 :
        spl = splitlist[node.splitnum]
        cnt = 0
        for check in spl[1] :
            if sample[attributelist.index(spl[0])] == check :
                cnt = 1
        if cnt == 1 :
            node = node.leftchild
        else :
            node = node.rightchild
    return valuelist[attributelist[-1]][node.result]

def output(filename, node) :
    global testdb
    global attributelist
    w = open(filename, mode = 'w', encoding = 'utf-8')
    w.write('\t'.join(attributelist))
    for sample in testdb :
        w.write('\n')
        w.write('\t'.join(sample))
        w.write('\t' + test(sample, node))
    w.close()
    return

if __name__ == "__main__":
    readFile(sys.argv[1], 'train')
    readFile(sys.argv[2], 'test')
    make_valuelist()
    node = make_DecisionTree()
    output(sys.argv[3], node)
    cnt = 0