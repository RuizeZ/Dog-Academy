import copy
class Predicates():
    def __init__(self, predicate):
        finalPredicateList = predicate.split('(')
        if '~' in finalPredicateList[0]:
            self.isNegative = True
        else:
            self.isNegative = False
        self.predicateName = finalPredicateList[0]
        self.arguments = finalPredicateList[1][:-1].split(',')
        # print("predicate.predicateName: ", self.predicateName)
        # print("predicate.arguments: ", self.arguments)


def toCNF(sentence, sentenceIndex):
    global predicateDict
    global finalPredicateList
    isRight = False
    tempCNF = []
    temppredicateList = []
    sentenceList = sentence.split(' ')

    # sentence
    if len(sentenceList) != 1:
        # convert sentence to CNF
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

        # add to predicateDict
        for i in range(len(tempCNF)):
            splitPredicate = tempCNF[i].split('(')
            predicate = splitPredicate[0]
            # print("predicate: ", predicate)
            if predicate not in predicateDict.keys():
                predicateDict[predicate] = []
            predicateDict[predicate].append([sentenceIndex, i])
            # convert to object
            temppredicateList.append(Predicates(tempCNF[i]))
        finalPredicateList.append(temppredicateList)

    # single literal
    else:
        splitPredicate = sentenceList[0].split('(')
        predicate = splitPredicate[0]
        print(predicate)
        if predicate not in predicateDict.keys():
            predicateDict[predicate] = []
        predicateDict[predicate].append([sentenceIndex, 0])
        finalPredicateList.append([Predicates(sentenceList[0])])


def resolution(query):
    global predicateDict
    global finalPredicateList
    
    oldQueryPredicateName = query.predicateName
    newCNF = []
    isNegation = False
    variableIndex = -1
    variableDict = {}
    if query.isNegative == False:
        query.predicateName = '~' + query.predicateName
        query.isNegative = True
        isNegation = True
    else:
        query.predicateName = query.predicateName[1:]
    newCNF.append(query)
    while newCNF:
        predicateList = copy.deepcopy(finalPredicateList)
        query = newCNF[0]
        print("query.predicateName: ", query.predicateName)
        print("query.arguments: ", query.arguments)
        if query.isNegative == True:
            predicateNameNeeded = query.predicateName[1:]
        else:
            predicateNameNeeded = '~' + query.predicateName
        if predicateDict.get(predicateNameNeeded) == None:
            print("Forward")
        index = predicateDict.get(predicateNameNeeded).copy()
        # print("predicateNameNeeded: ", predicateNameNeeded)
        # print("index: ", index)
        if len(index) == 1:
            index = index[0]
        else:
            sameConstant = False
            tempIndex = index.copy()
            for i in index:
                tempPredicate = predicateList[i[0]][i[1]]
                for j in range(len(tempPredicate.arguments)):
                    variableIndex += 1
                    if tempPredicate.arguments[j][0].isupper():
                        if tempPredicate.arguments[j] == query.arguments[variableIndex]:
                            sameConstant = True
                        else:
                            tempIndex.pop(tempIndex.index(i))
                            sameConstant = False
                            break
                variableIndex = -1
                if sameConstant:
                    index = i
                    break
            if not sameConstant:
                if len(tempIndex) == 0:
                    return False
                index = tempIndex[0]


        # print("predicateList: ", index)
        # print("query.predicateName: ", query.predicateName)

        # unify variables
        targetPredicate = predicateList[index[0]][index[1]]
        # print("targetPredicate.predicateName: ", targetPredicate.predicateName)
        for i in range(len(targetPredicate.arguments)):
            variableIndex += 1
            if len(targetPredicate.arguments[i]) == 1 and targetPredicate.arguments[i].islower():
                unifySuccess = True
                variableName = targetPredicate.arguments[i]
                targetPredicate.arguments[i] = query.arguments[variableIndex]
                # print("predicate.arguments[i]: ", targetPredicate.arguments[i])
                variableDict[variableName] = query.arguments[variableIndex]
            else:
                if targetPredicate.arguments[i] == query.arguments[variableIndex]:
                    unifySuccess = True
                    continue
                else:
                    unifySuccess = False
                    return False
        variableIndex = -1
        # print("variableDict: ", variableDict)
        for predict in predicateList[index[0]]:
            for i in range(len(predict.arguments)):
                variableIndex += 1
                if len(predict.arguments[i]) == 1 and predict.arguments[i].islower():
                    variableName = predict.arguments[i]
                    predict.arguments[i] = variableDict.get(variableName)
            variableIndex = -1
            # print("predict.predicateName: ", predict.predicateName)
            # print("predicate.arguments[i]: ", predict.arguments)
        variableDict = {}
        tempPredicateList = predicateList[index[0]].copy()
        tempPredicateList.pop(index[1])
        prevCNF = newCNF.copy()
        newCNF.pop(0)
        newCNF = tempPredicateList + newCNF
        # for i in predicateList:
        #     for j in i:
        #         print(j.predicateName)
        # print("newCNF")
        # for i in newCNF:
        #     print(i.predicateName)
        #     print(i.arguments)
    return True


# read input file
lineNum = 0
queryNum = 0
FOLNum = 0
queryList = []
FOLList = []
predicateDict = {}
sentenceList = []
finalPredicateList = []
sentenceIndex = 0
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
        toCNF(line.strip("\n"), sentenceIndex)
        sentenceIndex += 1
        FOLList.append(line.strip("\n"))
# print(queryNum)
# print(queryList)
# print(FOLNum)
# print("len predicateList: ",len(predicateList))
print("predicateDict =", predicateDict)
for query in queryList:
    print(resolution(query))