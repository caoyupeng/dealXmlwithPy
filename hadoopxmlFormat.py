#!/usr/bin/python
from xml.dom.minidom import parse 
from xml.dom.minidom import getDOMImplementation 
from sys import argv, exit
from getopt import getopt, GetoptError

def setValue(val, nodeW):
    valW = domW.createTextNode(val)
    nodeW.appendChild(valW)

def setAttri(root, nodeW):
    for i in range(root.attributes.length):
        attrKey = root.attributes.item(i).name
        attrVal = root.attributes.item(i).value
        attr = domW.createAttribute(attrKey)
        nodeW.setAttributeNode(attr)
        nodeW.setAttribute(attrKey, attrVal)
    
def setxmlText(root, rootW, key, value, name_key, property):
    if root.ELEMENT_NODE == root.nodeType: 
        nodeW = domW.createElement(root.nodeName)
        rootW.appendChild(nodeW)

        if root.hasAttributes():
            setAttri(root, nodeW)

        if root.nodeName == key:
            for text in root.childNodes:
                val = text.nodeValue.strip()
                if val in property:
                    name_key.append(val)
                if '' != val:
                    setValue(val, nodeW)
        elif root.nodeName == value: 
            for text in root.childNodes:
                val = text.nodeValue.strip()
                if len(name_key) != 0:
                    namekeyTmp = name_key.pop()
                    if '' != val and '' != namekeyTmp and property[namekeyTmp] != val:
                        val = property[namekeyTmp]
                if '' != val:
                    setValue(val, nodeW)
        else:
            for node in root.childNodes:
                setxmlText(node, nodeW, key, value, name_key, property)
    elif root.TEXT_NODE == root.nodeType:
        val = root.nodeValue.rstrip().strip()
        if '' != val:
            valW = domW.createTextNode(val)
            rootW.appendChild(valW)

        
def getxmlVal(node, name, value, key_name, property):
    name_key_tmp = ''
    for child in node.childNodes:
        if child.nodeName == name:
            for text in child.childNodes:
                val = text.nodeValue.strip()
                if key_name == val and val not in property:
                    property[val] = ''
                    name_key_tmp = val
        elif child.nodeName == value: 
            for text in child.childNodes:
                val = text.nodeValue.strip()
                if '' != val and '' != name_key_tmp:
                    property[name_key_tmp] = val
        elif child.hasChildNodes(): 
            getxmlVal(child, name, value, key_name, property )

def printHelp():
    print("get nodevalue of value from xml by nodevalue of key")
    print("options:")
    print("\t -k nodename of key    ")
    print("\t -v nodename of value  ")
    print("\t -n nodevalue of key   ")
    print("\t -i input file         ")
    print("set nodevalue of value from xml by nodevalue of key")
    print("options:")
    print("\t -k nodename of key    ")
    print("\t -v nodename of value  ")
    print("\t -n nodevalue of key   ")
    print("\t -m nodevalue of value ")
    print("\t -i input file         ")
    exit(0)

def getOpts(argv):
    try:
        opts, args = getopt(argv[1:], "k:v:i:m:n:h")
        for op, val in opts:
            if op == '-k':
                tplkey = val
            if op == '-v':
                tplvalue = val
            if op == '-i':
                indata = val
            if op == '-m':
                valName = val
            if op == '-n':
                keyName = val
            if op == '-h':
                printHelp()
        if 4 == len(opts):
            return tplkey, tplvalue, keyName, indata
        elif 5 == len(opts):
            return tplkey, tplvalue, keyName, valName, indata
        else:
            printHelp() 
    except GetoptError:
        printHelp()

if __name__ == '__main__':
    impl = getDOMImplementation()
    optTuple = getOpts(argv) 

    if 4 == len(optTuple):
        key, value, key_name, xmlfile = optTuple
        dom = parse(xmlfile)
        root = dom.documentElement
        property = dict()
        getxmlVal(root, key, value, key_name, property)
        if key_name in property:
            print property[key_name]
        else:
            print "fail to get " + key_name

    elif 5 == len(optTuple):
        key, value, key_name, value_name, xmlfile = optTuple

        dom = parse(xmlfile)
        root = dom.documentElement
        property = dict()
        getxmlVal(root, key, value, key_name, property)
        if key_name in property:
            property[key_name] = value_name
        else:
            print "fail to get " + key_name

        domW = impl.createDocument(None, root.nodeName, None)
        rootW = domW.documentElement

        output = open(xmlfile, 'w')
        for node in root.childNodes:
            name_key = [] 
            if root.ELEMENT_NODE == root.nodeType: 
                setxmlText(node, rootW, key, value, name_key, property)

        domW.writexml(output, addindent = '	', newl = '\n', encoding = 'utf-8')
        output.close()
