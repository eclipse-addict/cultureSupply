from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'articles/index.html')

def detail(request, pk):
    pass

def create(request):
    pass

def update(request, pk):
    pass

def delete(request, pk):
    pass


