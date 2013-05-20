#!/usr/bin/python
from sys import argv, exit
from getopt import getopt, GetoptError

def readXml(inFile, stepLen, xmlList):
    inputFile = open(inFile)

    flagRead = False
    outStr = ''
    keyStart = ''
    count = 0

    for line in iter(inputFile.readline, ''):
        if not flagRead and line.find('<') == 0 and line.find('>') != -1: 
            if line.find('!') == -1 and line.find('?') == -1:
                flagRead = True
                keyStart = line[line.find('<') + 1 : line.find('>')]
        if flagRead:
            outStr = outStr + line
        if line.find(keyStart) != -1 and line.find('</') == 0:
            flagRead = False
            keyStart = ''
            count = count + 1
        if not flagRead and count == stepLen:
            xmlList.append(outStr)
            outStr = ''
            count = 0
    inputFile.close()

def printHelp():
    print("sort xml in input file")
    print("options:")
    print("\t -i input file                                 ")
    print("\t -n the num of xml in a recode (2 as default)  ")
    exit(0)

def getOpts(argv):
    try:
        opts, args = getopt(argv[1:], "i:n:h")
        for op, val in opts:
            if op == '-i':
                indata = val
            if op == '-n':
                stepLen = val
            if op == '-h':
                printHelp()
        if 1 == len(opts):
            return indata, 2 
        elif 2 == len(opts):
            return indata, stepLen 
        else:
            printHelp() 
    except GetoptError:
        printHelp()

if __name__ == '__main__':
    inFile, stepLen = getOpts(argv) 
    xmlList = [] 

    readXml(inFile, int(stepLen), xmlList)
    #sort xml list and print 
    xmlList.sort()
    for item in xmlList:
        print item
