#Michael Furst
#February 4, 2018
#Read SPRL XML file and parse matching data from other files into new file

import xml.etree.ElementTree as ET
import re
class File:
    def __init__(self):
        self.text=""
        self.fileName=""
        return
    def __str__(self):
        s = ""
        s+=self.fileName+"\n"
        s+=self.text+"\n"
        return s
def findMatch(text):
    for i in range(0,774):
        name = "TRIPS_parses/train-sentences.txt-"+str(i+100)+".xml"
        try:
            _tree = ET.parse(name)
        except (FileNotFoundError,ET.ParseError):
            continue
        for scene in _tree.getroot():
            for element in scene:
                if element.tag=='SENTENCE':
                    if element.find('TEXT').text==text:
                        return name
    return ""

def cleanString(string):
    string = re.sub('[^a-zA-Z]',"",string)
    string = string.replace('A','a')
    string = string.replace('B','b')
    string = string.replace('C','c')
    string = string.replace('D','d')
    string = string.replace('E','e')
    string = string.replace('F','f')
    string = string.replace('G','g')
    string = string.replace('H','h')
    string = string.replace('I','i')
    string = string.replace('J','j')
    string = string.replace('K','k')
    string = string.replace('L','l')
    string = string.replace('M','m')
    string = string.replace('N','n')
    string = string.replace('O','o')
    string = string.replace('P','p')
    string = string.replace('Q','q')
    string = string.replace('R','r')
    string = string.replace('S','s')
    string = string.replace('T','t')
    string = string.replace('U','u')
    string = string.replace('V','v')
    string = string.replace('W','w')
    string = string.replace('X','x')
    string = string.replace('Y','y')
    string = string.replace('Z','z')
    return string

def findMatch(text,files):
    for file in files:
        t1 = cleanString(file.text)
        t2 = cleanString(text)
        if (t1==t2):
            return file.fileName
    return ""

def indexFiles():
    files=[]
    for i in range(0,774):
        name = "TRIPS_parses/train-sentences.txt-"+str(i+100)+".xml"
        try:
            _tree = ET.parse(name)
            if (_tree.getroot().tag=='SPRL'):
                for scene in _tree.getroot():
                    for element in scene:
                        if element.tag=='SENTENCE':
                            text = element.find('TEXT').text
                            file = File()
                            file.fileName=name
                            file.text=text
                            files+=[file]
            elif (_tree.getroot().tag=='SENTENCE'):
                text = _tree.getroot().find('TEXT').text
                file = File()
                file.fileName=name
                file.text=text
                files+=[file]
        except (FileNotFoundError,ET.ParseError):
            s="DO NOTHING"
    return files

def _pullElements(root):
    elements=[]
    for scene in root:
        for element in scene:
            if element.tag=='SENTENCE':
                for elem in element:
                    if elem.tag!='TEXT':
                        elements+=[elem]
    return elements
def pullElements(fileName):
    tree=ET.parse(fileName)
    root=tree.getroot()
    if root.tag=='SPRL':
        return _pullElements(root)
    elements=[]
    for elem in root:
        if elem.tag!='TEXT':
            elements+=[elem]
    return elements
        

def main():
    files = indexFiles()
    tree = ET.parse('sprl2017_train.xml')
    log=""
    root = tree.getroot()
    for scene in list(root):
        for element in list(scene):
            if element.tag=='SENTENCE':
                text = element.find('TEXT').text
                match=findMatch(text,files)
                if match=="":
                    log+="No match found for:\n"
                    log+=text+"\n"
                    log+="--------------------------------------\n"
                    root.remove(scene)
                    break
                else:
                    for sub in list(element):
                        if sub.tag!='TEXT':
                            element.remove(sub)
                    for elem in list(pullElements(match)):
                        element.append(elem)
                    #ET.dump(element)
    tree.write("output.xml")
    logFile = open("log.txt",'a')
    logFile.write(log)
    logFile.close()
    return


main()
