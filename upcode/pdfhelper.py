"""
this needs to account for ACTs and SATS when they are fine. code should take 
20 to 25 minutes to add extra features. also change the repetitive code.
This goes back to refactoring issues to stream line each page and add error
handling. Pages should be processed individually in case an issue arrises with 
edge finder breaking.

Current idea is to black out area outside outer edge and work towards the 
inside. black out should be made after website is up with analytics and 
pdf is made with BP report and I get my statistical data 


*1 is for no changes needed
*2 is for changes need to occur
"""
from PyPDF2 import PdfFileWriter, PdfFileReader

i=0
pdf=PdfFileReader('04192019.pdf','rb')
jk=open('outpdf.pdf','wb')
outp=PdfFileWriter()

textin=open('04192019.txt','r')
helper=[]
for x in textin:
    x=x.strip()
    x=x.split()
    helper.append(x)


print(helper)
print(pdf.getNumPages())
i=0
for x in helper:
    print(i)
    if x[2]=='1':
        outp.addPage(pdf.getPage(i+0))
        outp.addPage(pdf.getPage(i+1))
        outp.addPage(pdf.getPage(i+2))
        outp.addPage(pdf.getPage(i+3))
        outp.addPage(pdf.getPage(i+4))
        outp.addPage(pdf.getPage(i+5))
        i+=6
    else:
        if x[1]=='SAT2':
            outp.addPage(pdf.getPage(i+0))
            outp.addPage(pdf.getPage(i+1))
            outp.addPage(pdf.getPage(i+2))
            #outp.addPage(pdf.getPage(i+3))
            outp.addPage(pdf.getPage(i+4))
            #outp.addPage(pdf.getPage(i+5))
            outp.addPage(pdf.getPage(i+6))
            #outp.addPage(pdf.getPage(i+7))
            outp.addPage(pdf.getPage(i+8))
            #outp.addPage(pdf.getPage(i+9))
            outp.addPage(pdf.getPage(i+10))
            outp.addPage(pdf.getPage(i+11))
            i+=12
        else:
            outp.addPage(pdf.getPage(i+0))
            outp.addPage(pdf.getPage(i+1))
            outp.addPage(pdf.getPage(i+2))
            #outp.addPage(pdf.getPage(i+3))
            outp.addPage(pdf.getPage(i+4))
            #outp.addPage(pdf.getPage(i+5))
            outp.addPage(pdf.getPage(i+6))
            #outp.addPage(pdf.getPage(i+7))
            outp.addPage(pdf.getPage(i+8))
            #outp.addPage(pdf.getPage(i+9))
            
            i+=10
outp.write(jk)



"""
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

"""