from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import sys, cv2, imutils, os
from matplotlib import pyplot as plt
import time

def dope():
    


    lT=os.listdir(sys.argv[1])
    #print(lT)
    currI=lT[0][0]
    curr=0
    #print(currI)
    holder=[[]]
    for x in range(len(lT)):
        if lT[x][0] != currI:
            currI=lT[x][0]
            curr+=1
            holder.append([])
        tempPic=cv2.imread(sys.argv[1]+"/"+lT[x])
        (h,w)=tempPic.shape[:2]

        holder[curr].append((h,w,lT[x]))
        
    print(holder)
dope()