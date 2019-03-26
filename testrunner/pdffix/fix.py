#import tempfile
from pdf2image import convert_from_path

#with tempfile.TemporaryDirectory() as path:
#    imag = convert_from_path('check.pdf', output_folder=path)
    #imag = convert_from_path('02172019.pdf', output_folder=path)
#imag=convert_from_path('02172019.pdf')
#imag=convert_from_path('check.pdf')
#print(len(imag))

from PyPDF2 import PdfFileWriter, PdfFileReader
"""
inputpdf = PdfFileReader(open("check2.pdf", "rb"))
print(inputpdf.numPages)
for i in range(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)

"""
inputpdf = PdfFileReader(open("check2.pdf", "rb"))
print(inputpdf.numPages)
output = PdfFileWriter()
for i in range(8):
    
    output.addPage(inputpdf.getPage(i))

with open("document-page%s.pdf" % 1, "wb") as outputStream:
        output.write(outputStream)


imag=convert_from_path('document-page{}.pdf'.format(1))
imag[0].save('d-p{}.pdf'.format(1))

#ount+=len(imag)
print(len(imag))



"""
count=0
for x in range(0,101):
    imag=convert_from_path('document-page{}.pdf'.format(x))
    imag[0].save('d-p{}.pdf'.format(x))
    count+=len(imag)
    print(count)
"""