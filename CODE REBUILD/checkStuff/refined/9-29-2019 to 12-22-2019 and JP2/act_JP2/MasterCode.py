from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os
from matplotlib import pyplot as plt
import time

tempDir="./tempDir/"

def tmain():
    

def readTXT(txtFile):
    fileObj = open(txtFile,"r")
    tests=[]
    for line in fileObj:
        line=line.strip()
        line=line.split()
        line[1]=int(line[1])
        tests.append(line)
        print(line)
    return tests

def parsePDF(inPDF):


def parseinput(nameIn):
    inputpdf=PdfFileReader(open("{}".format(nameIn), "rb"))
    print(inputpdf.numPages)
    pglist=[]
    for i in range(inputpdf.numPages):
        output=PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        pglist.append(i)
        with open("./tempDir/{}.pdf".format(i),"wb") as outstream:
            output.write(outstream)
    return pglist


readTXT(sys.argv[1])