from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os
from matplotlib import pyplot as plt
import time,json

tempDir="./tempDir/"

SHADEVAL=400
gFac=325
pathName="./dep_folder/"
ANSLIST=['A','B','C','D','E','F']
ABCLIST=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


calcSIZEZACT={0: [0.52, 0.56],
 1: [0.52, 0.56],
 2: [0.52, 0.56],
 3: [0.52, 0.56],
 4: [0.62, 0.67],
 5: [0.62, 0.67],
 6: [0.62, 0.67]}

# original sizes SAT
# calcSIZEZSAT={0: [0.3764839572192513, 0.37796657754010693],
#  1: [0.37620320855614975, 0.37796657754010693],
#  2: [0.1292457219251337, 0.12943877005347593],
#  3: [0.2818251336898396, 0.28296363636363636],
#  4: [0.3764058823529412, 0.3774823529411765], 
#  5: [0.26086470588235294, 0.2610590909090909], 
#  6: [0.27106844919786094, 0.2716748663101604], 
#  7: [0.6497037433155081, 0.6513909090909091], 
#  8: [0.6504208556149733, 0.651875935828877], 
#  9: [0.6490927807486631, 0.651264705882353]}


calcSIZEZSAT={0: [0.37, 0.382],
 1: [0.37, 0.382],
 2: [0.125, 0.131],
 3: [0.279, 0.289],
 4: [0.37, 0.382], 
 5: [0.258, 0.269], 
 6: [0.269, 0.279], 
 7: [0.64, 0.659], 
 8: [0.645, 0.659], 
 9: [0.64, 0.659]}

# Original Data PSAT
# 0: [0.36521764705882354, 0.37110802139037435]
# 1: [0.3690053475935829, 0.3708294117647059]
# 2: [0.12588770053475937, 0.12705]
# 3: [0.27394385026737966, 0.27844652406417114]
# 4: [0.2000673796791444, 0.2041229946524064]
# 5: [0.2762524064171123, 0.2780909090909091]
# 6: [0.6370139037433155, 0.6396449197860963]
# 7: [0.6374935828877005, 0.6402323529411764]
# 8: [0.6361794117647059, 0.6398764705882353]

calcSIZEZPSAT={0: [0.355, 0.375],
1: [0.36, 0.375],
2: [0.115, 0.132],
3: [0.265, 0.283],
4: [0.195, 0.23],
5: [0.27, 0.28],
6: [0.63, 0.641],
7: [0.63, 0.641],
8: [0.63, 0.641]}

def tmain(txtFile,pdfUsed):
    tList=readTXT(txtFile)
    picList=parseinput(pdfUsed)
    parsePDF(tList,picList)
    

def parsePDF(txtFile,pdfList):
    PSAT=[]
    SAT=[]
    ACT=[]
    count=0
    psatcount=0
    satcount=0
    actcount=0
    errorList=[]
    for x in txtFile:
        print("HERE")
        if x[0] == 'ACT':
            count2=0
            for y in range(x[1]):
                ACT.append([])
                
                for z in range(7):
                    ACT[y].append(pdfList[count])
                    count+=1
                print("current list length ACT", len(ACT[y]))
                print("ACT COUNT ",count)
                ACT[y]=ACTProcess(ACT[y])
                for z in range(len(ACT[y])):
                    if calcSIZEZACT[z][0]<= ACT[y][z][1]<=calcSIZEZACT[z][1]:
                        ACT[y][z].append("T")
    
                    else:
                        ACT[y][z].append("F")
                        errorList.append(["ACT",actcount,z])
                    cv2.imwrite("./dep_folder/ACT/{}_{}.jpg".format(actcount,z),ACT[y][z][0])
                # currently here for code, making the jsons
                ACT[y]=ACTJSONMaker(ACT[y],actcount)

                actcount+=1
                
        elif x[0] == 'SAT':
            count2=0
            for y in range(x[1]):
                SAT.append([])
                
                for z in range(8):
                    SAT[y].append(pdfList[count])
                    count+=1

                SAT[y]=SATProcess(SAT[y])
                for z in range(len(SAT[y])):
                    if calcSIZEZSAT[z][0]<= SAT[y][z][1]<=calcSIZEZSAT[z][1]:
                        SAT[y][z].append("T")
                        
                    else:
                        SAT[y][z].append("F")
                        errorList.append(["SAT",satcount,z])
                    cv2.imwrite("./dep_folder/SAT/{}_{}.jpg".format(satcount,z),SAT[y][z][0])
                SAT[y]=SATJSONMaker(SAT[y],satcount)
                satcount+=1

        elif x[0] == 'PSAT':
            count2=0
            for y in range(x[1]):
                PSAT.append([])
                
                for z in range(7):
                    PSAT[y].append(pdfList[count])
                    count+=1
                PSAT[y]=PSATProcess(PSAT[y])
                for z in range(len(PSAT[y])):
                    if calcSIZEZPSAT[z][0]<= PSAT[y][z][1]<=calcSIZEZPSAT[z][1]:
                        PSAT[y][z].append("T")
                        
                    else:
                        PSAT[y][z].append("F")
                        errorList.append(["PSAT",psatcount,z,PSAT[y][z][1]])
                    cv2.imwrite("./dep_folder/PSAT/{}_{}.jpg".format(psatcount,z),PSAT[y][z][0])
                PSAT[y]=PSATJSONMaker(PSAT[y],psatcount)
                psatcount+=1
                    
    # print("PSAT LEN",len(PSAT))
    # print("SAT LEN",len(SAT[0]))
    # print("ACT LEN",len(ACT[0]))
    print("****************************************************")
    print(errorList)
    print(len(errorList))

def ACTJSONMaker(tlist, tc):
    x=[]
    outputDict={}
    x.append(transform_info(SS_ACT(tlist[0][0],76,tlist[0][2])))
    x.append(transform_info(SS_ACTMath(tlist[1][0],61,tlist[1][2])))
    x.append(transform_info(SS_ACT(tlist[2][0],41,tlist[2][2])))
    x.append(transform_info(SS_ACT(tlist[3][0],41,tlist[3][0],)))
    x.append(surveyPage3(tlist[4][0],tlist[4][2]))
    x.append(surveyPage2(tlist[5][0],tlist[5][2]))
    x.append(surveyPage1(tlist[6][0],tlist[6][2]))

    outputDict['first_Name'] = x[4]['First Name']
    outputDict['last_Name'] = x[4]['Last Name']
    outputDict['DOB'] = str(x[5]['Birthday Month'])+'/'+str(x[5]['Birthday Day'])+'/'+str(x[5]['Birthday Year'])
    outputDict['test_date'] = str(x[5]['Date Month'])+'/'+str(x[5]['Date Day'])+'/'+str(x[5]['Date Year'])
    outputDict['grad_yr'] = ""
    outputDict['school_code'] = x[5]['School Code']
    outputDict['test_code'] = x[5]['Test Code']
    outputDict['survey'] =x[4]['Student QList']
        
    outputDict['survey_cont'] =x[5]['Survey Questions List']
    
    outputDict['Timing'] = x[6]
    outputDict['Reading'] = x[2]
    outputDict['English'] = x[0]
    outputDict['Math'] = x[1]
    outputDict['Science'] = x[3]

    with open('dep_folder/testJSONS/dataACT_{}.txt'.format(tc), 'w') as outfile:
        json.dump(outputDict, outfile)

    return outputDict


def SATJSONMaker(tlist, tc):
    x=[]
    outputDict={}
    x.append(transform_info(SS_PSAT(tlist[0][0],53,tlist[0][2])))
    x.append(transform_info(SS_PSAT(tlist[1][0],45,tlist[1][2])))
    x.append(transform_info(SS_PSAT31(tlist[2][0],16,tlist[2][2])))
    x.append(transform_info(SS_PSATFR(tlist[3][0],16,5,tlist[3][2])))
    x.append(transform_info(SS_PSAT(tlist[4][0],31,tlist[4][2])))


    
    x.append(transform_info(SS_PSATFR(tlist[6][0],31,5,tlist[5][2])))
    x.append(transform_info(SS_PSATFR(tlist[5][0],36,3,tlist[6][2])))

    x.append(surveyPage3(tlist[7][0],tlist[7][2]))
    x.append(surveyPage2(tlist[8][0],tlist[8][2]))
    x.append(surveyPage1(tlist[9][0],tlist[9][2]))

    outputDict['first_Name'] = x[7]['First Name']
    outputDict['last_Name'] = x[7]['Last Name']
    outputDict['DOB'] = str(x[8]['Birthday Month'])+'/'+str(x[8]['Birthday Day'])+'/'+str(x[8]['Birthday Year'])
    outputDict['test_date'] = str(x[8]['Date Month'])+'/'+str(x[8]['Date Day'])+'/'+str(x[8]['Date Year'])
    outputDict['grad_yr'] = x[8]['Grad Yr']
    outputDict['school_code'] = x[8]['School Code']
    outputDict['test_code'] = x[8]['Test Code']
    outputDict['survey'] =x[7]['Student QList']
        
    outputDict['survey_cont'] =x[8]['Survey Questions List']
    
    
    outputDict['Timing'] = x[9]
    outputDict['Reading'] = x[0]
    outputDict['English'] = x[1]
    outputDict['Math1'] = x[2]
    outputDict['Math2'] = x[3]
    outputDict['Math3'] = x[4]
    outputDict['Math4'] = x[5]
    outputDict['Math5'] = x[6]

    with open('dep_folder/testJSONS/dataSAT_{}.txt'.format(tc), 'w') as outfile:
        json.dump(outputDict, outfile)

    return outputDict

def PSATJSONMaker(tlist, tc):
    x=[]
    outputDict={}
    x.append(transform_info(SS_PSAT(tlist[0][0],53,tlist[0][2])))
    x.append(transform_info(SS_PSAT(tlist[1][0],45,tlist[1][2])))
    x.append(transform_info(SS_PSAT31(tlist[2][0],14,tlist[2][2])))
    x.append(transform_info(SS_PSATFR(tlist[3][0],14,4,tlist[3][2])))
    x.append(transform_info(SS_PSAT41(tlist[4][0],28,tlist[4][2])))
    x.append(transform_info(SS_PSATFR(tlist[5][0],28,4,tlist[5][2])))

    x.append(surveyPage3(tlist[6][0],tlist[6][2]))
    x.append(surveyPage2(tlist[7][0],tlist[7][2]))
    x.append(surveyPage1(tlist[8][0],tlist[8][2]))

    outputDict['first_Name'] = x[6]['First Name']
    outputDict['last_Name'] = x[6]['Last Name']
    outputDict['DOB'] = str(x[7]['Birthday Month'])+'/'+str(x[7]['Birthday Day'])+'/'+str(x[7]['Birthday Year'])
    outputDict['test_date'] = str(x[7]['Date Month'])+'/'+str(x[7]['Date Day'])+'/'+str(x[7]['Date Year'])
    outputDict['grad_yr'] = x[7]['Grad Yr']
    outputDict['school_code'] = x[7]['School Code']
    outputDict['test_code'] = x[7]['Test Code']
    outputDict['survey'] =x[6]['Student QList']
        
    outputDict['survey_cont'] =x[7]['Survey Questions List']
    
    
    outputDict['Timing'] = x[8]
    outputDict['Reading'] = x[0]
    outputDict['English'] = x[1]
    outputDict['Math1'] = x[2]
    outputDict['Math2'] = x[3]
    outputDict['Math3'] = x[4]
    outputDict['Math4'] = x[5]

    with open('dep_folder/testJSONS/dataPSAT_{}.txt'.format(tc), 'w') as outfile:
        json.dump(outputDict, outfile)

    return outputDict

def ACTProcess(tlist):
    outList=[]
    for x in range(len(tlist)):
        # print("picfixmass args 1 and 3rd ",1,x)
        try:
            outList.append(picfixmassACT(1,tlist[x],x))
        except:
            outList.append([tlist[x],1])
            print("::::::::::::::::::::::::::::::::::::::::")
            print("::::::::::::::::::::::::::::::::::::::::")
            print(x)
            print("::::::::::::::::::::::::::::::::::::::::")
            print("::::::::::::::::::::::::::::::::::::::::")
    print(len(outList))
    return outList

def SATProcess(tlist):
    outList=[]
    for x in range(len(tlist)):
        if x ==2 or x==4:
            try:
                pic=picfixmassSAT(2,tlist[x],x)
                outList.append(pic[0])
                outList.append(pic[1])
            except:
                outList.append([tlist[x],1])
                outList.append([tlist[x],1])
                print("::::::::::::::::::::::::::::::::::::::::")
                print("::::::::::::::::::::::::::::::::::::::::")
                print(x)
                print("::::::::::::::::::::::::::::::::::::::::")
                print("::::::::::::::::::::::::::::::::::::::::")
            
        else:
            try:
                outList.append(picfixmassSAT(1,tlist[x],x))
            except:
                outList.append([tlist[x],1])
                print("::::::::::::::::::::::::::::::::::::::::")
                print("::::::::::::::::::::::::::::::::::::::::")
                print(x)
                print("::::::::::::::::::::::::::::::::::::::::")
                print("::::::::::::::::::::::::::::::::::::::::")
    print(len(outList))
    return outList

def PSATProcess(tlist):
    outList=[]
    for x in range(len(tlist)):
        if x ==2 or x==3:
            try:
                pic=picfixmassPSAT(2,tlist[x],x)
                outList.append(pic[0])
                outList.append(pic[1])
            except:
                outList.append([tlist[x],1])
                outList.append([tlist[x],1])
                print("::::::::::::::::::::::::::::::::::::::::")
                print("::::::::::::::::::::::::::::::::::::::::")
                print(x)
                print("::::::::::::::::::::::::::::::::::::::::")
                print("::::::::::::::::::::::::::::::::::::::::")
            
        else:
            try:
                outList.append(picfixmassPSAT(1,tlist[x],x))
            except:
                outList.append([tlist[x],1])
                print("::::::::::::::::::::::::::::::::::::::::")
                print("::::::::::::::::::::::::::::::::::::::::")
                print(x)
                print("::::::::::::::::::::::::::::::::::::::::")
                print("::::::::::::::::::::::::::::::::::::::::")
    print(len(outList))
    return outList

#ACT CODE
def transform_info(qlist):
    dictHelp={}
    for x in qlist:
        dictHelp[x[0]] = [x[1],x[2]]
    return dictHelp
# 0 is 75
# 1 is 60
# 2 is 40
# 3 is 40
# 4 is namePG #surveypage3
# 5 is school codes #surveypage2
# 6 is times #surveypage1


def frCalc(data):
    FRRep=['-','-','-','-']
    amt=4
    t1=''
    counter=0
    spos=False
    dotpos=False
    t2=''
    for x in range(0,len(data)):
        hold=data[x]
        h1=hold[0]-2
        h2=hold[1]
        if h1 == -2:
            h1='/'
            counter+=1
        if h1 == -1:
            h1='.'
            counter+=1
            dotpos=True
        FRRep[h2]=h1
        #print("{} {}".format(h2,h1))
    ans=''
    for x in range(0,len(FRRep)):
        if FRRep[3-x]=='-':
            del FRRep[3-x]
    #print(FRRep)
    if len(FRRep) == 0:
        return "INV"
    if counter > 1:
        return "INV"
    if FRRep[0] == '/':
        return "INV"
    if FRRep[0] == '.':
        return "INV"
    if len(FRRep)==2 and FRRep[1] == '/':
        return "INV"
    if len(FRRep)==3 and FRRep[2] == '/':
        return "INV"
    if len(FRRep)==4 and FRRep[3] == '/':
        return "INV"
    if len(FRRep)==3 and FRRep[1] == '/':
        return FRRep[0] / FRRep[2]
    if len(FRRep)==4 and FRRep[1] == '/':
        return FRRep[0] / int(str(FRRep[2])+str(FRRep[3]))
    if len(FRRep)==4 and FRRep[2] == '/':
        return int(str(FRRep[0])+str(FRRep[1])) / int(FRRep[3])
    if dotpos == True:
        for x in range(0,len(FRRep)):
            ans+=str(FRRep[x])
        return float(ans)
    if counter == 0:
        for x in range(0,len(FRRep)):
            ans+=str(FRRep[x])
        return int(ans)
    return "INV"

def SS_PSAT(image,amt,tval):

    if tval=="F":
        anslist=[]
        for x in range(amt):
            anslist.append([x,'Z','NG'])
        return anslist

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

def SS_PSAT31(image,amt,tval):

    if tval=="F":
        anslist=[]
        for x in range(amt):
            anslist.append([x,'Z','NG'])
        return anslist

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

def SS_PSAT41(image,amt,tval):

    if tval=="F":
        anslist=[]
        for x in range(amt):
            anslist.append([x,'Z','NG'])
        return anslist


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

def SS_PSATFR(image,num,times,tval):

    if tval=="F":
        anslist=[]
        for x in range(times):
            anslist.append([x+num,'Z','NG'])
        return anslist


    helper=viewAdjust(image,5)
    joke=[]
    count2=0
    for x in range(0,times):
        temp=helper[x]
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
        thresh4 = thresh2[int(h*.145):h,int(w*.29):w]
        (h,w)=thresh4.shape[:2]
        #cv2.imshow("testIV {}".format(x),thresh4)
        y=int(h*.084)
        mlist=[]
        output=[]
        count=0
        for t in range(0,12):
            q=thresh4[y*t:y*(t+1),0:w]
            #if t==1 or t==0:
            #cv2.imshow("{} t{}".format(x,t),q)
            (length,wid)=q.shape[:2]
            amt=int(wid/4)
            k0=q[0:length,0:amt]
            k1=q[0:length,amt:amt*2]
            k2=q[0:length,amt*2:amt*3]
            k3=q[0:length,amt*3:amt*4]
            mlist.append(cv2.countNonZero(k0))
            mlist.append(cv2.countNonZero(k1))
            mlist.append(cv2.countNonZero(k2))
            mlist.append(cv2.countNonZero(k3))
            #cv2.imshow("{} t{} a".format(x,t),k0)
            #cv2.imshow("{} t{} b".format(x,t),k1)
            #cv2.imshow("{} t{} c".format(x,t),k2)
            #cv2.imshow("{} t{} d".format(x,t),k3)
            mnum=max(mlist)
            if mlist[0]>gFac:
                output.append([t,0])
            if mlist[1]>gFac:
                output.append([t,1])
            if mlist[2]>gFac:
                output.append([t,2])
            if mlist[3]>gFac:
                output.append([t,3])
            print("{} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],output,mnum,len(output)))
            count=0
            mlist=[]
        t=['-','-','-']
        t[1]=frCalc(output)
        t[0]=num+x
        t[2]=hold
        cv2.waitKey(0)
        joke.append(t)
        print("*************************************")
    return joke

def SS_ACT(image,amt,tval):

    if tval=="F":
        anslist=[]
        for x in range(amt):
            anslist.append([x,'Z','NG'])
        return anslist


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

def SS_ACTMath(image,amt,tval):

    if tval=="F":
        anslist=[]
        for x in range(amt):
            anslist.append([x,'Z','NG'])
        return anslist

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

def surveyPage1(doc,val):

    if val =="F":
        return {1.1:'',1.2:'',1.3:'',1.4:'',2.1:'',
        2.2:'',2.3:'',2.4:'',3.1:'',
        3.2:'',3.3:'',3.4:'',4.1:'',4.2:'',
        4.3:'',4.4:''}



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
    return {1.1:y1ans,1.2:u1ans,1.3:u2ans,1.4:u3ans,2.1:y2ans,
    2.2:u4ans,2.3:u5ans,2.4:u6ans,3.1:y3ans,
    3.2:d1ans,3.3:d2ans,3.4:d3ans,4.1:y4ans,4.2:d4ans,
    4.3:d5ans,4.4:d6ans}

def surveyPage2(doc, val):

    if val == "F":
        return {'Birthday Month':'','Birthday Day':'','Birthday Year':'',
            'Date Month':'','Date Day':'','Date Year':'',
            'Grad Yr':'','School Code':'','Test Code':'',
            'Survey Questions List':''}
    
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

    dday=ttResponse(dayDate)
    dmon=ttResponse(monDate)
    dyear=fTResponse(yrDate)
    scCode=fTResponse(schoolCode)
    tcCode=threeResp(testCode)
    
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

def surveyPage3(doc,val):

    if val =="F":
        return {'First Name':'','Last Name':'','Student QList':''}

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

def picfixmassACT(num,gray,pos):
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
    # print(num)
    avg=[]
    for x in range(0,len(docstore2)):
        if x ==2:
            break
        tt=four_point_transform(gray, docstore2[x].reshape(4, 2))
        (hNew,wNew)=tt.shape[:2]
        avg.append((hNew*wNew)/aORG)

        # cv2.imshow("check {}, length{}".format(x,len(docstore2)),tt)
    # print("Pick the Best one ",len(avg))
    # cv2.waitKey(0)


    if calcSIZEZACT[pos][0]<= avg[0] <= calcSIZEZACT[pos][1]:
        # print("1 HIT 1")
        return [four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]]
    else:
        # print("2 HIT 2")
        warped = four_point_transform(gray, docstore2[0].reshape(4, 2))
        return picfixSmallACT(num,warped,pos,aORG,gray)

def picfixSmallACT(num,warped,pos,aORG,grayORG):
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
        if calcSIZEZACT[pos][0]<= avg <= calcSIZEZACT[pos][1]:
            return [paper,avg]
        else:
            return [grayORG,avg]

def picfixmassPSAT(num,gray,pos):
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
        return picfixSmallPSAT(num,warped,pos,aORG,gray)
        
    elif num ==2:
        if pos == 2:
            areaStore=[]
            # 2: [0.12, 0.13],
            # 3: [0.27, 0.28],

            if calcSIZEZPSAT[2][0] <= avg[1] <= calcSIZEZPSAT[2][1]:
                areaStore.append([four_point_transform(gray, docstore2[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZPSAT[3][0] <= avg[0] <= calcSIZEZPSAT[3][1]:
                areaStore.append([four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore
        if pos == 3:
            areaStore=[]
            # 4: [0.198, 0.23],
            # 5: [0.27, 0.28],

            if calcSIZEZPSAT[4][0] <= avg[1] <= calcSIZEZPSAT[4][1]:
                areaStore.append([four_point_transform(gray, docstore2[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZPSAT[5][0] <= avg[0] <= calcSIZEZPSAT[5][1]:
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
        if calcSIZEZPSAT[pos][0]<= avg[0] <= calcSIZEZPSAT[pos][1]:
            return [four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]]
        else:
            warped = four_point_transform(gray, docstore2[0].reshape(4, 2))
            return picfixSmallPSAT(num,warped,pos,aORG,gray)

def picfixSmallPSAT(num,warped,pos,aORG,grayORG):
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
        if calcSIZEZPSAT[pos][0]<= avg <= calcSIZEZPSAT[pos][1]:
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

            if calcSIZEZPSAT[2][0] <= avg[1] <= calcSIZEZPSAT[2][1]:
                areaStore.append([four_point_transform(gray2, docstore[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZPSAT[3][0] <= avg[0] <= calcSIZEZPSAT[3][1]:
                areaStore.append([four_point_transform(gray2, docstore[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore
        if pos == 3:
            areaStore=[]
            # 4: [0.198, 0.23],
            # 5: [0.27, 0.28],

            if calcSIZEZPSAT[4][0] <= avg[1] <= calcSIZEZPSAT[4][1]:
                areaStore.append([four_point_transform(gray2, docstore[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZPSAT[5][0] <= avg[0] <= calcSIZEZPSAT[5][1]:
                areaStore.append([four_point_transform(gray2, docstore[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore

def picfixmassSAT(num,gray,pos):
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
    # print(num)
    avg=[]
    for x in range(0,len(docstore2)):
        if x ==2:
            break
        tt=four_point_transform(gray, docstore2[x].reshape(4, 2))
        (hNew,wNew)=tt.shape[:2]
        avg.append((hNew*wNew)/aORG)

        # cv2.imshow("check {}, length{}".format(x,len(docstore2)),tt)
    # print("Pick the Best one")
    # cv2.waitKey(0)


    if num==2 and len(docstore2)==1:
        warped = four_point_transform(gray, docstore2[0].reshape(4, 2))
        return picfixSmallSAT(num,warped,pos,aORG,gray)
        
    elif num ==2:
        if pos == 2:
            areaStore=[]
            #  2: [0.125, 0.131],
            #  3: [0.279, 0.289],

            if calcSIZEZ[2][0] <= avg[1] <= calcSIZEZ[2][1]:
                areaStore.append([four_point_transform(gray, docstore2[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZ[3][0] <= avg[0] <= calcSIZEZ[3][1]:
                areaStore.append([four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore
        if pos == 4:
            areaStore=[]
            #5: [0.258, 0.269],
            #6: [0.269, 0.279],

            if calcSIZEZ[5][0] <= avg[1] <= calcSIZEZ[5][1]:
                areaStore.append([four_point_transform(gray, docstore2[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZ[6][0] <= avg[0] <= calcSIZEZ[6][1]:
                areaStore.append([four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore
    else:
        if pos !=0 and pos != 1 and pos!=3:
            pos= pos+2
        if pos==3:
            pos+=1
        if calcSIZEZSAT[pos][0]<= avg[0] <= calcSIZEZSAT[pos][1]:
            return [four_point_transform(gray, docstore2[0].reshape(4, 2)),avg[0]]
        else:
            warped = four_point_transform(gray, docstore2[0].reshape(4, 2))
            return picfixSmallSAT(num,warped,pos,aORG,gray)

def picfixSmallSAT(num,warped,pos,aORG,grayORG):
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
        # print("pos right herer",pos)
        paper= four_point_transform(gray2, docCnt.reshape(4, 2))
        (h4,w4)=paper.shape[:2]
        avg=((h4*w4)/aORG)
        if calcSIZEZSAT[pos][0]<= avg <= calcSIZEZSAT[pos][1]:
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
            #  2: [0.125, 0.131],
            #  3: [0.279, 0.289],,

            if calcSIZEZSAT[2][0] <= avg[1] <= calcSIZEZSAT[2][1]:
                areaStore.append([four_point_transform(gray2, docstore[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZSAT[3][0] <= avg[0] <= calcSIZEZSAT[3][1]:
                areaStore.append([four_point_transform(gray2, docstore[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore
        if pos == 4:
            areaStore=[]
            #5: [0.258, 0.269],
            #6: [0.269, 0.279],

            if calcSIZEZSAT[5][0] <= avg[1] <= calcSIZEZSAT[5][1]:
                areaStore.append([four_point_transform(gray2, docstore[1].reshape(4, 2)),avg[1]])
            else:
                areaStore.append([gray,avg[1]])

            if calcSIZEZSAT[6][0] <= avg[0] <= calcSIZEZSAT[6][1]:
                areaStore.append([four_point_transform(gray2, docstore[0].reshape(4, 2)),avg[0]])
            else:
                areaStore.append([gray,avg[0]])
            return areaStore

def readTXT(txtFile):
    fileObj = open(txtFile,"r")
    tests=[]
    count=0
    for line in fileObj:
        line=line.strip()
        line=line.split()
        line[1]=int(line[1])
        tests.append(line)
        print(line)
        if line[0] == "ACT":
            count+=(7*line[1])
        if line[0] == "PSAT":
            count+=(7*line[1])
        if line[0] == "SAT":
            count+=(8*line[1])
    print("Pages of tests to be parsed ",count)
    print("****************************************************")
    return tests

def parseinput(nameIn):
    inputpdf=PdfFileReader(open("{}".format(nameIn), "rb"))
    print("Original document size: ",inputpdf.numPages)
    pglist=[]
    for i in range(inputpdf.numPages):
        output=PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        # pglist.append(i)
        fileName="{}{}.pdf".format(tempDir,i)
        with open(fileName,"wb") as outstream:
            output.write(outstream)
        temp=convert_from_path(fileName)
        temp[0].save(fileName,"JPEG")
        temp=cv2.imread(fileName)
        temp=cv2.cvtColor(temp,cv2.COLOR_BGR2GRAY)
        pixelCount=np.sum(temp==255)
        if pixelCount <3200000:
            pglist.append(temp)

    print("Pages after removing blanks ",len(pglist))
    print("****************************************************")
    return pglist

tmain(sys.argv[1],sys.argv[2])
# readTXT(sys.argv[1])