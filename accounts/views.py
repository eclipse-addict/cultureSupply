from django.shortcuts import render

# Create your views here.

def login(request):
    pass

def logout(request):
    pass


def signup(request):
    if request.method == 'POST':
        pass
    else: 
        return render(request, 'accounts/policy.html')
