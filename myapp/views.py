from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'name':'Heeramani',
        'age':'15'
    }
    return render(request, 'index.html',context)

def download(request):
    return HttpResponse("<h1> You are here to download something....</h1>")

def counter(request):
    words = request.GET['words']
    count = len(words.split())
    return render(request,'counter.html', {'count':count})
