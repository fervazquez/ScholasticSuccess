from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os
from matplotlib import pyplot as plt
import time

tpath="./tempDir/"
#needs the full name of input
def tmake():
    print(cv2.__version__)
    docList=parseinput(sys.argv[1])
    y=0
    tcount=0
    testList=[]
    print(len(docList))
    tstop=cv2.imread("ouch.jpg")
    errorList=[]
    pageSizes=[]
    for x in range(0,len(docList)):
        print("right here BITCHES ",x)

        temp=convert_from_path("{}{}.pdf".format(tpath,docList[x]))
        temp[0].save("{}{}.jpg".format(tpath,docList[x]),"JPEG")
        print("{}{}.jpg".format(tpath,docList[x]))
        docList[x]=cv2.imread("{}{}.jpg".format(tpath,docList[x]))
        print("lolol")
        gray = cv2.cvtColor(docList[x], cv2.COLOR_BGR2GRAY)
        try:
            pic=picfixmass(1,gray)
            testList.append(pic)
        except:
            try:
                pic=picfixSmall(1,gray)
                testList.append(pic)
            except:
                testList.append(gray)
            errorList.append((tcount,y,x))
            
        (h,w)=gray.shape[:2]
        pageSizes.append(("Page: {}, Test Count: {}".format(y,tcount),h,w))
        y+=1
        if y==7:
            print("YOYOYOYOYOYYOYOYOOYYOYOYOYOYOYOOYYOYOYOYO")
            for g in range(len(testList)):
                cv2.imwrite("./dep_folder/{}_{}.jpg".format(tcount,g),testList[g])
                # testList[x].save("{}{}_{}.jpg".format(tpath,tcount,testList[g]),"JPEG")
            tcount+=1
            y=0
            testList=[]
    print(pageSizes)
    print("********************")
    print(errorList)
    
def parseinput(nameIn):
    inputpdf=PdfFileReader(open("{}".format(nameIn), "rb"))
    print(inputpdf.numPages)
    pglist=[]
    for i in range(inputpdf.numPages):
        output=PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        pglist.append(i)
        with open("./tempDir/{}.pdf".format(i),"wb") as outstream:
            output.write(outstream)

    return pglist

def picfixmass(num,gray):
    (h,w)=gray.shape[:2]
    print("popop",h,w)
    gray = gray[int(h*0.05):h-int(h*.04),int(w*.045):w-int(w*.05)]
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    cnts = cnts[0]
    docCnt = None
    docstore2=[]
    # ensure that at least one contour was found
    #print("koolololo",len(cnts))
    if len(cnts) > 0:
        # sort the contours according to their size in
        # descending order
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        # loop over the sorted contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points,
            # then we can assume we have found the paper
            if len(approx) == 4:
                docCnt = approx
                # print("LLLLLLLLLL")
                docstore2.append(docCnt)
                #break
    # print(num)
    # for x in range(0,len(docstore2)):
    #     if x ==4:
    #         break
    #     tt=four_point_transform(gray, docstore2[x].reshape(4, 2))
    #     cv2.imshow("check {}, length{}".format(x,len(docstore2)),tt)
    # print("Pick the Best one")
    # cv2.waitKey(0)
    ################################FUN CODE#################################
    # if num==2:

    #     print("FUCK YOU 9")
    #     num2= input("does this need extra processing Yes: 1, No: 2 ")
    #     print(num2) 
    #     num2=int(num2)
    #     num4=0
    #     if num2==2:
    #         retStore=[]
    #         retStore.append(four_point_transform(gray, docstore2[1].reshape(4, 2)))
    #         retStore.append(four_point_transform(gray, docstore2[0].reshape(4, 2)))
    #         return retStore
    # else:
    #     print("FUCK YOU 8")
    #     num4 = input("Enter number starting at ZERO or 3 to skip: ") 
    #     print(num4) 
    #     num4=int(num4)
    #     if num4==3:
    #         return four_point_transform(gray, docstore2[0].reshape(4, 2))
        

    #     num2= input("does this need extra processing Yes: 1, No: 2 ")
    #     print(num2) 
    #     num2=int(num2)
        
    #     if num2==2:
    #         return four_point_transform(gray, docstore2[num4].reshape(4, 2))
    warped = four_point_transform(gray, docstore2[0].reshape(4, 2))
    ##############################FUN CODE###################################
    return picfixSmall(num,warped)

def picfixSmall(num,warped):
    (h,w)=warped.shape[:2]
    gray2 = warped[int(h*0.01):h-int(h*.01),int(w*.01):w-int(w*.01)]

    blurred = cv2.GaussianBlur(gray2, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    # find contours in the edge map, then initialize
    # the contour that corresponds to the document
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] #if imutils.is_cv2() else cnts[1]
    docCnt = None
    docstore=[]
    # ensure that at least one contour was found
    if len(cnts) > 0:
        # sort the contours according to their size in
        # descending order
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        # loop over the sorted contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points,
            # then we can assume we have found the paper
            if len(approx) == 4 and num==1:
                docCnt = approx
                # print("LLLLLLLLLL")
                break
            if len(approx) == 4 and num ==2:
                docCnt = approx
                docstore.append(docCnt)
    areaStore=[]
    if num == 1:
        paper = four_point_transform(gray2, docCnt.reshape(4, 2))
        return paper
    if num == 2:
        areaStore.append(four_point_transform(gray2, docstore[1].reshape(4, 2)))
        areaStore.append(four_point_transform(gray2, docstore[0].reshape(4, 2)))
        return areaStore



start_time = time.time()
tmake()
end_time= time.time()