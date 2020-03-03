"""from pdf2image import convert_from_path
pages = convert_from_path('pdf_file', 500)

for page in pages:
    page.save('out.jpg', 'JPEG')
"""

from pdf2image import convert_from_path
import cv2
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import sys

gFac=350
#import SSOMR
#"""

#
#second parameter is for type of output
#0 is for me while 1 is for entering into 
#spreadsheets


#img = convert_from_path('images/test82618.pdf')
#img = convert_from_path('images/test9218.pdf')
#img = convert_from_path('images/test9918.pdf')
#img = convert_from_path('images/test91618.pdf')
#img = convert_from_path('images/test92318.pdf')
#img = convert_from_path('images/test93018.pdf')
#img = convert_from_path('images/test10718.pdf')
#img = convert_from_path('images/test102118.pdf')
#img = convert_from_path('images/test11418.pdf')
img = convert_from_path('images/test12918.pdf')
# dont use # simg = convert_from_path('images/testtoday.pdf')
print(len(img))
"""
for x in range(0,len(img)):

    img[x].save('outchecks{}.jpg'.format(x), 'JPEG')
    print(x)

#"""
def readIntest(idname):
    fileobj=open(str(sys.argv[1]),'r')
    idamt=fileobj.readline().strip()
    idlist=[]
    for  x in range(0, int(idamt)):
        idlist.append(fileobj.readline().split())
        print(idlist[x][0])
        print(idlist[x][1])
    return idlist

def setpicloc(tlist,img,typ):
    print("kool {}".format(len(tlist)))
    current=0
    testout=[]
    che=int(typ)
    for x in range(0,len(tlist)):
        pichold=[]
        fixedlist=[]
        loc='sstest/{}'.format(tlist[x][0])
        tspec=int(tlist[x][1])
        if tspec ==1:
            tsize=4
        elif tspec ==2:
            tsize=4
        elif tspec==3:
            tsize=5
        for y in range(0,tsize):
            num=current+y
            print("current page {}".format(num))
            img[num].save('{}/pic{}.jpg'.format(loc,y), 'JPEG')
            pichold.append('{}/pic{}.jpg'.format(loc,y))
        current=current+tsize
        print("length before popop {}".format(len(pichold)))
        for y in range(0, len(pichold)):
            #cv2.imshow("shsh",pichold[y])
            #cv2.waitKey(0)
            print("OPOPOPOPOPOOPOPOPOPOPPPO")
            print(pichold[y])
            if (tspec==2 and (y==1 or y==0)) or (tspec==3 and (y==1 or y==0 or y==3)):
                fixedlist.append(picfixmass(1,pichold[y]))
            elif tspec==1:
                fixedlist.append(picfixmass(1,pichold[y]))
            elif (tspec==2 and(y==2 or y==3)) or (tspec==3 and(y==2 or y==4)):
                temp=picfixmass(2,pichold[y])
                fixedlist.append(temp[0])
                fixedlist.append(temp[1])
                temp=[]
        ###Currentyl here before tutoring session. if statemnets
        ###are not adding to fixedlist. check number assigned to 
        ###the test on ssids. I think tspec comes from it
        testout.append(testManage(fixedlist,tspec,loc,che))
        #print(pichold)
    return testout

def testManage(tlist,typeCode,loc,kind):
    print("fuck {}".format(len(tlist)))
    if typeCode==1:
        output=ACTOMR(tlist,loc,kind)
    elif typeCode==2:
        output=PSATOMR(tlist,loc,kind)
    else:
        output=SATOMR(tlist,loc,kind)
    return output

def getGuesses(answers):
    y=[]
    for x in range(0,len(answers)):
        hold = answers[x]
        if hold[2] == 'G':
            y.append([hold[0],hold[2]])
    return y

def viewAdjust(pic,amt):
    #cv2.imshow("kklklkllll",pic)
    #cv2.waitKey(0)
    hold=[]
    (h,w)=pic.shape[:2]
    val=int(w/amt)
    for x in range(0,amt):
        hold.append(pic[0:h,val*x:val*(x+1)])
    return hold

def ACTOMR(tlist,loc,kind):
    h1=SS_ACT(tlist[0],76)
    h2=SS_ACT2(tlist[1],61)
    h3=SS_ACT(tlist[2],41)
    h4=SS_ACT(tlist[3],41)
    fileobj=open("{}/outData.txt".format(loc),"w")
    fileobj.write("test1\n")
    processOut(h1,fileobj,kind)
    
    fileobj.write("*******************************\n")
    processOut(h2,fileobj,kind)
   
    fileobj.write("*******************************\n")
    processOut(h3,fileobj,kind)

    fileobj.write("*******************************\n")
    processOut(h4,fileobj,kind)
    return ["ACT",h1,h2,h3,h4]

def PSATOMR(tlist,loc,kind):
    print("fdfdfdfdfd")
    print(len(tlist))

    h1=SS_PSAT(tlist[0],48)
    h2=SS_PSAT(tlist[1],45)
    h31=SS_PSAT31(tlist[3],14)
    h32=SS_PSATFR(tlist[2],14,4)
    #print(h32)
    #print("&&&&&&&&&&&&&&&&&")
    h41=SS_PSAT41(tlist[5],28)
    h42=SS_PSATFR(tlist[4],28,4)
    #print(h42)
    #print("&&&&&&&&&&&&&&&&&")
    fileobj=open("{}/outData1.txt".format(loc),"w")
    fileobj.write("test2\n")
    processOut(h1,fileobj,kind)
    
    fileobj.write("*******************************\n")
    processOut(h2,fileobj,kind)

    fileobj.write("*******************************\n")
    processOut(h31,fileobj,kind)

    fileobj.write("*******************************\n")
    processOut(h32,fileobj,kind)
    fileobj.write("*******************************\n")
    processOut(h41,fileobj,kind)
    fileobj.write("*******************************\n")
    processOut(h42,fileobj,kind)

    return ["PSAT",h1,h2,h31,h32,h41,h42]

def SATOMR(tlist,loc,kind):
    print("fdfdfdfdfd")
    print(len(tlist))

    h1=SS_PSAT(tlist[0],53)
    h2=SS_PSAT(tlist[1],45)
    h31=SS_PSAT31(tlist[3],16)
    h32=SS_PSATFR(tlist[2],16,5)
    h4=SS_PSAT(tlist[4],31)
    h51=SS_PSATFR(tlist[5],0,5)
    h52=SS_PSATFR(tlist[6],6,3)
    #print(h32)
    #print("&&&&&&&&&&&&&&&&&")
    #h41=SS_PSAT41(tlist[5],28)
    #h42=SS_PSATFR(tlist[4],28)
    #print(h42)
    #print("&&&&&&&&&&&&&&&&&")
    fileobj=open("{}/outData1.txt".format(loc),"w")
    fileobj.write("test2\n")
    processOut(h1,fileobj,kind)
    
    fileobj.write("*******************************\n")
    processOut(h2,fileobj,kind)

    fileobj.write("*******************************\n")
    processOut(h31,fileobj,kind)

    fileobj.write("*******************************\n")
    processOut(h32,fileobj,kind)
    fileobj.write("*******************************\n")
    processOut(h4,fileobj,kind)
    fileobj.write("*******************************\n")
    processOut(h51,fileobj,kind)
    fileobj.write("*******************************\n")
    processOut(h52,fileobj,kind)
    return ["SAT",h1,h2,h31,h32,h4,h51,h52]
#def runOMR(ids):
    
#def fileManage():

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
        output='W'
    if count==0:
        output='O'
    print("{} {} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],output,mnum,output2,mlist[4]))
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
        output='O'
    print("{} {} {} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],mlist[4],output,mnum,output2,mlist[5]))
    olist.append(count2)
    olist.append(output)
    olist.append(output2)
    return olist

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
        cv2.waitKey(0)
    print(joke)
    print("*************************************")
    return joke
    #cv2.waitKey(0)

def SS_ACT2(image,amt):
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
        cv2.waitKey(0)
    print(joke)
    
    print("*************************************")
    return joke
    #cv2.waitKey(0)

def processOut(outData,fileobj,kind):
    joke=''
    #temp=int(sys.argv[2])
    temp=kind
    for x in range(0,len(outData)):
        h2=outData[x]

        if temp==0:
            store='{} {} {}\n'.format(h2[0],h2[1],h2[2])
            fileobj.write(store)
        elif temp==1:
            store='{}\n'.format(h2[1])
            fileobj.write(store)
        #this is not done dumbass
        #joke+="{} {}, ".format([h2[0],h2[2]])
        
    #fileobj.write(joke)
    fileobj.write("*******************************\n")

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
    
def picfixmass(typet,loc):
    num=typet
    help1=cv2.imread(loc)
    #cv2.imshow("name",help1)

    gray = cv2.cvtColor(help1, cv2.COLOR_BGR2GRAY)

    #cv2.imshow("check 0",gray)
    #cv2.waitKey(0)

    (h,w)=gray.shape[:2]
    gray = gray[int(h*0.05):h-int(h*.04),int(w*.05):w-int(w*.05)]
    #cv2.imshow("check 6",gray)
    #cv2.imwrite("test.jpg",gray)
    #cv2.waitKey(0)


    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    # find contours in the edge map, then initialize
    # the contour that corresponds to the document
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    docCnt = None

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
                break
    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper


        
    #paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))


    (h,w)=warped.shape[:2]
    gray2 = warped[int(h*0.02):h-int(h*.02),int(w*.02):w-int(w*.02)]

    #cv2.imshow("check help",warped)
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
                print("LLLLLLLLLL")
                break
            if len(approx) == 4 and num ==2:
                docCnt = approx
                docstore.append(docCnt)
    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper


    areaStore=[]
    if num == 1:
        paper = four_point_transform(gray2, docCnt.reshape(4, 2))
        #cv2.imshow("check 2",paper)
        #print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        #cv2.waitKey(0)
        return paper
    if num == 2:
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
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

def trythis(name1,type1):
    ntlist=readIntest(name1)
    setpicloc(ntlist,img,type1)

def dataDump(loc,dat):
    fileobj=open(loc,'w')
    
    print(dat)
    print(len(dat[0][1][0]))
    check='{}\n'.format(len(dat))

    print(check)
    print("**********")
    fileobj.write(check)
    
    for x in range(0,len(dat)):
        fileobj.write(dat[x][0])
    #    for y in range()
    #file.write(dat)
#picfixmass()
#python largeinput.py ssid92.txt 0
#allignment is off for PSAT FR
if __name__ == "__main__":
    ntlist=readIntest(sys.argv[1])
    info=setpicloc(ntlist,img,sys.argv[2])
    #dataDump(sys.argv[3],info)
    #trythis()
#"""