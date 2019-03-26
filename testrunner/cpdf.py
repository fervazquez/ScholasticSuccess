import PyPDF2 as pdf2

pageobj=open('02172019.pdf','rb')
reader=pdf2.pdffileReader(pageobj)

for x in range(0,reader.getNumPages()):
    