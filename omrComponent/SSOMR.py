# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import sys
import imutils
import cv2
import random

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to the input image")
#args = vars(ap.parse_args())

#lines 24 to 57 in order to get the image to the proper viewing area

# load the image, convert it to grayscale, blur it
# slightly, then find edges
#image = cv2.imread(args["image"])


def picfix(image,num):
	#cv2.imshow("st",image)
	#cv2.waitKey(0)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
	paper = four_point_transform(image, docCnt.reshape(4, 2))
	warped = four_point_transform(gray, docCnt.reshape(4, 2))

	#cv2.imshow("st",warped)
	#cv2.waitKey(0)

	blurred = cv2.GaussianBlur(warped, (5, 5), 0)
	edged = cv2.Canny(blurred, 75, 200)

	# find contours in the edge map, then initialize
	# the contour that corresponds to the document
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	docCnt = None
	#cv2.drawContours(edged, cnts, -1, (0,255,0), 3)
	#cv2.imshow("test2", edged)
	#print(cnts)
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
				break
			if len(approx) == 4 and num ==2:
				docCnt = approx
				docstore.append(docCnt)
	
	#print(docstore)

	# apply a four point perspective transform to both the
	# original image and grayscale image to obtain a top-down
	# birds eye view of the paper
	areaStore=[]
	if num == 1:
		paper = four_point_transform(paper, docCnt.reshape(4, 2))
		return paper
	if num == 2:
		areaStore.append(four_point_transform(paper, docstore[0].reshape(4, 2)))
		areaStore.append(four_point_transform(paper, docstore[1].reshape(4, 2)))
		return areaStore

def viewAdjust(workArea,amt):
	help=[]
	(h,w)=workArea.shape[:2]
	cw=int((w/amt))
	for x in range(0,amt):
		help.append(workArea[0:h, cw*x:cw*(x+1)])
	return help

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
	mlist.append(cv2.countNonZero(k0))
	#cv2.imshow("{} t{}".format(x,t),k0)
	#if count2 == 19:#or count2 == 39:
	#	cv2.imshow("{} t{}".format(x,t),q)
	#	cv2.imshow("{} t{} 0".format(x,t),k0)
	#	cv2.imshow("{} t{} 1".format(x,t),k1)
	#	cv2.imshow("{} t{} 2".format(x,t),k2)
	#	cv2.imshow("{} t{} 3".format(x,t),k3)
	#	cv2.imshow("{} t{} 4".format(x,t),k4)
	mnum=max(mlist)
	if mlist[4]>gFac:
		output2='G'
	else:
		output2='NG'
	if mlist[0]>gFac:
		if count2%2 == 0 and z == 1:
			output='F'
		else:
			output='A'
		count+=1
	if mlist[1]>gFac:
		if count2%2 == 0 and z == 1:
			output='G'
		else:
			output='B'
		count+=1
	if mlist[2]>gFac:
		if count2%2 == 0 and z == 1:
			output='H'
		else:
			output='C'
		count+=1
	if mlist[3]>gFac:
		if count2%2 == 0 and z == 1:
			output='J'
		else:
			output='D'
		count+=1
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
	mlist.append(cv2.countNonZero(k0))
	#cv2.imshow("{} t{}".format(x,t),k0)
	#if count2 < 10:#or count2 == 39:
	#	cv2.imshow("{} t{}".format(x,t),q)
	#	cv2.imshow("{} t{} 0".format(x,t),k0)
	#	cv2.imshow("{} t{} 1".format(x,t),k1)
	#	cv2.imshow("{} t{} 2".format(x,t),k2)
	#	cv2.imshow("{} t{} 3".format(x,t),k3)
	#	cv2.imshow("{} t{} 4".format(x,t),k4)
	#	cv2.imshow("{} t{} 5".format(x,t),k5)
	mnum=max(mlist)
	if mlist[5]>gFac:
		output2='G'
	else:
		output2='NG'
	if mlist[0]>gFac:
		if count2%2 == 0:
			output='F'
		else:
			output='A'
		count+=1
	if mlist[1]>gFac:
		if count2%2 == 0:
			output='G'
		else:
			output='B'
		count+=1
	if mlist[2]>gFac:
		if count2%2 == 0:
			output='H'
		else:
			output='C'
		count+=1
	if mlist[3]>gFac:
		if count2%2 == 0:
			output='J'
		else:
			output='D'
		count+=1
	if mlist[4]>gFac:
		if count2%2 == 0:
			output='K'
		else:
			output='E'
		count+=1
	if count>=2:
		output='W'
	if count==0:
		output='O'
	print("{} {} {} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],mlist[4],output,mnum,output2,mlist[5]))
	olist.append(count2)
	olist.append(output)
	olist.append(output2)
	return olist

gFac=220
def SS_SAT1(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)
		(h,w)=thresh.shape[:2]

		thresh2 = thresh[int(h*.01):h-int(h*.03),int(w*.1):w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		y=int(h*.078)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,13):
			count2+=1
			if count2<53:
				joke.append(calcAns(x,y,t,thresh2,count2,w,0))
	print("*************************************")
	return joke

def SS_SAT2(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)

		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.01):h-int(h*.03),int(w*.1):w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		y=int(h*.078)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,13):
			count2+=1
			if count2<45:
				joke.append(calcAns(x,y,t,thresh2,count2,w,0))
	print("*************************************")
	return joke

def SS_SAT31(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)

		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.01):h-int(h*.03),int(w*.1):w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		y=int(h*.25)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,4):
			count2+=1
			if count2==16:
				break
			else:
				joke.append(calcAns(x,y,t,thresh2,count2,w,0))
	print("*************************************")
	return joke

def SS_SAT32(paper,num):
	helper=viewAdjust(paper,5)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI ",thresh)

		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.1):h-int(h*.05),0:w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		thresh3=thresh2[0:h-int(h*.945),int(w*.05):w-int(w*.79)]
		val=cv2.countNonZero(thresh3)
		hold="NG"
		if val>gFac:
			hold="G"
		print("{} {}".format(val,hold))
		#cv2.imshow("testIII {}".format(x),thresh3)
		thresh4 = thresh2[int(h*.15):h,int(w*.29):w]
		#cv2.imshow("testIV {}".format(x),thresh4)
		y=int(h*.073)
		mlist=[]
		output=[]
		count=0
		for t in range(0,12):
			q=thresh4[y*t:y*(t+1),0:w]
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
			#print("{} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],output,mnum,len(output)))
			count=0
			mlist=[]
		t=['-','-','-']
		t[1]=frCalc(output)
		t[0]=num+x
		t[2]=hold
		joke.append(t)
	print("*************************************")
	return joke

def SS_SAT4(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)
		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.02):h-int(h*.03),int(w*.1):w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		y=int(h*.078)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,13):
			count2+=1
			if count2<31:
				joke.append(calcAns(x,y,t,thresh2,count2,w,0))
	print("*************************************")
	return joke

def SS_SAT51(paper,num):
	helper=viewAdjust(paper,5)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI ",thresh)

		(h,w)=thresh.shape[:2]

		thresh2 = thresh[int(h*.1):h-int(h*.05),0:w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		
		thresh3=thresh2[0:h-int(h*.945),int(w*.05):w-int(w*.79)]
		val=cv2.countNonZero(thresh3)
		hold="NG"
		if val>gFac:
			hold="G"
		print("{} {}".format(val,hold))
		#cv2.imshow("testIII {}".format(x),thresh3)
		thresh4 = thresh2[int(h*.15):h,int(w*.29):w]
		#cv2.imshow("testIV {}".format(x),thresh4)
		y=int(h*.073)
		mlist=[]
		output=[]
		count=0
		for t in range(0,12):
			q=thresh4[y*t:y*(t+1),0:w]
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
			#print("{} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],output,mnum,len(output)))
			count=0
			mlist=[]
		t=['-','-','-']
		t[1]=frCalc(output)
		t[0]=num+x
		t[2]=hold
		joke.append(t)
	print("*************************************")
	return joke

def SS_SAT52(paper,num):
	helper=viewAdjust(paper,5)
	joke=[]
	count2=0
	for x in range(0,3):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI ",thresh)

		(h,w)=thresh.shape[:2]
		thresh2 = thresh[0:h-int(h*.04),0:w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)
		(h,w)=thresh2.shape[:2]
		
		thresh3=thresh2[int(h*.01):h-int(h*.94),int(w*.04):w-int(w*.79)]
		val=cv2.countNonZero(thresh3)
		hold="NG"
		if val>gFac:
			hold="G"
		print("{} {}".format(val,hold))
		#cv2.imshow("testIII {}".format(x),thresh3)
		thresh4 = thresh2[int(h*.15):h,int(w*.29):w]
		#cv2.imshow("testIV {}".format(x),thresh4)
		y=int(h*.073)
		mlist=[]
		output=[]
		count=0
		for t in range(0,12):
			q=thresh4[y*t:y*(t+1),0:w]
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
			#print("{} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],output,mnum,len(output)))
			count=0
			mlist=[]
		t=['-','-','-']
		t[1]=frCalc(output)
		t[0]=num+x
		t[2]=hold
		joke.append(t)
	print("*************************************")
	return joke

def SS_PSAT1(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)
		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.01):h-int(h*.03),int(w*.1):w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		y=int(h*.078)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,13):
			count2+=1
			if count2<48:
				joke.append(calcAns(x,y,t,thresh2,count2,w,0))
	print("*************************************")
	return joke

def SS_PSAT2(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)
		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.01):h-int(h*.04),int(w*.1):w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		y=int(h*.078)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,13):
			count2+=1
			if count2<45:
				joke.append(calcAns(x,y,t,thresh2,count2,w,0))
	print("*************************************")
	return joke

def SS_PSAT31(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)

		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.01):h-int(h*.1),int(w*.1):w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)
		(h,w)=thresh2.shape[:2]
		y=int(h*.25)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,4):
			count2+=1
			if count2==14:
				break
			else:
				joke.append(calcAns(x,y,t,thresh2,count2,w,0))
	print("*************************************")
	return joke

def SS_PSAT32(paper,num):
	helper=viewAdjust(paper,5)
	joke=[]
	count2=0
	for x in range(0,4):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI ",thresh)
		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.1):h-int(h*.05),0:w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		thresh3=thresh2[0:h-int(h*.945),int(w*.05):w-int(w*.79)]
		val=cv2.countNonZero(thresh3)
		hold="NG"
		if val>gFac:
			hold="G"
		print("{} {}".format(val,hold))
		#cv2.imshow("testIII {}".format(x),thresh3)
		thresh4 = thresh2[int(h*.15):h,int(w*.29):w]
		#cv2.imshow("testIV {}".format(x),thresh4)
		y=int(h*.073)
		mlist=[]
		output=[]
		count=0
		for t in range(0,12):
			q=thresh4[y*t:y*(t+1),0:w]
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
		joke.append(t)
	print("*************************************")
	return joke

def SS_PSAT41(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] #original
		#thresh = cv2.threshold(cropped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)
		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.01):h-int(h*.03),int(w*.1):w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		y=int(h*.1429)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,7):
			count2+=1
			if count2<28:
				joke.append(calcAns(x,y,t,thresh2,count2,w,0))
	print("*************************************")
	return joke

def SS_PSAT42(paper,num):
	helper=viewAdjust(paper,5)
	joke=[]
	count2=0
	for x in range(0,4):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI ",thresh)
		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.09):h-int(h*.04),0:w-int(w*.1)]
		#cv2.imshow("testII {}".format(x),thresh2)

		(h,w)=thresh2.shape[:2]
		thresh3=thresh2[int(h*.035):h-int(h*.915),int(w*.05):w-int(w*.79)]
		val=cv2.countNonZero(thresh3)
		hold="NG"
		if val>gFac:
			hold="G"
		#print("{} {}".format(val,hold))
		#cv2.imshow("testIII {}".format(x),thresh3)
		thresh4 = thresh2[int(h*.17):h,int(w*.29):w]
		#cv2.imshow("testIV {}".format(x),thresh4)
		y=int(h*.073)
		mlist=[]
		output=[]
		count=0
		for t in range(0,12):
			q=thresh4[y*t:y*(t+1),0:w]
			#if t==1 or t==0:
			#	cv2.imshow("{} t{}".format(x,t),q)
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
			#print("{} {} {} {} {} {} {} {} {}".format(x,t,mlist[0],mlist[1],mlist[2],mlist[3],output,mnum,len(output)))
			count=0
			mlist=[]
		t=['-','-','-']
		t[1]=frCalc(output)
		t[0]=num+x
		t[2]=hold
		joke.append(t)
	print("*************************************")
	return joke

def SS_ACT1(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)

		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*0.016):h-int(h*.04),int(w*.05):w-int(w*.18)]
		#cv2.imshow("testII {}".format(x),thresh2)
		(h,w)=thresh2.shape[:2]
		y=int(h*.053)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,19):
			count2+=1
			if count2<76:
				joke.append(calcAns(x,y,t,thresh2,count2,w,1))
	print("*************************************")
	return joke

def SS_ACT2(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)
		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.0165):h-int(h*.03),int(w*.05):w-int(w*.05)]
		#cv2.imshow("testII {}".format(x),thresh2)
		(h,w)=thresh2.shape[:2]
		y=int(h*.0535)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,19):
			count2+=1
			if count2<61:
				joke.append(calcAnsACT(x,y,t,thresh2,count2,w))
	print("*************************************")
	return joke

def SS_ACT3(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)
		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.0165):h-int(h*.03),int(w*.05):w-int(w*.15)]
		#cv2.imshow("testII {}".format(x),thresh2)
		(h,w)=thresh2.shape[:2]
		y=int(h*.0535)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,19):
			count2+=1
			if count2<41:
				joke.append(calcAns(x,y,t,thresh2,count2,w,1))
	print("*************************************")
	return joke

def SS_ACT4(paper):
	helper=viewAdjust(paper,4)
	joke=[]
	count2=0
	for x in range(0,len(helper)):
		temp=helper[x]
		warped = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
		# apply Otsu's thresholding method to binarize the warped piece of paper
		thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		#cv2.imshow("testI",thresh)
		(h,w)=thresh.shape[:2]
		thresh2 = thresh[int(h*.0165):h-int(h*.03),int(w*.05):w-int(w*.15)]
		#cv2.imshow("testII {}".format(x),thresh2)
		(h,w)=thresh2.shape[:2]
		y=int(h*.0533)
		mlist=[]
		output=""
		count=0
		output2=""
		for t in range(0,19):
			count2+=1
			if count2<41:
				joke.append(calcAns(x,y,t,thresh2,count2,w,1))
	print("*************************************")
	return joke

#"""
#fileobj=open("testRES.txt","r")
#rRES=getRES(fileobj,52)
#wRES=getRES(fileobj,44)

def getRES(fileobj,amt):
	relist=[]
	for x in range(0, int(amt)):
		relist.append(fileobj.readline().strip())
	return relist

def compare(l1,l2):
	incorrect=[]
	if len(l1) != len(l2):
		return False
	for x in range(0,len(l1)):
		if l1[x] != l2[x]:
			return False
	return True

def pg1SAT(marker):
	hold="images/{}/SATPG{}1.jpg".format(marker,marker)
	image = cv2.imread(hold)
	paper1=picfix(image,1)
	hapy=SS_SAT1(paper1)
	#cv2.imshow("paper1",paper1)
	print(hapy)
	print(len(hapy))
	h1=getGuesses(hapy)
	print(h1)
	len(h1)
	print("********************************************")
	return hapy

def pg2SAT(marker):
	hold="images/{}/SATPG{}2.jpg".format(marker,marker)
	image2 = cv2.imread(hold)
	paper2=picfix(image2,1)
	hapy2=SS_SAT2(paper2)
	#cv2.imshow("paper2",paper2)
	print(hapy2)
	print(len(hapy2))
	h1=getGuesses(hapy2)
	print(h1)
	len(h1)
	print("********************************************")
	return hapy2

def pg31SAT(marker):
	hold="images/{}/SATPG{}3.jpg".format(marker,marker)
	image3 = cv2.imread(hold)
	paper3=picfix(image3,2)
	#cv2.imshow("pg3MC",paper3[1])
	hapy31=SS_SAT31(paper3[1])
	print(hapy31)
	print(len(hapy31))
	h1=getGuesses(hapy31)
	print(h1)
	len(h1)
	print("********************************************")
	return hapy31

def pg32SAT(marker):
	hold="images/{}/SATPG{}3.jpg".format(marker,marker)
	image3 = cv2.imread(hold)
	paper3=picfix(image3,2)
	#cv2.imshow("FRPG3",paper3[0])
	hapy32=SS_SAT32(paper3[0],16)
	print(hapy32)
	print(len(hapy32))
	h1=getGuesses(hapy32)
	print(h1)
	len(h1)
	print("********************************************")
	return hapy32

def pg4SAT(marker):
	hold="images/{}/SATPG{}4.jpg".format(marker,marker)
	image4 = cv2.imread(hold)
	paper4=picfix(image4,1)
	hapy4=SS_SAT4(paper4)
	#cv2.imshow("paper4",paper4)
	print(hapy4)
	print(len(hapy4))
	h1=getGuesses(hapy4)
	print(h1)
	len(h1)
	print("********************************************")
	return hapy4

def pg51SAT(marker):
	hold="images/{}/SATPG{}5.jpg".format(marker,marker)
	image5 = cv2.imread(hold)
	paper51=picfix(image5,2)
	#cv2.imshow("paper51",paper51[0])
	hapy51=SS_SAT51(paper51[0],31)
	print(hapy51)
	print(len(hapy51))
	h1=getGuesses(hapy51)
	print(h1)
	len(h1)
	print("********************************************")
	return hapy51

def pg52SAT(marker):
	hold="images/{}/SATPG{}5.jpg".format(marker,marker)
	image5 = cv2.imread(hold)
	paper51=picfix(image5,2)
	#cv2.imshow("paper52",paper51[1])
	hapy52=SS_SAT52(paper51[1],36)
	print(hapy52)
	print(len(hapy52))
	h1=getGuesses(hapy52)
	print(h1)
	len(h1)
	print("********************************************")
	return hapy52

def pg1PSAT(marker):
	hold="images/{}/PSATPG{}1.jpg".format(marker,marker)
	imgPSAT1 = cv2.imread(hold)
	PSAT1fix=picfix(imgPSAT1,1)
	psat1=SS_PSAT1(PSAT1fix)
	#cv2.imshow("PSATpaper1",PSAT1fix)
	print(psat1)
	print(len(psat1))
	h1=getGuesses(psat1)
	print(h1)
	len(h1)
	print("********************************************")
	return psat1

def pg2PSAT(marker):
	hold="images/{}/PSATPG{}2.jpg".format(marker,marker)
	imgPSAT2 = cv2.imread(hold)
	PSAT2fix=picfix(imgPSAT2,1)
	psat2=SS_PSAT2(PSAT2fix)
	#cv2.imshow("PSATpaper2",PSAT2fix)
	print(psat2)
	print(len(psat2))
	h1=getGuesses(psat2)
	print(h1)
	len(h1)
	print("********************************************")
	return psat2

def pg31PSAT(marker):
	hold="images/{}/PSATPG{}3.jpg".format(marker,marker)
	image3 = cv2.imread(hold)
	#cv2.imshow("check",image3)
	paper3=picfix(image3,2)
	#cv2.imshow("pg3MC",paper3[1])
	psat31=SS_PSAT31(paper3[1])
	print(psat31)
	print(len(psat31))
	h1=getGuesses(psat31)
	print(h1)
	len(h1)
	print("********************************************")
	return psat31

def pg32PSAT(marker):
	hold="images/{}/PSATPG{}3.jpg".format(marker,marker)
	image3 = cv2.imread(hold)
	#cv2.imshow("check",image3)
	paper3=picfix(image3,2)
	#cv2.imshow("FRPG3",paper3[0])
	psat32=SS_PSAT32(paper3[0],14)
	print(psat32)
	print(len(psat32))
	h1=getGuesses(psat32)
	print(h1)
	len(h1)
	print("********************************************")
	return psat32

def pg41PSAT(marker):
	hold="images/{}/PSATPG{}4.jpg".format(marker,marker)
	image4 = cv2.imread(hold)
	#cv2.imshow("check",image4)
	paper4=picfix(image4,2)
	#cv2.imshow("pg4MC",paper4[1])
	psat41=SS_PSAT41(paper4[1])
	print(psat41)
	print(len(psat41))
	h1=getGuesses(psat41)
	print(h1)
	len(h1)
	print("********************************************")
	return psat41

def pg42PSAT(marker):
	hold="images/{}/PSATPG{}4.jpg".format(marker,marker)
	image4 = cv2.imread(hold)
	#cv2.imshow("check",image4)
	paper4=picfix(image4,2)
	#cv2.imshow("FRPG4",paper4[0])
	psat42=SS_PSAT42(paper4[0],28)
	print(psat42)
	print(len(psat42))
	h1=getGuesses(psat42)
	print(h1)
	len(h1)
	print("********************************************")
	return psat42

def pg1ACT(marker):
	hold="images/{}/ACTPG{}1.jpg".format(marker,marker)
	#print(hold)
	imgACT1 = cv2.imread(hold)
	ACT1fix=picfix(imgACT1,1)
	ACT1=SS_ACT1(ACT1fix)
	#cv2.imshow("ACTpaper1",ACT1fix)
	print(ACT1)
	print(len(ACT1))
	h1=getGuesses(ACT1)
	print(h1)
	print(len(h1))
	print("********************************************")
	return ACT1
	

def pg2ACT(marker):
	hold="images/{}/ACTPG{}2.jpg".format(marker,marker)
	imgACT2 = cv2.imread(hold)
	#cv2.imshow("ACTpaper2",imgACT2)	
	#cv2.waitKey(0)
	ACT2fix=picfix(imgACT2,1)
	ACT2=SS_ACT2(ACT2fix)
	#cv2.imshow("ACTpaper2",ACT2fix)
	print(ACT2)
	print(len(ACT2))
	h1=getGuesses(ACT2)
	print(h1)
	print(len(h1))
	print("********************************************")
	return ACT2

def pg3ACT(marker):
	hold="images/{}/ACTPG{}3.jpg".format(marker,marker)
	imgACT3 = cv2.imread(hold)
	ACT3fix=picfix(imgACT3,1)
	ACT3=SS_ACT3(ACT3fix)
	#cv2.imshow("ACTpaper3",ACT3fix)
	print(ACT3)
	print(len(ACT3))
	h1=getGuesses(ACT3)
	print(h1)
	print(len(h1))
	print("********************************************")
	return ACT3

def pg4ACT(marker):
	hold="images/{}/ACTPG{}4.jpg".format(marker,marker)
	imgACT4 = cv2.imread(hold)
	ACT4fix=picfix(imgACT4,1)
	ACT4=SS_ACT4(ACT4fix)
	#cv2.imshow("ACTpaper4",ACT4fix)
	print(ACT4)
	print(len(ACT4))
	h1=getGuesses(ACT4)
	print(h1)
	print(len(h1))
	print("********************************************")
	return ACT4

def PSATmanage(fileobj,mark):
	hold1=pg1PSAT(mark)
	hold2=pg2PSAT(mark)
	hold31=pg31PSAT(mark)
	hold32=pg32PSAT(mark)
	hold41=pg41PSAT(mark)
	hold42=pg42PSAT(mark)
	
	fileobj.write("testF\ntestL\n")
	t3=len(hold31)+len(hold32)
	t4=len(hold41)+len(hold42)
	fileobj.write("{}\n{}\n{}\n{}\n".format(len(hold1),len(hold2),t3,t4))
	processOut(hold1,fileobj)
	processOut(hold2,fileobj)
	processOut(hold31,fileobj)
	processOut(hold32,fileobj)
	processOut(hold41,fileobj)
	processOut(hold42,fileobj)
	

def SATmanage(fileobj,mark):
	hold1=pg1SAT(mark)
	hold2=pg2SAT(mark)
	hold31=pg31SAT(mark)
	hold32=pg32SAT(mark)
	hold41=pg4SAT(mark)
	hold42=pg51SAT(mark)
	hold43=pg52SAT(mark)
	fileobj.write("testF\ntestL\n")
	t3=len(hold31)+len(hold32)
	t4=len(hold41)+len(hold42)+len(hold43)
	fileobj.write("{}\n{}\n{}\n{}\n".format(len(hold1),len(hold2),t3,t4))
	processOut(hold1,fileobj)
	processOut(hold2,fileobj)
	processOut(hold31,fileobj)
	processOut(hold32,fileobj)
	processOut(hold41,fileobj)
	processOut(hold42,fileobj)
	processOut(hold43,fileobj)

def ACTmanage(fileobj,mark):
	hold1=pg1ACT(mark)
	hold2=pg2ACT(mark)
	hold3=pg3ACT(mark)
	hold4=pg4ACT(mark)
	fileobj.write("testF\ntestL\n")
	fileobj.write("{}\n{}\n{}\n{}\n".format(len(hold1),len(hold2),len(hold3),len(hold4)))
	processOut(hold1,fileobj)
	fileobj.write("************************\n")
	processOut(hold2,fileobj)
	fileobj.write("************************\n")
	processOut(hold3,fileobj)
	fileobj.write("************************\n")
	processOut(hold4,fileobj)
	fileobj.write("************************\n")

def getGuesses(answers):
	y=[]
	for x in range(0,len(answers)):
		hold = answers[x]
		if hold[2] == 'G':
			y.append([hold[0],hold[2]])
	return y

def processOut(outData,fileobj):
	for x in range(0,len(outData)):
		h2=outData[x]
		store='{} {} {}\n'.format(h2[0],h2[1],h2[2])
		#store='{}\n'.format(h2[1])
		fileobj.write(store)
	fileobj.write("*******************************\n")


#python SSOMR.py KATETEST.txt KATEF testnum "ie: 1 or 2 or 3"
fileobj=open(str(sys.argv[1]),"w")
name=str(sys.argv[2])
#hold=pg1SAT()
#processOut(pg1SAT(),fileobj)
#pg1PSAT()
#pg2PSAT()
#pg31PSAT()
#pg32PSAT()
#pg41PSAT()
#pg42PSAT()
#pg1ACT()
#pg2ACT()
#pg3ACT()
#pg4ACT()
#name=name.strip()
if int(sys.argv[3])==1:
	ACTmanage(fileobj,name)
if int(sys.argv[3])==2:
	SATmanage(fileobj,name)
if int(sys.argv[3])==3:
	PSATmanage(fileobj,name)
"""print(rRES)
print(len(rRES))
print("********************************************")
print(wRES)
print(len(wRES))
print("*******************check*************************")
print(compare(hapy,rRES))
print(compare(hapy2,wRES))

"""

cv2.waitKey(0)

