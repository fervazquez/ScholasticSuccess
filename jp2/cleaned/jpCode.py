from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os
from matplotlib import pyplot as plt

tpath="./tempDir/"
SHADEVAL=400
def runner():
    try:
        doc = parseinput(sys.argv[1])
    except:
        print("Program stopped at line 11")
        sys.exit("line 11 you twat")

    print(doc)
    y=0
    doc.reverse()
    surveyList=[]
    testList=[]

    for x in range(0,len(doc)):
        # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        # print(len(surveyList)," LLLLLLLLLLLLLLLLLLLLLLLLLL")
        if len(surveyList)==3:

            surveyProcess(surveyList)

            # for z in range(0,3):
            #     cv2.imshow("check {}".format(z),surveyList[z])
            #     cv2.imwrite("{}.jpg".format(z),surveyList[z])
            # cv2.waitKey(0)
            surveyList=[]
        if y==8:    #this number will change based on the tests
            
            # break
            
            y=0
        # print("*************************************")
        # print("numbers here x{} y{}".format(x,y))
        # print("*************************************")
        temp=convert_from_path("{}{}.pdf".format(tpath,doc[x]))

        print(doc[x]," Im here")

        temp[0].save("{}{}.jpg".format(tpath,doc[x]),"JPEG")
        print("{}{}.jpg".format(tpath,doc[x]))
        doc[x]=cv2.imread("{}{}.jpg".format(tpath,doc[x]))
        # print(doc[x])
        gray = cv2.cvtColor(doc[x], cv2.COLOR_BGR2GRAY)
        if y==0:

            y+=1
            continue
        if y==4 or y==5:    #So will these choices
            print("yo")
            pic=picfixmass(2,gray)
            #print(len(pic))
            # cv2.imshow("check 0",pic[0])
            # cv2.imshow("check 1",pic[1])
            #cv2.waitKey(0)
            #print("PPPPPPPPPPPPPPPPP")

        else:
            pic=picfixmass(1,gray)
            #print(len(pic))
            # cv2.imshow("check 0",pic)
            #cv2.waitKey(0)
            
            #print("PPPPPPPPPPPPPPPPP")

        if y==1 or y==2 or y==3:    #this will remain the same for surveys but not tests
            surveyList.append(pic)
            
        

        y+=1
        
        #print(cv2.countNonZero(gray))
    
def surveyProcess(doc):
    print(len(doc)," KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    for x in range(0,len(doc)):
        h,w=doc[x].shape[:2]
        print("************sizes h:{} w:{}".format(h,w))

    surveyPage1(doc[0])
    surveyPage2(doc[1])
    #surveyPage3(doc[2])
    # cv2.waitKey(0)

def surveyPage1(doc):
    # doc = cv2.threshold(doc, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    (h,w)=doc.shape[:2]
    gray = doc[int(h*0.07):h-int(h*.12),int(w*.05):w]
    # cv2.imshow("surveyPage1",gray)
    # cv2.imwrite("surveyPage1.jpg",gray)

    (h,w)=gray.shape[:2]
    amt=int(w/6)
    height=int(h/2)-70
    u1=gray[13:height,5:int(amt/2)-15]         #Has y/n response
    u2=gray[185:height,amt+30:(amt*2)-100]
    u3=gray[185:height,((amt*2)+85):(amt*3)-50]
    u4=gray[13:height,((amt*3)+50):(amt*4)-80]   #Has y/n response
    u5=gray[185:height,((amt*4)+75):(amt*5)-50]
    u6=gray[185:height,((amt*5)+20+int(amt/2)):amt*6]

    y1=u1[0:35,0:80]
    y2=u4[0:35,0:80]
    u1sizeh,u1sizew=u1.shape[:2]
    u4sizeh,u4sizew=u4.shape[:2]
    u1=u1[172:height,0:u1sizew]
    u4=u4[172:height,0:u4sizew]

    # u1h,u1w=u1.shape[:2]
    # u2h,u2w=u2.shape[:2]
    # u3h,u3w=u3.shape[:2]
    # u4h,u4w=u4.shape[:2]
    # u5h,u5w=u5.shape[:2]
    # u6h,u6w=u6.shape[:2]

    # print("u1 height:{} width:{}".format(u1h,u1w))
    # print("u2 height:{} width:{}".format(u2h,u2w))
    # print("u3 height:{} width:{}".format(u3h,u3w))
    # print("u4 height:{} width:{}".format(u4h,u4w))
    # print("u5 height:{} width:{}".format(u5h,u5w))
    # print("u6 height:{} width:{}".format(u6h,u6w))

    # cv2.imshow("y1",y1)
    # cv2.imshow("y2",y2)
    # cv2.imshow("u1",u1)
    # cv2.imshow("u2",u2)
    # cv2.imshow("u3",u3)
    # cv2.imshow("u4",u4)
    # cv2.imshow("u5",u5)
    # cv2.imshow("u6",u6)

    # cv2.waitKey(0)

    h2=int(h/2)+90
    d1=gray[h2:h,5:int(amt/2)-15]         #Has y/n response
    d2=gray[h2+172:h,amt+30:(amt*2)-100]
    d3=gray[h2+172:h,((amt*2)+85):(amt*3)-50]
    d4=gray[h2:h,((amt*3)+50):(amt*4)-80]   #Has y/n response
    d5=gray[h2+172:h,((amt*4)+75):(amt*5)-50]
    d6=gray[h2+172:h,((amt*5)+20+int(amt/2)):amt*6]

    y3=d1[0:35,0:80]
    y4=d4[0:35,0:80]
    d1sizeh,d1sizew=d1.shape[:2]
    d4sizeh,d4sizew=d4.shape[:2]
    d1=d1[172:h,0:u1sizew]
    d4=d4[172:h,0:u4sizew]


    # d1h,d1w=d1.shape[:2]
    # d2h,d2w=d2.shape[:2]
    # d3h,d3w=d3.shape[:2]
    # d4h,d4w=d4.shape[:2]
    # d5h,d5w=d5.shape[:2]
    # d6h,d6w=d6.shape[:2]

    # print("d1 height:{} width:{}".format(d1h,d1w))
    # print("d2 height:{} width:{}".format(d2h,d2w))
    # print("d3 height:{} width:{}".format(d3h,d3w))
    # print("d4 height:{} width:{}".format(d4h,d4w))
    # print("d5 height:{} width:{}".format(d5h,d5w))
    # print("d6 height:{} width:{}".format(d6h,d6w))

    # cv2.imshow("y3",y3)
    # cv2.imshow("y4",y4)
    # cv2.imshow("d1",d1)
    # cv2.imshow("d2",d2)
    # cv2.imshow("d3",d3)
    # cv2.imshow("d4",d4)
    # cv2.imshow("d5",d5)
    # cv2.imshow("d6",d6)
    u1ans=ttResponse(u1)
    u2ans=ttResponse(u2)
    u3ans=ttResponse(u3)
    u4ans=ttResponse(u4)
    u5ans=ttResponse(u5)
    u6ans=ttResponse(u6)
    d1ans=ttResponse(d1)
    d2ans=ttResponse(d2)
    d3ans=ttResponse(d3)
    d4ans=ttResponse(d4)
    d5ans=ttResponse(d5)
    d6ans=ttResponse(d6)
    y1ans=twoRep(y1)
    y2ans=twoRep(y2)
    y3ans=twoRep(y3)
    y4ans=twoRep(y4)

    print("****************************")
    print("y1Ans ", y1ans)
    print("u1 ",u1ans)
    print("u2 ",u2ans)
    print("u3 ",u3ans)
    print("****************************")
    print("y2Ans ", y2ans)
    print("u4 ",u4ans)
    print("u5 ",u5ans)
    print("u6 ",u6ans)
    print("****************************")
    print("y3Ans ", y3ans)
    print("d1 ",d1ans)
    print("d2 ",d2ans)
    print("d3 ",d3ans)
    print("****************************")
    print("y4Ans ", y4ans)
    print("d4 ",d4ans)
    print("d5 ",d5ans)
    print("d6 ",d6ans)
    print("****************************")

def surveyPage2(doc):
    (h,w)=doc.shape[:2]
    gray = doc[int(h*0.1):h,0:w-int(w*.035)]
    (h,w)= gray.shape[:2]
    gray1=gray[0:int(h/3)-82,0:w]
    gray2=gray[int(h/3):h,0:w]

    cv2.imshow("gray2", gray2)
    cv2.waitKey(0)

    #D0B, grad yr, date, HS code. Use gray1
    (h,w)=gray1.shape[:2]
    sec1=gray1[0:h,0:int(w*.271)]
    sec2=gray1[0:h,int(w*.295):int(w*0.56)]
    sec3=gray1[0:h,int(w*.655):w]
    # cv2.imshow("last Part", sec3)
    # cv2.imshow("DOB",sec1)
    # cv2.imshow("date",sec2)
    #DOB Code
    (h1,w1)=sec1.shape[:2]

    monDOB=sec1[0:h1,5:int((2/8)*w1)]
    dayDOB=sec1[0:h1,int((2/8)*w1)+5:int(w1/2)]
    yrDOB=sec1[0:h1,int(w1/2)+5:w]

    # cv2.imshow("monDOB",monDOB)
    # cv2.imshow("dayDOB",dayDOB)
    # cv2.imshow("yrDOB",yrDOB)

    #Date Code
    (h3,w3)=sec2.shape[:2]

    monDate=sec2[0:h3,5:int((2/8)*w3)]
    dayDate=sec2[0:h3,int((2/8)*w3)+5:int(w3/2)]
    yrDate=sec2[0:h3,int(w3/2)+5:w]

    # cv2.imshow("monDate",monDate)
    # cv2.imshow("dayDate",dayDate)
    # cv2.imshow("yrDate",yrDate)

    print("sizes h:{} w:{}".format(h,w))

    #last part code
    (h4,w4)=sec3.shape[:2]
    gradyr=sec3[0:h4,0:int(w4*.19)]
    schoolCode=sec3[0:h4,int(w4*.26):int(w4*.645)]
    testCode=sec3[0:h4,int(w4*.72):w4]

    #cv2.imshow("gradyr",gradyr)
    # cv2.imshow("schoolCode",schoolCode)
    # cv2.imshow("testCode",testCode)

    
    bmon=ttResponse(monDOB)
    bday=ttResponse(dayDOB)
    dmon=ttResponse(monDate)
    dday=ttResponse(dayDate)
    gyr=ttResponse(gradyr)

    byear=fTResponse(yrDOB)
    dyear=fTResponse(yrDate)
    scCode=fTResponse(schoolCode)

    tcCode=threeResp(testCode)



    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    print("Birthday Month:{}".format(bmon))
    print("Birthday Day:{}".format(bday))
    print("Birthday Year:{}".format(byear))
    print("Date Month:{}".format(dmon))
    print("Date Day:{}".format(dday))
    print("Date Year:{}".format(dyear))
    print("Grad Yr:{}".format(gyr))
    print("School Code:{}".format(scCode))
    print("Test Code:{}".format(tcCode))
    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")

    # cv2.imshow("surveyPage2top",gray1)
    # cv2.imwrite("surveyPage2top.jpg",gray1)
    # cv2.imshow("surveyPage2bottom",gray2)
    # cv2.imwrite("surveyPage2bottom.jpg",gray2)
    # cv2.waitKey(0)

def twoRep(pic):
    pic = cv2.threshold(pic, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    (h,w)=pic.shape[:2]
    t1=pic[0:h,0:int(w/2)]
    t2=pic[0:h,int(w/2):w]
    val1=cv2.countNonZero(t1)
    val2=cv2.countNonZero(t2)
    
    if val1<SHADEVAL:
        val1=-1
    else:
        val1=1
    if val2<SHADEVAL:
        val2=-1
    else:
        val2=1
    
    if (val1==1) and (val2==1):
        return "BAS"
    if (val1==1) and (val2==-1):
        return "Y"
    if (val1==-1) and (val2==1):
        return "N"
    else:
        return "DNE"
    
def ttResponse(pic):
    #cv2.imshow("whole",pic)
    pic = cv2.threshold(pic, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cv2.imshow("output here",pic)
    # cv2.waitKey(0)
    (h,w)=pic.shape[:2]
    calc=int(h/10)
    arr1=[]
    arr2=[]
    for x in range(0,10):
        temp=pic[calc*x:calc*(x+1),0:int(w/2)]
        temp2=pic[calc*x:calc*(x+1),int(w/2):w]
        # cv2.imshow("poss: {}".format(x),temp)
        # cv2.imshow("poss2: {}".format(x),temp2)
        arr1.append(cv2.countNonZero(temp))
        arr2.append(cv2.countNonZero(temp2))
    # print(arr2)
    # print(arr1)
    val1=max(arr1)
    val2=max(arr2)
    if val1>SHADEVAL:
        val1=arr1.index(val1)
    else:
        val1=-1
    if val2>SHADEVAL:
        val2=arr2.index(val2)
    else:
        val2=-1

    if (val1==-1) and (val2==-1):
        return -1
    
    if (val1!=-1) and (val2==-1):
        return int(val1)
    if (val1==-1) and (val2!=-1):
        return int(val2)
    else:
        helper="{}{}".format(val1,val2)
        return int(helper)
    
    #cv2.waitKey(0)


def threeResp(pic):
    print("big yo")
    #cv2.imshow("whole",pic)
    pic = cv2.threshold(pic, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cv2.imshow("output here",pic)
    # cv2.waitKey(0)
    (h,w)=pic.shape[:2]
    calc=int(h/10)
    arr1=[]
    arr2=[]
    arr3=[]
    for x in range(0,10):
        tval1=calc*x
        tval2=calc*(x+1)
        temp=pic[tval1:tval2,0:int(w*0.3333)]
        temp2=pic[tval1:tval2,int(w*0.3333):int(w*0.6666)]
        temp3=pic[tval1:tval2,int(w*0.6666):w]
        # cv2.imshow("poss: {}".format(x),temp)
        # cv2.imshow("poss2: {}".format(x),temp2)
        arr1.append(cv2.countNonZero(temp))
        arr2.append(cv2.countNonZero(temp2))
        arr3.append(cv2.countNonZero(temp3))
    # print(arr2)
    # print(arr1)
    val1=max(arr1)
    val2=max(arr2)
    val3=max(arr3)
    if val1>SHADEVAL:
        val1=arr1.index(val1)
        if val1==0:
            val1="P"
        elif val1==1:
            val1="S"
        elif val1==1:
            val1="A"
        else:
            val1="I"
        
    else:
        val1=-1
    if val2>SHADEVAL:
        val2=arr2.index(val2)
    else:
        val2=-1
    if val3>SHADEVAL:
        val3=arr3.index(val3)
    else:
        val3=-1

    if (val1==-1) and (val2==-1):
        return -1
    
    if (val1!=-1) and (val2==-1):
        return int(val1)
    if (val1==-1) and (val2!=-1):
        return int(val2)
    else:
        helper="{}{}{}".format(val1,val2,val3)
        return helper

def fTResponse(pic):
    print("yo")
    #cv2.imshow("whole",pic)
    pic = cv2.threshold(pic, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cv2.imshow("output here",pic)
    # cv2.waitKey(0)
    (h,w)=pic.shape[:2]
    calc=int(h/10)
    arr1=[]
    arr2=[]
    arr3=[]
    arr4=[]
    for x in range(0,10):
        tval1=calc*x
        tval2=calc*(x+1)
        temp=pic[tval1:tval2,0:int(w*0.25)]
        temp2=pic[tval1:tval2,int(w*0.25):int(w*0.5)]
        temp3=pic[tval1:tval2,int(w*0.5):int(w*0.75)]
        temp4=pic[tval1:tval2,int(w*0.75):w]
        # cv2.imshow("poss: {}".format(x),temp)
        # cv2.imshow("poss2: {}".format(x),temp2)
        arr1.append(cv2.countNonZero(temp))
        arr2.append(cv2.countNonZero(temp2))
        arr3.append(cv2.countNonZero(temp3))
        arr4.append(cv2.countNonZero(temp4))
    # print(arr2)
    # print(arr1)
    val1=max(arr1)
    val2=max(arr2)
    val3=max(arr3)
    val4=max(arr4)
    if val1>SHADEVAL:
        val1=arr1.index(val1)
    else:
        val1=-1
    if val2>SHADEVAL:
        val2=arr2.index(val2)
    else:
        val2=-1
    if val3>SHADEVAL:
        val3=arr3.index(val3)
    else:
        val3=-1
    if val4>SHADEVAL:
        val4=arr4.index(val4)
    else:
        val4=-1

    if (val1==-1) and (val2==-1):
        return -1
    
    if (val1!=-1) and (val2==-1):
        return int(val1)
    if (val1==-1) and (val2!=-1):
        return int(val2)
    else:
        helper="{}{}{}{}".format(val1,val2,val3,val4)
        return int(helper)


def surveyPage3(doc):
    (h,w)=doc.shape[:2]
    gray = doc[int(h*0.1):h-int(h*0.02),0:w]
    cv2.imshow("surveyPage3",gray)
    cv2.imwrite("surveyPage3.jpg",gray)
    # cv2.waitKey(0)


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
    edged = cv2.Canny(blurred, 75, 200)

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
                print("LLLLLLLLLL")
                docstore2.append(docCnt)
                #break
    # print("22222222222222222222")
    # print(len(docstore2))
    # for x in range(0,len(docstore2)):
    #     tt=four_point_transform(gray, docstore2[x].reshape(4, 2))
    #     cv2.imshow("check {}".format(x),tt)
    # cv2.waitKey(0)

    if (len(docstore2)==4 and num==2):
        retStore=[]
        retStore.append(four_point_transform(gray, docstore2[0].reshape(4, 2)))
        retStore.append(four_point_transform(gray, docstore2[1].reshape(4, 2)))
        return retStore
    if (len(docstore2)==4 and num==1):
        
        return four_point_transform(gray, docstore2[0].reshape(4, 2))



    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper
    #paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docstore2[0].reshape(4, 2))

    #warped=gray
    (h,w)=warped.shape[:2]
    gray2 = warped[int(h*0.01):h-int(h*.01),int(w*.01):w-int(w*.01)]
    # cv2.imshow("check help",warped)
    # cv2.imwrite("test.jpg",warped)
    #cv2.waitKey(0)
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




runner()