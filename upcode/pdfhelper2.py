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
# inputpdf=PdfFileReader(open("{}.pdf".format("07-16-2019"), "rb"))
inputpdf=PdfFileReader(open("{}.pdf".format("07-27-2019"), "rb"))
print(inputpdf.numPages)
output=PdfFileWriter()

output.addPage(inputpdf.getPage(4))
output.addPage(inputpdf.getPage(5))
output.addPage(inputpdf.getPage(6))
output.addPage(inputpdf.getPage(7))
output.addPage(inputpdf.getPage(0))
output.addPage(inputpdf.getPage(1))
output.addPage(inputpdf.getPage(2))
output.addPage(inputpdf.getPage(3))


# output.addPage(inputpdf.getPage(9))
# output.addPage(inputpdf.getPage(10))
# output.addPage(inputpdf.getPage(11))
# output.addPage(inputpdf.getPage(12))
# output.addPage(inputpdf.getPage(5))
# output.addPage(inputpdf.getPage(6))
# output.addPage(inputpdf.getPage(7))
# output.addPage(inputpdf.getPage(8))
# output.addPage(inputpdf.getPage(18))
# output.addPage(inputpdf.getPage(19))
# output.addPage(inputpdf.getPage(20))
# output.addPage(inputpdf.getPage(12))
# output.addPage(inputpdf.getPage(13))
# output.addPage(inputpdf.getPage(14))
# output.addPage(inputpdf.getPage(15))
# output.addPage(inputpdf.getPage(16))
# output.addPage(inputpdf.getPage(17))


# for i in range(0,2):
    
#     x=i*8
#     """
#     if i==1:    #this part was added bcz of a SAT missing the last blank page of the surveys        
#         output.addPage(inputpdf.getPage(x+5))
#         output.addPage(inputpdf.getPage(x+6))
#         output.addPage(inputpdf.getPage(x+7))
#         output.addPage(inputpdf.getPage(x-1))
#         output.addPage(inputpdf.getPage(x+0))
#         output.addPage(inputpdf.getPage(x+1))
#         output.addPage(inputpdf.getPage(x+2))
#         output.addPage(inputpdf.getPage(x+3))
#         output.addPage(inputpdf.getPage(x+4))
#         output.addPage(inputpdf.getPage(x-1))
#     else:    
#     """ 
#     output.addPage(inputpdf.getPage(x+4))
#     output.addPage(inputpdf.getPage(x+5))
#     output.addPage(inputpdf.getPage(x+6))
#     output.addPage(inputpdf.getPage(x+7))
#     output.addPage(inputpdf.getPage(x+0))
#     output.addPage(inputpdf.getPage(x+1))
#     output.addPage(inputpdf.getPage(x+2))
#     output.addPage(inputpdf.getPage(x+3))
# """
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
        

with open("./hold/07272019.pdf","wb") as outstream:
    output.write(outstream)
    #i=i+7
    #print(i)
    