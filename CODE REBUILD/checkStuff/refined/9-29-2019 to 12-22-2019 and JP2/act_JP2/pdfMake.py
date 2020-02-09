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


x1=PdfFileReader(open("1-20-2019.pdf","rb"))


actMega = PdfFileWriter()
actMega2 = PdfFileWriter()

for x in range(0,8):
    actMega.addPage(x1.getPage(x))

for x in range(8,32):
    actMega2.addPage(x1.getPage(x))

with open("1-20-2020SAT.pdf","wb") as outstream:
    actMega.write(outstream)

with open("1-20-2020ACT.pdf","wb") as outstream:
    actMega2.write(outstream)