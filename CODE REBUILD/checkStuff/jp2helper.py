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


x1=PdfFileReader(open("9-29-2019.pdf","rb"))
x2=PdfFileReader(open("10-7-2019.pdf","rb"))
x3=PdfFileReader(open("10-13-2019.pdf","rb"))
x4=PdfFileReader(open("10-27-2019.pdf","rb"))
x5=PdfFileReader(open("11-12-2019.pdf","rb"))
x6=PdfFileReader(open("11-17-2019.pdf","rb"))
x7=PdfFileReader(open("11-24-2019.pdf","rb"))
x8=PdfFileReader(open("12-2-2019.pdf","rb"))


isee = PdfFileWriter()
sat = PdfFileWriter()
psat = PdfFileWriter()
act = PdfFileWriter()

#x1
act = getPg(act,x1,0,14)
psat = getPg(psat,x1,14,14)

#x2
isee =  getPg(isee,x2,0,7)
sat = getPg(sat,x2,8,8)
psat = getPg(psat,x2,16,7)
psat = getPg(psat,x2,24,7)

#x3
sat = getPg(sat,x3,0,8)
isee =  getPg(isee,x3,8,7)

#x4
isee =  getPg(isee,x4,0,7)
act = getPg(act,x4,8,7)
act.addPage(x4.getPage(16))
act.addPage(x4.getPage(18))
act.addPage(x4.getPage(20))
act.addPage(x4.getPage(22))
act.addPage(x4.getPage(24))
act.addPage(x4.getPage(26))
act.addPage(x4.getPage(28))

#x5
sat = getPg(sat,x5,0,24)

#x6
sat = getPg(sat,x6,0,8)
act = getPg(act,x6,8,7)

#x7
sat = getPg(sat,x7,0,8)

#x8
act = getPg(act,x8,0,7)
act = getPg(act,x8,8,7)
act = getPg(act,x8,16,7)



with open("isee.pdf","wb") as outstream:
    isee.write(outstream)

with open("sat.pdf","wb") as outstream:
    sat.write(outstream)

with open("psat.pdf","wb") as outstream:
    psat.write(outstream)

with open("act.pdf","wb") as outstream:
    act.write(outstream)