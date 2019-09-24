from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os, random
from matplotlib import pyplot as plt
import time

tpath="./tempDir/"
SHADEVAL=400
gFac=325
ANSLIST=['A','B','C','D','E','F']
ABCLIST=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def runner4():
    pathName=os.getcwd()+'/testgen2/9-22/psatDep/done/'
    dloc=os.listdir(pathName)
    xlist=[]
    count=0
    tlist=[]
    for x in dloc:
        hold=cv2.imread(pathName+x)
        gray=cv2.cvtColor(hold, cv2.COLOR_BGR2GRAY)
        xlist.append(gray)
        count+=1
        if count==9:
            tlist.append(xlist)
            xlist=[]
            count=0


    for y in tlist:
        ans3=surveyPage1(y[0])
        ans2=surveyPage2(y[1])
        ans1=surveyPage3(y[2])
        tout=testMaker2([y[3],y[4],y[5],y[6],y[7],y[8]])

        sout,bDate,tDate=surveyOut([ans1,ans2,ans3])
        firstName=ans1[0][1]
        lastName=ans1[1][1]
        testCode=ans2[8][1]

        b1=listToTestTXT(tout[0],2)
        b2=listToTestTXT(tout[1],2)
        b3=listToTestTXT(tout[2],2)
        b32=listToTestTXT(tout[3],2)
        b4=listToTestTXT(tout[4],2)
        b42=listToTestTXT(tout[5],2)

        l1=listToTestTXT(tout[0],1)
        l2=listToTestTXT(tout[1],1)
        l3=listToTestTXT(tout[2],1)
        l32=listToTestTXT(tout[3],1)
        l4=listToTestTXT(tout[4],1)
        l42=listToTestTXT(tout[5],1)

        fileObj2=open('./testDep2/{}_{}__{}__{}.txt'.format(firstName,lastName,tDate,bDate),'w')
        fileObj2.write("{}************************\n".format(sout))
        fileObj2.write(b1)
        fileObj2.write("*************************\n")
        fileObj2.write(b2)
        fileObj2.write("*************************\n")
        fileObj2.write(b3)
        fileObj2.write(b32)
        fileObj2.write("*************************\n")
        fileObj2.write(b4)
        fileObj2.write(b42)
        fileObj2.write("*************************\n")


        fileObj=open('./testDep2/t {}_{}__{}__{}.txt'.format(firstName,lastName,tDate,bDate),'w')
        
        # fileObj.write('{}\n\n\n'.format(sout))
        # fileObj.write(l1)
        # fileObj.write('\n\n\n\n\n\n\n\n\n\n\n\n')
        # fileObj.write(l2)
        # fileObj.write(l3)
        # fileObj.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        # fileObj.write(l4)

        fileObj.write("{}************************\n".format(sout))
        fileObj.write(l1)
        fileObj.write("*************************\n")
        fileObj.write(l2)
        fileObj.write("*************************\n")
        fileObj.write(l3)
        fileObj.write(l32)
        fileObj.write("*************************\n")
        fileObj.write(l4)
        fileObj.write(l42)
        fileObj.write("*************************\n")
       
def runner5(): #ACT
    #pathName=os.getcwd()+'/ACT/nicholas15/tdep/'
    pathName=os.getcwd()+'/testgen2/9-22/actDep/done/'
    dloc=os.listdir(pathName)
    xlist=[]
    count=0
    tlist=[]
    for x in dloc:
        hold=cv2.imread(pathName+x)
        gray=cv2.cvtColor(hold, cv2.COLOR_BGR2GRAY)
        xlist.append(gray)
        count+=1
        if count==7:
            tlist.append(xlist)
            xlist=[]
            count=0


    for y in tlist:
        ans3=surveyPage1(y[0])
        ans2=surveyPage2(y[1])
        ans1=surveyPage3(y[2])
        tout=testMaker([y[3],y[4],y[5],y[6]])

        sout,bDate,tDate=surveyOut([ans1,ans2,ans3])
        firstName=ans1[0][1]
        lastName=ans1[1][1]
        testCode=ans2[8][1]

        b1=listToTestTXT(tout[0],2)
        b2=listToTestTXT(tout[1],2)
        b3=listToTestTXT(tout[2],2)
        b4=listToTestTXT(tout[3],2)

        l1=listToTestTXT(tout[0],1)
        l2=listToTestTXT(tout[1],1)
        l3=listToTestTXT(tout[2],1)
        l4=listToTestTXT(tout[3],1)

        fileObj2=open('./testDep2/{}_{}__{}__{}.txt'.format(firstName,lastName,tDate,bDate),'w')
        fileObj2.write("{}************************\n".format(sout))
        fileObj2.write(b1)
        fileObj2.write("*************************\n")
        fileObj2.write(b2)
        fileObj2.write("*************************\n")
        fileObj2.write(b3)
        fileObj2.write("*************************\n")
        fileObj2.write(b4)
        fileObj2.write("*************************\n")


        fileObj=open('./testDep2/t {}_{}__{}__{}.txt'.format(firstName,lastName,tDate,bDate),'w')
        
        fileObj.write('{}\n\n\n'.format(sout))
        fileObj.write(l1)
        fileObj.write('\n\n\n\n\n\n\n\n\n\n\n\n')
        fileObj.write(l2)
        fileObj.write(l3)
        fileObj.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        fileObj.write(l4)

        
        

def runner3():
    pathName=os.getcwd()+'/PSAT/'
    actRep=os.listdir(pathName)
    prepedList=[]
    for x in actRep:
        p2=pathName+x+'/done/'
        print(p2)
        dLoc=os.listdir(p2)
        splitList=[]
        xlist=[]
        holder=0
        for y in dLoc:
            # xlist.append(y)
            xlist.append(p2+y)
            holder+=1
            if holder==9:
                # print(len(xlist))
                # print(xlist)
                #splitList.append(p2+xlist)
                splitList.append(xlist)
                
                xlist=[]
                holder=0
            
        # print(len(splitList))
        #print(len(dLoc))
        #print(dLoc)
        prepedList.append(splitList)
    # print(len(prepedList))
    # print(prepedList)
    psatRemake2(prepedList)
    
    #print(len(actRep))

def runner2():
    pathName=os.getcwd()+'/ACT/'
    actRep=os.listdir(pathName)
    prepedList=[]
    for x in actRep:
        p2=pathName+x+'/done/'
        print(p2)
        dLoc=os.listdir(p2)
        splitList=[]
        xlist=[]
        holder=0
        for y in dLoc:
            # xlist.append(y)
            xlist.append(p2+y)
            holder+=1
            if holder==7:
                # print(len(xlist))
                # print(xlist)
                #splitList.append(p2+xlist)
                splitList.append(xlist)
                
                xlist=[]
                holder=0
            
        # print(len(splitList))
        #print(len(dLoc))
        #print(dLoc)
        prepedList.append(splitList)
    # print(len(prepedList))
    # print(prepedList)
    actRemake(prepedList)
    #print(len(actRep))

def actRemake(picL):
    print(len(picL))
    outx=0
    for tbank in picL:
        print("::::::::::::::::::::::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::::::::::::::::::::::")
        print("Current directory:{} {}".format(len(tbank),outx))
        print("::::::::::::::::::::::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::::::::::::::::::::::")
        outx+=1
        yout=0
        for y in tbank:
            print(len(y))
            actlist=[]
            
            for tests in y:
                hold=cv2.imread(tests)
                gray=cv2.cvtColor(hold, cv2.COLOR_BGR2GRAY)    
                #cv2.imshow("test",gray)
                actlist.append(gray)
                # cv2.waitKey(0)
            print(len(actlist))
            print("???????????????????????????????????????????????????????")
            print("???????????????????????????????????????????????????????")
            print("{}".format(yout))
            print("???????????????????????????????????????????????????????")
            act2(actlist)
            print("???????????????????????????????????????????????????????")
            print("???????????????????????????????????????????????????????")
            yout+=1
            # actList.append()
            #print(y)
        # cv2.waitKey(0)

def act2(picL):

    sout=surveyProcess([picL[0],picL[1],picL[2]])
    tout=testMaker([picL[3],picL[4],picL[5],picL[6]])
    outputMaker(sout,tout)

def psatRemake2(picL):
    print(len(picL))
    outx=0
    for tbank in picL:
        print("::::::::::::::::::::::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::::::::::::::::::::::")
        print("Current directory:{} {}".format(len(tbank),outx))
        print("::::::::::::::::::::::::::::::::::::::::::::::")
        print("::::::::::::::::::::::::::::::::::::::::::::::")
        outx+=1
        yout=0
        for y in tbank:
            print(len(y))
            psatlist=[]
            for tests in y:
                hold=cv2.imread(tests)
                gray=cv2.cvtColor(hold, cv2.COLOR_BGR2GRAY)    
                #cv2.imshow("test",gray)
                psatlist.append(gray)
                # cv2.waitKey(0)
            print(len(psatlist))
            print("???????????????????????????????????????????????????????")
            print("???????????????????????????????????????????????????????")
            print("{}".format(yout))
            print("???????????????????????????????????????????????????????")
            psat2(psatlist)
            print("???????????????????????????????????????????????????????")
            print("???????????????????????????????????????????????????????")
            yout+=1
            # actList.append()
            #print(y)
        # cv2.waitKey(0)

def psat2(picL):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(len(picL))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    sout=surveyProcess([picL[0],picL[1],picL[2]])
    tout=testMaker2([picL[3],picL[4],picL[5],picL[6],picL[7],picL[8]])
    outputMaker(sout,tout)

def runner():
    start=time.time()
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
       
        
        print("im right here: ",y)
        if y==7:    #this number will change based on the tests
            
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
        # if y==0:

        #     y+=1
        #     continue
        # # if y==4 or y==5:    #So will these choices
        # #     print("yo")
        # #     pic=picfixmass(2,gray)
        # #     #print(len(pic))
        # #     # cv2.imshow("check 0",pic[0])
        # #     # cv2.imshow("check 1",pic[1])
        # #     #cv2.waitKey(0)
        # #     #print("PPPPPPPPPPPPPPPPP")


        # else:
        #     pic=picfixmass(1,gray)
        #     # testList.append(pic)
        #     # #print(len(pic))
        #     # cv2.imshow("check 0",pic)
        #     # cv2.waitKey(0)
            
            #print("PPPPPPPPPPPPPPPPP")
        if y==3 or y==4 or y==5 or y==6:
            if y==3 or y==4:
                pic=picfixmass(2,gray)
                print(len(pic))
                # cv2.imshow("check 0",pic[0])
                # cv2.imshow("check 1",pic[1])
                # cv2.waitKey(0)
                testList.append(pic[0])
                testList.append(pic[1])


            else:
                pic=picfixmass(1,gray)
                testList.append(pic)
            
            #print(len(pic))
            # cv2.imshow("check 0",pic)
            # cv2.waitKey(0)
        if y==0 or y==1 or y==2:    #this will remain the same for surveys but not tests
            pic=picfixmass(1,gray)
            surveyList.append(pic)
            
        if len(testList)==6 and len(surveyList)==3:
            surveyDep=surveyProcess(surveyList)
            #responseList=testMaker(testList) #for ACT

            responseList=testMaker2(testList) #for PSAT
            # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            # print(surveyDep)
            # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            # print(responseList)

            #********hold this for a moment *****I****
            #outputMaker(surveyDep,responseList)
            #********hold this for a moment *****I****

            surveyList=[]
            testList=[]

        y+=1
        
        #print(cv2.countNonZero(gray))
    end=time.time()
    print("Time Taken is {} sec".format(end-start))
    
def outputMaker(survey,rlist):
    # outputString=""
    # strName,strContent=survey[0][0]
    # outputString+=strContent+"\n"
    # strName,strContent=survey[0][1]
    # outputString+=strContent+"\n"
    # print(outputString)
    firstName=survey[0][0][1]
    lastName=survey[0][1][1]
    testCode=survey[1][8][1]
    # l2=listToTestTXT(rlist[0],1)
    # l3=listToTestTXT(rlist[1],1)
    # l1=listToTestTXT(rlist[2],1)
    # l4=listToTestTXT(rlist[3],1)
    # print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")

    # print(survey)
    # print("WWWWWWWWWWWWWWWWWWWWWWW")
    # print(survey[0])
    # print("WWWWWWWWWWWWWWWWWWWWWWW")
    # print(survey[1])
    # print("WWWWWWWWWWWWWWWWWWWWWWW")
    # print(survey[2])
    # print("WWWWWWWWWWWWWWWWWWWWWWW")
    # print(len(survey))
    # print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")

    # b1=listToTestTXT(rlist[0],2)
    # b2=listToTestTXT(rlist[1],2)
    # b3=listToTestTXT(rlist[2],2)
    # b4=listToTestTXT(rlist[3],2)

    b1=listToTestTXT(rlist[0],2)
    b2=listToTestTXT(rlist[1],2)
    b3=listToTestTXT(rlist[2],2)
    b32=listToTestTXT(rlist[3],2)
    b4=listToTestTXT(rlist[4],2)
    b42=listToTestTXT(rlist[5],2)


    sout,bDate,tDate=surveyOut(survey)
    fileObj=open('./testDep2/t {}_{}__{}__{}.txt'.format(firstName,lastName,tDate,bDate),'w')
    fileObj2=open('./testDep2/{}_{}__{}__{}.txt'.format(firstName,lastName,tDate,bDate),'w')
    
    # fileObj.write('{}\n\n\n'.format(sout))
    # fileObj.write(l1)
    # fileObj.write('\n\n\n\n\n\n\n\n\n\n\n\n')
    # fileObj.write(l2)
    # fileObj.write(l3)
    # fileObj.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    # fileObj.write(l4)



    fileObj2.write("{}************************\n".format(sout))
    fileObj2.write(b1)
    fileObj2.write("*************************\n")
    fileObj2.write(b2)
    fileObj2.write("*************************\n")
    fileObj2.write(b3)
    fileObj2.write(b32)
    fileObj2.write("*************************\n")
    fileObj2.write(b4)
    fileObj2.write(b42)
    fileObj2.write("*************************\n")
    
def surveyOut(slist):

    print("yo")
    pg1=slist[0]
    pg2=slist[1]
    pg3=slist[2]

    firstName=pg1[0][1]
    lastName=pg1[1][1]
    

    birthDate=dateVerify(pg2[0][1],pg2[1][1],pg2[2][1])
    testDate=dateVerify(pg2[3][1],pg2[4][1],pg2[5][1])
    gradYr=pg2[6][1]
    schoolCode=pg2[7][1]
    testCode=pg2[8][1]

    rlist="{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(firstName,lastName,birthDate,testDate,gradYr,schoolCode,testCode)
    
    squestions=pg1[2][1]
    squestions2=pg2[9][1]
    s1=surveyQtoText(squestions)
    s2=surveyQtoText(squestions2)
    rlist+=s1+s2
    s3=surveyQtoText(pg3)
    #s3='\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
    rlist+=s3
    # print("??????????????????????")
    # print(rlist)
    # print("??????????????????????")
    return rlist,birthDate,testDate

def surveyQtoText(slist):
    rStr=""
    for x in slist:
        rStr+="{} {}\n".format(x[0],x[1])
    return rStr

def dateVerify(month,day,year):
    if month==-1:
        return -1
    if day==-1:
        return -1
    if year ==-1:
        return -1
    else:
        return "{}-{}-{}".format(month,day,year)


def listToTestTXT(tlist,t):
    # print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    # print(len(tlist))
    outString=""
    if t==1:
        for x in tlist:
            if x[2]=='G':
                outString+='{}?\n'.format(x[1])
            else:
                outString+='{}\n'.format(x[1])
        # outString+='**********************************JKJKJKJKJKJ****************\n'
        return outString
    else:
        for x in tlist:
            outString+='{} {} {}\n'.format(x[0],x[1],x[2])
            
        # outString+='**********************************JKJKJKJKJKJ****************\n'
        return outString

def testMaker2(tlist):
    print(len(tlist)," KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    for x in range(0,len(tlist)):
        h,w=tlist[x].shape[:2]
        print("************sizes h:{} w:{}".format(h,w))
    print("JAKSASS")
    print(len(tlist))
    print(tlist)
    out1=SS_PSAT(tlist[5],48)
    out2=SS_PSAT(tlist[4],45)
    out31=SS_PSAT31(tlist[3],14)
    out32=SS_PSATFR(tlist[2],14,4)
    out41=SS_PSAT41(tlist[1],28)
    out42=SS_PSATFR(tlist[0],28,4)
    print(out1)
    print("\n")
    print(out2)
    print("\n")
    print(out31)
    print("\n")
    print(out32)
    print("\n")
    print(out41)
    print("\n")
    print(out42)

    print("We DONE")
    return [out1,out2,out31,out32,out41,out42]

def SS_PSAT(image,amt):
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
        thresh2 = thresh[int(h*0.025):h-int(h*.035),int(w*.09):w-int(w*.1)]
        #cv2.imshow("{}".format(x),thresh2)
        #cv2.waitKey(0)
        (h,w)=thresh2.shape[:2]
        y=int(h*.077)
        mlist=[]
        output=""
        count=0
        output2=""
        for t in range(0,13):
            count2+=1
            if count2<amt:
                joke.append(calcAns(x,y,t,thresh2,count2,w,0))
        cv2.waitKey(0)
    print(joke)
    print("*************************************")
    return joke
    #cv2.waitKey(0)

def SS_PSAT31(image,amt):
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
        thresh2 = thresh[int(h*0.025):h-int(h*.035),int(w*.09):w-int(w*.1)]
        #cv2.imshow("{}".format(x),thresh2)
        (h,w)=thresh2.shape[:2]
        y=int(h*.25)
        mlist=[]
        output=""
        count=0
        output2=""
        for t in range(0,4):
            count2+=1
            if count2<amt:
                joke.append(calcAns(x,y,t,thresh2,count2,w,0))
        cv2.waitKey(0)
    print(joke)
    print("*************************************")
    return joke
    cv2.waitKey(0)

def SS_PSAT41(image,amt):
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
        thresh2 = thresh[int(h*0.025):h-int(h*.035),int(w*.09):w-int(w*.1)]
        #cv2.imshow("{}".format(x),thresh2)
        (h,w)=thresh2.shape[:2]
        y=int(h*.142857)
        mlist=[]
        output=""
        count=0
        output2=""
        for t in range(0,7):
            count2+=1
            if count2<amt:
                joke.append(calcAns(x,y,t,thresh2,count2,w,0))
        cv2.waitKey(0)
    print(joke)
    print("*************************************")
    return joke
    #cv2.waitKey(0)

def SS_PSATFR(image,num,times):
    helper=viewAdjust(image,5)
    joke=[]
    count2=0
    for d in range(0,times):
        temp=helper[d]
        #warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        # apply Otsu's thresholding method to binarize the warped piece of paper
        thresh = cv2.threshold(temp, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #cv2.imshow("testI ",thresh)
        (h,w)=thresh.shape[:2]
        thresh2 = thresh[int(h*.09):h-int(h*.04),0:w-int(w*.1)]
        #cv2.imshow("testII {}".format(x),thresh2)
        #cv2.waitKey(0)
        (h,w)=thresh2.shape[:2]
        thresh3=thresh2[int(h*.035):h-int(h*.915),int(w*.05):w-int(w*.79)]


        #allignment is off for PSAT FR
        #cv2.imshow("testguess {}".format(x),thresh3)
        #cv2.waitKey(0)
        val=cv2.countNonZero(thresh3)
        hold="NG"
        if val>gFac:
            hold="G"
        #print("{} {}".format(val,hold))
        #cv2.imshow("testIII {}".format(x),thresh3)

        pic = thresh2[int(h*.145):h,int(w*.29):w]
        (h,w)=pic.shape[:2]
        #cv2.imshow("testIV {}".format(x),thresh4)

        arr1=[]
        arr2=[]
        arr3=[]
        arr4=[]

        calc=int(h/12)

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
        output=[]
        if val1>gFac:
            output.append(arr1.index(val1))
        if val2>gFac:
            output.append(arr2.index(val2))
        if val3>gFac:
            output.append(arr3.index(val3))
        if val4>gFac:
            output.append(arr4.index(val4))

        mlist=[]
        
        count=0
        
        t=['-','-','-']
        t[1]=frCalc(output)
        t[0]=num+d
        t[2]=hold
        #cv2.waitKey(0)
        joke.append(t)
        print("*************************************")


    return joke

def frCalc(data):
    FRRep=['-','-','-','-']
    amt=4
    t1=''
    counter=0
    spos=False
    dotpos=False
    t2=''
    for x in range(len(data)):
        data[x]-=2
        if data[x] ==-2:
            data[x]='/'
            counter+=1
        if data[x]==-1:
            data[x]='.'
            counter+=1
            dotpos=True

    # for x in range(0,len(data)):
    #     hold=data[x]
    #     h1=hold[0]-2
    #     h2=hold[1]
    #     if h1 == -2:
    #         h1='/'
    #         counter+=1
    #     if h1 == -1:
    #         h1='.'
    #         counter+=1
    #         dotpos=True
    #     FRRep[h2]=h1
    #     #print("{} {}".format(h2,h1))
    
    # for x in range(0,len(FRRep)):
    #     if FRRep[3-x]=='-':
    #         del FRRep[3-x]
    #print(FRRep)
    ans=''
    FRRep=data


    if len(FRRep) == 0:
        return "Z"
    if counter > 1:
        return "Z"
    if FRRep[0] == '/':
        return "Z"
    # if FRRep[0] == '.':
    #     return "Z"
    if len(FRRep)==2 and FRRep[1] == '/':
        return "Z"
    if len(FRRep)==3 and FRRep[2] == '/':
        return "Z"
    if len(FRRep)==4 and FRRep[3] == '/':
        return "Z"
    if len(FRRep)==3 and FRRep[1] == '/':
        if FRRep[2]==0:
            return "Z"
        return FRRep[0] / FRRep[2]
    if len(FRRep)==4 and FRRep[1] == '/':
        return FRRep[0] / int(str(FRRep[2])+str(FRRep[3]))
    if len(FRRep)==4 and FRRep[2] == '/':
        if int(FRRep[3])==0:
            return "Z"
        return int(str(FRRep[0])+str(FRRep[1])) / int(FRRep[3])
    if dotpos == True:
        for x in range(0,len(FRRep)):
            ans+=str(FRRep[x])
        return float(ans)
    if counter == 0:
        for x in range(0,len(FRRep)):
            ans+=str(FRRep[x])
        return int(ans)
    return "Z"

def testMaker(tlist):

    print(len(tlist)," KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    for x in range(0,len(tlist)):
        h,w=tlist[x].shape[:2]
        print("************sizes h:{} w:{}".format(h,w))

    out1=SS_ACT(tlist[3],76)
    out2=SS_ACTMath(tlist[2],61)
    out3=SS_ACT(tlist[1],41)
    out4=SS_ACT(tlist[0],41)
    # print(out1)
    # print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    # print(out2)
    # print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    # print(out3)
    # print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    # print(out4)
    # print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    return [out1,out2,out3,out4]

def surveyProcess(doc):
    print(len(doc)," KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    for x in range(0,len(doc)):
        h,w=doc[x].shape[:2]
        print("************sizes h:{} w:{}".format(h,w))

    ans3=surveyPage1(doc[0])
    ans2=surveyPage2(doc[1])
    ans1=surveyPage3(doc[2])
    return [ans1,ans2,ans3]
    # cv2.waitKey(0)

def viewAdjust(pic,amt):
    hold=[]
    (h,w)=pic.shape[:2]
    val=int(w/amt)
    for x in range(0,amt):
        hold.append(pic[0:h,val*x:val*(x+1)])
    return hold

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
    return [["1.1",y1ans],["1.2",u1ans],["1.3",u2ans],["1.4",u3ans],
    ["2.1",y2ans],["2.2",u4ans],["2.3",u5ans],["2.4",u6ans],
    ["3.1",y3ans],["3.2",d1ans],["3.3",d2ans],["3.4",d3ans],
    ["4.1",y4ans],["4.2",d4ans],["4.3",d5ans],["4.4",d6ans]]

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
    print("Survey Questions List {}".format(qList))
    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")

    # cv2.imshow("surveyPage2top",gray1)
    # cv2.imwrite("surveyPage2top.jpg",gray1)
    # cv2.imshow("surveyPage2bottom",gray2)
    # cv2.imwrite("surveyPage2bottom.jpg",gray2)
    # cv2.waitKey(0)
    return [["Birthday Month",bmon],["Birthday Day",bday],["Birthday Year",byear],
    ["Date Month",dmon],["Date Day",dday],["Date Year",dyear],
    ["Grad Yr",gyr],["School Code",scCode],["Test Code",tcCode],
    ["Survey Questions List", qList]]

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
    print("first Name")
    firstName=nameBuilder(rg)
    print("LAst Name")
    lastName=nameBuilder(lg)
    print("Student Name {} {}".format(firstName,lastName))
    print("Student QList: {}".format(qList))
    #print(qList)
    #cv2.waitKey(0)

    return [["First Name",firstName],["Last Name",lastName],["Student QList",qList]]

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

    rList=[[1,q1],[2,q2],[3,q3],[4,q4],[5,q5],[6,q6],[7,q7],[8,q8],[9,q9],[10,q10],[11,q11],[12,q12]]
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


    rList=[[13,q13],[14,q14],[15,q15],[16,q16],[17,q17],[18,q18],[19,q19],[20,q20],[21,q21],[22,q22],[23,q23],[24,q24]]
    return rList
    # cv2.imshow("pic1",pic1)
    # cv2.waitKey(0)
   
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

    for x in range(0,len(docstore2)):

        tt=four_point_transform(gray, docstore2[x].reshape(4, 2))
        cv2.imshow("check {}, length{}".format(x,len(docstore2)),tt)
    cv2.waitKey(0)

    if (len(docstore2)==4 and num==2):
        print("FUCK YOU")
        retStore=[]
        retStore.append(four_point_transform(gray, docstore2[0].reshape(4, 2)))
        retStore.append(four_point_transform(gray, docstore2[1].reshape(4, 2)))
        return retStore
    if (len(docstore2)==1 and num==1):
        print("FUCK YOU 2")
        return four_point_transform(gray, docstore2[0].reshape(4, 2))
        #four_point_transform(gray, docstore2[0].reshape(4, 2))

    print("FUCK YOU 3")


    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper
    #paper = four_point_transform(image, docCnt.reshape(4, 2))
    #warped = four_point_transform(gray, docstore2[0].reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))

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

#runner()
start=time.time()
#runner2()
#runner3()
#runner4()
runner5()
end=time.time()
print("Time Taken is {} sec".format(end-start))