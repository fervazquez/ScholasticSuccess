str1="raceCar"
str2="electrocardiogram"

holdlist=[]
for x in range(0,len(str1)):
    for y in range(0,len(str2)):
        if str1[x]==str2[y]:

            i=x
            t=y
            temp=""
            while str1[i] ==str2[t]:
                temp+=str1[i]
                i+=1
                t+=1
            holdlist.append(temp)

print(holdlist)