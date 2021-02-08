import sys
import copy
import math


db = [] #trainset
attributelist = ()  #kinds of attribute
valuelist = {}  #kinds of values of each attribute
splitlist = []  #all possible binary partition
testdb = [] #testset

## There is implementation of two measurement that are information gain + gain ratio and gini index
## Choose gini after testing because of accuracy(gini index : 338/346, gain_ratio : 322/346 at tester program)
## If tester want to test information gain, please change output(sys.argv[3], node, node_gain, 'gini') in main function
## I comment [Gini] : , and [Gain] : for each measurement function


# [Gini] : Node for making tree using gini measure
class Node :
    def __init__(self, result, candidateSet, parent) :
        self.rightchild = -1
        self.leftchild = -1
        self.splitnum = -1
        self.result = result
        self.candidateSet = candidateSet
        self.parent = parent

# [Gain] : Node for making tree using Information gain + Gain Ratio measure
class Node_forGain :
    def __init__(self, result, set, parent) :
        self.childlist = []
        self.myAtt = -1
        self.result = result
        self.candidateSet = set
        self.parent = parent


# [Gain] : function for calculating information gain
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

# [Gain] : function for finding best attribute by using information gain + gain ratio
def bestnextnode(candidateAttr, candidateSample) :
    global valuelist
    global attributelist
    myinfo = info_Gain(candidateSample)
    if myinfo == 0 :
        return -1
    gain = []
    for cand in candidateAttr :
        partialinfo = []
        # splitinfo for Gain_Ratio
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
                # calculate Gain_Ratio of every candidate of child attribute
                splitinfo.append(math.log(len(newsample)/len(candidateSample),2)*len(newsample)/len(candidateSample))
        gain.append((myinfo - sum(partialinfo))/(-sum(splitinfo)))
    if max(gain) <= 0 :
        return -1
    return candidateAttr[gain.index(max(gain))]

# [Gain] : recursive function for making complete tree 
def choose_node(candidateAttr, candidateSample, parent) :
    global db
    global attributelist
    global valuelist
    node = Node_forGain(-1, candidateSample, parent)
    node.myAtt = bestnextnode(candidateAttr, candidateSample)
    # terminal condition if no more attribute for classification
    if node.myAtt == -1 :
        node.result = calculate(node)
        return node
    myatt = copy.deepcopy(candidateAttr)
    myatt.remove(node.myAtt)

    for val in valuelist[attributelist[node.myAtt]] :
        newSet = []
        for sample in candidateSample :
            if db[sample][node.myAtt] == val :
                newSet.append(sample)
        # terminal condition if candidate sample is none.
        if len(newSet) == 0 :
            node.childlist.append(Node_forGain(calculate(node),[],node))
        else :
            node.childlist.append(choose_node(myatt, newSet, node))
    return node

# [Gain] : Making decision tree by using a measurement of information gain + gain ratio
def make_DecisionTree_Gain() :
    global db
    global attributelist
    initialSample = list(range(0,len(db)))
    initialAttr = list(range(0,len(attributelist)-1))
    node = choose_node(initialAttr, initialSample, 0)
    return node

# [Gini], [Gain]  : function for find appropriate class label to leaf node 
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

# [Gini] : recursive function for Making tree by using gini index
def choose(node, splitcandidate, depth) :
    global splitlist
    global attributelist
    global db
    # terminal condition if there is no candidate in leaf node
    if len(node.candidateSet) == 0 :
        node.result = calculate(node.parent)
        return;

    # post prunning for avoiding overfitting
    if depth ==  10 :
        node.result = calculate(node)
        return;

    #threshold : if you want to quit the recursion early, change this variable more than 0
    initial = -100000

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

    # terminal condition if there is no more attribute that delta gini is positive
    if node.leftchild == -1 or node.rightchild == -1 :
        node.result = calculate(node)

# [Gini] : function for calculating gini indexA
def calculate_giniA(candidateSet, leftcandidate, rightcandidate) :
    if len(candidateSet) == 0 :
        return 0
    return (len(leftcandidate)/len(candidateSet))*gini_index(leftcandidate) + (len(rightcandidate)/len(candidateSet))*gini_index(rightcandidate)

# [Gini] : function for calculating gini index
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

# [Gini] : function for making all possible combination of split
def make_ginisplit() :
    global attributelist

    for i in range (0, len(attributelist) - 1) :
        split([], [], i, 0 )
        split([], [], i, 0 )

# [Gini] : recursive function for making all possible combination of split
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

# [Gini] : Function for starting to make decision by using decision tree
def make_DecisionTree() :
    global db
    global attributelist
    global splitlist
    initialSample = list(range(0,len(db)))
    make_ginisplit()
    node = Node(-1, initialSample, -1)
    choose(node,list(range(0,len(splitlist))),0)
    return node 

# Save test input to testdb
def testFileHandler(lines) :
    global testdb
    del lines[0]
    for temp in lines :
        testdb.append(temp.split())

# Save train input to db
def trainFileHandler(lines) :
    global attributelist
    global valuelist
    global db
    # Make set of kinds of attribute
    attributelist = lines[0].split()
    del lines[0]
    for temp in lines :
        db.append(temp.split())

# Make list of all possible kinds of value of every attributes
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

# Read file that has filename, parameter mode means which that file traintext or testtext
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

# [Gini] : Function for testing the testdb by using decision tree that made by Gini Index
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

# [Gain] : Function for testing the testdb by using decision tree that made by Information Gain + Gain Ratio
def test_Gain(sample, node) :
    global valuelist
    global attributelist
    while node.result == -1 :
        node = node.childlist[valuelist[attributelist[node.myAtt]].index(sample[node.myAtt])]
    return valuelist[attributelist[-1]][node.result]

# File write function
def output(filename, node, node_gain, measurement) :
    global testdb
    global attributelist
    w = open(filename, mode = 'w', encoding = 'utf-8')
    w.write('\t'.join(attributelist))
    for sample in testdb :
        w.write('\n')
        w.write('\t'.join(sample))
        if measurement == 'gini' :
            w.write('\t' + test(sample, node))
        if measurement == 'gain' :
             w.write('\t' + test_Gain(sample, node_gain))
    w.close()
    return

# Main function
if __name__ == "__main__":
    readFile(sys.argv[1], 'train')
    readFile(sys.argv[2], 'test')
    make_valuelist()
    node = make_DecisionTree()
    node_gain = make_DecisionTree_Gain()
    output(sys.argv[3], node, node_gain, 'gini') #if you want to using gain, change gini to gain
