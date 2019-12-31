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


x1=PdfFileReader(open("fixAvery.pdf","rb"))
x2=PdfFileReader(open("fixlauren.pdf","rb"))
x3=PdfFileReader(open("fixmariska.pdf","rb"))
x4=PdfFileReader(open("fixnicholas.pdf","rb"))


actMega = PdfFileWriter()

for x in range(x1.numPages):
    actMega.addPage(x1.getPage(x))

for x in range(x2.numPages):
    actMega.addPage(x2.getPage(x))

for x in range(x3.numPages):
    actMega.addPage(x3.getPage(x))

for x in range(x4.numPages):
    actMega.addPage(x4.getPage(x))

with open("actTOT.pdf","wb") as outstream:
    actMega.write(outstream)