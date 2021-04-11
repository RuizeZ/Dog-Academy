class Predicates():
    def __init__(self, predicate):
        predicateList = predicate.split('(')
        if '~' in predicateList[0]:
            self.predicateName = predicateList[0][1:]
            self.isNegative = True
        else:
            self.predicateName = predicateList[0]
            self.isNegative = False
        self.arguments = predicateList[1][:-1].split(',')


def toCNF(sentence):
    isRight = False
    CNFList = []
    tempCNF = []
    global predicateDict
    sentenceList = sentence.split(' ')
    print(sentenceList)
    # parse sentence
    if len(sentenceList) != 1:
        for literal in sentenceList:
            if literal == "=>":
                isRight = True
                continue
            if not isRight:
                if literal == '&':
                    continue
                if literal[0] == '~':
                    tempCNF.append(literal[1:])
                else:
                    tempCNF.append('~'+literal)
            else:
                tempCNF.append(literal)
        # print("tempCNF: ",tempCNF)
        for i in range(len(tempCNF)):
            splitPredicate = tempCNF[i].split('(')
            predicate = splitPredicate[0]
            if predicate not in predicateDict.keys():
                predicateDict[predicate] = []
                # print(predicateDict)
            variable = splitPredicate[1][:-1]
            if len(variable) != 1:
                variable = variable.split(',')
            else:
                variable = [variable]
            tempCNFCopy = tempCNF.copy()
            tempCNFCopy.pop(i)
            # print("tempCNFCopy: ", tempCNFCopy)
            predicateDict[predicate].append([variable, tempCNFCopy])
            # print(predicateDict)
    else:
        splitPredicate = sentenceList[0].split('(')
        predicate = splitPredicate[0]
        if predicate not in predicateDict.keys():
            predicateDict[predicate] = []
            # print(predicateDict)
        variable = splitPredicate[1][:-1]
        if len(variable) != 1:
            variable = variable.split(',')
        else:
            variable = [variable]
        # print("tempCNFCopy: ", tempCNFCopy)
        predicateDict[predicate].append([variable])
        print(predicateDict)


# read input file
lineNum = 0
queryNum = 0
FOLNum = 0
queryList = []
FOLList = []
predicateDict = {}
inputFile = open("input.txt", "r")
for line in inputFile:
    lineNum += 1
    if lineNum == 1:
        queryNum = int(line.strip("\n"))
    elif lineNum <= queryNum + 1:
        queryLine = line.strip("\n")
        queryList.append(Predicates(queryLine))
    elif lineNum == queryNum + 2:
        FOLNum = int(line.strip("\n"))
    else:
        toCNF(line.strip("\n"))
        FOLList.append(line.strip("\n"))
# print(queryNum)
# print(queryList)
# print(FOLNum)
# print(FOLList)
# print("predicateDict =", predicateDict)
