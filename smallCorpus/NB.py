from collections import Counter
import sys, os, json, math


class Node:
    #we have this class just to store variables that are closely related to this file
    #exists to make life very easy isntead of juggling so many dictionaries
    def __init__(self, fileName, label, corrispondingVector):
        self.name = fileName
        self.label = label
        self.vector = corrispondingVector

    #not good code
    #it just gets the vocab of the local file, not of the whole directory
    #so then make it return a dictionary?
    def getVocab(self):
        count = 0
        for word in self.vector:
            count += 1
        return count
    
    #TODO
    #make sure these class functions make sense and function properlly
    #itll be a bitch to count :///
    #i could also use the smaller corpus to really make it easier for me

    #this is great code, itll help a lot when it comes to finding localTokens
    #under a label
    def getToken(self):
        count = 0
        for word in self.vector:
            count += self.vector[word]
        return count

    def printNode(self):
        print(self.name, self.label)
        print(self.vector)

    #this has the potential to blow up
    #mathematically speaking ofc
    #itll def come from how the labels and her tokens will work out
    def addOneSmoothing(self, tokens, vocab):
        for word in self.vector:
            self.vector[word] = ((self.vector[word] + 1)/(tokens+vocab))


def totalDoc(fileDirectory):
    #simple function, finds teh total amount of documents in our wanted directory
    #that being train
    #important for our prob of class
    count = 0
    for root, dirs, files in os.walk(fileDirectory):
        for file in files:
            count+=1
    return count

def getSubDirectories(fileDirectory):
    for root, dirs, files in os.walk(fileDirectory):
        return dirs

#gets our probability of all lables in our train file
def findLabelProb(fileDirectory, totalDocuments, classLabel):
    count = 0
    for root, dirs, files in os.walk(fileDirectory):
        for file in files:
            if classLabel in root:
                if(file.endswith(".txt")):
                    count += 1
    print("There are", count, "documents in the class label",classLabel)
    return (count/totalDocuments)

def loadJSONInput(jsonFile):
    temp = {}
    with open(jsonFile, 'r') as file:
        temp = json.load(file)
    return temp

def classifyVectors(vectorSpace):
    #this is going to be a dictionary of appropriate information
    temp = {}
    for label in vectorSpace:
        for file in vectorSpace[label]:
            temp[file] = Node(file, label, vectorSpace[label][file])
    return temp

def getTotalVocab(vecorSpace):
    totalVocab = 0
    vocabDictionary = {}
    for file in vecorSpace:
        for word in vecorSpace[file].vector:
            if word not in vocabDictionary:
                vocabDictionary[word] = 1
                totalVocab += 1
            else:
                continue
    return totalVocab

def getLocalTokens(label, vectors):
    tokens = 0
    for file in vectors:
        if label == vectors[file].label:
            tokens += vectors[file].getToken()
    return tokens

def globalVocab(vectors):
    temp = {}
    count = 0

    for file in vectors:
        temp = Counter(temp)+ Counter(vectors[file].vector)

    for word in temp:
        count += 1

    print("there are", count, "words in our documents")
    return temp

def trainNB(labelProbs, vectors, labelTokens, totalVocab):
    
    #logprior is our labels which we imported
    logPrior = {}
    for label in labelProbs:
        logPrior[label] = math.log(labelProbs[label], 10)

    v = globalVocab(vectors)
    #v = vocabulary of D
        #meaning that v represents the entire vocabulary of all these documents
    
    bigdoc = {}
    for classLabel in labelProbs:
        if classLabel not in bigdoc:
            bigdoc[classLabel] = {}
    
    for classLabel in labelProbs:
        #this is if the label exists in the label
        for file in vectors:
            if vectors[file].label != classLabel:
                continue
            else:
                temp = vectors[file].vector
                #the appending temp to bigdoc
                #apperently counter does what i need to do

                #this should be an empty list
                bigdoc[classLabel] = Counter(temp) + Counter(bigdoc[classLabel])
                #print(bigdoc[classLabel])
        
        loglikelihood = {}
        for classLabel in labelProbs:
            loglikelihood[classLabel] = {}

        for label in bigdoc:
            for word in bigdoc[label]:
                #print(word, label, (bigdoc[label][word]+1), (labelTokens[label] + totalVocab), labelTokens[label], totalVocab)
                #gotta define the base for log
                loglikelihood[label][word] = math.log( (bigdoc[label][word]+1) / (labelTokens[label] + totalVocab), 10)

    return logPrior, loglikelihood, v 

#function logic was ripped out of the textbook
#god i hope this works
def testNB(testDoc, logprior, loglikelihood, labelProbs, V):
    for classLabel in labelProbs:
        sum[classLabel] = logprior[classLabel]
        for i in testDoc:
            word = testDoc[i]
            if word in V:
                sum[classLabel] = sum[classLabel] + loglikelihood[word][classLabel]
    #what the fuck does this mean by returning the best c?

    return argmax(sum)

def argmax(x):
    #unironically a leetcode question
    #x is a list, remember that
    max = -sys.maxsize - 1
    guessedLabel = ""
    for classLabel in x:

        if x[classLabel]>max:
            max = x[classLabel]
            guessedLabel = classLabel
    #print(max, guessedLabel)
    return max, guessedLabel

#this is strictly for part c of the hw2 spec
#remember that this string has an unknown label and we wish to figure out what it is
def answerForPartC(string, logPrior, loglikelihood, v, c):
    #dont forget to get rid of the words that you dont want
    temp = string.split()
    #cool, so we have our words, now what do we want to do?
    #compare said words with waht?

    #the algorithm is functionally comparable to testNB
    #parameters and algorithm was modified so it can just take a string of data rather than a vector space
    #doesnt take much space besides the comments included inside this function
    sum = {}
    for classLabel in c:
        sum[classLabel] = logPrior[classLabel]
        for word in temp:
            if word in v:
                if word in loglikelihood[classLabel]:
                    sum[classLabel] = sum[classLabel] + loglikelihood[classLabel][word]
        
                #TODO
                    #what do we do with words that do not appear in one label but appear in another?
                    #we cant have 0 becuase itll take up WAYY too much space
                    #the size of N would be too big
                    #>ignore unknown words?
                        #lets try taht
                    #yeah just ignore the unknown words, thats the shit that works
            if word not in v:
                print("now what?")
    
    print("the shitty function is done", sum)
    return argmax(sum)

def main(**args):
    trainFile = sys.argv[1]
    testFile = sys.argv[2]
    parameterFile = sys.argv[3]
    trainPPFile = sys.argv[4]
    testPPFile = sys.argv[5]


    totalDocuments = totalDoc(trainFile)
    print("There are", totalDocuments, "total documents")

    #this lets us get the possible classes according to our binary system
    classes = getSubDirectories(trainFile)

    #stores our class label probs into a place where its easy to get thanks to loop functions
    classLabelProbs = {}
    for labelProb in classes:
        classLabelProbs[labelProb] = findLabelProb(trainFile, totalDocuments, labelProb)

    #print(classLabelProbs)

    #code to modify our input vector files
    trainVectors = loadJSONInput(trainPPFile)
    testVectors = loadJSONInput(testPPFile)

    #yummy OOP variables to hold this ton of data
    trainClasses = classifyVectors(trainVectors)
    testClasses = classifyVectors(testVectors)

    #gotta write code to get the local class Tokens and the totalVocab
    totalVocab = getTotalVocab(trainClasses)

    labelTokens = {}
    for label in classes:
        labelTokens[label] = getLocalTokens(label, trainClasses)

    #making sure that the localClassLabel is associated with the file label
    #would by my problem for this function
    print(labelTokens)
    print(totalVocab)

    #this returns the data we get out of training our NB information
    #logPrior holds the logged probability of our class probability
    #loglikelihood holds all the logged addOneSmoothing under 
        #we log everything so we can just add instead of multiplying
        #saves so much computation 
    #v holds ALL vocabulary and their counted tokens
        #basically merges our class dictionaries and their values so we can see how many words exist
            # under train instead of our local class vocabulary
        # v just makes it easy to execute add one smoothing
        # eventually it will be needed for trainNB to find the sum of the current classFile we're on
        
        #TODO
            #theres something else this will need to find out how accurate our labeled test files are
        

    #cant really use the textbook algorithm for testNB, it'll need some other kind of information
        #aka, wont really fit into the parameters ive supplied and it wont do what i need it to do 
        #which is finding how accurate our current test document label is to the information that was found in train
        #we do this by
    trainTouple = trainNB(classLabelProbs, trainClasses, labelTokens, totalVocab)
    logPrior = trainTouple[0]
    loglikelihood = trainTouple[1]
    v = trainTouple[2]


    print(trainTouple)

    #im ashamed to hard code this in
    #but with the way i set up trainNB, it needs labels to properly function
    #maybe i can actually try to dynamically solve this, we'll see how it plays out

    #TODO
        #create a new name for classLabelProbs, its a shitty name for the information it holds
        #find a way to ONLY run this if we're thinking on the small corpus
        #maybe add more args functions?
    answerForPartC("fast couple shoot fly", logPrior, loglikelihood, v, classLabelProbs)


    #testdocument shit
    #we have our test document space ofc
    for file in testClasses:
        testClasses[file].printNode()
    #remember that most of the variables in this parameter come from
    #training data, just worry about your test classes
    #testNB(testClasses, logPrior, loglikelihood, classLabelProbs,v)


    #now i have to fix the test document shit
    #its the same algorithm that i used for train isnt it
    

if __name__ == "__main__":
    main()