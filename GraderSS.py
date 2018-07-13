import codecs,re,collections,time

class Question(object):
    def __init__(self,num,akey,testName,secName):
        self.num=num
        self.akey=akey
        self.testName=testName
        self.secName=secName

    def setresp(self, resp):
        self.resp=resp

    def calcCNC(self):
        if self.testName=='SAT1' and self.num==31 and self.secName=='MathCalc':
            if float(self.resp)<=6 and float(self.resp)>=4:
                self.val='C'
            else:
                self.val='NC'
        elif self.resp == self.akey:
            self.val='C'
        else:
            self.val='NC'

    def printQ(self):
        return '{:>3}: Key: {:<5} Resp: {:<5} V: {:<5}'.format(self.num,self.akey,self.resp,self.val)

class Category(object):
    def __init__(self,cat,ql):
        self.cat=cat
        self.ql=ql
        self.posstat=0
        self.negstat=0
        self.countpos=0
        self.countneg=0
    def calcStat(self,anslist):
        self.totnum=len(self.ql)
        
        self.countpos=0
        self.countneg=0
        for x in range(0,self.totnum):
            tempq=int(self.ql[x].quest)        
            if anslist[tempq-1].val=='C':
                self.countpos+=1
            else:
                if len(self.ql[x].plist)!=0:
                    for y in range(0,len(self.ql[x].plist)):
                        if str(anslist[tempq-1].resp)==str(self.ql[x].plist[y]):
                            if anslist[tempq].val=='NC':
                                self.countneg+=1
                else:
                    self.countneg+=1
        if self.countpos==0:
            self.posstat=0
        else:
            self.posstat=self.countpos/self.totnum
        if self.countneg==0:
            self.negstat=0
        else:
            self.negstat=self.countneg/self.totnum

    def printstat(self):
        cate=self.cat
        posper=round(self.posstat, 3)*100
        negper=round(self.negstat, 3)*100
        tot=self.totnum
        pos=self.countpos
        neg=self.countneg
        #if self.countpos!=0 and self.countneg!=0:
        catTemp='{:>32}: Positive Stat: {:>5}% {:>2}/{:<2} Negative Stat: {:>4}% {:>2}/{:<2}'.format(cate,posper,pos,tot,negper,neg,tot)
        return catTemp
    def printCat(self):
        catTemp='{:>32}: '.format(self.cat)
        for x in range(0, len(self.ql)):
            catTemp+=(str(self.ql[x].printCQue())+' ')
        return catTemp

#save plist into a list, even if its just one
class CatQuestion(object):
    def __init__(self,quest,plist):
        self.quest=quest
        self.plist=plist
    def printCQue(self):
        cq='{:>3}: '.format(self.quest)
        for x in range(0, len(self.plist)):
            cq+= str(self.plist[x])+' '
        return cq
    
class TestHold(object):
    def __init__(self,name,catL,keyL,tname):
        self.name=name
        self.catL=catL
        self.keyL=keyL
        self.tname=tname
        self.catList=[]
        self.qListAns=[]
        self.cAns=0
        self.wAns=0
        self.score=0
    
    def doCalc(self):
        for x in range(0,len(self.catList)):
            self.catList[x].calcStat(self.qListAns)
    def getstat(self):
        catTemp=''
        for x in range(0,len(self.catList)):
            if self.catList[x].posstat==0 and self.catList[x].negstat==0:
                catTemp+=''
            else:
                catTemp+=str(self.catList[x].printstat())+' \n'
        return catTemp
    def getCats(self,fileobj):
        check=re.compile('[a-zA-Z]',re.IGNORECASE)
        checknum=re.compile('[0-9]',re.IGNORECASE)
        parCheck=re.compile('\(([^)]+)\)',re.IGNORECASE)
        for x in range(0, int(self.catL)):
            line=fileobj.readline()
            result1=''
            qList=[]
            count=0
            temp=line.split()
            catmul=[]
            qnum=0
            for word in temp:
                count+=1
                if re.match(check,word)is not None:
                    word+=''
                    result1+=word
                if re.match(checknum,word)is not None:
                    qnum=int(word)
                    if count< len(temp):
                        if temp[count]:
                            if re.match(parCheck,temp[count]):
                                for x in range(1,len(temp[count])-1):
                                    catmul.append(temp[count][x])
                                #print(len(catmul))
                    qList.append(CatQuestion(qnum,catmul))
                    catmul=[]
            self.catList.append(Category(result1,qList))
    def getkeys(self,fileobj):  
        for x in range(0, int(self.keyL)):
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
            self.qListAns.append(Question(result2,result1,self.tname,self.name))
    def setanswers(self,resp):
        for x in range(0,len(self.qListAns)):
            self.qListAns[x].setresp(resp[x])
            self.qListAns[x].calcCNC()
            if self.qListAns[x].val=='C':
                self.cAns+=1
            else:
                self.wAns+=1
    def printC(self):
        for x in range(0,len(self.catList)):
            print(self.catList[x].printCat())
                
    def printQuestions(self):
        for x in range(0,len(self.qListAns)):
            print(self.qListAns[x].printQ())


def runGrade():
    start=time.time()
    fileobj=open("ggtest.txt", "r")
    tname=fileobj.readline().strip()
    tL=fileobj.readline().strip()
    tests=[]
    for x in range(0,int(tL)):
        name=fileobj.readline().strip()
        cats=fileobj.readline().strip()
        ques=fileobj.readline().strip()
        tests.append(TestHold(name,cats,ques,tname))
    scoreNum=fileobj.readline().strip()
    
    for x in range(0,int(tL)):
        tests[x].getCats(fileobj)
        tests[x].getkeys(fileobj)


    fileobj2=open("studentRes.txt", "r")
    fName=fileobj2.readline().strip()
    lName=fileobj2.readline().strip()
    sec1=fileobj2.readline().strip()
    sec2=fileobj2.readline().strip()
    sec3=fileobj2.readline().strip()
    sec4=fileobj2.readline().strip()
    redres=readres(fileobj2,sec1)
    writeres=readres(fileobj2,sec2)
    MNCres=readres(fileobj2,sec3)
    MCalcres=readres(fileobj2,sec4)


    
    tests[0].setanswers(redres)
    tests[1].setanswers(writeres)
    tests[2].setanswers(MNCres)
    tests[3].setanswers(MCalcres)
    
    tests[0].printC()
    tests[0].printQuestions()
    tests[1].printC()
    tests[1].printQuestions()
    tests[2].printC()
    tests[2].printQuestions()
    tests[3].printC()
    tests[3].printQuestions()

    tests[0].doCalc()
    tests[1].doCalc()
    tests[2].doCalc()
    tests[3].doCalc()

    print(tests[0].getstat())
    print(tests[1].getstat())
    print(tests[2].getstat())
    print(tests[3].getstat())

    print(tests[0].cAns)
    print(tests[1].cAns)
    print(tests[2].cAns)
    print(tests[3].cAns)

    print(tname)
    end=time.time()
    print(end-start)
    scorehold=getScoreCon(fileobj,scoreNum)
    print(scorehold)
    #3+2 then 0 then 1
    math=int(tests[2].cAns) + int(tests[3].cAns)
    reading=int(tests[0].cAns)
    writing=int(tests[1].cAns)

    mathScore=scorehold[0][math]
    readingScore=scorehold[1][reading]
    writingScore=scorehold[2][writing]

    print('Combined Math Score: {}'.format(mathScore))
    print('Reading Score: {}'.format(int(readingScore)*10))
    print('Writing and Language Score: {}'.format(int(writingScore)*10))

    

    print('Total Score: {}'.format(((int(mathScore))+(int(readingScore)*10)+(int(writingScore)*10))))

    

def getScoreCon(fileobj,amt):
    testhold=[]
    testhold.append([])
    testhold.append([])
    testhold.append([])
    for x in range(0, int(amt)):
        line=fileobj.readline()
        result=0
        result=line.split()
        if len(result)>1 and result[1]:
            testhold[0].append(result[1])
        if len(result)>2 and result[2]:
            testhold[1].append(result[2])
        if len(result)>3 and result[3]:
            testhold[2].append(result[3])
        #print(result)
    return testhold
    
def readres(fileobj2, amt):
    relist=[]
    for x in range(0, int(amt)):
        relist.append(fileobj2.readline().strip())
    return relist




runGrade()
