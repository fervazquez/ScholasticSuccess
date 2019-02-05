import codecs,re,collections,time, sys

class Question(object):
    def __init__(self,num,akey,testName,secName):
        self.num=num
        self.akey=akey
        self.testName=testName
        self.secName=secName
        self.categories=[]

    def setresp(self, resp):
        self.resp=resp
    
    def setCat(self,category):
        self.categories.append(category)
    
    def printCategory(self):
        hold=""
        for x in range(0,len(self.categories)):
            hold+=self.categories[x]+" "
        return hold
    
    def setGuess(self,guess):
        self.guess=guess

    def calcCNC(self):
        if self.testName=='SAT1' and self.num==31 and self.secName=='MathCalc':
            if self.resp=='INV':
                self.val='NC'
            elif float(self.resp)<=6 and float(self.resp)>=4:
                self.val='C'
            else:
                self.val='NC'
        elif self.resp == self.akey:
            self.val='C'
        else:
            self.val='NC'

    def printQ(self):
        return '{:>3}: Key: {:<5} Resp: {:<5} V: {:<5} Guess?: {:<5}'.format(self.num,self.akey,self.resp,self.val,self.guess)
    
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
        #print("XXXXXXXX")
        #print(self.totnum)
        #print("XXXXXXXX")
        for x in range(0,self.totnum):
            tempq=int(self.ql[x].quest)
            #print(tempq)
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
        self.gAns=0
        self.NGAns=0
        self.gperf=0
        self.incgperf=0
        self.guesses=[]
        self.wrong=[]
        self.correct=[]
        self.nonguesses=[]
    
    def setcatList(self,li):
        self.catList=li
    
    def setQuestCats(self):
        for x in range(0,len(self.catList)):
            if len(self.catList[x].ql)!=0:
                #print("hi")
                hold=self.catList[x].ql
                for y in range(0,len(self.qListAns)):
                    for z in range(0,len(hold)):
                        if self.qListAns[y].num == hold[z].quest:
                            self.qListAns[y].setCat(self.catList[x].cat)
    
    def doCalc(self):
        #print(len(self.catList))
        for x in range(0,len(self.catList)):
            #print("CCCCCCCCCCCCCCC")
            #print(x)
            #print("CCCCCCCCCCCCCCC")
            self.catList[x].calcStat(self.qListAns)
    
    def getqcats(self):
        for x in range(0,len(self.qListAns)):
            self.qListAns[x].printCategory()
    
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
    
    def getGuesses(self):
        helper=""
        for x in range(0,len(self.guesses)):
            helper+=self.guesses[x].printQ()+" \n"+self.guesses[x].printCategory()+" \n"
        return helper
        #print(self.guesses)
    
    def getIncorrect(self):
        helper=""
        for x in range(0,len(self.wrong)):
            helper+=self.wrong[x].printQ()+" \n"+self.wrong[x].printCategory()+" \n"
        return helper
        #print(self.wrong)
    
    def setanswers(self,resp):
        for x in range(0,len(self.qListAns)):
            qlhelp=self.qListAns[x]
            qlhelp.setresp(resp[x][1])
            qlhelp.setGuess(resp[x][2])
            qlhelp.calcCNC()
            if qlhelp.val=='C':
                self.cAns+=1
                self.correct.append(qlhelp)
            else:
                self.wAns+=1
                self.wrong.append(qlhelp)
            if qlhelp.guess=='G':
                self.gAns+=1
                self.guesses.append(qlhelp)
            else:
                self.NGAns+=1
                self.nonguesses.append(qlhelp)
            if qlhelp.val=='C' and qlhelp.guess=='G':
                self.gperf+=1
            if qlhelp.val=='NC' and qlhelp.guess=='G':
                self.incgperf+=1

    def getSecStats(self):
        ql=self.qListAns
        out='  Raw performance: {} out of {}, {:>3}%\n'.format(self.cAns,len(ql),round(self.cAns/len(ql), 3)*100)
        out+='          Guesses: {} out of {}, {:>3}%\n'.format(self.gAns,len(ql),round(self.gAns/len(ql), 3)*100)
        out+='  Correct Guesses: {} out of {}, {:>3}%\n'.format(self.gperf,self.gAns,round(self.gperf/self.gAns, 3)*100)
        out+='Incorrect Guesses: {} out of {}, {:>3}%\n'.format(self.incgperf,self.gAns,round(self.incgperf/self.gAns, 3)*100)
        return out

    def printC(self):
        for x in range(0,len(self.catList)):
            print(self.catList[x].printCat())
                
    def printQuestions(self):
        for x in range(0,len(self.qListAns)):
            print(self.qListAns[x].printQ())

    #def getLastTEN(self):
    #    for x in rnage

def runGradeSAT():
    #start=time.time()
    fileobj=open("SAT1KEY.txt", "r")
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

    fileobj2=open("SATTESTCASE.txt", "r")
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

    #print(redres)
    
    tests[0].setanswers(redres)
    tests[1].setanswers(writeres)
    tests[2].setanswers(MNCres)
    tests[3].setanswers(MCalcres)
    
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Reading SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #tests[0].printC()
    tests[0].printQuestions()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Writing Language SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #tests[1].printC()
    tests[1].printQuestions()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Math NoCALC SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #tests[2].printC()
    tests[2].printQuestions()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Math CALC SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #tests[3].printC()
    tests[3].printQuestions()

    tests[0].doCalc()
    tests[1].doCalc()
    tests[2].doCalc()
    tests[3].doCalc()

    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Reading SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[0].getstat())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Writing Language SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[1].getstat())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Math NoCALC SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[2].getstat())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Math CALC SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[3].getstat())
    """
    print(tests[0].cAns)
    print(tests[1].cAns)
    print(tests[2].cAns)
    print(tests[3].cAns)
    """
    print(tname)
    #end=time.time()
    #print(end-start)
    scorehold=getScoreSAT(fileobj,scoreNum)
    #print(scorehold)
    #3+2 then 0 then 1
    math=int(tests[2].cAns) + int(tests[3].cAns)
    reading=int(tests[0].cAns)
    writing=int(tests[1].cAns)

    mathScore=scorehold[0][math]
    readingScore=scorehold[1][reading]
    writingScore=scorehold[2][writing]

    print("***************************************************")
    print('Combined Math Score: {}'.format(mathScore))
    print('Reading Score: {}'.format(int(readingScore)*10))
    print('Writing and Language Score: {}'.format(int(writingScore)*10))
    print('Total Score: {}'.format(((int(mathScore))+(int(readingScore)*10)+(int(writingScore)*10))))
    
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Reading SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[0].getSecStats())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Writing Language SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[1].getSecStats())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Math NoCALC SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[2].getSecStats())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Math CALC SECTION")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[3].getSecStats())

    tests[0].setQuestCats()
    tests[1].setQuestCats()
    tests[2].setQuestCats()
    tests[3].setQuestCats()
    #qs=tests[2].keyL + tests[3].keyL
    #tests.append(TestHold("MathComb",39,qs,"SAT"))
    list1=combList(tests[2].catList,tests[3].catList)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("COMBINED MATH CALCULATIONS")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #print(list1)
    catTemp=""
    for x in range(0,len(list1)):
        st=list1[x]
        catTemp+='{:>32}: Positive Stat: {:>5}% {:>2}/{:<2} Negative Stat: {:>4}% {:>2}/{:<2}'.format(st[0],st[4],st[2],st[1],st[5],st[3],st[1])+" \n"
    print(catTemp)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #list1[0].printCat()
    #tests[4].printC()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Reading SECTION Guesses")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[0].getGuesses())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Writing Language SECTION Guesses")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[1].getGuesses())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Math NoCALC Section Guesses")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[2].getGuesses())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Math CALC Section Guesses")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[3].getGuesses())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Incorrect for Reading Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[0].getIncorrect())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Incorrect for Writing Language Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[1].getIncorrect())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Incorrect for Math No CALC Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[2].getIncorrect())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Incorrect for Math CALC Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[3].getIncorrect())

def runGradeACT():
    #start=time.time()
    fileobj=open("ACTP10KEY.txt", "r")
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

    fileobj2=open("ACTTESTCASE.txt", "r")
    fName=fileobj2.readline().strip()
    lName=fileobj2.readline().strip()
    
    sec1=fileobj2.readline().strip()
    sec2=fileobj2.readline().strip()
    sec3=fileobj2.readline().strip()
    sec4=fileobj2.readline().strip()

    englishres=readres(fileobj2,sec1)
    mathres=readres(fileobj2,sec2)
    readingres=readres(fileobj2,sec3)
    scienceres=readres(fileobj2,sec4)

    #print(redres)
    
    tests[0].setanswers(englishres)
    tests[1].setanswers(mathres)
    tests[2].setanswers(readingres)
    tests[3].setanswers(scienceres)
    
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("ENGLISH Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #tests[0].printC()
    tests[0].printQuestions()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("MATH Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #tests[1].printC()
    tests[1].printQuestions()
    
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("READING Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #tests[2].printC()
    tests[2].printQuestions()
    
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("SCIENCE Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    #tests[3].printC()
    tests[3].printQuestions()
    
    tests[0].doCalc()
    tests[1].doCalc()
    tests[2].doCalc()
    tests[3].doCalc()
    
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("English Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[0].getstat())
    
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Math Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[1].getstat())
    
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Reading Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[2].getstat())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Science Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[3].getstat())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    """
    print(tests[0].cAns)
    print(tests[1].cAns)
    print(tests[2].cAns)
    print(tests[3].cAns)
    """
    print(tname)
    #end=time.time()
    #print(end-start)
    scorehold=getScoreACT(fileobj,scoreNum)
    #print(scorehold)
    english=int(tests[0].cAns)
    math=int(tests[1].cAns)
    reading=int(tests[2].cAns)
    science=int(tests[3].cAns)

    englishScore=int(scorehold[0][english])
    mathScore=int(scorehold[1][math])
    readingScore=int(scorehold[2][reading])
    scienceScore=int(scorehold[3][science])
    totscore=round(((englishScore+mathScore+readingScore+scienceScore)/4), 0)
    print("***************************************************")
    print('Writing Score: {}'.format(englishScore))
    print('Math Score: {}'.format(mathScore))
    print('Reading Score: {}'.format(readingScore))
    print('Science Score: {}'.format(scienceScore))
    print('Total Score: {}'.format(totscore))
    print("***************************************************")
    print("sec 1")
    print(tests[0].getSecStats())
    print("sec 2")
    print(tests[1].getSecStats())
    print("sec 3")
    print(tests[2].getSecStats())
    print("sec 4")
    print(tests[3].getSecStats())

    tests[0].setQuestCats()
    tests[1].setQuestCats()
    tests[2].setQuestCats()
    tests[3].setQuestCats()

    print("Guesses for English Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[0].getGuesses())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Guesses for Math Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[1].getGuesses())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Guesses for Reading Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[2].getGuesses())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Guesses for Science Section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[3].getGuesses())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Incorrect for English section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[0].getIncorrect())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Incorrect for Math section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[1].getIncorrect())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Incorrect for Reading section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[2].getIncorrect())
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("Incorrect for Science section")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(tests[3].getIncorrect())
    #" ""

def combList(l1,l2):
    lx=[]
    for x in range(0,len(l1)):
        h1=l1[x]
        h2=l2[x]
        lp=[]
        lp.append(h1.cat)
        lp.append(len(h1.ql)+len(h2.ql))
        lp.append(h1.countpos+h2.countpos)
        lp.append(h1.countneg+h2.countneg)

        if lp[2]==0:
            lp.append(0)
        else:
            
            lp.append(round((lp[2]/lp[1]), 3)*100)
        if lp[3]==0:
            lp.append(0)
        else:
            lp.append(round((lp[3]/lp[1]), 3)*100)
        
        lx.append(lp)
        #li=l1[x].ql+l2[x].ql
        
        #print(lp)
    #for y in range(0,len(lt)):
    #    li.append(lt[y])
    #lx.append(li)
    #print(lx)
    #print(len(l1))

    return lx

def getScoreSAT(fileobj,amt):
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
    
def getScoreACT(fileobj,amt):
    testhold=[]
    testhold.append([])
    testhold.append([])
    testhold.append([])
    testhold.append([])
    for x in range(0, int(amt)):
        line=fileobj.readline()
        #print(line)
        result=0
        result=line.split()
        if len(result)>1 and result[1]:
            testhold[0].append(result[1])
        if len(result)>2 and result[2]:
            testhold[1].append(result[2])
        if len(result)>3 and result[3]:
            testhold[2].append(result[3])
        if len(result)>4 and result[4]:
            testhold[3].append(result[4])
        #print(result)
    return testhold

def readres(fileobj2, amt):
    relist=[]
    for x in range(0, int(amt)):
        relist.append(fileobj2.readline().strip().split())
    #print(relist[1])
    return relist

if int(sys.argv[1])==1:
    runGradeACT()
if int(sys.argv[1])==2:
    runGradeSAT()
if int(sys.argv[1])==3:
    runGradePSAT()