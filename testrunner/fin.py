from pdf2image import convert_from_path,convert_from_bytes
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os
import tempfile

"""
ACT Codes are ACTP10, ACTP16
SAT Codes are SAT2, SAT4, SAT3
PSAT Codes are PSAT15, PSAT16

Configlist is [length of surveys, ]

"""
gFac=350

def runner():
    configlist=configsetup()
    listStore=convertstart(sys.argv[1],configlist)
    print(listStore)
    nlist=textout(listStore)
    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    for x in nlist:
        print(len(x[1]))
    #print(nlist)

def textout(listHold):
    klist=[]
    for x in listHold:
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(x)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #print(x[len(x)-1])
        print("****************************************")
        fileobj=open('{}/outdata.txt'.format(x[5]),"w")
        fileobj2=open('{}/outexcel.txt'.format(x[5]),"w")
        xlen=len(x)
        print(x[5])
        print("************")
        print(len(x))
        print("***********")
        for sec in x[xlen-1]:
            for z in sec:
                store='{} {} {}\n'.format(z[0],z[1],z[2])
                fileobj.write(store)
                if z[2]=='G':
                    store2='{}?\n'.format(z[1])    
                else:
                    store2='{}\n'.format(z[1])
                fileobj2.write(store2)
                #print(len(z))
            fileobj.write("*************************************\n")
            fileobj2.write("*************************************\n")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        klist.append([[x[0],x[1],x[5]],x[xlen-1]])
    return klist


def configsetup():
    hold=[]
    fileobj=open('config.txt')  #This will be a backend hit
    for x in fileobj:
        hold.append(x)
    hold[0]=int(hold[0])
    print("***********")
    print(hold)
    print("***********")
    return hold

def convertstart(img,conlist):
    pdf=img+".pdf"
    names=img+".txt"
    print("{} {} {}".format(pdf,names,type(conlist[0])))

    file=open(names)
    namehelp=[]
    for x in file:
        x=x.strip()
        x=x.split()
        x.append(x[0]+"_"+x[1]+"_"+img)
        namehelp.append(x)
    #print(namehelp)
    
    check=os.getcwd()
    check=check+"/dep/"+img
    try:
        os.mkdir(check)
    except FileExistsError:
        print("Directory exists, Program will continue")


    
    #with tempfile.TemporaryDirectory() as path:
        #images_from_path = convert_from_path('/home/kankroc/example.pdf', output_folder=path)
     #   pdflist= convert_from_path(pdf,output_folder=path)
    print("we got a problem")
    
    #inputpdf= PdfFileReader(pdf)
    pdflist= convert_from_path(pdf)
    #h=inputpdf.getNumPages()
    #rint(h)

    current=0
    for x in namehelp:
        if x[1]=="ACTP10" or x[1]=="ACTP16":
            x.append(4+conlist[0])
            x.append("ACT")
        elif x[1]=="SAT2" or x[1]=="SAT4" or x[1]=="SAT3":
            x.append(5+conlist[0])
            x.append("SAT")
        elif x[1]=="PSAT15" or x[1]=="PSAT16":
            x.append(4+conlist[0])
            x.append("PSAT")
        
        checktemp=check+"/"+x[2]
        try:
            os.mkdir(checktemp)
        except FileExistsError:
            print("Directory exists, Program will continue")
        print("ha")


        #print(checktemp)
        x.append(checktemp)
        """
        outputpdf=PdfFileWriter()
        for z in range(current,current+x[3]+1):
            outputpdf.addPage(inputpdf.getPage(z))
        jk='{}/{}/{}test.pdf'.format(check,x[2],x[2])
        #outputStream = open(file(jk,"wb"))
        """
        #outputpdf.write(open(jk,"wb"))
        #print(outputpdf.getNumPages())
        #current=x[3]+1+current
        #print(jk)
        #lo=open(jk,"rb")
        #pdflist= convert_from_path(lo)
        #print(len(pdflist))
        
        print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        print(x)
        count=0
        #"""
        for y in range(0,x[3]):
            num=y+current
            print("look here")
            print(num)
            if y<conlist[0]:
                pdflist[num].save('{}/{}/surveyPG{}.jpg'.format(check,x[2],y),'JPEG')
            else:
                hold='{}/{}/PG{}.jpg'.format(check,x[2],y)
                pdflist[num].save(hold,'JPEG')
                #print('{} {}'.format(x[4], y))
                    
                if (x[4]=='SAT' and (y==2+conlist[0])) or (x[4]=='SAT' and y==(4+conlist[0])):
                    temp=picfixmass(2,hold)
                    x.append(temp[0])
                    x.append(temp[1])
                elif (x[4]=='PSAT' and y==(2+conlist[0])) or (x[4]=='PSAT' and y==(3+conlist[0])):
                    temp=picfixmass(2,hold)
                    x.append(temp[0])
                    x.append(temp[1])
                else:
                    x.append(picfixmass(1,hold))
                
                count+=1
                print(count)
                #pdflist[num]
        
        if x[4]=='SAT':
            current+=1
        print(len(x))
        x.append(testmanage(x))
        print(len(x))
        current+=x[3]
        #current+=1
        #"""

    #print(namehelp)
    #print(check)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("____________________________________________________________")
    return namehelp
    
    
def testmanage(holdlist):
    if holdlist[4]=='ACT':
        output=ACTOMR(holdlist)
    elif holdlist[4]=='PSAT':
        output=PSATOMR(holdlist)
    elif holdlist[4]=='SAT':
        output=SATOMR(holdlist)
    elif holdlist[4]=='ISEE':
        output=ISEEOMR(holdlist)
    return output

def viewAdjust(pic,amt):
    #cv2.imshow("kklklkllll",pic)
    #cv2.waitKey(0)
    hold=[]
    (h,w)=pic.shape[:2]
    val=int(w/amt)
    for x in range(0,amt):
        hold.append(pic[0:h,val*x:val*(x+1)])
    return hold

def ACTOMR(listACT):
    out1=SS_ACT(listACT[6],76)
    out2=SS_ACTMath(listACT[7],61)
    out3=SS_ACT(listACT[8],41)
    out4=SS_ACT(listACT[9],41)

    print(out1)
    print("\n")
    print(out2)
    print("\n")
    print(out3)
    print("\n")
    print(out4)
    return [out1,out2,out3,out4]

def PSATOMR(listPSAT):
    out1=SS_PSAT(listPSAT[6],48)
    out2=SS_PSAT(listPSAT[7],45)
    out31=SS_PSAT31(listPSAT[9],14)
    out32=SS_PSATFR(listPSAT[8],14,4)
    out41=SS_PSAT41(listPSAT[11],28)
    out42=SS_PSATFR(listPSAT[10],28,4)
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
    return [out1,out2,out31,out32,out41,out42]

def SATOMR(listSAT):
    out1=SS_PSAT(listSAT[6],53)
    out2=SS_PSAT(listSAT[7],45)
    out31=SS_PSAT31(listSAT[9],16)
    out32=SS_PSATFR(listSAT[8],16,5)
    out4=SS_PSAT(listSAT[10],31)
    out51=SS_PSATFR(listSAT[11],31,5)
    out52=SS_PSATFR(listSAT[12],36,3)
    print(out1)
    print("\n")
    print(out2)
    print("\n")
    print(out31)
    print("\n")
    print(out32)
    print("\n")
    print(out4)
    print("\n")
    print(out51)
    print("\n")
    print(out52)
    return [out1,out2,out31,out32,out4,out51,out52]

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
        cv2.waitKey(0)
    print(joke)
    
    print("*************************************")
    return joke
    #cv2.waitKey(0)

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

runner()