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
    global finalPredicateDict
    global finalPredicateList
    global singleLiteralList
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

        # add to finalPredicateDict
        for i in range(len(tempCNF)):
            splitPredicate = tempCNF[i].split('(')
            predicate = splitPredicate[0]
            # print("predicate: ", predicate)
            if predicate not in finalPredicateDict.keys():
                finalPredicateDict[predicate] = []
            finalPredicateDict[predicate].append([sentenceIndex, i])
            # convert to object
            temppredicateList.append(Predicates(tempCNF[i]))

        finalPredicateList.append(temppredicateList)

    # single literal
    else:
        splitPredicate = sentenceList[0].split('(')
        predicate = splitPredicate[0]
        # print(predicate)
        if predicate not in finalPredicateDict.keys():
            finalPredicateDict[predicate] = []
        finalPredicateDict[predicate].append([sentenceIndex, 0])
        tempPredicatesPbject = Predicates(sentenceList[0])
        singleLiteralList.append(tempPredicatesPbject)
        finalPredicateList.append([tempPredicatesPbject])

def negateQuery(query):
    if query.isNegative == False:
        query.predicateName = '~' + query.predicateName
        query.isNegative = True
    else:
        query.isNegative = False
        query.predicateName = query.predicateName[1:]

def resolution(query):
    global finalPredicateDict
    global finalPredicateList
    global singleLiteralList
    newCNF = []
    variableIndex = -1
    predicateList = copy.deepcopy(finalPredicateList)
    predicateDict = copy.deepcopy(finalPredicateDict)
    #negate query and add to predicateList and predicateDict
    negateQuery(query)
    predicateList.append([query])
    if query.predicateName not in predicateDict.keys():
        predicateDict[query.predicateName] = []
    predicateDict[query.predicateName].append([len(predicateList)-1, 0])
    ###

    copySingleLiteralList = copy.deepcopy(singleLiteralList)
    copySingleLiteralList.append(query)

    for singleLiteral in copySingleLiteralList:
        if singleLiteral.isNegative == True:
            predicateNameNeeded = singleLiteral.predicateName[1:]
        else:
            predicateNameNeeded = '~' + singleLiteral.predicateName
        if predicateDict.get(predicateNameNeeded) == None:
            continue
        index = predicateDict.get(predicateNameNeeded).copy()
        # print("predicateNameNeeded: ", predicateNameNeeded)
        # print("index: ", index)
        for currentIndex in index:
            variableDict = {}
            nextIndex = False
            tempPredicateList = copy.deepcopy(predicateList[currentIndex[0]])
            targetPredicate = tempPredicateList[currentIndex[1]]
            # print("predicateList: ", index)
            # print("query.predicateName: ", query.predicateName)

            # unify variables
            # print("targetPredicate.predicateName: ", targetPredicate.predicateName)
            for i in range(len(targetPredicate.arguments)):
                if targetPredicate.arguments[i].islower() and not singleLiteral.arguments[i].islower():
                    variableName = targetPredicate.arguments[i]
                    targetPredicate.arguments[i] = singleLiteral.arguments[i]
                    # print("predicate.arguments[i]: ", targetPredicate.arguments[i])
                    variableDict[variableName] = singleLiteral.arguments[i]
                elif not targetPredicate.arguments[i].islower() and singleLiteral.arguments[i].islower():
                    variableName = singleLiteral.arguments[i]
                    singleLiteral.arguments[i] = targetPredicate.arguments[i]
                    # print("predicate.arguments[i]: ", targetPredicate.arguments[i])
                    variableDict[variableName] = targetPredicate.arguments[i]
                elif not targetPredicate.arguments[i].islower() and not singleLiteral.arguments[i].islower():
                    if targetPredicate.arguments[i] != singleLiteral.arguments[i]:
                        nextIndex = True
                        break
                    if targetPredicate.arguments[i] == singleLiteral.arguments[i]:
                        continue
            if nextIndex:
                continue
            
            # print("variableDict: ", variableDict)
            for predict in tempPredicateList:
                for i in range(len(predict.arguments)):
                    if predict.arguments[i].islower():
                        variableName = predict.arguments[i]
                        if variableDict.get(variableName) != None:
                            predict.arguments[i] = variableDict.get(variableName)
            
            # print("predict.predicateName: ", predict.predicateName)
            # print("predicate.arguments[i]: ", predict.arguments)
            tempPredicateList.pop(currentIndex[1])
            if not tempPredicateList:
                return True

            predicateList.append(tempPredicateList)
            tempIndex = 0
            for predicate in tempPredicateList:
                if predicate.predicateName not in predicateDict.keys():
                    predicateDict[predicate.predicateName] = []
                predicateDict[predicate.predicateName].append([len(predicateList)-1, tempIndex])
                tempIndex += 1
            if len(tempPredicateList) == 1:
                copySingleLiteralList.append(tempPredicateList[0])
    return False

def output(answer, currentQuery, queryNum):
    f = open("output.txt", "a")
    if answer:
        f.write("TRUE")
    else:
        f.write("FALSE")
    if currentQuery != queryNum:
        f.write("\n")

# read input file
lineNum = 0
queryNum = 0
FOLNum = 0
currentQuery = 0
queryList = []
FOLList = []
finalPredicateDict = {}
sentenceList = []
finalPredicateList = []
singleLiteralList = []
sentenceIndex = 0
inputFile = open("input.txt", "r")
outputFile = open("output.txt", "w")
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
for query in queryList:
    currentQuery += 1
    answer = resolution(query)
    output(answer, currentQuery, queryNum)
    print(answer)