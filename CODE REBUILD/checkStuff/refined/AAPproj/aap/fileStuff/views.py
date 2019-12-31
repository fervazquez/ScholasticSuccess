from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
#from .forms import UploadFileForm

def index(request):
    try:
        #form = UploadFileForm(request.POST, request.FILES)
        print("***********************")
        print(request.POST)
        print("***********************")
        print("***********************")
        print("***********************")
        print(request.Files)
        fileFun = request.FILES['file']
        print(type(fileFun))
        return HttpResponse("Hello, world. You're at the polls index.")
    except:
        return HttpResponse("You Fuck")