import codecs,re,collections

class Question(object):
    catList=[]
    def __init__(self,num,val):
        self.num=num
        self.val=val

    def printdata(self):
        return (str(self.num)+' '+self.val)

class Category(object):
    nlLen=0
    nlcor=0
    def __init__(self,numList,hold):
        self.numList=numList
        self.hold=hold
        self.nlLen=len(self.hold)

    def setList(self,listh):
        self.hold=listh

    def sStat(self):
        for x in range(0, len(self.hold)):
            if self.hold[x].val == True:
                self.nlLen+=1

    def printCat(self):
        cathold=''
        cathold+=self.numList
        cathold+=': '
        for x in range(0, len(self.hold)):
            cathold+= str(self.hold[x])+' '
        return cathold

class testHold(object):
    def __init__(self,name,catL,qL):
        self.name=name
        self.catL=catL
        self.qL=qL
        self.ansLis=[]
        
    def outData(self):
        print(self.name)
        for x in range(0,len(self.catL)):
            print(self.catL[x].printCat())
        for x in range(0, len(self.qL)):
            print(self.qL[x].printdata())
        for x in range(0, len(self.ansLis)):
            print(self.ansLis[x])
    
    def setRes(self, resList):
        self.resList=resList

    def compScore(self):
        for x in range(0,len(self.qL)):
            temp1=self.qL[x].val
            temp2=self.resList[x]
            if temp1 == temp2:
                self.ansLis.append(1)
            else:
                
                if self.qL[x].val[1]:
                    multi=self.qL[x].val.split()
                    for x in range(0,len(multi)):
                        if multi[x] == temp2:
                            self.ansLis.append(1)
                            break
                        else:
                            self.ansLis.append(2)
                else:
                    self.ansLis.append(2)



def runT():
    fileobj=open("ggtest.txt", "r")
    red=fileobj.readline()
    redC=fileobj.readline()
    redQ=fileobj.readline()

    write=fileobj.readline()
    writeC=fileobj.readline()
    writeQ=fileobj.readline()

    MNoCalc=fileobj.readline()
    MNoCalcC=fileobj.readline()
    MNoCalcQ=fileobj.readline()

    MCalc=fileobj.readline()
    MCalcC=fileobj.readline()
    MCalcQ=fileobj.readline()

    reading=readInSET(fileobj,red,redC,redQ)
    write=readInSET(fileobj,write,writeC,writeQ)
    MNoCalc=readInSET(fileobj,MNoCalc,MNoCalcC,MNoCalcQ)
    MCalc=readInSET(fileobj,MCalc,MCalcC,MCalcQ)
    

    fileobj=open("studentRes.txt","r")

    fName=fileobj.readline()
    lName=fileobj.readline()
    t1=fileobj.readline()
    t2=fileobj.readline()
    t3=fileobj.readline()
    t4=fileobj.readline()

    resRead=readres(fileobj, t1)
    writeRead=readres(fileobj, t2)
    MNORead=readres(fileobj, t3)
    MCaRead=readres(fileobj, t4)

    reading.setRes(resRead)
    write.setRes(writeRead)
    MNoCalc.setRes(MNORead)
    MCalc.setRes(MCaRead)

    reading.compScore()
    write.compScore()
    MNoCalc.compScore()
    MCalc.compScore()




    #reading.outData() #test output
    write.outData() #test output
    #MNoCalc.outData() #test output
    #MCalc.outData() #test output " ""

def readres(fileobj, amt):
    relist=[]
    for x in range(0, int(amt)):
        relist.append(fileobj.readline().strip())
    return relist

def readInSET(fileobj,name,cLen,qLen):
    catListRe=[]

    check=re.compile('[a-zA-Z]',re.IGNORECASE)
    checknum=re.compile('[0-9]',re.IGNORECASE)
    parCheck=re.compile('\(([^)]+)\)',re.IGNORECASE)
    for x in range(0, int(cLen)):
        line=fileobj.readline()
        result1=''
        qList4=[]
        count=0
        temp=line.split()
        catmul=None
        for word in temp:
            count+=1
            if re.match(check,word)is not None:
                word+=''
                result1+=word
            if re.match(checknum,word)is not None:
                qList4.append(int(word))
                if count< len(temp):
                    if temp[count]:
                        if re.match(parCheck,temp[count]):
                            print(temp[count])
        catListRe.append(Category(result1,qList4))
    print('*****************sss***********************')
    

    qListAns=[]
    for x in range(0, int(qLen)):
        line=fileobj.readline()
        result1=''
        result2=0
        result=line.split()
        result2=int(result[0])
        if len(result) > 2:
            for y in range(0, len(result)-1):
                result1+=result[y+1]
                result1+=' '
        else:
            result1=result[1]
            result1+=''
            
        qListAns.append(Question(result2,result1))


    return testHold(name,catListRe,qListAns)




def readInput():
    inList=[]


runT()