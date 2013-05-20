#!/usr/bin/python
from xml.dom.minidom import parse 
from xml.dom.minidom import getDOMImplementation 
from sys import argv, exit
from getopt import getopt, GetoptError
import os

CTRL_A = ''
CTRL_B = ''
CTRL_C = ''
keyVal = dict()
repeatId = dict()

def fstrDict(nameStr):
    if nameStr in keyVal:
        return True
    else:
        nameList = nameStr.split(CTRL_C, 1)
        if len(nameList) == 2:
            return fstrDict(nameList[1])
        else:
            return False

def setVaule(keyName, nodeW):
    itemList = keyVal[keyName].pop(0)
    if 0 == len(keyVal[keyName]):
        del keyVal[keyName]
    valW = domW.createTextNode(itemList)
    nodeW.appendChild(valW)

def setAttri(root, nodeW):
    for i in range(root.attributes.length):
        attrKey = root.attributes.item(i).name
        attrVal = root.attributes.item(i).value
        attr = domW.createAttribute(attrKey)
        nodeW.setAttributeNode(attr)
        nodeW.setAttribute(attrKey, attrVal)
    
def setxmlText(root, rootW, nameStr):
    if root.ELEMENT_NODE == root.nodeType: 
        nodeW = domW.createElement(root.nodeName)
        rootW.appendChild(nodeW)

        nameStr = nameStr + CTRL_C + root.nodeName

        if root.hasAttributes():
            setAttri(root, nodeW)

        if root.nodeName in keyVal: 
            setVaule(root.nodeName, nodeW)
        elif fstrDict(nameStr): 
            while nameStr not in keyVal:
                nameStr = nameStr.split(CTRL_C, 1)[1]
            setVaule(nameStr, nodeW)
        else:
            for node in root.childNodes:
                setxmlText(node, nodeW, nameStr)
    elif root.TEXT_NODE == root.nodeType:
        val = root.nodeValue.rstrip().strip()
        if '' != val:
            valW = domW.createTextNode(val)
            rootW.appendChild(valW)

def getkeyVal(line):
    inList = line.strip().split(CTRL_A)
    for item in inList:
        tmpList = item.split(CTRL_B)
        if tmpList[0] not in keyVal:
            keyVal[tmpList[0]] = [tmpList[1]]
        else:
            keyVal[tmpList[0]].append(tmpList[1])
        
def getRepeat():
    for key in keyVal:
        if len(keyVal[key]) > 1:
            tmpKey = key.split(CTRL_C)[0]
            if tmpKey not in repeatId:
                repeatId[tmpKey] = len(keyVal[key])
            else:
                if repeatId[tmpKey] < len(keyVal[key]):
                    repeatId[tmpKey] = len(keyVal[key])

def setRepeat(root, domR):
    if root.ELEMENT_NODE == root.nodeType: 
        for node in root.childNodes:
            if node.nodeName in repeatId: 
                nodeList = domR.getElementsByTagName(node.nodeName)
                #the length of nodeList is 1
                for i in range(repeatId[node.nodeName] -1):
                    newNode = nodeList[0].cloneNode('deep')
                    root.appendChild(newNode)
                del repeatId[node.nodeName]
            setRepeat(node, domR)

def getrepeatDom(tpl, line):
    repeatId.clear()
    getRepeat()

    dom = parse(tpl)
    root = dom.documentElement
    domR = impl.createDocument(None, root.nodeName, None)
    rootW = domR.documentElement
    for node in root.childNodes:
        if root.ELEMENT_NODE == root.nodeType: 
            newNode = node.cloneNode('deep')
            rootW.appendChild(newNode)
    setRepeat(rootW, domR)
    return domR

def printxmlVal(node):
    for child in node.childNodes:
        val = child.nodeValue.strip()
        if '' != val:
            print val

def getxmlVal(node, key):
    print key
    for child in node.childNodes:
        if child.nodeName == key:
            printxmlVal(child) 
        elif child.hasChildNodes(): 
            getxmlVal(child, key)

def delemptyNode(xmlList):
    hasEmpty = False
    keyLast = ''
    key = ''
    count = 0

    for line in xmlList: 
        if line.find('</') != -1 and line.find('>') != -1: 
            key = line[line.find('</') + 2 : line.find('>')]
        elif line.find('<') != -1 and line.find('>') != -1: 
            key = line[line.find('<') + 1 : line.find('>')]
            if key.find('fieldName') != -1:
                key = key[:key.find('fieldName')]
        else:
            key = 'Text'
        
        if key.strip() == keyLast.strip():
            del xmlList[count]
            del xmlList[count - 1]
            hasEmpty = True

        keyLast = key
        count = count + 1

    return hasEmpty

def delemptyeElemet(inFile, outFile):
    inputFile = open(inFile)
    outputFile = open(outFile, 'w')
    hasEmpty = True

    xmlList = [] 
    for line in iter(inputFile.readline, ''):
        if line.rfind('/>') != -1 and line.find('<') != -1:
            continue
        xmlList.append(line)
    inputFile.close()

    while hasEmpty:
        hasEmpty = delemptyNode(xmlList) 

    for line in xmlList:
        outputFile.write(line) 
    outputFile.close()
    os.remove(inFile)

def printHelp():
    print("transform testdata to xml by xmltpls")
    print("options:")
    print("\t -k xml tpl for key  ")
    print("\t -v xml tpl for value")
    print("\t -i input file       ")
    print("\t -o output file      ")
    print("set value by key in xml file")
    print("options:")
    print("\t -k key  ")
    print("\t -v new value for key")
    print("\t -i xml file to edit")
    print("get value by key in xml file")
    print("options:")
    print("\t -k key  ")
    print("\t -i xml file")

    exit(0)

def getOpts(argv):
    try:
        opts, args = getopt(argv[1:], "k:v:i:o:h")
        for op, val in opts:
            if op == '-k':
                tplkey = val
            if op == '-v':
                tplval = val
            if op == '-i':
                indata = val
            if op == '-o':
                outfile = val
            if op == '-h':
                printHelp()
        if 4 == len(opts):
            return tplkey, tplval, indata, outfile
        elif 3 == len(opts):
            return tplkey, tplval, indata
        elif 2 == len(opts):
            return tplkey, indata
        else:
            printHelp() 
    except GetoptError:
        printHelp()

if __name__ == '__main__':
    impl = getDOMImplementation()
    optTuple = getOpts(argv) 
    if 4 == len(optTuple):
        tplkey, tplval, indata, outfile = optTuple
        tmpoutFile = outfile + '_tmp'

        inputFile = open(indata)
        output = open(tmpoutFile, 'w')
        i = 0

        for line in iter(inputFile.readline, ''):
            if line.find('#') == 0 or line == '\n':
                continue
            keyVal.clear()
            getkeyVal(line)
            if 0 == i % 2:
                dom = getrepeatDom(tplkey, line) 
                root = dom.documentElement
                domW = impl.createDocument(None, root.nodeName, None)
                rootW = domW.documentElement
                nameStr = root.nodeName
                for node in root.childNodes:
                    if root.ELEMENT_NODE == root.nodeType: 
                        setxmlText(node, rootW, nameStr)
                domW.writexml(output, addindent = '	', newl = '\n', encoding = 'utf-8')
            else:
                dom = getrepeatDom(tplval, line) 
                root = dom.documentElement
                domW = impl.createDocument(None, root.nodeName, None)
                rootW = domW.documentElement
                nameStr = root.nodeName
                for node in root.childNodes:
                    if root.ELEMENT_NODE == root.nodeType: 
                        setxmlText(node, rootW, nameStr)
                domW.writexml(output, addindent = '	', newl = '\n', encoding = 'utf-8')
            i = i + 1
        inputFile.close()
        output.close()
        delemptyeElemet(tmpoutFile, outfile)

    elif 3 == len(optTuple):
        key, value, xmlfile = optTuple
        getkeyVal(key + CTRL_B + value)
        nameStr = ''

        dom = parse(xmlfile)
        root = dom.documentElement
        domW = impl.createDocument(None, root.nodeName, None)
        rootW = domW.documentElement

        output = open(xmlfile, 'w')
        nameStr = root.nodeName
        for node in root.childNodes:
            if root.ELEMENT_NODE == root.nodeType: 
                setxmlText(node, rootW, nameStr)

        domW.writexml(output, addindent = '	', newl = '\n', encoding = 'utf-8')
        output.close()

    elif 2 == len(optTuple):
        key, xmlfile = optTuple
        dom = parse(xmlfile)
        root = dom.documentElement
        getxmlVal(root, key)

