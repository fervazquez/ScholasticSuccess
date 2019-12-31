from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os



# inputpdf=PdfFileReader(open("{}.pdf".format("07-08-2019"), "rb"))
#inputpdf=PdfFileReader(open("{}.pdf".format("07-16-2019"), "rb"))
# inputpdf=PdfFileReader(open("{}.pdf".format("07-27-2019"), "rb"))

def getPg(output,indoc,start,amt):
    
    for x in range(amt):
        output.addPage(indoc.getPage(x+start))

    return output

# x616=PdfFileReader(open("06162019.pdf","rb"))
# x618=PdfFileReader(open("06182019.pdf","rb"))
# x625=PdfFileReader(open("06252019.pdf","rb"))
# x626=PdfFileReader(open("06262019.pdf","rb"))
# x701=PdfFileReader(open("07012019.pdf","rb"))
# x708=PdfFileReader(open("07082019.pdf","rb"))
# x716=PdfFileReader(open("07162019.pdf","rb"))
# x727=PdfFileReader(open("07272019.pdf","rb"))
# x826=PdfFileReader(open("08262019.pdf","rb"))
# x827=PdfFileReader(open("08272019.pdf","rb"))
# x902=PdfFileReader(open("09022019.pdf","rb"))

# x907=PdfFileReader(open("09072019.pdf","rb"))
# jpout4=PdfFileWriter()
# isee=PdfFileWriter()
# psat=PdfFileWriter()
# sat=PdfFileWriter()
# act=PdfFileWriter()


#act=PdfFileWriter()
psat=PdfFileWriter()

sat=PdfFileWriter()
isee=PdfFileWriter()
# x1=PdfFileReader(open("9-29-2019.pdf","rb"))
x1=PdfFileReader(open("10-7-2019.pdf","rb"))
#x2=PdfFileReader(open("2.pdf","rb"))
#x3=PdfFileReader(open("3.pdf","rb"))
#x4=PdfFileReader(open("4.pdf","rb"))



# act=getPg(act,x1,0,14)
psat=getPg(psat,x1,16,16)
sat=getPg(sat,x1,8,8)
isee=getPg(isee,x1,0,8)

#act=getPg(act,x4,0,21)

#sat=getPg(sat,x1,0,8)
#psat=getPg(psat,x1,8,7)
#psat=getPg(psat,x3,0,7)


# for i in range(0,21):
    
    
#     if i>4:
#         output.addPage(inputpdf.getPage(i))
#     if i==20:    #this part was added bcz of a SAT missing the last blank page of the surveys        
#         output.addPage(inputpdf.getPage(4))
# jpout4=getPg(jpout4,x907,0,7)
# jpout4=getPg(jpout4,x907,7,7)
# jpout4=getPg(jpout4,x907,14,7)
# jpout4=getPg(jpout4,x907,21,7)

# with open("jpSmall4.pdf","wb") as outstream:
#     jpout4.write(outstream)

# isee=getPg(isee,x616,0,8)
# isee=getPg(isee,x616,8,8)
# isee=getPg(isee,x616,16,8)
# psat=getPg(psat,x616,24,8)
# psat=getPg(psat,x616,32,8)
# psat=getPg(psat,x616,40,8)

# act=getPg(act,x618,0,8)
# sat=getPg(sat,x618,8,9)
# act=getPg(act,x618,17,8)
# act=getPg(act,x618,25,8)
# act=getPg(act,x618,33,8)
# act=getPg(act,x618,41,8)
# isee=getPg(isee,x618,49,8)

# act=getPg(act,x625,0,8)
# psat=getPg(psat,x625,8,8)
# psat=getPg(psat,x625,16,8)
# psat=getPg(psat,x625,24,8)
# psat=getPg(psat,x625,32,8)

# act=getPg(act,x626,0,8)
# act=getPg(act,x626,8,8)

# act=getPg(act,x701,0,8)
# act=getPg(act,x701,8,8)

# psat=getPg(psat,x708,0,8)
# psat=getPg(psat,x708,8,8)

# act=getPg(act,x716,0,8)
# sat=getPg(sat,x716,8,9)

# psat=getPg(psat,x727,0,8)

# isee=getPg(isee,x827,0,8)
# sat=getPg(sat,x827,8,8)

# act=getPg(act,x826,0,8)
# act=getPg(act,x826,8,8)
# act=getPg(act,x826,16,8)
# act=getPg(act,x826,24,8)
# act=getPg(act,x826,32,8)
# act=getPg(act,x826,40,8)
# act=getPg(act,x826,48,8)

# act=getPg(act,x902,0,8)

#"""
# for i in range(0,2):
    
#     x=i*8
#     output.addPage(inputpdf2.getPage(x+4))
#     output.addPage(inputpdf2.getPage(x+5))
#     output.addPage(inputpdf2.getPage(x+6))
#     output.addPage(inputpdf2.getPage(x+7))
#     output.addPage(inputpdf2.getPage(x+0))
#     output.addPage(inputpdf2.getPage(x+1))
#     output.addPage(inputpdf2.getPage(x+2))
#     output.addPage(inputpdf2.getPage(x+3))
# """
        
with open("10-7-2019_isee.pdf","wb") as outstream:
    isee.write(outstream)

with open("10-7-2019_psat.pdf","wb") as outstream:
    psat.write(outstream)

with open("10-7-2019_sat.pdf","wb") as outstream:
    sat.write(outstream)

# with open("act.pdf","wb") as outstream:
#     act.write(outstream)