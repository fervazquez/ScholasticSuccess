from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os
def getPg(output,indoc,start,amt):
    
    for x in range(amt):
        output.addPage(indoc.getPage(x+start))

    return output


x1=PdfFileReader(open("SPAlexandra.pdf","rb"))
x2=PdfFileReader(open("SPCaitlyn.pdf","rb"))
x3=PdfFileReader(open("SPIsabella.pdf","rb"))
x4=PdfFileReader(open("SPMarkus.pdf","rb"))


psatMega = PdfFileWriter()

for x in range(x1.numPages):
    psatMega.addPage(x1.getPage(x))

for x in range(x2.numPages):
    psatMega.addPage(x2.getPage(x))

for x in range(x3.numPages):
    psatMega.addPage(x3.getPage(x))

for x in range(x4.numPages):
    psatMega.addPage(x4.getPage(x))

with open("psatTOT.pdf","wb") as outstream:
    psatMega.write(outstream)