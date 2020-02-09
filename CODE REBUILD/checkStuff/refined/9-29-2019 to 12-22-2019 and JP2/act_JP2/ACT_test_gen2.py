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
# Original Data
# {0: [0.5335427807486631, 0.5391617647058824],
# 1: [0.5331401069518716, 0.5389026737967915],
# 2: [0.5327374331550803, 0.5416395721925134],
# 3: [0.5338970588235294, 0.5399229946524065],
# 4: [0.6373689839572193, 0.6400010695187166],
# 5: [0.6390401069518716, 0.6417994652406417],
# 6: [0.6385596256684491, 0.6410695187165776]}

calcSIZEZ={0: [0.52, 0.56],
 1: [0.52, 0.56],
 2: [0.52, 0.56],
 3: [0.52, 0.56],
 4: [0.62, 0.67],
 5: [0.62, 0.67],
 6: [0.62, 0.67]}

def tmake():
    print(cv2.__version__)
    docList=parseinput(sys.argv[1])
    y=0
    tcount=0
    testList=[]
    print(len(docList))
    # tstop=cv2.imread("ouch.jpg")
    errorList=[]
    pageSizes=[]
    topError=0
    transferList=[]
    pixelCount=[]
    docList2=[]

    for x in range(0,len(docList)):
        print("right here BITCHES ",x)

        temp=convert_from_path("{}{}.pdf".format(tpath,docList[x]))
        temp[0].save("{}{}.jpg".format(tpath,docList[x]),"JPEG")
        print("{}{}.jpg".format(tpath,docList[x]))
        docList[x]=cv2.imread("{}{}.jpg".format(tpath,docList[x]))
        # print("lolol")
        gray = cv2.cvtColor(docList[x], cv2.COLOR_BGR2GRAY)
        # This will count white pixels. Over 3.2 Million, means blank page
        tcountPix=np.sum(gray == 255)
        pixelCount.append(tcountPix)
        print("page pixel count",tcountPix)
        # docList[x]=gray
        if tcountPix < 3200000:
            docList2.append(gray)

    averagesFound=[]
    for x in range(0,len(docList2)):
        
        gray=docList2[x]
        try:
            pic=picfixmass(1,gray,y)
            testList.append([pic[0],gray,(tcount,y,x)])
            averagesFound.append((tcount,y,x,pic[1]))
        except:
            topError+=1
            try:
                pic=picfixSmall(1,gray,y)
                testList.append([pic[0],gray,(tcount,y,x)])
                averagesFound.append((tcount,y,x,pic[1]))
            except:
                testList.append([gray,gray,(tcount,y,x)])
            errorList.append((tcount,y,x))
            

        # (h,w)=gray.shape[:2]
        # pageSizes.append(("Page: {}, Test Count: {}".format(y,tcount),h,w))
        y+=1
        if y==7:
            print("YOYOYOYOYOYYOYOYOOYYOYOYOYOYOYOOYYOYOYOYO")
            for g in range(len(testList)):
                cv2.imwrite("./dep_folder/{}_{}.jpg".format(tcount,g),testList[g][0])
                # testList[x].save("{}{}_{}.jpg".format(tpath,tcount,testList[g]),"JPEG")
            transferList.append(testList)
            tcount+=1
            y=0
            testList=[]

    # print(pageSizes)
    print("********************")
    # print(errorList)
    print("topError",topError)
    # print(len(transferList))
    print("LLLLLLLLLLLLLLLLLLLLL")
    results= addData(transferList)
    print("PPPPPPPPPPPPPPPPPPPPPPPPPP")
    print(results[0][0][2])
    print("results len",len(results))
    print("len of results[1]",len(results[1]))
    for g in range(len(results[1])):
        print(results[1][g][1])
        cv2.imwrite("./errorList/{}_{}_{}.jpg".format(results[1][g][1][0],results[1][g][1][1],results[1][g][1][2]),results[1][g][0])
    print("PIXEL COUNT*********************")
    print(pixelCount)
    print("******** min count ", min(pixelCount))
    print("docList",len(docList))
    print("docList2",len(docList2))
    print("*******************Averages Found**********************")
    print(averagesFound)

def addData(tList):
    EList=[]
    for test in tList:
        countx=0
        for testpg in test:
            # print(len(testpg))
            (h1,w1)=testpg[0].shape[:2]
            (h2,w2)=testpg[1].shape[:2]
            (testCount,testPage,PDFPage)=testpg[2]
            avgfound = (h1*w1)/(h2*w2)
            tval=True
            if calcSIZEZ[countx][0] <= avgfound <= calcSIZEZ[countx][1]:
                tval=True
            else:
                tval=False
                EList.append([testpg[1], [testCount,testPage,countx,PDFPage,avgfound,tval]])
            
            testpg[2]=[testCount,testPage,countx,PDFPage,avgfound,tval]
            countx+=1
    return [tList,EList]
            
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

def picfixmass(num,gray,pos):
    (h,w)=gray.shape[:2]
    aORG = h*w

    gray = gray[int(h*0.05):h-int(h*.04),int(w*.045):w-int(w*.05)]
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
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
                docstore2.append(docCnt)
                #break
    print(num)
    avg=[]
    for x in range(0,len(docstore2)):
        if x ==2:
            break
        tt=four_point_transform(gray, docstore2[x].reshape(4, 2))
        (hNew,wNew)=tt.shape[:2]
        avg.append((hNew*wNew)/aORG)

        # cv2.imshow("check {}, length{}".format(x,len(docstore2)),tt)
    print("Pick the Best one")
    # cv2.waitKey(0)


    if calcSIZEZ[pos][0]<= avg[0] <= calcSIZEZ[pos][1]:
        print("1 HIT 1")
        return [four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]]
    else:
        print("2 HIT 2")
        warped = four_point_transform(gray, docstore2[0].reshape(4, 2))
        return picfixSmall(num,warped,pos,aORG,gray)

def picfixSmall(num,warped,pos,aORG,grayORG):
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
    areaStore=[]
    if num == 1:
        print("pos right herer",pos)
        paper= four_point_transform(gray2, docCnt.reshape(4, 2))
        # cv2.imshow("checklength",paper)
        # cv2.waitKey(0)
        (h4,w4)=paper.shape[:2]
        avg=((h4*w4)/aORG)
        print(avg)
        if calcSIZEZ[pos][0]<= avg <= calcSIZEZ[pos][1]:
            return [paper,avg]
        else:
            return [grayORG,avg]

start_time = time.time()
tmake()
end_time= time.time()
print(end_time-start_time)