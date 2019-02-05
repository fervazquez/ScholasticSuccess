class Category(object):
    def __init__(self, rank, name, arr):
        self.rank=rank
        self.name=name
        self.locnum=0
        self.arr=arr

    def display(self):
        return '{:<8} <<{}>>  {}'.format(self.rank,self.name,self.arr)

def mStr(arr):
    mode=arr[0]
    helper=""
    help2=arr[1]

    for x in range(2,len(arr)):
        #helper=helper+" {}".format(arr[x])
        arr[x]=float(arr[x])
    #print("{} {}....".format(mode,helper))
    #return mode, helper, help2
    #if 2<len(arr):
    del arr[0]
    del arr[0]

    return Category(mode,help2,arr)

def setRanK(arr):
    for x in range(0, len(arr)):
        currM=0
        currC=0
        currS=0
        currSS=0
        if arr[x].rank=='M':
            arr[x].locnum=x


def prepare(fname):
    file = open(fname, "r")
    hold=file.readline().strip()
    #print("{} hi2".format(hold))
    quest=file.readline().strip()
    #print("{} hi".format(quest))
    secCats=[]
    ans=[]
    for x in range(0,int(hold)):
        hep=file.readline().strip()
        jk=hep.split()
        #print(jk)
        #mode,catname,condensed=mStr(jk)
        #print("{} <<<{}>>> <<{}>>".format(mode,catname,condensed))
        catcom=mStr(jk)
        secCats.append(catcom)
        print(catcom.display())
        #print('{:<8} <<{}>>'.format(catcom.rank,catcom.name))
    for x in range(0,int(quest)):
        ans.append(file.readline().strip())
    print(ans)
    #print(secCats)
    #print(quest)
    return secCats, ans

def getScoreConv(fname,tipo):
    file=open(fname,"r")
    size=file.readline().strip()
    testhold=[]
    testhold.append([])
    testhold.append([])
    testhold.append([])
    for x in range(0, int(size)):
        line=file.readline()
        result=0
        result=line.split()
        if len(result)>1 and result[1]:
            testhold[0].append(result[1])
        if len(result)>2 and result[2]:
            testhold[1].append(result[2])
        if len(result)>3 and result[3]:
            testhold[2].append(result[3])
        if tipo==1 and len(result)>4 and result[4]:
            testhold[3].append(result[4])
        #print(result)
    return testhold


def PSAT16():

    readCats, readans = prepare("PSAT16cats/PSAT16ReadingCATS.txt")
    writeCats, writeAns = prepare("PSAT16cats/PSAT16WritingLangCATS.txt")
    scoreconv= getScoreConv("PSAT16cats/scoreConv.txt",0)
    print("***************************")
    print(readans)
    print("********************")
    print(writeAns)
    print(scoreconv)
    
    #prepare("PSAT16cats/PSAT16ReadingCATS.txt")
    #prepare("PSAT16cats/PSAT16ReadingCATS.txt")

def ACTP10():
    scoreconv= getScoreConv("PSAT16/scoreConv.txt",1) #the one is for the ACT
if __name__== '__main__':
    PSAT16()

