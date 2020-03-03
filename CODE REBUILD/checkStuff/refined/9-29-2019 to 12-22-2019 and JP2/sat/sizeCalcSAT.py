from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os, re
from matplotlib import pyplot as plt
import time

tpath="./tempDir/"
def readDep():
    depList=os.listdir("./dep_folder/")
    count=0
    tcount=0
    xList=[[]]
    for x in depList:
        if count==10:
            count=0
            tcount+=1
            xList.append([])
        xList[tcount].append("./dep_folder/"+x)
        count+=1
        
    pdfList=parseinput("sat_cr.pdf")
    #print(pdfList)
    print(len(pdfList))

    outList=[]

    sizeDict={}
    sizeDict[0]=[]

    sizeDict[1]=[]

    sizeDict[2]=[]
    sizeDict[3]=[]

    sizeDict[4]=[]

    sizeDict[5]=[]
    sizeDict[6]=[]

    sizeDict[7]=[]
    sizeDict[8]=[]
    sizeDict[9]=[]

    for x in xList:
        #print(x[0])
        regFind=re.findall("[0-9]+\_",x[0])
        regFind=regFind[0][:-1]

        #print(int(regFind))
        flist=pdfList[int(regFind)]

        x=[
        [cv2.imread(x[0],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[0],cv2.IMREAD_GRAYSCALE)],
        [cv2.imread(x[1],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[1],cv2.IMREAD_GRAYSCALE)],
        [cv2.imread(x[2],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[2],cv2.IMREAD_GRAYSCALE)],
        [cv2.imread(x[3],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[2],cv2.IMREAD_GRAYSCALE)],
        [cv2.imread(x[4],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[3],cv2.IMREAD_GRAYSCALE)],
        [cv2.imread(x[5],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[4],cv2.IMREAD_GRAYSCALE)],
        [cv2.imread(x[6],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[4],cv2.IMREAD_GRAYSCALE)],
        [cv2.imread(x[7],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[5],cv2.IMREAD_GRAYSCALE)],
        [cv2.imread(x[8],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[6],cv2.IMREAD_GRAYSCALE)],
        [cv2.imread(x[9],cv2.IMREAD_GRAYSCALE),cv2.imread(flist[7],cv2.IMREAD_GRAYSCALE)]
        ]

        
        
        #(h,w)=warped.shape[:2]
        countDict=0
        for y in x:
            
            (hRef,wRef)=y[0].shape[:2]
            (hOrg,wOrg)=y[1].shape[:2]
            areaRef=hRef*wRef
            areaOrg=hOrg*wOrg
            sizePercentage=areaRef/areaOrg
            y[0]=(hRef,wRef,areaRef)
            y[1]=(hOrg,wOrg,areaOrg)
            y.append(sizePercentage)

            sizeDict[countDict].append(sizePercentage)
            countDict+=1
            if countDict==10:
                countDict=0

        # print("**********************")
        # print(x)
        # print(len(x))
        # print(len(x[0]))
        # print(len(x[1]))
        # print("**********************")
        outList.append(x)

    # print(xList)
    print(len(xList))
    print("**********************")
    print(outList)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    outDict={}
    outDict[0]=[min(sizeDict[0]),max(sizeDict[0])]
    outDict[1]=[min(sizeDict[1]),max(sizeDict[1])]
    outDict[2]=[min(sizeDict[2]),max(sizeDict[2])]
    outDict[3]=[min(sizeDict[3]),max(sizeDict[3])]
    outDict[4]=[min(sizeDict[4]),max(sizeDict[4])]
    outDict[5]=[min(sizeDict[5]),max(sizeDict[5])]
    outDict[6]=[min(sizeDict[6]),max(sizeDict[6])]
    outDict[7]=[min(sizeDict[7]),max(sizeDict[7])]
    outDict[8]=[min(sizeDict[8]),max(sizeDict[8])]
    outDict[9]=[min(sizeDict[9]),max(sizeDict[9])]
    print("##############################")
    print(outDict)
    print("(((((((((((((())))))))))))))")


def parseinput(nameIn):
    inputpdf=PdfFileReader(open("{}".format(nameIn), "rb"))
    print(inputpdf.numPages)
    pglist=[]
    for i in range(inputpdf.numPages):
        pglist.append("./tempDir/{}.jpg".format(i))
    count=0
    Tcount=0
    tlist=[[]]
    for x in pglist:
        if count==8:
            count=0
            Tcount+=1
            tlist.append([])
        tlist[Tcount].append(x)
        count+=1

    pglist=tlist
    return pglist

readDep()
            