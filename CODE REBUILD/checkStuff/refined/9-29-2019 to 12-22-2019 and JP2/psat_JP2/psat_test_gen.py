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
# 0: [0.36521764705882354, 0.37110802139037435]
# 1: [0.3690053475935829, 0.3708294117647059]
# 2: [0.12588770053475937, 0.12705]
# 3: [0.27394385026737966, 0.27844652406417114]
# 4: [0.2000673796791444, 0.2041229946524064]
# 5: [0.2762524064171123, 0.2780909090909091]
# 6: [0.6370139037433155, 0.6396449197860963]
# 7: [0.6374935828877005, 0.6402323529411764]
# 8: [0.6361794117647059, 0.6398764705882353]

calcSIZEZ={0: [0.355, 0.375],
1: [0.36, 0.375],
#####################
2: [0.12, 0.13],
3: [0.27, 0.28],
4: [0.198, 0.23],
5: [0.27, 0.28],
#####################
6: [0.63, 0.641],
7: [0.63, 0.641],
8: [0.63, 0.641]}

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
        if y==2 or y==3:
            try:
                pic=picfixmass(2,gray,y)
                testList.append([pic[0][0],gray,(tcount,y,x)])
                testList.append([pic[1][0],gray,(tcount,y,x)])
            except:
                topError+=1
                try:
                    pic=picfixSmall(2,gray,y)
                    testList.append([pic[0][0],gray,(tcount,y,x)])
                    testList.append([pic[1][0],gray,(tcount,y,x)])
                except:
                    testList.append([gray,gray,(tcount,y,x)])
                    testList.append([gray,gray,(tcount,y,x)])
                errorList.append((tcount,y,x))
                errorList.append((tcount,y,x))
        else:
            try:
                pic=picfixmass(1,gray,y)
                testList.append([pic[0],gray,(tcount,y,x)])
            except:
                topError+=1
                try:
                    pic=picfixSmall(1,gray,y)
                    testList.append([pic[0],gray,(tcount,y,x)])
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


    if num==2 and len(docstore2)==1:
        warped = four_point_transform(gray, docstore2[0].reshape(4, 2))
        return picfixSmall(num,warped,pos,aORG,gray)
        
    elif num ==2:
        if pos == 2:
            areaStore=[]
            # 2: [0.12, 0.13],
            # 3: [0.27, 0.28],

            if calcSIZEZ[2][0] <= avg[1] <= calcSIZEZ[2][1]:
                areaStore.append([four_point_transform(gray, docstore2[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZ[3][0] <= avg[0] <= calcSIZEZ[3][1]:
                areaStore.append([four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore
        if pos == 3:
            areaStore=[]
            # 4: [0.198, 0.23],
            # 5: [0.27, 0.28],

            if calcSIZEZ[4][0] <= avg[1] <= calcSIZEZ[4][1]:
                areaStore.append([four_point_transform(gray, docstore2[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZ[5][0] <= avg[0] <= calcSIZEZ[5][1]:
                areaStore.append([four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore
    else:
        if pos !=0 and pos != 1:
            pos= pos+2
        # print("CHECK HEREREREE")
        # print(pos)
        # print("CHECK HEREREREE")
        # print("CHECK HEREREREE")
        if calcSIZEZ[pos][0]<= avg[0] <= calcSIZEZ[pos][1]:
            return [four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]]
        else:
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
            if len(approx) == 4 and num ==2:
                docCnt = approx
                docstore.append(docCnt)
    areaStore=[]
    if num == 1:
        print("pos right herer",pos)
        paper= four_point_transform(gray2, docCnt.reshape(4, 2))
        (h4,w4)=paper.shape[:2]
        avg=((h4*w4)/aORG)
        if calcSIZEZ[pos][0]<= avg <= calcSIZEZ[pos][1]:
            return [paper,avg]
        else:
            return [grayORG,avg]

    if num == 2:
        if len(docstore)==1:
            return [[grayORG,1],[grayORG,1]]

        avg=[]
        for x in range(0,len(docstore)):
            if x ==2:
                break
            tt=four_point_transform(gray2, docstore[x].reshape(4, 2))
            (hNew,wNew)=tt.shape[:2]
            avg.append((hNew*wNew)/aORG)
        
        if pos == 2:
            areaStore=[]
            # 2: [0.12, 0.13],
            # 3: [0.27, 0.28],

            if calcSIZEZ[2][0] <= avg[1] <= calcSIZEZ[2][1]:
                areaStore.append([four_point_transform(gray2, docstore[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZ[3][0] <= avg[0] <= calcSIZEZ[3][1]:
                areaStore.append([four_point_transform(gray2, docstore[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore
        if pos == 3:
            areaStore=[]
            # 4: [0.198, 0.23],
            # 5: [0.27, 0.28],

            if calcSIZEZ[4][0] <= avg[1] <= calcSIZEZ[4][1]:
                areaStore.append([four_point_transform(gray2, docstore[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZ[5][0] <= avg[0] <= calcSIZEZ[5][1]:
                areaStore.append([four_point_transform(gray2, docstore[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore

start_time = time.time()
tmake()
end_time= time.time()
print(end_time-start_time)