#libraries for directory delving
import os, os.path
import re
import json
import sys

#TODO
#fix this so that your file names are a subdictionary of the label
#this way you can quickly get and understand what label this document falls under

def getSubDirectories(fileDirectory):
    for root, dirs, files in os.walk(fileDirectory):
        return dirs


def main():
    #these two are to find the probability of our labels in the training directory
    #might end up chopping off the true function
    # import required module

    #someplace to hold all of the files and their corresponding words

    fileDirectory = sys.argv[1]
    vectors = {}
    os.listdir(fileDirectory)

    classes = getSubDirectories(fileDirectory)

    for label in classes:
        vectors[label] = {}
        for root, dirs, files in os.walk(fileDirectory):
            for file in files:
                with open(os.path.join(root, file), "r", encoding="utf8") as auto:
                    if label not in root:
                        continue
                    try:
                        temp = auto.read()
                        temp = temp.lower()
                        temp = temp.replace('\'', '')
                        temp = temp.replace('-', '')
                        
                        temp.replace("<br /><br />", " br br ")
                        #TODO
                        #finish fixing regex logic
                        #you have a problem with your apostrophe character
                        list = re.sub(r'[^\w\s]', ' ', temp)

                        if file not in vectors:
                            vectors[label][file] = {}
                        
                        for word in list.split():
                            if word not in vectors[label][file]:
                                vectors[label][file][word] = 1
                            elif word in vectors[label][file]:
                                vectors[label][file][word] += 1

                    finally:
                        auto.close()
    
    jsonOutput = json.dumps(vectors, indent = 4)

    with open(sys.argv[1]+"OUTPUT.json", "w", encoding="utf8") as outfile:
        outfile.write(jsonOutput)
if __name__ == "__main__":
    main()
