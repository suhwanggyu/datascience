import sys
import copy
import math
db = []
attributelist = ()
valuelist = {}
testdb = []

class Node :
    def __init__(self, result) :
        self.childlist = []
        self.myAtt = -1
        self.result = result

def calculate(candidateSample) :
    global valuelist
    global db
    global attributelist
    count = [0] * len(valuelist[attributelist[-1]])
    for idx, value in enumerate(valuelist[attributelist[-1]]) :
        for cand in candidateSample :
            if db[cand][-1] == value :
                count[idx] = count[idx] + 1
    return count.index(max(count))

def info_Gain(candidateSample) :
    global valuelist
    global db
    global attributelist
    if len(candidateSample) == 0 :
        return 0
    count = [0] * len(valuelist[attributelist[-1]])
    for idx, value in enumerate(valuelist[attributelist[-1]]) :
        for cand in candidateSample :
            if db[cand][-1] == value :
                count[idx] = count[idx] + 1
    currentinfo = 0
    for cnt in count :
        prob = cnt/len(candidateSample)
        if cnt != 0 :    
            currentinfo = currentinfo - (prob * math.log(prob,2))
    
    return currentinfo

def bestnextnode(candidateAttr, candidateSample) :
    global valuelist
    global attributelist
    myinfo = info_Gain(candidateSample)
    if myinfo == 0 :
        return -1
    gain = []
    for cand in candidateAttr :
        partialinfo = []
        for value in valuelist[attributelist[cand]] :
            newsample = []
            for sample in candidateSample :
                if db[sample][cand] == value :
                    newsample.append(sample)
            partialinfo.append(info_Gain(newsample)*len(newsample)/len(candidateSample))
        gain.append(myinfo - sum(partialinfo))
    if max(gain) <= 0.2 :
        return -1
    return candidateAttr[gain.index(max(gain))]

def choose_node(candidateAttr, candidateSample,depth) :
    global db
    global attributelist
    node = Node(-1)
    if len(candidateAttr) == 0 or info_Gain(candidateSample) == 0:
        node.result = calculate(candidateSample)
        return node
    node.myAtt = bestnextnode(candidateAttr, candidateSample)
    if node.myAtt == -1 :
        node.result = calculate(candidateSample)
        return node
    myatt = copy.deepcopy(candidateAttr)
    myatt.remove(node.myAtt)

    for val in valuelist[attributelist[node.myAtt]] :
        newSet = []
        for sample in candidateSample :
            if db[sample][node.myAtt] == val :
                newSet.append(sample)
        if len(newSet) == 0 :
            node.childlist.append(Node(calculate(candidateSample)))
        else :
            node.childlist.append(choose_node(myatt, newSet,depth+1))
    return node




def make_DecisionTree() :
    global db
    global attributelist
    initialSample = list(range(0,len(db)))
    initialAttr = list(range(0,len(attributelist)-1))
    node = choose_node(initialAttr, initialSample, 0)
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
    while node.result == -1 :
        node = node.childlist[valuelist[attributelist[node.myAtt]].index(sample[node.myAtt])]
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
