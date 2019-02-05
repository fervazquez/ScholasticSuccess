import os,sys

def maketxt():
    tname=sys.argv[1]
    tname+=".txt"
    return open(tname)

def getinput():
    ql=[]
    while True:
        inp=input("Enter Category to add a Category Name: ")
        if inp =="category":
            check=input("Enter Category Name: ")
            print("numbers will now be entered in order to stop please input 999")
            hold=[]
            while True:
                num=input("Enter a question number that belongs in {}: ".format(check))
                if num == 999:
                    break
                else:
                    hold.append(num)
            ql.append([check,hold])


            
        elif inp =="QN":
            print("hi")

        else:
            print("list will now be printed")
            break
    print(ql)

getinput()