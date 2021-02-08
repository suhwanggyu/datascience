import sys
import copy
import math
db = []
attributelist = ()
valuelist = {}
testdb = []

class Node_forGain :
    def __init__(self, result, set, parent) :
        self.childlist = []
        self.myAtt = -1
        self.result = result
        self.set = set
        self.parent = parent

def calculate_forGain(candidateSample, node) :
    global valuelist
    global db
    global attributelist
    count = [0] * len(valuelist[attributelist[-1]])
    for idx, value in enumerate(valuelist[attributelist[-1]]) :
        for cand in candidateSample :
            if db[cand][-1] == value :
                count[idx] = count[idx] + 1
    #if  count.count(max(count)) > 1 :
    tmp = [i for i,x in enumerate(count) if x == max(count)]
    return tmp[-1]
    #    print(count)
    #    print(node.set)
    #    return calculate_forGain(node.parent.set, node.parent)
        #print('aa')
        #print(count)
        #pick = 0
        #for idx, cnt in enumerate(count) :
        #    if count[idx] == max(count) and pick == 1:
        #        return idx
        #    if count[idx] == max(count) :
        #        pick = 1
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
        splitinfo = []
        for value in valuelist[attributelist[cand]] :
            newsample = []
            for sample in candidateSample :
                if db[sample][cand] == value :
                    newsample.append(sample)
            partialinfo.append(info_Gain(newsample)*len(newsample)/len(candidateSample))
            if len(newsample) == 0 :
                splitinfo.append(0)
            else :
                splitinfo.append(math.log(len(newsample)/len(candidateSample),2)*len(newsample)/len(candidateSample))
        gain.append((myinfo - sum(partialinfo))/(-sum(splitinfo)))
    if max(gain) <= 0 :
        return -1
    return candidateAttr[gain.index(max(gain))]

def choose_node(candidateAttr, candidateSample, parent) :
    global db
    global attributelist
    global valuelist
    node = Node_forGain(-1, candidateSample, parent)
    if len(candidateSample) <= 200 and info_Gain(candidateSample) < 0 * len(valuelist[attributelist[node.myAtt]]):
        node.result = calculate_forGain(candidateSample, node)
        return node
    if len(candidateSample) <= 100 and info_Gain(candidateSample) < 0 * len(valuelist[attributelist[node.myAtt]]):
        node.result = calculate_forGain(candidateSample, node)
        return node
    if len(candidateSample) <=30 and info_Gain(candidateSample) < 0 * len(valuelist[attributelist[node.myAtt]]):
        
        node.result = calculate_forGain(candidateSample, node)
        return node
    if len(candidateSample) <=20 and info_Gain(candidateSample) < 0 * len(valuelist[attributelist[node.myAtt]]):
        
        node.result = calculate_forGain(candidateSample, node)
        return node
    if len(candidateAttr) == 0 or info_Gain(candidateSample) == 0:
        node.result = calculate_forGain(candidateSample, node)
        return node
    node.myAtt = bestnextnode(candidateAttr, candidateSample)
    if node.myAtt == -1 :
        node.result = calculate_forGain(candidateSample, node)
        return node
    myatt = copy.deepcopy(candidateAttr)
    myatt.remove(node.myAtt)

    for val in valuelist[attributelist[node.myAtt]] :
        newSet = []
        for sample in candidateSample :
            if db[sample][node.myAtt] == val :
                newSet.append(sample)
        if len(newSet) == 0 :
            node.childlist.append(Node_forGain(calculate_forGain(candidateSample, node),[],node))
        else :
            node.childlist.append(choose_node(myatt, newSet, node))
    return node




def make_DecisionTree_Gain() :
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
def test_Gain(sample, node) :
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
        w.write('\t' + test_Gain(sample, node))
    w.close()
    return

if __name__ == "__main__":
    readFile(sys.argv[1], 'train')
    readFile(sys.argv[2], 'test')
    make_valuelist()
    node = make_DecisionTree_Gain()
    output(sys.argv[3], node)
    cnt = 0