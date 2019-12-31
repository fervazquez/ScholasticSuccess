from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os, random
from matplotlib import pyplot as plt
import time, json

SHADEVAL=400
gFac=325
pathName="./dep_folder/"
ANSLIST=['A','B','C','D','E','F']
ABCLIST=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def runCode():
    locData = os.listdir(pathName)
    #print(locData)
    count = 0
    count2 = 0
    dataList=[[]]
    print(locData)
    for x in locData:
        if count ==7:
            dataList.append([])
            count=0
            count2+=1
        print(x)
        hold=cv2.imread(pathName+x)
        gray=cv2.cvtColor(hold, cv2.COLOR_BGR2GRAY)
        dataList[count2].append(gray)
        count+=1
        
        
    print(dataList)
    print(len(dataList))
    lastDict={}
    count3=0
    for x in dataList:
        size={}
        outputDict={}
        print(len(x))
        for y in range(len(x)):
            h,w=x[y].shape[:2]
            size['{}'.format(y)]=(h,w)



        x[0]=transform_info(SS_ACT(x[0],76))
        x[1]=transform_info(SS_ACTMath(x[1],61))
        x[2]=transform_info(SS_ACT(x[2],41))
        x[3]=transform_info(SS_ACT(x[3],41))
        print(x[3])
        print(size)
        x[4]=surveyPage3(x[4])
        x[5]=surveyPage2(x[5])
        x[6]=surveyPage1(x[6])
        print(x[4])
        print("***************************")
        print(x[5])
        print("***************************")
        print(x[6])
        print("***************************")


        outputDict['first_Name'] = x[4]['First Name']
        outputDict['last_Name'] = x[4]['Last Name']
        outputDict['DOB'] = str(x[5]['Birthday Month'])+'/'+str(x[5]['Birthday Day'])+'/'+str(x[5]['Birthday Year'])
        outputDict['school_code'] = x[5]['School Code']
        outputDict['survey'] =x[4]['Student QList']
        
        outputDict['survey_cont'] =x[5]['Survey Questions List']
        outputDict['test_date'] = str(x[5]['Date Month'])+'/'+str(x[5]['Date Day'])+'/'+str(x[5]['Date Year'])
        outputDict['test_code'] = x[5]['Test Code']
        outputDict['Timing'] = x[6]
        outputDict['English'] = x[0]
        outputDict['Math'] = x[1]
        outputDict['Reading'] = x[2]
        outputDict['Science'] = x[3]
        lastDict[count3]=outputDict
        count3+=1
    with open('data.txt', 'w') as outfile:
        json.dump(lastDict, outfile)

        

def transform_info(qlist):
    dictHelp={}
    for x in qlist:
        dictHelp['{}'.format(x[0])] = [x[1],x[2]]
    return dictHelp

# 0 is 75
# 1 is 60
# 2 is 40
# 3 is 40
# 4 is namePG #surveypage3
# 5 is school codes #surveypage2
# 6 is times #surveypage1

def SS_ACT(image,amt):
    imgadj=viewAdjust(image,4)
    joke=[]
    count2=0
    for x in range(0,len(imgadj)):
        gg=imgadj[x]
        #warped = cv2.cvtColor(gg, cv2.COLOR_BGR2GRAY)
        # apply Otsu's thresholding method to binarize the warped piece of paper
        thresh = cv2.threshold(gg, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #cv2.imshow("testI",thresh)
        (h,w)=thresh.shape[:2]
        thresh2 = thresh[int(h*0.01):h-int(h*.02),int(w*.05):w-int(w*.15)]
        #cv2.imshow("{}".format(x),thresh2)
        (h,w)=thresh2.shape[:2]
        y=int(h*.05263)
        mlist=[]
        output=""
        count=0
        output2=""
        for t in range(0,19):
            count2+=1
            if count2<amt:
                joke.append(calcAns(x,y,t,thresh2,count2,w,1))
        # cv2.waitKey(0)
    # print(joke)
    # print("*************************************")
    return joke
    #cv2.waitKey(0)

def SS_ACTMath(image,amt):
    imgadj=viewAdjust(image,4)
    joke=[]
    count2=0
    for x in range(0,len(imgadj)):
        gg=imgadj[x]
        #warped = cv2.cvtColor(gg, cv2.COLOR_BGR2GRAY)
        # apply Otsu's thresholding method to binarize the warped piece of paper
        thresh = cv2.threshold(gg, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #cv2.imshow("testI",thresh)
        (h,w)=thresh.shape[:2]
        thresh2 = thresh[int(h*0.01):h-int(h*.03),int(w*.05):w-int(w*.05)]
        #cv2.imshow("{}".format(x),thresh2)
        #cv2.waitKey(0)
        (h,w)=thresh2.shape[:2]
        y=int(h*.05263)
        mlist=[]
        output=""
        count=0
        output2=""
        for t in range(0,19):
            count2+=1
            if count2<amt:
                joke.append(calcAnsACT(x,y,t,thresh2,count2,w))
        # cv2.waitKey(0)
    # print(joke)
    # print("*************************************")
    return joke
    #cv2.waitKey(0)

def viewAdjust(pic,amt):
    hold=[]
    (h,w)=pic.shape[:2]
    val=int(w/amt)
    for x in range(0,amt):
        hold.append(pic[0:h,val*x:val*(x+1)])
    return hold

def calcAns(x,y,t,pic,count2,w,z):
    mlist=[]
    olist=[]
    output=""
    output2=""
    count=0
    half=int(y*(t+1))-int(y*t)
    half=int(half/2)
    half=(y*t)+half
    q=pic[half:y*(t+1),0:w]
    #cv2.imshow("{} t{}".format(x,t),q)
    (length,wid)=q.shape[:2]
    amt=int(wid/6)
    k0=q[0:length,0:amt]
    k1=q[0:length,((amt*2)+5):amt*3]
    k2=q[0:length,((amt*3)+5):amt*4]
    k3=q[0:length,((amt*4)+5):amt*5]
    k4=q[0:length,((amt*5)+5):amt*6]
    mlist.append(cv2.countNonZero(k1))
    mlist.append(cv2.countNonZero(k2))
    mlist.append(cv2.countNonZero(k3))
    mlist.append(cv2.countNonZero(k4))
    
    #cv2.imshow("{} t{}".format(x,t),k0)
    #if count2 == 19:# or count2 == 8 or count2 == 15 or count2 == 19:
    #    cv2.imshow("{} t{}".format(x,t),q)
    #	cv2.imshow("{} t{} 0".format(x,t),k0)
    #	cv2.imshow("{} t{} 1".format(x,t),k1)
    #	cv2.imshow("{} t{} 2".format(x,t),k2)
    #	cv2.imshow("{} t{} 3".format(x,t),k3)
    #	cv2.imshow("{} t{} 4".format(x,t),k4)
    mnum=max(mlist)
    
    if mlist[0]==mnum:
        if count2%2 == 0 and z == 1:
            output='F'
        else:
            output='A'
        count+=1
    if mlist[1]==mnum:
        if count2%2 == 0 and z == 1:
            output='G'
        else:
            output='B'
        count+=1
    if mlist[2]==mnum:
        if count2%2 == 0 and z == 1:
            output='H'
        else:
            output='C'
        count+=1
    #if mlist[3]>gFac:
    if mlist[3]==mnum:
        if count2%2 == 0 and z == 1:
            output='J'
        else:
            output='D'
        count+=1
    mlist.append(cv2.countNonZero(k0))
    if mlist[4]>gFac:
        output2='G'
    else:
        output2='NG'
    if count>=2:
        output='Z'
    if count==0:
        output='Z'
    # print("{} {} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],output,mnum,output2,mlist[4]))
    olist.append(count2)
    olist.append(output)
    olist.append(output2)
    return olist

def calcAnsACT(x,y,t,pic,count2,w):
    mlist=[]
    olist=[]
    output=""
    output2=""
    count=0
    half=int(y*(t+1))-int(y*t)
    half=int(half/2)
    half=(y*t)+half
    q=pic[half:y*(t+1),0:w]

    #cv2.imshow("{} t{}".format(x,t),q)
    (length,wid)=q.shape[:2]
    amt=int(wid/7)
    k0=q[0:length,0:amt]
    k1=q[0:length,((amt*2)+5):amt*3]
    k2=q[0:length,((amt*3)+5):amt*4]
    k3=q[0:length,((amt*4)+5):amt*5]
    k4=q[0:length,((amt*5)+5):amt*6]
    k5=q[0:length,((amt*6)+5):amt*7]
    mlist.append(cv2.countNonZero(k1))
    mlist.append(cv2.countNonZero(k2))
    mlist.append(cv2.countNonZero(k3))
    mlist.append(cv2.countNonZero(k4))
    mlist.append(cv2.countNonZero(k5))
    
    #cv2.imshow("{} t{}".format(x,t),k0)
    #if count2 == 18 or count2 == 19 or count2 == 37 or count2 == 38:
    #	cv2.imshow("{} t{}".format(x,t),q)
    #	cv2.imshow("{} t{} 0".format(x,t),k0)
    #	cv2.imshow("{} t{} 1".format(x,t),k1)
    #	cv2.imshow("{} t{} 2".format(x,t),k2)
    #	cv2.imshow("{} t{} 3".format(x,t),k3)
    #	cv2.imshow("{} t{} 4".format(x,t),k4)
    #	cv2.imshow("{} t{} 5".format(x,t),k5)
    mnum=max(mlist)
    
    #if mlist[0]>gFac:
    if mlist[0]==mnum:
        if count2%2 == 0:
            output='F'
        else:
            output='A'
        count+=1
    if mlist[1]==mnum:
        if count2%2 == 0:
            output='G'
        else:
            output='B'
        count+=1
    if mlist[2]==mnum:
        if count2%2 == 0:
            output='H'
        else:
            output='C'
        count+=1
    if mlist[3]==mnum:
        if count2%2 == 0:
            output='J'
        else:
            output='D'
        count+=1
    if mlist[4]==mnum:
        if count2%2 == 0:
            output='K'
        else:
            output='E'
        count+=1
    mlist.append(cv2.countNonZero(k0))
    if mlist[5]>gFac:
        output2='G'
    else:
        output2='NG'
    if count>=2:
        output='W'
    if count==0:
        output='Z'
    # print("{} {} {} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],mlist[4],output,mnum,output2,mlist[5]))
    olist.append(count2)
    olist.append(output)
    olist.append(output2)
    return olist

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

    # print("****************************")
    # print("1.1 ", y1ans)
    # print("1.2 ",u1ans)
    # print("1.3 ",u2ans)
    # print("1.4 ",u3ans)
    # print("****************************")
    # print("2.1 ", y2ans)
    # print("2.2 ",u4ans)
    # print("2.3 ",u5ans)
    # print("2.4 ",u6ans)
    # print("****************************")
    # print("3.1 ", y3ans)
    # print("3.2 ",d1ans)
    # print("3.3 ",d2ans)
    # print("3.4 ",d3ans)
    # print("****************************")
    # print("4.1 ", y4ans)
    # print("4.2 ",d4ans)
    # print("4.3 ",d5ans)
    # print("4.4 ",d6ans)
    # print("****************************")
    return {'1.1':y1ans,'1.2':u1ans,'1.3':u2ans,'1.4':u3ans,'2.1':y2ans,
    '2.2':u4ans,'2.3':u5ans,'2.4':u6ans,'3.1':y3ans,
    '3.2':d1ans,'3.3':d2ans,'3.4':d3ans,'4.1':y4ans,'4.2':d4ans,
    '4.3':d5ans,'4.4':d6ans}

def surveyPage2(doc):
    (h,w)=doc.shape[:2]
    gray = doc[int(h*0.1):h,0:w-int(w*.035)]
    (h,w)= gray.shape[:2]
    gray1=gray[0:int(h/3)-82,0:w]
    gray2=gray[int(h/3):h,0:w]

    #cv2.imshow("gray2", gray2)
    # cv2.waitKey(0)


    (h,w)=gray2.shape[:2]
    fBlock=gray2[int(h*.045):int(h*.22),int(w*.155):int(w*.35)]
    secBlock=gray2[int(h*.295):int(h*.47),int(w*.155):int(w*.28)]
    thirdBlock=gray2[int(h*.55):int(h*.72),int(w*.155):int(w*.28)]
    fourthBlock=gray2[int(h*.8):int(h*.97),int(w*.155):int(w*.28)]

    qList=surveyResp2(fBlock,secBlock,thirdBlock,fourthBlock)
    # print("qList: ",qList)
    # cv2.imshow("fBlock", fBlock)
    # cv2.imshow("secBlock", secBlock)
    # cv2.imshow("fourthBlock", fourthBlock)
    # cv2.imshow("thirdBlock", thirdBlock)
    # cv2.waitKey(0)



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

    #print("sizes h:{} w:{}".format(h,w))

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
    
    byear=fTResponse(yrDOB)
    gyr=ttResponse(gradyr)

    # dday=ttResponse(dayDate)
    # dmon=ttResponse(monDate)
    # dyear=fTResponse(yrDate)
    # scCode=fTResponse(schoolCode)
    # tcCode=threeResp(testCode)
    dday=14
    dmon=9
    dyear=2019
    scCode="445578"
    tcCode="A06"

    # print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    # print("Birthday Month:{}".format(bmon))
    # print("Birthday Day:{}".format(bday))
    # print("Birthday Year:{}".format(byear))
    
    # print("Date Month:{}".format(dmon))
    # print("Date Day:{}".format(dday))
    # print("Date Year:{}".format(dyear))

    # print("Grad Yr:{}".format(gyr))
    # print("School Code:{}".format(scCode))
    # print("Test Code:{}".format(tcCode))
    # print("Survey Questions List {}".format(qList))
    # print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")

    # cv2.imshow("surveyPage2top",gray1)
    # cv2.imwrite("surveyPage2top.jpg",gray1)
    # cv2.imshow("surveyPage2bottom",gray2)
    # cv2.imwrite("surveyPage2bottom.jpg",gray2)
    # cv2.waitKey(0)
    return {'Birthday Month':bmon,'Birthday Day':bday,'Birthday Year':byear,
    'Date Month':dmon,'Date Day':dday,'Date Year':dyear,
    'Grad Yr':gyr,'School Code':scCode,'Test Code':tcCode,
    'Survey Questions List':qList}

def surveyPage3(doc):
    
    (h,w)=doc.shape[:2]
    gray = doc[int(h*0.1):h-int(h*0.023),0:w]
    # cv2.imshow("surveyPage3",gray)
    # cv2.imwrite("surveyPage3.jpg",gray)
    # cv2.waitKey(0)
    lg=gray[0:int(h*.675),0:int(w*.485)]
    rg=gray[0:int(h*.675),int(w*.515):w]
    bg=doc[int(h*.837):int(h*.985),int(w*.04):int(w*.75)]
    # cv2.imshow("bg",bg)
    
    qList=bqParser(bg)
    # cv2.imshow("rg",rg)
    # cv2.imshow("lg",lg)

    # cv2.imwrite("rg.jpg",rg)
    # cv2.imwrite("lg.jpg",lg)
    #print("first Name")
    firstName=nameBuilder(rg)
    #print("LAst Name")
    lastName=nameBuilder(lg)
    #print("Student Name {} {}".format(firstName,lastName))
    #print("Student QList: {}".format(qList))
    #print(qList)
    #cv2.waitKey(0)

    return {'First Name':firstName,'Last Name':lastName,'Student QList':qList}

def circleHelp(pic):
    (h,w)=pic.shape[:2]
    s1=pic[0:int(h*.22),0:w]
    s2=pic[int(h*.4):int(h*.6),0:int(w*.75)]
    s3=pic[int(h*.8):h,0:int(w*.5)]
    # cv2.imshow("s1",s1)
    # cv2.imshow("s2",s2)
    # cv2.imshow("s3",s3)
    # cv2.waitKey(0)

    f=markGetter(s1,4)
    sec=markGetter(s2,3)
    thi=markGetter(s3,2)
    # print("CHECK HERE ((((((((((((((")
    # print("{} {} {}".format(f,sec,thi))

    return f,sec,thi

def markGetter(pic,amt):
    pic = cv2.threshold(pic, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    (h,w)=pic.shape[:2]
    qholder=[]
    
    calc=w/amt
    for x in range(0,amt):
        t=pic[0:h,int(calc*x):int(calc*(x+1))]
        qholder.append(cv2.countNonZero(t))
    val=max(qholder)
    if val>SHADEVAL:
        val=ANSLIST[qholder.index(val)]
    else:
        val=-1
    return val

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
        elif val1==2:
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
        try:
            y=int(helper)
            return y
        except:
            return "DNE"

def bqParser(pic):
    (h,w)=pic.shape[:2]
    col1=pic[0:h,0:int(w*.085)]
    col2=pic[0:h,int(w*.255):int(w*.345)]
    col3=pic[0:h,int(w*.515):int(w*.6)]
    col4=pic[0:h,int(w*.77):w]

    # cv2.imshow("col1",col1)
    # cv2.imshow("col2",col2)
    # cv2.imshow("col3",col3)
    # cv2.imshow("col4",col4)
    q1,q2,q3,q4=bgParser2(col1)
    q5,q6,q7,q8=bgParser2(col2)

    (h,w)=col3.shape[:2]
    calc=h/7
    c1=col3[0:int(h/7),0:w]
    c2=col3[int(h*(2/7)):int(h*(3/7)),0:w]
    # cv2.imshow("c1",c1)
    # cv2.imshow("c2",c2)
    q9=twoRep(c1)
    q10=twoRep(c2)

    (h,w)=col4.shape[:2]
    calc=h/7
    c11=col4[0:int(h/7),int(w*.05):int(w*.4)]
    c12=col4[int(h*(2/7)):int(h*(3/7)),0:w]
    # cv2.imshow("c11",c11)
    # cv2.imshow("c12",c12)
    q11=twoRep(c11)
    q12=markGetter(c12,5)
    # cv2.waitKey(0)

    rList={'1':q1,'2':q2,'3':q3,'4':q4,'5':q5,'6':q6,'7':q7,
    '8':q8,'9':q9,'10':q10,'11':q11,'12':q12}
    #print(rList)
    #print("LOOK UP <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    # cv2.waitKey(0)
    return rList

def bgParser2(pic):
    (h,w)=pic.shape[:2]
    calc=h/7
    c1=pic[0:int(h/7),0:w]
    c2=pic[int(h*(2/7)):int(h*(3/7)),0:w]
    c3=pic[int(h*(4/7)):int(h*(5/7)),0:w]
    c4=pic[int(h*(6/7)):h,0:w]

    # cv2.imshow("c1",c1)
    # cv2.imshow("c2",c2)
    # cv2.imshow("c3",c3)
    # cv2.imshow("c4",c4)
    # cv2.waitKey(0)

    q1=twoRep(c1)
    q2=twoRep(c2)
    q3=twoRep(c3)
    q4=twoRep(c4)
    return q1,q2,q3,q4

def nameBuilder(pic):
    pic = cv2.threshold(pic, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    (h,w)=pic.shape[:2]
    wCalc=w/15
    hCalc=h/26
    nameList=[]
    name=""
    for x in range(0,15):
        nameList.append([])
        for y in range(0,26):
            temp=pic[int(hCalc*y):int(hCalc*(y+1)),int(wCalc*x):int(wCalc*(x+1))]
            nameList[x].append(cv2.countNonZero(temp))
        val=max(nameList[x])
        
        if val>520:
            name+=str(ABCLIST[nameList[x].index(val)])
        nameList[x]=val
        #nameList[x]=nameList[x].index(val)
    

    if len(name)==0:
        name="NO_{}_NAME".format(random.randint(0,9999))
    # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    # print(name)

    return name

def surveyResp2(pic1,pic2,pic3,pic4):

    (h,w)=pic1.shape[:2]
    s1=pic1[0:int(h*.22),0:w]
    s2=pic1[int(h*.4):int(h*.6),0:int(w*.5)]
    s3=pic1[int(h*.8):h,0:int(w*.33333)]
    # cv2.imshow("s1",s1)
    # cv2.imshow("s2",s2)
    # cv2.imshow("s3",s3)
    # cv2.waitKey(0)
    q13=markGetter(s1,6)
    q14=markGetter(s2,3)
    q15=markGetter(s3,2)


    q16,q17,q18=circleHelp(pic2)
    q19,q20,q21=circleHelp(pic3)
    q22,q23,q24=circleHelp(pic4)


    rList={'13':q13,'14':q14,'15':q15,'16':q16,'17':q17,'18':q18,
    '19':q19,'20':q20,'21':q21,'22':q22,'23':q23,'24':q24}
    return rList
    # cv2.imshow("pic1",pic1)
    # cv2.waitKey(0)



runCode()