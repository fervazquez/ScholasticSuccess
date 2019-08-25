from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os


#inputpdf=PdfFileReader(open("{}.pdf".format("06-16-2019"), "rb"))
#inputpdf=PdfFileReader(open("{}.pdf".format("06-18-2019"), "rb"))
#inputpdf=PdfFileReader(open("{}.pdf".format("06-25-2019"), "rb"))
#inputpdf2=PdfFileReader(open("{}.pdf".format("06-26-2019"), "rb"))
# inputpdf=PdfFileReader(open("{}.pdf".format("07-01-2019"), "rb"))
# inputpdf=PdfFileReader(open("{}.pdf".format("07-08-2019"), "rb"))
inputpdf=PdfFileReader(open("{}.pdf".format("07-16-2019"), "rb"))
# inputpdf=PdfFileReader(open("{}.pdf".format("07-27-2019"), "rb"))
print(inputpdf.numPages)
output=PdfFileWriter()



for i in range(0,21):
    
    
    if i>4:
        output.addPage(inputpdf.getPage(i))
    if i==20:    #this part was added bcz of a SAT missing the last blank page of the surveys        
        output.addPage(inputpdf.getPage(4))
       
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
        

with open("Done07162019.pdf","wb") as outstream:
    output.write(outstream)
    #i=i+7
    #print(i)
    