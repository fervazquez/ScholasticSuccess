from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os




pdflist= convert_from_path(sys.argv[1])
print(pdflist)


"""
inputpdf=PdfFileReader(open("{}.pdf".format(sys.argv[1]), "rb"))
print(inputpdf.numPages)
for i in range(inputpdf.numPages):
    output=PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("{}.pdf".format(i),"wb") as outstream:
        output.write(outstream)
"""