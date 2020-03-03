from PyPDF2 import PdfFileWriter, PdfFileReader


i=0
pdf=PdfFileReader('doc2.pdf','rb')
outp=PdfFileWriter()

while i<pdf.getNumPges():


    if type =="ACT" or "PDF":
        outp.addPage(pdf.getPages(i+0))
        outp.addPage(pdf.getPages(i+1))
        outp.addPage(pdf.getPages(i+2))
        outp.addPage(pdf.getPages(i+4))
        outp.addPage(pdf.getPages(i+6))
        outp.addPage(pdf.getPages(i+8))
    else:
        outp.addPage(pdf.getPages(i+0))
        outp.addPage(pdf.getPages(i+1))
        outp.addPage(pdf.getPages(i+2))
        outp.addPage(pdf.getPages(i+4))
        outp.addPage(pdf.getPages(i+6))
        outp.addPage(pdf.getPages(i+8))
        outp.addPage(pdf.getPages(i+10))
        outp.addPage(pdf.getPages(i+11))
        p=pdf.getPages()