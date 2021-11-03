import spacy
from spacy.lang.de.examples import sentences
import os
import matplotlib.pyplot as plt
import collections
import xml.etree.ElementTree as ET
import graphviz

#Aufgabe 2.3 Auswertung

def DateiAuslesen(filename):
    datei = open(filename, encoding = "utf-8").read() #Inhalt der Datei wird geöffnet und in datei reingepackt
    
    nlp = spacy.load('de_core_news_sm')
    doc = nlp(datei)
    for token in doc:
        print(token.text)

def DateiTaggen(filename):
    datei = open(filename, encoding = "utf-8").read() #Inhalt der Datei wird geöffnet und in datei reingepackt
    nlp = spacy.load('de_core_news_sm')
    doc = nlp(datei)
    
    POS_counts = doc.count_by(spacy.attrs.POS)
    #print(POS_counts)

    for k,v in sorted(POS_counts.items()):
        print(f'{k:{4}}. {doc.vocab[k].text:{5}}: {v}')

def SpatialEntities(filename):
    datei = open(filename, encoding = "utf-8").readlines()
    counterSPATIAL_ENTITY = 0
    counterPLACE     = 0
    counterMOTION    = 0
    counterLOCATION  = 0
    counterSIGNAL    = 0
    counterQSLINK    = 0
    counterOLINK     = 0
    
    for i in datei:
        erstesWort = i.split(' ', 1)[0]
        #print(erstesWort)
        
        if "<SPATIAL_ENTITY" == erstesWort:
            counterSPATIAL_ENTITY += 1
        if "<PLACE" == erstesWort:
            counterPLACE += 1
        if "<MOTION" == erstesWort:
            counterMOTION += 1
        if "<LOCATION" == erstesWort:
            counterLOCATION += 1
        if "<SIGNAL" == erstesWort:
            counterSIGNAL += 1
        if "<QSLINK" == erstesWort:
            counterQSLINK += 1
        if "<OLINK" == erstesWort:
            counterOLINK += 1

        
    print(counterSPATIAL_ENTITY)
    print(counterPLACE)
    print(counterMOTION)
    print(counterLOCATION)
    print(counterSIGNAL)
    print(counterQSLINK)
    print(counterOLINK)
    

def QSLinks(filename):
    datei = open(filename, encoding = "utf-8").readlines()

    global counterIN
    global counterOut  
    global counterDC   
    global counterEC   
    global counterPO   
    global counterTPP  
    global counterITPP
    global counterNTPP
    global counterEQ

    for zeile in datei:
        if "IN" in zeile:
            counterIN += 1
        if "Out" in zeile:
            counterOut += 1
        if "DC" in zeile:
            counterDC += 1
        if "EC" in zeile:
            counterEC += 1
        if "PO" in zeile:
            counterPO += 1
        if "TPP" in zeile:
            counterTPP += 1
        if "ITPP" in zeile:
            counterITPP += 1
        if "NTPP" in zeile:
            counterNTPP += 1
        if "EQ" in zeile:
            counterEQ += 1

counterIN   = 0
counterOut  = 0
counterDC   = 0
counterEC   = 0
counterPO   = 0
counterTPP  = 0
counterITPP = 0
counterNTPP = 0
counterEQ   = 0

def Satzlänge(filename):
    datei = open(filename, encoding = "utf-8").read()
    Satzlängen = []
    Häufigkeiten = []
    
    nlp = spacy.load('de_core_news_sm')
    doc = nlp(datei)
    for satz in doc.sents:
        #print(satz.text)
        Satzlängen.append(len(satz.text))

    for element in Satzlängen:
        Häufigkeit = Satzlängen.count(element)
        Häufigkeiten.append([element, Häufigkeit])

    #print(Häufigkeiten)
       
    x, y = zip(*Häufigkeiten)
    plt.bar(x, y)
    plt.xlabel("Satzlänge")
    plt.ylabel("Häufigkeit")
    plt.show()

def Präpositionen(filename):
    datei = open(filename, encoding = "utf-8").readlines() #für zeile
    datei_worte = open(filename, encoding = "utf-8").read() #für einzelne wörter
    
    QSLinks = []
    OLinks  = []
    QSIDs = []
    OIDs = []
    QSPräposition = []
    OPräposition  = [] 
    
    
    nlp = spacy.load('de_core_news_sm')
    doc = nlp(datei_worte)
    
    for i in datei:
        erstesWort = i.split(' ', 1)[0]
        if "<QSLINK" == erstesWort:
                    QSLinks.append(i)
        if "<OLINK" == erstesWort:
                    OLinks.append(i)

    for zeile in QSLinks:
        start = zeile.find('trigger="') + len('trigger="')
        ende  = zeile.find('" comment')
        ID = zeile[start:ende]
        QSIDs.append(ID)

    for zeile in OLinks:
        start = zeile.find('trigger="') + len('trigger="')
        ende  = zeile.find('" frame_type')
        ID = zeile[start:ende]
        OIDs.append(ID)
        
    #print(QSIDs)
    #print(OIDs)
    counter=0
    QSIDs[:] = (value for value in QSIDs if value != "")
    OIDs[:] = (value for value in OIDs if value != "")
    #print(QSIDs)
    
    #print(OIDs)
    for ID in QSIDs:
        counter+=1
        for zeile in datei:
            erstesWort = zeile.split(' ', 1)[0]
            
        #print(erstesWort)
            if "<SPATIAL_SIGNAL" == erstesWort:
                
                if ID in zeile:
                    start = zeile.find('text="') + len('text="')
                    ende  = zeile.find('" cluster')
                    Präposition = zeile[start:ende]
                    QSPräposition.append(Präposition)

    for ID in OIDs:
        for zeile in datei:
            erstesWort = zeile.split(' ', 1)[0]
        #print(erstesWort)
            if "<SPATIAL_SIGNAL" == erstesWort:
                if ID in zeile:
                    start = zeile.find('text="') + len('text="')
                    ende  = zeile.find('" cluster')
                    Präposition = zeile[start:ende]
                    OPräposition.append(Präposition)

    QScounter = collections.Counter(QSPräposition)
    Ocounter = collections.Counter(OPräposition)
    #print(QSPräposition)
    #print(OPräposition)
    print("QScounter", QScounter)
    print("Ocounter", Ocounter)


def MOTION(filename):
    datei = open(filename, encoding = "utf-8").readlines() #für zeile
    motion = []
    
    for zeile in datei:
        erstesWort = zeile.split(' ', 1)[0]
        if "<MOTION" == erstesWort:
            start = zeile.find('text="') + len('text="')
            ende  = zeile.find('" domain')
            ID = zeile[start:ende]
            motion.append(ID)

    motion_counter = collections.Counter(motion)
    print(motion_counter)
                                        

#Aufgabe 2.4 Visualisierung

def Visualisierung():
    Aufgabe4 = ET.parse("C:/Users/berna/Desktop/Uni/Master Informtik/1. Semester/Text2Scene/Fingerübung/Traning/Aufgabe_2.4/Bicycles.xml")
    root = Aufgabe4.getroot()
    #datei = open(filename, encoding = "utf-8").readlines()
    entities   = ["PLACE", "LOCATION", "SPATIAL_ENTITY", "NONMOTIONEVENT", "PATH"]
    colors     = ["chartreuse", "deepskyblue", "deeppink", "darkorange1", "yellow"]
    links      = ["QSLINK", "OLINK"]
    linkcolors = ["plum", "powderblue"]
    knoten     = []
    metalinks  = []
    kanten     = []
    
    

    for i in range(len(list(root[1]))):
        tag = root[1][i].tag
        if tag == "METALINK":
            entfromID = root[1][i].attrib['fromID']
            enttoID = root[1][i].attrib['toID']
            if not(entfromID in metalinks):
                metalinks.append(entfromID)
            if not(enttoID in metalinks):
                metalinks.append(enttoID)
                
                
    for i in range(len(list(root[1]))):
        tag = root[1][i].tag
        if tag in entities:
            entId   = root[1][i].attrib['id']
            entText = root[1][i].attrib['text']
            #if entId in metalinks: 
            knoten.append((tag, entId, entText))


    for i in range(len(list(root[1]))):
        tag = root[1][i].tag
        if tag in links:
            entfromID = root[1][i].attrib['fromID']
            enttoID = root[1][i].attrib['toID']
            entrelType = root[1][i].attrib['relType']
            kanten.append((entfromID, enttoID, entrelType, tag))



    graph = graphviz.Digraph()
    for k in knoten:
        graph.node(k[1], label = k[2], color = colors[entities.index(k[0])]) #wir weisen die Farbe zu, die den gleichen Index wie der Tag hat
        #print(k[1])
    for k in kanten:
        graph.edge(k[0], k[1], label = k[2], color = linkcolors[links.index(k[3])])

    #graph.render()
           
    
rootdir = "C:\\Users\\berna\\Desktop\\Uni\\Master Informtik\\1. Semester\\Text2Scene\\Fingerübung\\Traning"
Visualisierung()
for subdir, dirs, files in os.walk(rootdir):
    for file in files:                                      #Die for-Schleife geht durch alle Ordner 
        DateiAuslesen(os.path.join(subdir,file))
        DateiTaggen(os.path.join(subdir,file))
        SpatialEntities(os.path.join(subdir,file))
        QSLinks(os.path.join(subdir,file))
        Satzlänge(os.path.join(subdir,file))
        Präpositionen(os.path.join(subdir,file))
        MOTION(os.path.join(subdir,file))
        pass

#print(counterIN,"IN")
#print(counterOut,"Out")
#print(counterDC,"DC")
#print(counterEC,"EC")  
#print(counterPO,"PO")  
#print(counterTPP,"TPP")
#print(counterITPP,"ITPP") 
#print(counterNTPP,"NTPP")
#print(counterEQ,"EQ")


        



