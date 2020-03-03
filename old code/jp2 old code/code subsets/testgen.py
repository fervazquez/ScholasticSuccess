from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os
from matplotlib import pyplot as plt
import time

tpath="./tempDir/"

def tmake():

    docList=parseinput(sys.argv[1])
    y=0
    docList.reverse()
    tcount=0
    testList=[]
    print(len(docList))
    for x in range(0,len(docList)):
        print("right here BITCHES ",x)
        print("TEST Num: ",tcount)

        temp=convert_from_path("{}{}.pdf".format(tpath,docList[x]))
        temp[0].save("{}{}.jpg".format(tpath,docList[x]),"JPEG")
        print("{}{}.jpg".format(tpath,docList[x]))
        docList[x]=cv2.imread("{}{}.jpg".format(tpath,docList[x]))
        gray = cv2.cvtColor(docList[x], cv2.COLOR_BGR2GRAY)
        # THIS IS FOR PSAT
        # if y==3 or y==4 or y==5 or y==6:
        #     if y==3 or y==4:
        #         pic=picfixmass(2,gray)
        #         print(len(pic))
        #         # cv2.imshow("check 0",pic[0])
        #         # cv2.imshow("check 1",pic[1])
        #         # cv2.waitKey(0)
        #         testList.append(pic[0])
        #         testList.append(pic[1])


        #     else:
        #         pic=picfixmass(1,gray)
        #         testList.append(pic)
            
        #     #print(len(pic))
        #     # cv2.imshow("check 0",pic)
        #     # cv2.waitKey(0)
        # if y==0 or y==1 or y==2:    #this will remain the same for surveys but not tests
        #     
        #     testList.append(pic)

        #THIS IS FOR ACT

        pic=picfixmass(1,gray)
        testList.append(pic)
        y+=1
        if y==7:
            print("YOYOYOYOYOYYOYOYOOYYOYOYOYOYOYOOYYOYOYOYO")
            for g in range(len(testList)):
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                cv2.imwrite("1{}_{}.jpg".format(tcount,g),testList[g])
                # testList[x].save("{}{}_{}.jpg".format(tpath,tcount,testList[g]),"JPEG")
            tcount+=1
            y=0
            testList=[]
        


def parseinput(nameIn):
    inputpdf=PdfFileReader(open("{}.pdf".format(nameIn), "rb"))
    print(inputpdf.numPages)
    pglist=[]
    for i in range(inputpdf.numPages):
        output=PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        pglist.append(i)
        with open("./tempDir/{}.pdf".format(i),"wb") as outstream:
            output.write(outstream)

    return pglist

def picfixmass(typet,loc):
    num=typet
    #help1=cv2.imread(loc)
    #cv2.imshow("name",help1)
    #gray = cv2.cvtColor(loc, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("check 0",gray)
    #cv2.waitKey(0)

    gray=loc
    (h,w)=gray.shape[:2]
    gray = gray[int(h*0.05):h-int(h*.05),int(w*.045):w-int(w*.05)]
    #cv2.imshow("check 6",gray)
    # cv2.imwrite("test111111.jpg",gray)
    #cv2.waitKey(0)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 250)

    # plt.subplot(111),plt.imshow(edged,cmap = 'gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    # plt.show()
    # find contours in the edge map, then initialize
    # the contour that corresponds to the document
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    docCnt = None
    docstore2=[]
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
            if len(approx) == 4:
                docCnt = approx
                # print("LLLLLLLLLL")
                docstore2.append(docCnt)
                #break
    # print("22222222222222222222")
    # print(len(docstore2))
    print(num)
    for x in range(0,len(docstore2)):
        if x ==4:
            break
        tt=four_point_transform(gray, docstore2[x].reshape(4, 2))
        cv2.imshow("check {}, length{}".format(x,len(docstore2)),tt)
    # print("Pick the Best one")
    cv2.waitKey(0)

    if num==2:

        print("FUCK YOU 9")
        num2= input("does this need extra processing Yes: 1, No: 2 ")
        print(num2) 
        num2=int(num2)
        num4=0
        if num2==2:
            retStore=[]
            retStore.append(four_point_transform(gray, docstore2[0].reshape(4, 2)))
            retStore.append(four_point_transform(gray, docstore2[1].reshape(4, 2)))
            return retStore
    else:
        print("FUCK YOU 8")
        num4 = input("Enter number starting at ZERO or 3 to skip: ") 
        print(num4) 
        num4=int(num4)
        if num4==3:
            return four_point_transform(gray, docstore2[0].reshape(4, 2))
        

        num2= input("does this need extra processing Yes: 1, No: 2 ")
        print(num2) 
        num2=int(num2)
        
        if num2==2:
            return four_point_transform(gray, docstore2[num4].reshape(4, 2))




    # if (len(docstore2)==4 and num==2):
    #     print("FUCK YOU")
    #     retStore=[]
    #     retStore.append(four_point_transform(gray, docstore2[0].reshape(4, 2)))
    #     retStore.append(four_point_transform(gray, docstore2[1].reshape(4, 2)))
    #     return retStore
    # if (len(docstore2)==1 and num==1):
    #     print("FUCK YOU 2")
    #     return four_point_transform(gray, docstore2[0].reshape(4, 2))
    #     #four_point_transform(gray, docstore2[0].reshape(4, 2))

    print("FUCK YOU 3")


    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper
    #paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docstore2[num4].reshape(4, 2))
    #warped = four_point_transform(gray, docCnt.reshape(4, 2))

    #warped=gray
    (h,w)=warped.shape[:2]
    gray2 = warped[int(h*0.01):h-int(h*.01),int(w*.01):w-int(w*.01)]
    # cv2.imshow("check help",warped)
    # cv2.imwrite("test.jpg",warped)
    # cv2.waitKey(0)
    blurred = cv2.GaussianBlur(gray2, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    # find contours in the edge map, then initialize
    # the contour that corresponds to the document
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
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
    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper
    #cv2.imshow("check TTTT",gray2)
    #print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    #cv2.waitKey(0)


    areaStore=[]
    
    if num == 1:
        paper = four_point_transform(gray2, docCnt.reshape(4, 2))
        #cv2.imshow("check 2",paper)
        #print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        #cv2.waitKey(0)
        return paper
    if num == 2:
        # print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")

        areaStore.append(four_point_transform(gray2, docstore[0].reshape(4, 2)))
        areaStore.append(four_point_transform(gray2, docstore[1].reshape(4, 2)))
        #cv2.imshow("check 2",areaStore[1])
        #cv2.imshow("check 21",areaStore[0])
        #cv2.waitKey(0)
        return areaStore




    #paper = four_point_transform(image, docCnt.reshape(4, 2))
    #warped = four_point_transform(gray2, docCnt.reshape(4, 2))
    #cv2.imshow("check22",warped)
    #cv2.imshow("check",gray2)
    cv2.waitKey(0)



tmake()